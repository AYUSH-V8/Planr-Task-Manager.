import json
import os
from datetime import datetime

class JournalManager:
    def __init__(self, data_file='data/journal.json'):
        self.data_file = data_file
        self.entries = self.load_entries()
    
    def load_entries(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_entries(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.entries, f, indent=2)
    
    def add_entry(self, content):
        entry = {
            'id': len(self.entries) + 1,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'content': content,
            'mood': 'neutral'
        }
        self.entries.append(entry)
        self.save_entries()
        return f"Journal entry saved for {entry['date']}"
    
    def view_entries(self, days=7):
        if not self.entries:
            return "No journal entries yet."
        
        recent = sorted(self.entries, key=lambda x: x['date'], reverse=True)[:days]
        result = f"📓 Recent Journal Entries (Last {days} days):\n"
        for entry in recent:
            result += f"[{entry['date']} {entry['time']}]\n{entry['content']}\n\n"
        return result
    
    def view_today_entries(self):
        today = datetime.now().strftime('%Y-%m-%d')
        today_entries = [e for e in self.entries if e['date'] == today]
        
        if not today_entries:
            return "No journal entries for today."
        
        result = "📔 Today's Entries:\n"
        for entry in today_entries:
            result += f"[{entry['time']}]\n{entry['content']}\n\n"
        return result
    
    def set_mood(self, entry_id, mood):
        moods = ['happy', 'sad', 'anxious', 'calm', 'excited', 'neutral']
        if mood not in moods:
            return f"Invalid mood. Choose from: {', '.join(moods)}"
        
        for entry in self.entries:
            if entry['id'] == entry_id:
                entry['mood'] = mood
                self.save_entries()
                return f"Mood set to '{mood}' for entry {entry_id}"
        return "Entry not found."
