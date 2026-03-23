import json
import os
from datetime import datetime

class NotesManager:
    def __init__(self, data_file='data/notes.json'):
        self.data_file = data_file
        self.notes = self.load_notes()
    
    def load_notes(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_notes(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.notes, f, indent=2)
    
    def add_note(self, title, content):
        note = {
            'id': len(self.notes) + 1,
            'title': title,
            'content': content,
            'created_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'modified_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.notes.append(note)
        self.save_notes()
        return f"Note '{title}' created!"
    
    def view_notes(self):
        if not self.notes:
            return "No notes saved."
        
        result = "📝 Your Notes:\n"
        for note in self.notes:
            preview = note['content'][:50] + "..." if len(note['content']) > 50 else note['content']
            result += f"[{note['id']}] {note['title']}: {preview}\n"
        return result
    
    def view_note(self, note_id):
        for note in self.notes:
            if note['id'] == note_id:
                return f"📄 {note['title']}\n{note['content']}\n(Created: {note['created_on']})"
        return "Note not found."
    
    def edit_note(self, note_id, content):
        for note in self.notes:
            if note['id'] == note_id:
                note['content'] = content
                note['modified_on'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_notes()
                return f"Note '{note['title']}' updated!"
        return "Note not found."
    
    def delete_note(self, note_id):
        self.notes = [n for n in self.notes if n['id'] != note_id]
        self.save_notes()
        return f"Note {note_id} deleted."
