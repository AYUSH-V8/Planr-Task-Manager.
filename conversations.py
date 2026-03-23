import json
import os
from datetime import datetime

class ConversationManager:
    """Manages conversation history and retrieval"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.conversations_file = os.path.join(data_dir, 'conversations.json')
        self.current_session_id = self._generate_session_id()
        self.load_conversations()
    
    def _generate_session_id(self):
        """Generate unique session ID based on current time"""
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    def load_conversations(self):
        """Load all conversations from file"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        if os.path.exists(self.conversations_file):
            try:
                with open(self.conversations_file, 'r', encoding='utf-8') as f:
                    self.conversations = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.conversations = {}
        else:
            self.conversations = {}
    
    def save_conversations(self):
        """Save conversations to file"""
        with open(self.conversations_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversations, f, ensure_ascii=False, indent=2)
    
    def add_message(self, user_message, bot_response, session_id=None):
        """Add a message to current conversation"""
        if session_id is None:
            session_id = self.current_session_id
        
        # Initialize session if not exists
        if session_id not in self.conversations:
            self.conversations[session_id] = {
                'started_at': datetime.now().isoformat(),
                'messages': [],
                'title': self._generate_title(user_message)
            }
        
        # Add message
        self.conversations[session_id]['messages'].append({
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'bot': bot_response
        })
        
        self.save_conversations()
    
    def _generate_title(self, first_message):
        """Generate conversation title from first message"""
        # Extract first 50 characters or first sentence
        title = first_message.strip()[:50]
        if len(first_message) > 50:
            title += '...'
        return title if title else 'New Conversation'
    
    def get_all_conversations(self):
        """Get list of all conversations with summary"""
        conversations_list = []
        for session_id, conv_data in sorted(self.conversations.items(), reverse=True):
            conversations_list.append({
                'id': session_id,
                'title': conv_data.get('title', 'Untitled'),
                'started_at': conv_data.get('started_at', ''),
                'message_count': len(conv_data.get('messages', [])),
                'last_message': conv_data.get('messages', [{}])[-1].get('user', '')[:50] if conv_data.get('messages') else ''
            })
        return conversations_list
    
    def get_conversation(self, session_id):
        """Get full conversation by session ID"""
        return self.conversations.get(session_id, None)
    
    def delete_conversation(self, session_id):
        """Delete a conversation"""
        if session_id in self.conversations:
            del self.conversations[session_id]
            self.save_conversations()
            return True
        return False
    
    def clear_all_conversations(self):
        """Clear all conversations (with confirmation)"""
        self.conversations = {}
        self.save_conversations()
    
    def export_conversation(self, session_id):
        """Export conversation as text"""
        conv = self.get_conversation(session_id)
        if not conv:
            return None
        
        text = f"Conversation: {conv.get('title', 'Untitled')}\n"
        text += f"Started: {conv.get('started_at', '')}\n"
        text += "=" * 60 + "\n\n"
        
        for msg in conv.get('messages', []):
            text += f"You: {msg['user']}\n"
            text += f"Bot: {msg['bot']}\n\n"
        
        return text
    
    def search_conversations(self, keyword):
        """Search conversations by keyword"""
        results = []
        keyword_lower = keyword.lower()
        
        for session_id, conv_data in self.conversations.items():
            for msg in conv_data.get('messages', []):
                if keyword_lower in msg['user'].lower() or keyword_lower in msg['bot'].lower():
                    results.append({
                        'session_id': session_id,
                        'title': conv_data.get('title', ''),
                        'message': msg,
                        'timestamp': msg.get('timestamp', '')
                    })
                    break  # Only add session once per search
        
        return results
