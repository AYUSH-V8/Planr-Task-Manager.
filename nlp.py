import re
from datetime import datetime

class NLPProcessor:
    """
    Natural Language Processing for intelligent request understanding
    Converts casual user requests to appropriate commands
    """
    
    def __init__(self):
        self.intent_patterns = {
            # ORDER MATTERS - More specific patterns first!
            'set_reminder': [
                r"(?:remind|alert|notify|set an alarm)\s+(?:me\s+)?(?:to\s+)?(.+?)\s+at\s+(\d{1,2}):(\d{2})",
                r"set\s+(?:a\s+)?(?:reminder|alarm)\s+(?:to|for|about)\s+(.+?)\s+at\s+(\d{1,2}):(\d{2})",
            ],
            'add_event': [
                r"(?:schedule|add|meeting|event)\s+(?:with)?\s*(.+?)\s+(?:on|for)\s+(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
            ],
            'define': [
                r"what\s+(?:does|is)\s+([a-z]+)\s+mean",
                r"define\s+([a-z]+)",
            ],
            'calculate': [
                r"what\s+is\s+(\d+)\s+times\s+(\d+)",
                r"what\s+is\s+(\d+\s+(?:plus|minus|times|divided by|[+\-*/%])\s+.+)[\s?!]*$",
                r"calculate\s+(.+)[\s?!]*$",
            ],
            'view_tasks': [
                r"what\s+(?:do|should)\s+i\s+(?:do|need to do)\s+today",
                r"(?:show|list|display)\s+(?:my\s+)?(?:tasks|todos)",
                r"what\s+(?:'s|is)\s+on\s+my\s+(?:list|agenda)",
            ],
            'mark_complete': [
                r"(?:i\s+)?(?:just\s+)?(?:completed|finished)\s+(?:my\s+)?(.+)",
                r"(?:i\s+)?did\s+(.+)",
            ],
            'delete_task': [
                r"(?:delete|remove)\s+(?:task|todo)\s+(\d+)",
            ],
            'delete_note': [
                r"(?:delete|remove)\s+(?:note|notes)\s+(\d+)",
                r"delete\s+note\s+(\d+)",
            ],
            'delete_tracking': [
                r"(?:delete|remove)\s+(?:activity|tracking|session)\s+(\d+)",
                r"delete\s+(?:today|today's)\s+(?:activity|activities|tracking|sessions)",
                r"clear\s+today(?:'s)?\s+(?:activity|activities|tracking|sessions)",
            ],
            'add_task': [
                r"(?:i\s+)?(?:need|should|must|want|gotta|have to|need to)\s+(?:to\s+)?(.+)[\s?!]*$",
                r"(?:add|create)\s+(?:task|todo)\s+(.+)",
            ],
            'add_note': [
                r"note\s+(?:that\s+)?(.+)",
                r"(?:i\s+)?note\s+(.+)",
            ],
            'view_notes': [
                r"(?:show|list|display)\s+(?:my\s+)?notes",
            ],
            'start_tracking': [
                r"(?:i'm|i am|im|i\'m)\s+(?:working on|studying|tracking|doing|working)(?:\s+on)?\s*(.+)?",
                r"(?:start|begin)\s+tracking\s+(.+)",
            ],
            'stop_tracking': [
                r"(?:stop|end)\s+tracking",
                r"(?:i'm|i am|im)\s+(?:done|finished)",
            ],
            'journal': [
                r"journal\s+(.+)",
            ],
        }
    
    def detect_intent(self, user_input):
        """Detect user intent from natural language input"""
        user_input_lower = user_input.lower().strip()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, user_input_lower, re.IGNORECASE)
                if match:
                    return intent, match.groups()
        
        return None, None
    
    def convert_to_command(self, intent, extracted_data):
        """Convert detected intent to chatbot command"""
        
        if intent == 'add_task':
            task_text = extracted_data[0] if extracted_data and extracted_data[0] else ""
            return f"add task {task_text}" if task_text else None
        
        elif intent == 'view_tasks':
            return "show tasks"
        
        elif intent == 'mark_complete':
            if extracted_data and extracted_data[0]:
                return f"Understood! You completed '{extracted_data[0]}'. ✓\nUse 'mark task [number] done' to mark tasks by ID. Type 'show tasks' to see all tasks with IDs."
            return "show tasks"
        
        elif intent == 'delete_task':
            if extracted_data and extracted_data[0]:
                return f"delete task {extracted_data[0]}"
            return "show tasks"
        
        elif intent == 'set_reminder':
            if extracted_data and len(extracted_data) >= 3:
                reminder_text = extracted_data[0]
                hour = extracted_data[1] if extracted_data[1] else ""
                minute = extracted_data[2] if extracted_data[2] else ""
                
                if hour and minute:
                    time_str = f"{hour}:{minute}"
                    return f"set reminder {reminder_text} at {time_str}"
            return None
        
        elif intent == 'add_event':
            if extracted_data and len(extracted_data) >= 2:
                event_name = extracted_data[0]
                event_date = extracted_data[1]
                
                # Normalize date to YYYY-MM-DD if needed
                if '/' in event_date or '-' in event_date:
                    parts = re.split(r'[/-]', event_date)
                    if len(parts) == 3:
                        if len(parts[0]) == 4:  # Already YYYY-MM-DD
                            pass
                        else:  # Try to convert MM/DD/YYYY to YYYY-MM-DD
                            try:
                                event_date = f"{parts[2]}-{parts[0]}-{parts[1]}"
                            except:
                                pass
                
                return f"add event {event_name} on {event_date}"
            return None
        
        elif intent == 'add_note':
            note_text = extracted_data[0] if extracted_data and extracted_data[0] else ""
            return f"add note Untitled | {note_text}" if note_text else None
        
        elif intent == 'view_notes':
            return "show notes"
        
        elif intent == 'start_tracking':
            activity = extracted_data[0] if extracted_data and extracted_data[0] else "something"
            return f"start tracking {activity}"
        
        elif intent == 'stop_tracking':
            return "stop tracking"
        
        elif intent == 'delete_note':
            if extracted_data and extracted_data[0]:
                return f"delete note {extracted_data[0]}"
            return "show notes"
        
        elif intent == 'delete_tracking':
            if extracted_data:
                # If it matches "delete today activities"
                if extracted_data[0] and ('today' in extracted_data[0].lower()):
                    return "delete today activity"
                # If it matches a number
                try:
                    session_num = int(extracted_data[0])
                    return f"delete tracking {session_num}"
                except:
                    return "delete today activity"
            return "delete today activity"
        
        elif intent == 'calculate':
            if extracted_data:
                expression = extracted_data[0] if isinstance(extracted_data[0], str) else ""
                
                # Handle "what is X times Y" pattern
                if len(extracted_data) >= 2 and extracted_data[1]:
                    expression = f"{extracted_data[0]}*{extracted_data[1]}"
                else:
                    # Clean up the expression
                    expression = str(expression).replace(' times ', '*').replace(' divided by ', '/').replace(' plus ', '+').replace(' minus ', '-')
                
                return f"calculate {expression}" if expression else None
            return None
        
        elif intent == 'define':
            word = extracted_data[0] if extracted_data and extracted_data[0] else ""
            return f"define {word}" if word else None
        
        elif intent == 'journal':
            entry = extracted_data[0] if extracted_data and extracted_data[0] else ""
            return f"journal {entry}" if entry else None
        
        return None
