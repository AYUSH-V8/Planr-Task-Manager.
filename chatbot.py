import re
from datetime import datetime
from features.todo import TodoManager
from features.reminders import ReminderManager
from features.calendar import CalendarManager
from features.notes import NotesManager
from features.time_tracker import TimeTracker
from features.calculator import Calculator
from features.dictionary import Dictionary
from features.journal import JournalManager
from features.utilities import Utilities
from features.nlp import NLPProcessor
from features.conversations import ConversationManager
from features.habits import HabitTracker
from features.goals import GoalManager
from features.voice import VoiceAssistant
from features.notifications import NotificationManager
import random

class PersonalAssistant:
    def __init__(self):
        self.todo = TodoManager()
        self.reminders = ReminderManager()
        self.calendar = CalendarManager()
        self.notes = NotesManager()
        self.tracker = TimeTracker()
        self.calculator = Calculator()
        self.dictionary = Dictionary()
        self.journal = JournalManager()
        self.utils = Utilities()
        self.nlp = NLPProcessor()  # Add NLP processor for intent detection
        self.conversations = ConversationManager()  # Conversation history manager
        self.habits = HabitTracker()  # Habit tracking manager
        self.goals = GoalManager()  # Goal setting manager
        self.voice = VoiceAssistant()  # Voice input/output
        self.notifications = NotificationManager()  # System notifications
        
        # ========== GREETINGS ==========
        self.greetings = {
            'hello': "Hey there! 👋 How can I help you today?",
            'hi': "Hi! 😊 What can I do for you?",
            'hey': "Hey! 👋 What do you need?",
            'good morning': "Good morning! ☀️ Ready to organize your day?",
            'good afternoon': "Good afternoon! ☀️ How's your day going?",
            'good evening': "Good evening! 🌙 Winding down?",
            'good night': "Sleep well! 🌙 See you tomorrow!",
            'sup': "Hey! 👋 What's up with you?",
            'hiya': "Hiya! 😊 What's on your mind?",
        }
        
        # ========== HOW ARE YOU ==========
        self.how_are_you = [
            "I'm doing great, thanks for asking! 😊 How are you doing?",
            "I'm here and ready to help! What's on your mind?",
            "All systems running smoothly! How can I assist you?",
            "Feeling productive! Ready to help you get things done! 💪",
            "Doing amazing! Thanks for asking! 🌟",
            "Operating at 100%! What can I help with?",
            "Fantastic! How are YOU doing?",
            "Living my best assistant life! 😄 And you?",
        ]
        
        # ========== SMALL TALK ==========
        self.smalltalk = {
            'thanks': [
                "You're welcome! Happy to help! 😊", 
                "No problem! Anything else?", 
                "My pleasure! 🎉",
                "Anytime! 👍",
                "Glad I could help!",
            ],
            'thank you': [
                "You're welcome! 😊", 
                "Always happy to help!", 
                "Glad I could assist!",
                "More than happy to! 🌟",
                "That's what I'm here for!",
            ],
            'sorry': [
                "No worries at all! 😊", 
                "It's all good!", 
                "Don't worry about it!",
                "No problem! Everyone makes mistakes.",
                "All good, my friend! 👍",
            ],
            'bye': [
                "Goodbye! See you later! 👋", 
                "See you soon! 🚀", 
                "Take care! 😊",
                "Catch you later!",
                "Have an awesome day! 👋",
            ],
            'goodbye': [
                "Take care! 👋", 
                "See you next time!", 
                "Goodbye! Have a great day!",
                "Until next time! 🌟",
                "Keep being awesome! 👋",
            ],
        }
        
        # ========== MOOD & FEELINGS ==========
        self.mood_responses = {
            'happy': [
                "That's amazing! 🎉 You deserve to celebrate! What's making you happy?",
                "Awesome! I love the positive vibes! 😊 Keep that energy going!",
                "Fantastic! 🌟 Happiness looks good on you!",
            ],
            'sad': [
                "I'm sorry you're feeling down 😔 Want to talk about it? I'm here to listen!",
                "That's tough 💙 Would it help to talk about what's bothering you?",
                "Hang in there! 💪 Sometimes things get better when we talk about them.",
            ],
            'stressed': [
                "Oh no! 😰 Let's break things down. Want to organize your tasks to feel less overwhelmed?",
                "Stress is real! 😓 Maybe making a to-do list will help you feel more in control?",
                "Take a breather! 🌬️ How can I help you tackle what's stressing you?",
            ],
            'tired': [
                "You need some rest! 😴 Maybe we can organize your schedule so you can relax?",
                "Sounds like you've earned a break! 💤 Want help prioritizing so you can rest?",
                "Get some sleep! 🛌 Your wellbeing comes first!",
            ],
            'excited': [
                "Yesss! That excitement is contagious! 🚀 What's got you so pumped?",
                "Love the energy! ⚡ Tell me what you're excited about!",
                "That's awesome! 🎊 Keep riding that wave of excitement!",
            ],
            'confused': [
                "No worries! 🧠 I'm here to help clarify things. What's confusing?",
                "Don't worry, we can figure it out together! 💭 What's unclear?",
                "Let's break it down! What specific part is confusing you?",
            ],
        }
        
        # ========== GENERAL CHAT TOPICS ==========
        self.topic_responses = {
            'weather': [
                "I don't have real-time weather data, but you could check a weather app! 🌤️",
                "That's great! Can I help you plan your day around the weather?",
                "Weather is just one of those things! 🌦️ Need help with anything else?",
            ],
            'joke': [
                "Why did the developer go broke? Because he used up all his cache! 💻😄",
                "Why do Java developers wear glasses? Because they don't C#! 👓",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            ],
            'compliment': [
                "Aw, thanks! That's really kind of you! 🥰 You're pretty amazing yourself!",
                "That made my day! 😊 You're awesome too!",
                "You're so sweet! 💫 How can I help you today?",
            ],
            'motivation': [
                "You've got this! 💪 Remember: every task completed is progress!",
                "Believe in yourself! 🌟 You're more capable than you think!",
                "Keep pushing forward! 🚀 Great things take time and effort!",
                "You're doing great! 👏 One step at a time!",
            ],
            'help': [
                "I'm here to help! 🤝 What do you need?",
                "Absolutely! I've got your back! 💪 What's up?",
                "You got it! Tell me what you need! 👍",
            ],
        }
        
        # ========== RANDOM STATEMENTS ==========
        self.positive_responses = [
            "That's awesome! 🎉",
            "Sounds good to me! 👍",
            "I like your style! 😊",
            "Nice! 🌟",
            "Absolutely! 💯",
            "You got it! ✨",
            "Perfect! 🎯",
            "Excellent! 👏",
        ]
        
        self.encouraging_responses = [
            "You're doing great! Keep it up! 💪",
            "I believe in you! 🌟",
            "You've got the power! ⚡",
            "Stay positive! 😊",
            "Keep crushing it! 🚀",
            "You're awesome! 🌈",
        ]
    
    def process_command(self, user_input, _nlp_converted=False):
        """Process user input and return appropriate response"""
        user_input = user_input.lower().strip()
        
        # NATURAL LANGUAGE PROCESSING - Conversational AI
        response = self._process_conversation(user_input)
        if response:
            return response
        
        # TRY NLP INTENT DETECTION FIRST (understand natural requests)
        # Only try NLP once to prevent infinite recursion
        if not _nlp_converted:
            intent, extracted_data = self.nlp.detect_intent(user_input)
            if intent:
                command = self.nlp.convert_to_command(intent, extracted_data)
                if command and command != user_input:  # Only recurse if command is different
                    # Recursively process the converted command with flag to prevent re-conversion
                    return self.process_command(command, _nlp_converted=True)
        
        # HELP
        if user_input == 'help':
            return self.utils.get_help()
        
        # TODO TASKS
        elif 'add task' in user_input or 'add todo' in user_input:
            task = user_input.replace('add task', '').replace('add todo', '').strip()
            priority = 'medium'
            if 'high' in task:
                priority = 'high'
                task = task.replace('high', '')
            elif 'low' in task:
                priority = 'low'
                task = task.replace('low', '')
            return self.todo.add_task(task.strip(), priority)
        
        elif 'show tasks' in user_input or 'view tasks' in user_input or 'my tasks' in user_input:
            return self.todo.view_todos()
        
        elif 'mark task' in user_input and 'done' in user_input:
            match = re.search(r'\d+', user_input)
            if match:
                task_id = int(match.group())
                return self.todo.mark_complete(task_id)
            return "Please specify task ID."
        
        elif 'delete task' in user_input or 'remove task' in user_input:
            match = re.search(r'\d+', user_input)
            if match:
                task_id = int(match.group())
                return self.todo.remove_task(task_id)
            return "Please specify task ID."
        
        # REMINDERS
        elif 'set reminder' in user_input or 'remind me' in user_input:
            match = re.search(r'at\s(\d{1,2}:\d{2})', user_input)
            if match:
                time = match.group(1)
                text = user_input.replace('set reminder', '').replace('remind me', '').replace(f'at {time}', '').strip()
                return self.reminders.add_reminder(text, time)
            return "Please specify time (e.g., 'at 15:30')"
        
        elif 'show reminders' in user_input or 'view reminders' in user_input:
            return self.reminders.view_reminders()
        
        # CALENDAR
        elif 'add event' in user_input:
            match = re.search(r'on\s(\d{4}-\d{2}-\d{2})', user_input)
            if match:
                date = match.group(1)
                event = user_input.replace('add event', '').replace(f'on {date}', '').strip()
                return self.calendar.add_event(event, date)
            return "Please specify date (e.g., '2024-03-20')"
        
        elif 'show events' in user_input or 'view events' in user_input:
            return self.calendar.view_events()
        
        elif 'upcoming' in user_input and 'event' in user_input:
            return self.calendar.get_upcoming_events()
        
        elif 'show calendar' in user_input:
            return self.calendar.show_calendar()
        
        # NOTES
        elif 'add note' in user_input:
            note = user_input.replace('add note', '').strip()
            if '|' in note:
                title, content = note.split('|', 1)
                return self.notes.add_note(title.strip(), content.strip())
            return "Format: 'add note [title] | [content]'"
        
        elif 'show notes' in user_input or 'view notes' in user_input:
            return self.notes.view_notes()
        
        elif 'read note' in user_input or 'view note' in user_input:
            match = re.search(r'\d+', user_input)
            if match:
                note_id = int(match.group())
                return self.notes.view_note(note_id)
            return "Please specify note ID."
        
        elif 'delete note' in user_input or 'remove note' in user_input:
            match = re.search(r'\d+', user_input)
            if match:
                note_id = int(match.group())
                return self.notes.delete_note(note_id)
            return "Please specify note ID."
        
        # TIME TRACKING
        elif 'start tracking' in user_input:
            activity = user_input.replace('start tracking', '').strip()
            return self.tracker.start_tracking(activity)
        
        elif 'stop tracking' in user_input or 'end tracking' in user_input:
            return self.tracker.stop_tracking()
        
        elif 'time tracked' in user_input or 'activity summary' in user_input:
            return self.tracker.get_activity_summary()
        
        elif 'tracking' in user_input and ('show' in user_input or 'view' in user_input):
            return self.tracker.view_sessions()
        
        elif 'delete tracking' in user_input or 'remove tracking' in user_input or 'delete activity' in user_input or 'remove activity' in user_input:
            if 'today' in user_input or 'all today' in user_input:
                return self.tracker.delete_today_sessions()
            elif 'all' in user_input and 'confirm' in user_input:
                return self.tracker.delete_all_sessions()
            elif 'all' in user_input:
                return "Type 'delete all tracking confirm' to confirm deletion of all activities."
            else:
                match = re.search(r'\d+', user_input)
                if match:
                    activity_index = int(match.group()) - 1
                    return self.tracker.delete_session(activity_index)
            return "Format: 'delete tracking [number]' or 'delete today activity' or 'delete all tracking confirm'"
        
        # CALCULATOR
        elif 'calculate' in user_input:
            expr = user_input.replace('calculate', '').strip()
            return self.calculator.evaluate(expr)
        
        # DICTIONARY
        elif 'define' in user_input:
            word = user_input.replace('define', '').strip()
            return self.dictionary.search_word(word)
        
        elif 'dictionary' in user_input and 'show' in user_input:
            return self.dictionary.list_words()
        
        # JOURNAL
        elif 'journal' in user_input:
            entry = user_input.replace('journal', '').strip()
            if entry:
                return self.journal.add_entry(entry)
            return "Please write something for your journal entry."
        
        elif 'view journal' in user_input or 'show journal' in user_input:
            if 'today' in user_input:
                return self.journal.view_today_entries()
            return self.journal.view_entries()
        
        # ========== GOALS ==========
        elif 'create goal' in user_input or 'new goal' in user_input or 'set goal' in user_input:
            # Extract goal name and target
            goal_text = user_input.replace('create goal', '').replace('new goal', '').replace('set goal', '').strip()
            # Try to extract target number
            match = re.search(r'(\d+)', goal_text)
            if match:
                target = match.group(1)
                name = goal_text.replace(target, '').strip()
                if name:
                    self.notifications.notify('Goal Created', f'"{name}" created! 🎯', 'success')
                    return self.goals.create_goal(name, int(target))
            return "Please specify goal name and target (e.g., 'create goal read 10 books')"
        
        elif 'show goals' in user_input or 'view goals' in user_input or 'my goals' in user_input or 'list goals' in user_input:
            return self.goals.view_all_goals()
        
        elif 'goal progress' in user_input or 'update goal' in user_input:
            # Extract goal ID
            match = re.search(r'\d+', user_input)
            if match:
                goal_id = int(match.group())
                result = self.goals.update_progress(goal_id)
                if 'congratulations' in result.lower():
                    self.notifications.notify('Goal Completed! 🎉', result, 'success')
                return result
            return "Please specify goal ID (e.g., 'update goal 1')"
        
        elif 'goal summary' in user_input or 'goals summary' in user_input:
            return self.goals.get_goals_summary()
        
        # ========== NOTIFICATIONS ==========
        elif 'send notification' in user_input or 'notify me' in user_input:
            message = user_input.replace('send notification', '').replace('notify me', '').strip()
            if message:
                self.notifications.notify('Alert', message, 'info')
                return f"✓ Notification sent: {message}"
            return "Please specify what you want to be notified about."
        
        # UTILITIES
        elif 'what time' in user_input or 'current time' in user_input:
            return self.utils.get_time()
        
        elif 'what date' in user_input or 'current date' in user_input:
            return self.utils.get_date()
        
        elif 'today' in user_input or 'day details' in user_input:
            return self.utils.get_day_details()
        
        elif 'search' in user_input:
            query = user_input.replace('search', '').strip()
            return self.utils.web_search(query)
        
        elif 'play' in user_input and 'song' in user_input:
            song = user_input.replace('play', '').replace('song', '').strip()
            return self.utils.play_song(song)
        
        elif 'convert' in user_input:
            match = re.search(r'(\d+)\s+(\w+)\s+to\s+(\w+)', user_input)
            if match:
                value, from_unit, to_unit = match.groups()
                return self.utils.convert_units(value, from_unit, to_unit)
            return "Format: 'convert [value] [from_unit] to [to_unit]' (e.g., '5 km to miles')"
        
        # HABITS
        elif 'create habit' in user_input or 'new habit' in user_input:
            habit = user_input.replace('create habit', '').replace('new habit', '').strip()
            frequency = 'daily'
            if 'weekly' in habit:
                frequency = 'weekly'
                habit = habit.replace('weekly', '')
            elif 'monthly' in habit:
                frequency = 'monthly'
                habit = habit.replace('monthly', '')
            return self.habits.create_habit(habit.strip(), frequency=frequency)
        
        elif 'log habit' in user_input or 'complete habit' in user_input or 'did habit' in user_input:
            habit = user_input.replace('log habit', '').replace('complete habit', '').replace('did habit', '').strip()
            result = self.habits.log_habit(habit)
            # Send notification on success
            if "🔥" in result:
                self.notifications.habit_reminder(habit)
            return result
        
        elif 'show habits' in user_input or 'view habits' in user_input or 'my habits' in user_input:
            return self.habits.view_all_habits()
        
        elif 'habit status' in user_input or 'habit progress' in user_input:
            match = re.search(r'habit [a-z ]+', user_input)
            if match:
                habit = match.group().replace('habit', '').strip()
                return self.habits.get_habit_status(habit)
            return "Please specify a habit name."
        
        elif 'streak' in user_input and 'summary' in user_input:
            return self.habits.get_streak_summary()
        
        elif 'streak' in user_input and ('show' in user_input or 'view' in user_input or 'calendar' in user_input):
            match = re.search(r'streak\s+(?:for\s+)?([a-z ]+)', user_input)
            if match:
                habit = match.group(1).strip()
                return self.habits.get_streak_visualization(habit)
            return "Please specify a habit name."
        
        elif 'delete habit' in user_input or 'remove habit' in user_input:
            habit = user_input.replace('delete habit', '').replace('remove habit', '').strip()
            return self.habits.delete_habit(habit)
        
        # GOALS
        elif 'create goal' in user_input or 'new goal' in user_input or 'set goal' in user_input:
            # Parse: "create goal [name] target [value]"
            match = re.search(r'(?:create|new|set)\s+goal\s+(.+?)\s+target\s+([\d.]+)', user_input)
            if match:
                goal_name, target = match.groups()
                category = 'general'
                if 'category' in user_input:
                    cat_match = re.search(r'category\s+(\w+)', user_input)
                    if cat_match:
                        category = cat_match.group(1)
                return self.goals.create_goal(goal_name, target, category=category)
            return "Format: 'create goal [name] target [value]' (e.g., 'create goal read books target 12')"
        
        elif 'update goal' in user_input or 'progress' in user_input and 'goal' in user_input:
            # Parse: "update goal [name] [amount]" or "progress on [goal] [amount]"
            match = re.search(r'(?:update\s+goal\s+|progress\s+on\s+)(.+?)\s+([\d.]+)', user_input)
            if match:
                goal_name, amount = match.groups()
                result = self.goals.update_progress(goal_name, amount)
                if "🎉" in result:
                    self.notifications.goal_achievement(goal_name)
                return result
            return "Format: 'update goal [name] [amount]'"
        
        elif 'goal status' in user_input or 'goal progress' in user_input:
            match = re.search(r'goal\s+(?:status\s+|progress\s+)?(?:for\s+)?([a-z ]+)', user_input)
            if match:
                goal = match.group(1).strip()
                return self.goals.get_goal_status(goal)
            return "Please specify a goal name."
        
        elif 'show goals' in user_input or 'view goals' in user_input or 'my goals' in user_input:
            return self.goals.view_all_goals()
        
        elif 'goals summary' in user_input or 'goal summary' in user_input:
            return self.goals.get_goals_summary()
        
        elif 'goal visualization' in user_input or 'goal bar' in user_input:
            match = re.search(r'(?:visualization|bar)\s+(?:for\s+)?([a-z ]+)', user_input)
            if match:
                goal = match.group(1).strip()
                return self.goals.get_progress_visualization(goal)
            return "Please specify a goal name."
        
        elif 'delete goal' in user_input or 'remove goal' in user_input:
            goal = user_input.replace('delete goal', '').replace('remove goal', '').strip()
            return self.goals.delete_goal(goal)
        
        elif 'deadline' in user_input and 'goal' in user_input:
            match = re.search(r'goal\s+(.+?)\s+(?:deadline|by)\s+(\d{4}-\d{2}-\d{2})', user_input)
            if match:
                goal_name, deadline = match.groups()
                return self.goals.set_deadline(goal_name, deadline)
            return "Format: 'goal [name] deadline 2024-12-31'"
        
        # VOICE COMMANDS
        elif 'speak' in user_input and 'listen' not in user_input:
            text = user_input.replace('speak', '').strip()
            if text:
                self.voice.speak(text)
                return f"🔊 Speaking: {text}"
            return "Please provide text to speak."
        
        elif 'listen' in user_input or 'activate voice input' in user_input:
            text = self.voice.listen()
            if text:
                return f"🎤 You said: {text}\n\nProcessing..."
            return "❌ Could not recognize speech. Please try again."
        
        elif 'voice test' in user_input:
            return self.voice.test_voice()
        
        elif 'enable voice' in user_input:
            if self.voice.enable_voice():
                return "✅ Voice output enabled!"
            return "❌ Could not enable voice!"
        
        elif 'disable voice' in user_input:
            self.voice.disable_voice()
            return "✅ Voice output disabled!"
        
        elif 'voice status' in user_input:
            status = "✅ Enabled" if self.voice.is_voice_enabled() else "❌ Disabled"
            return f"🔊 Voice Status: {status}"
        
        # NOTIFICATIONS
        elif 'send notification' in user_input or 'notify' in user_input:
            message = user_input.replace('send notification', '').replace('notify', '').strip()
            self.notifications.notify("Planr", message)
            return f"📬 Notification sent!"
        
        elif 'notification status' in user_input or 'notifications available' in user_input:
            return self.notifications.get_status()
        
        elif 'test notification' in user_input:
            self.notifications.notify(
                "Test Notification",
                "This is a test notification from Planr!",
                timeout=5
            )
            return "✅ Test notification sent!"

        elif user_input in ['quit', 'exit', 'bye', 'goodbye']:
            return "QUIT"
        
        else:
            # Smart suggestions
            similar_commands = self._find_similar_command(user_input)
            if similar_commands:
                return f"Did you mean one of these?\n{similar_commands}\n\nType 'help' for full commands list."
            return "I didn't understand that command. Type 'help' for available commands."
    
    def _process_conversation(self, user_input):
        """Handle natural conversation and small talk with comprehensive chat features"""
        
        # ========== GREETINGS ==========
        for greeting, response in self.greetings.items():
            if user_input == greeting or user_input.startswith(greeting + ' '):
                return response
        
        # ========== HOW ARE YOU ==========
        if any(phrase in user_input for phrase in ['how are you', 'how you doing', "how's it", 'how are things', 'how u doing', 'wuz up', "what's up"]):
            return random.choice(self.how_are_you)
        
        # ========== IDENTITY QUESTIONS ==========
        if any(phrase in user_input for phrase in ["what's your name", 'who are you', 'what are you', 'tell me about yourself', 'introduce yourself']):
            return "I'm Planr, your AI task manager! 📋 I can handle tasks, reminders, events, notes, time tracking, calculations, and much more. What do you need help with?"
        
        # ========== HELP REQUESTS ==========
        if 'can you help' in user_input or 'can you assist' in user_input or 'i need help' in user_input:
            return "Absolutely! I can help with tasks, reminders, notes, calendar events, time tracking, calculations, definitions, journaling, and more. What do you need?"
        
        # ========== CAPABILITIES ==========
        if 'what can you do' in user_input or 'what are your capabilities' in user_input or 'what can i do with you' in user_input:
            return "I can help with:\n• ✅ Tasks & To-Do lists\n• 🔔 Reminders\n• 📅 Calendar & Events\n• 📝 Notes\n• ⏱️ Time Tracking\n• 🧮 Calculations\n• 📖 Dictionary lookups\n• 📔 Journal entries\n• 🔥 Habit Tracking\n• 🎯 Goal Setting\n• 🔊 Voice Commands\n• 📬 Notifications\n• 🔍 Web searches\n• 📏 Unit conversions\n\nWhat would you like to do?"
        
        # ========== SMALL TALK ==========
        for phrase, responses in self.smalltalk.items():
            if user_input == phrase or user_input.startswith(phrase + ' '):
                return random.choice(responses)
        
        # ========== MOOD & FEELINGS ==========
        for mood, responses in self.mood_responses.items():
            if any(feeling in user_input for feeling in [mood, f"i'm {mood}", f"i am {mood}", f"feeling {mood}", f"feel {mood}"]):
                # Check for compound feelings like "stressed and tired"
                return random.choice(responses)
        
        # ========== TOPIC-BASED RESPONSES ==========
        for topic, responses in self.topic_responses.items():
            if topic in user_input:
                return random.choice(responses)
        
        # ========== SPECIFIC COMMON PHRASES ==========
        # Affirmations and encouragement
        if any(phrase in user_input for phrase in ['show me', 'demonstrate', 'example', 'demo']):
            return "I'd love to show you! What feature would you like to see in action?\n\nTry saying things like:\n• 'add task buy groceries'\n• 'set reminder study at 18:00'\n• 'add event meeting on 2024-03-25'\n• 'calculate 15+25*3'\n• 'define algorithm'"
        
        if any(phrase in user_input for phrase in ["don't know", "i dunno", "no idea", "clueless"]):
            return "No problem! Want me to help you figure it out? 🤔 Or I could explain what I can do - just ask 'what can you do'?"
        
        if any(phrase in user_input for phrase in ['test', 'try this', 'try me', 'test me', 'give me an example']) :
            return "Sure! Try one of these:\n• 'Add task finish report by tomorrow'\n• 'Remind me to call mom at 19:00'\n• 'What does photosynthesis mean?'\n• 'Calculate 123 * 456'\n• 'What time is it?'\n\nGo ahead, give it a shot! 🚀"
        
        if any(phrase in user_input for phrase in ['okay', 'ok', 'sure', 'alright', 'got it', 'understood', 'cool', 'nice', 'awesome', 'great']):
            return random.choice(self.positive_responses)
        
        if any(phrase in user_input for phrase in ['please', 'kindly', 'would you mind', 'could you']):
            return "Of course! I'm here to help! 😊 What do you need?"
        
        if any(phrase in user_input for phrase in ['i love', 'i like', 'i enjoy', 'i love it', 'awesome', 'amazing', 'brilliant']):
            return random.choice(self.encouraging_responses)
        
        if any(phrase in user_input for phrase in ['haha', 'lol', 'hehe', 'lmao', '😂', '😅', '😄']):
            return "Glad I could make you laugh! 😄 What else can I help with?"
        
        # ========== TIME-BASED RESPONSES ==========
        current_hour = datetime.now().hour
        if 'time' in user_input and any(word in user_input for word in ['what', 'current', 'now', 'is it']):
            current_time = datetime.now().strftime('%H:%M:%S')
            current_date = datetime.now().strftime('%A, %B %d, %Y')
            return f"🕐 It's {current_time}\n📅 {current_date}"
        
        # ========== GENERAL QUESTIONS ==========
        if user_input.endswith('?') and not any(cmd in user_input for cmd in ['add', 'show', 'mark', 'delete', 'calculate', 'define', 'convert', 'search', 'what time', 'when']):
            # It's a question but not a command
            question_responses = [
                "That's a great question! 🤔 Is there something specific I can help you with?",
                "Interesting! 💭 How can I assist you with that?",
                "Good question! Tell me more - how can I help?",
                "I wonder too! 🧐 What do you need help with?",
                "Great thinking! 💡 What can I do to help?",
            ]
            return random.choice(question_responses)
        
        # ========== STATEMENTS WITH SENTIMENT ==========
        if not user_input.endswith('?') and len(user_input) > 3:
            # Generic positive statements
            if any(word in user_input for word in ['love', 'like', 'enjoy', 'appreciate', 'amazing', 'awesome']):
                return random.choice(self.positive_responses)
            
            # Generic responses for statements
            if any(word in user_input for word in ['just', 'finished', 'completed', 'done', 'did']):
                return "Excellent! You're crushing it! 💪 Anything else I can help with?"
            
            if any(word in user_input for word in ['working on', 'trying to', 'attempting', 'gonna', 'will']):
                return "You got this! 🚀 Let me know if you need any help!"
        
        return None
    
    def _find_similar_command(self, user_input):
        """Find similar commands based on keywords"""
        keywords = {
            'task': "• Show tasks\n• Add task [name]\n• Mark task [id] done",
            'todo': "• Add task [name]\n• Show tasks",
            'reminder': "• Set reminder [text] at [time]\n• Show reminders",
            'event': "• Add event [name] on [date]\n• Show events",
            'note': "• Add note [title] | [content]\n• Show notes",
            'track': "• Start tracking [activity]\n• Stop tracking\n• Activity summary",
            'calculate': "• Calculate [expression] (e.g., '5+3*2')",
            'define': "• Define [word]\n• Dictionary",
            'journal': "• Journal [text]\n• View journal",
            'search': "• Search [query]",
            'time': "• What time\n• What date",
        }
        
        for keyword, commands in keywords.items():
            if keyword in user_input:
                return commands
        return None
