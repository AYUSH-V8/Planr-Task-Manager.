from flask import Flask, render_template, request, jsonify
from chatbot import PersonalAssistant
import os
import webbrowser
from threading import Timer

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

def open_browser():
    """Open browser after server starts"""
    webbrowser.open('http://localhost:5000')

# Initialize chatbot
assistant = PersonalAssistant()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    try:
        bot_response = assistant.process_command(user_message)
        # Save conversation to history
        assistant.conversations.add_message(user_message, bot_response)
        return jsonify({
            'user_message': user_message,
            'bot_response': bot_response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/help', methods=['GET'])
def get_help():
    help_text = assistant.utils.get_help()
    return jsonify({'help': help_text})

@app.route('/conversations', methods=['GET'])
def get_conversations():
    """Get list of all conversations"""
    conversations = assistant.conversations.get_all_conversations()
    return jsonify({'conversations': conversations})

@app.route('/conversation/<session_id>', methods=['GET'])
def get_conversation(session_id):
    """Get specific conversation by ID"""
    conv = assistant.conversations.get_conversation(session_id)
    if conv:
        return jsonify(conv)
    return jsonify({'error': 'Conversation not found'}), 404

@app.route('/conversation/<session_id>', methods=['DELETE'])
def delete_conversation(session_id):
    """Delete a conversation"""
    if assistant.conversations.delete_conversation(session_id):
        return jsonify({'status': 'deleted'})
    return jsonify({'error': 'Conversation not found'}), 404

@app.route('/conversations/clear', methods=['DELETE'])
def clear_conversations():
    """Clear all conversations"""
    assistant.conversations.clear_all_conversations()
    return jsonify({'status': 'cleared'})

@app.route('/conversations/search', methods=['POST'])
def search_conversations():
    """Search conversations by keyword"""
    data = request.json
    keyword = data.get('keyword', '').strip()
    if not keyword:
        return jsonify({'error': 'No keyword provided'}), 400
    results = assistant.conversations.search_conversations(keyword)
    return jsonify({'results': results})

# ========== VOICE ENDPOINTS ==========

@app.route('/voice/listen', methods=['POST'])
def voice_listen():
    """Listen for voice input and convert to text"""
    try:
        text = assistant.voice.listen()
        if text:
            return jsonify({'text': text})
        else:
            return jsonify({'error': 'No speech recognized'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/voice/speak', methods=['POST'])
def voice_speak():
    """Convert text to speech"""
    try:
        data = request.json
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        assistant.voice.speak(text)
        return jsonify({'status': 'success', 'message': 'Text spoken'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== GOALS ENDPOINTS ==========

@app.route('/goals/create', methods=['POST'])
def create_goal():
    """Create a new goal"""
    try:
        data = request.json
        name = data.get('name', '').strip()
        target = data.get('target', 0)
        deadline = data.get('deadline', None)
        
        if not name or target <= 0:
            return jsonify({'status': 'error', 'message': 'Invalid goal data'}), 400
        
        result = assistant.goals.create_goal(name, target, deadline)
        assistant.notifications.notify('Goal Created', f'"{name}" created! 🎯', 'success')
        return jsonify({'status': 'success', 'message': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/goals/list', methods=['GET'])
def list_goals():
    """Get all goals with summary"""
    try:
        goals = assistant.goals.view_all_goals()
        summary = assistant.goals.get_goals_summary()
        
        # Parse the summary string to extract numbers
        import re
        total = len(goals) if goals else 0
        completed = sum(1 for g in goals if 'Completed' in g.get('status', '')) if goals else 0
        in_progress = sum(1 for g in goals if 'In Progress' in g.get('status', '')) if goals else 0
        
        return jsonify({
            'goals': goals if goals else [],
            'summary': {
                'total': total,
                'completed': completed,
                'in_progress': in_progress
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/goals/update/<int:goal_id>', methods=['POST'])
def update_goal(goal_id):
    """Update goal progress"""
    try:
        result = assistant.goals.update_progress(goal_id)
        if 'congratulations' in result.lower():
            assistant.notifications.notify('Goal Completed! 🎉', result, 'success')
        else:
            assistant.notifications.notify('Progress Updated', result, 'success')
        return jsonify({'status': 'success', 'message': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/goals/delete/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    """Delete a goal"""
    try:
        result = assistant.goals.delete_goal(goal_id)
        return jsonify({'status': 'success', 'message': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/search', methods=['POST'])
def search():
    """Search across tasks, notes, goals, and conversations"""
    try:
        data = request.json
        query = data.get('query', '').strip().lower()
        
        if not query or len(query) < 2:
            return jsonify({'results': []})
        
        results = []
        
        # Search in goals
        goals = assistant.goals.view_all_goals()
        for goal in goals:
            if query in goal.get('name', '').lower():
                results.append({
                    'type': 'Goal',
                    'id': str(goal.get('id')),
                    'text': goal.get('name', 'Unknown goal')
                })
        
        # Search in conversations
        conversations = assistant.conversations.get_all_conversations()
        for conv in conversations:
            if query in conv.get('title', '').lower() or any(query in msg.get('content', '').lower() for msg in conv.get('messages', [])):
                results.append({
                    'type': 'Conversation',
                    'id': conv.get('id'),
                    'text': conv.get('title', 'Unknown conversation')
                })
        
        # Limit results to 10
        results = results[:10]
        
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== NOTIFICATIONS ENDPOINTS ==========

@app.route('/notify', methods=['POST'])
def send_notification():
    """Send a notification"""
    try:
        data = request.json
        title = data.get('title', 'Notification')
        message = data.get('message', '')
        notification_type = data.get('type', 'info')
        
        assistant.notifications.notify(title, message, notification_type)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("🎯 Personal Assistant Chatbot is starting...")
    print("Opening browser: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    
    # Open browser after 1 second delay (gives server time to start)
    Timer(1.0, open_browser).start()
    
    # Run the Flask server
    app.run(debug=False, host='localhost', port=5000, use_reloader=False)
