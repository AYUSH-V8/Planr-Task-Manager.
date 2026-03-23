"""
Habit Tracking Module
Tracks daily habits with streak tracking and visualization
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class HabitTracker:
    """Manages habits and tracks streaks"""
    
    def __init__(self, data_file='data/habits.json'):
        self.data_file = data_file
        self.habits = self.load_habits()
    
    def load_habits(self):
        """Load habits from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_habits(self):
        """Save habits to JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.habits, f, indent=2)
    
    def create_habit(self, habit_name, description="", frequency="daily"):
        """
        Create a new habit
        frequency: 'daily', 'weekly', 'monthly'
        """
        habit_name = habit_name.lower().strip()
        
        if habit_name in self.habits:
            return f"❌ Habit '{habit_name}' already exists!"
        
        self.habits[habit_name] = {
            'name': habit_name,
            'description': description,
            'frequency': frequency,
            'created_date': datetime.now().isoformat(),
            'current_streak': 0,
            'longest_streak': 0,
            'completed_dates': [],
            'total_completions': 0
        }
        
        self.save_habits()
        return f"✅ Habit '{habit_name}' created with {frequency} frequency!"
    
    def log_habit(self, habit_name):
        """Log habit completion for today"""
        habit_name = habit_name.lower().strip()
        
        if habit_name not in self.habits:
            return f"❌ Habit '{habit_name}' not found!"
        
        today = datetime.now().strftime('%Y-%m-%d')
        habit = self.habits[habit_name]
        
        if today in habit['completed_dates']:
            return f"✅ Habit '{habit_name}' already logged today!"
        
        habit['completed_dates'].append(today)
        habit['total_completions'] += 1
        self._update_streak(habit_name)
        
        self.save_habits()
        streak = self.habits[habit_name]['current_streak']
        return f"🔥 Logged '{habit_name}'! Current streak: {streak} days"
    
    def _update_streak(self, habit_name):
        """Update current and longest streaks"""
        habit = self.habits[habit_name]
        completed = sorted(habit['completed_dates'])
        
        if not completed:
            habit['current_streak'] = 0
            return
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Calculate current streak
        current_streak = 0
        check_date = datetime.strptime(today, '%Y-%m-%d')
        
        while check_date.strftime('%Y-%m-%d') in completed:
            current_streak += 1
            check_date -= timedelta(days=1)
        
        habit['current_streak'] = current_streak
        
        # Update longest streak if needed
        if current_streak > habit['longest_streak']:
            habit['longest_streak'] = current_streak
    
    def get_habit_status(self, habit_name):
        """Get detailed status of a habit"""
        habit_name = habit_name.lower().strip()
        
        if habit_name not in self.habits:
            return f"❌ Habit '{habit_name}' not found!"
        
        habit = self.habits[habit_name]
        today = datetime.now().strftime('%Y-%m-%d')
        logged_today = "✅ Yes" if today in habit['completed_dates'] else "❌ No"
        
        response = f"""
📊 Habit: {habit['name'].title()}
─────────────────────
Description: {habit['description'] or 'No description'}
Frequency: {habit['frequency']}
Current Streak: 🔥 {habit['current_streak']} days
Longest Streak: 🏆 {habit['longest_streak']} days
Total Completions: {habit['total_completions']}
Logged Today: {logged_today}
Created: {habit['created_date'][:10]}
"""
        return response.strip()
    
    def view_all_habits(self):
        """View all habits with current status"""
        if not self.habits:
            return "📝 No habits created yet. Start by creating one!"
        
        today = datetime.now().strftime('%Y-%m-%d')
        response = "🎯 All Habits:\n" + "─" * 40 + "\n"
        
        for habit_name, habit in self.habits.items():
            logged = "✅" if today in habit['completed_dates'] else "⭕"
            response += f"{logged} {habit_name.title()}\n"
            response += f"   Streak: 🔥 {habit['current_streak']} | Best: 🏆 {habit['longest_streak']}\n"
        
        return response.strip()
    
    def delete_habit(self, habit_name):
        """Delete a habit"""
        habit_name = habit_name.lower().strip()
        
        if habit_name not in self.habits:
            return f"❌ Habit '{habit_name}' not found!"
        
        del self.habits[habit_name]
        self.save_habits()
        return f"🗑️ Habit '{habit_name}' deleted!"
    
    def get_streak_summary(self):
        """Get summary of all streaks"""
        if not self.habits:
            return "📊 No habits to summarize!"
        
        response = "🔥 Streak Summary:\n" + "─" * 40 + "\n"
        
        # Sort by current streak
        sorted_habits = sorted(
            self.habits.items(),
            key=lambda x: x[1]['current_streak'],
            reverse=True
        )
        
        for habit_name, habit in sorted_habits:
            streak = habit['current_streak']
            longest = habit['longest_streak']
            completions = habit['total_completions']
            
            # Visual streak indicator
            if streak >= 30:
                indicator = "🔥🔥🔥"
            elif streak >= 14:
                indicator = "🔥🔥"
            elif streak >= 7:
                indicator = "🔥"
            else:
                indicator = "⭕"
            
            response += f"{indicator} {habit_name.title()}: {streak} days (Best: {longest})\n"
        
        return response.strip()
    
    def get_streak_visualization(self, habit_name):
        """Get visual representation of habit completion"""
        habit_name = habit_name.lower().strip()
        
        if habit_name not in self.habits:
            return f"❌ Habit '{habit_name}' not found!"
        
        habit = self.habits[habit_name]
        completed = set(habit['completed_dates'])
        
        # Get last 30 days
        response = f"📅 Last 30 days ({habit_name.title()}):\n"
        response += "─" * 32 + "\n"
        
        today = datetime.now()
        for i in range(29, -1, -1):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            symbol = "🟩" if date in completed else "⬜"
            
            if (29 - i) % 5 == 4:  # New line every 5 days
                response += symbol + "\n"
            else:
                response += symbol
        
        return response.strip()
