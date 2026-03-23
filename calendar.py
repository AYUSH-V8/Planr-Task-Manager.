import json
import os
from datetime import datetime, timedelta
import calendar

class CalendarManager:
    def __init__(self, data_file='data/events.json'):
        self.data_file = data_file
        self.events = self.load_events()
    
    def load_events(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_events(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.events, f, indent=2)
    
    def add_event(self, event_name, date, time='12:00'):
        event = {
            'id': len(self.events) + 1,
            'name': event_name,
            'date': date,
            'time': time,
            'created_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.events.append(event)
        self.save_events()
        return f"Event '{event_name}' scheduled for {date} at {time}"
    
    def view_events(self, month=None, year=None):
        if not self.events:
            return "No events scheduled."
        
        result = "📅 Your Events:\n"
        for event in sorted(self.events, key=lambda x: x['date']):
            result += f"[{event['id']}] {event['name']} - {event['date']} at {event['time']}\n"
        return result
    
    def get_upcoming_events(self, days=7):
        today = datetime.now().date()
        upcoming = []
        for event in self.events:
            try:
                event_date = datetime.strptime(event['date'], '%Y-%m-%d').date()
                if today <= event_date <= today + timedelta(days=days):
                    upcoming.append(event)
            except:
                pass
        
        if not upcoming:
            return f"No events in the next {days} days."
        
        result = f"📌 Upcoming events (next {days} days):\n"
        for e in upcoming:
            result += f"  • {e['name']} on {e['date']}\n"
        return result
    
    def remove_event(self, event_id):
        self.events = [e for e in self.events if e['id'] != event_id]
        self.save_events()
        return f"Event {event_id} removed."
    
    def show_calendar(self, month=None, year=None):
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year
        
        cal = calendar.month(year, month)
        return f"📆 {calendar.month_name[month]} {year}\n{cal}"
