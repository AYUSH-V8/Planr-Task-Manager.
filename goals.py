"""
Goal Setting Module
Track goals with progress tracking and visualization
"""

import json
import os
from datetime import datetime

class GoalManager:
    """Manages goals with progress tracking"""
    
    def __init__(self, data_file='data/goals.json'):
        self.data_file = data_file
        self.goals = self.load_goals()
    
    def load_goals(self):
        """Load goals from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_goals(self):
        """Save goals to JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.goals, f, indent=2)
    
    def create_goal(self, goal_name, target_value, description="", category="general"):
        """
        Create a new goal with target value
        target_value: numeric goal (e.g., read 12 books, exercise 100 times)
        """
        goal_name = goal_name.lower().strip()
        
        if goal_name in self.goals:
            return f"❌ Goal '{goal_name}' already exists!"
        
        try:
            target = float(target_value)
        except ValueError:
            return "❌ Target value must be a number!"
        
        self.goals[goal_name] = {
            'name': goal_name,
            'description': description,
            'category': category,
            'target': target,
            'current': 0,
            'created_date': datetime.now().isoformat(),
            'deadline': None,
            'status': 'in_progress',
            'progress_history': []
        }
        
        self.save_goals()
        return f"🎯 Goal '{goal_name}' created! Target: {target}"
    
    def update_progress(self, goal_name, amount):
        """Update progress toward a goal"""
        goal_name = goal_name.lower().strip()
        
        if goal_name not in self.goals:
            return f"❌ Goal '{goal_name}' not found!"
        
        goal = self.goals[goal_name]
        
        try:
            amount = float(amount)
        except ValueError:
            return "❌ Amount must be a number!"
        
        goal['current'] += amount
        goal['progress_history'].append({
            'date': datetime.now().isoformat(),
            'amount': amount
        })
        
        # Check if goal is complete
        if goal['current'] >= goal['target']:
            goal['status'] = 'completed'
            goal['current'] = goal['target']
            self.save_goals()
            return f"🎉 Congratulations! Goal '{goal_name}' completed!"
        
        self.save_goals()
        percentage = (goal['current'] / goal['target']) * 100
        return f"✅ Updated '{goal_name}'! Progress: {percentage:.1f}%"
    
    def set_deadline(self, goal_name, deadline):
        """Set a deadline for a goal (format: YYYY-MM-DD)"""
        goal_name = goal_name.lower().strip()
        
        if goal_name not in self.goals:
            return f"❌ Goal '{goal_name}' not found!"
        
        try:
            datetime.strptime(deadline, '%Y-%m-%d')
        except ValueError:
            return "❌ Invalid date format! Use YYYY-MM-DD"
        
        self.goals[goal_name]['deadline'] = deadline
        self.save_goals()
        return f"📅 Deadline set for '{goal_name}': {deadline}"
    
    def get_goal_status(self, goal_name):
        """Get detailed status of a goal"""
        goal_name = goal_name.lower().strip()
        
        if goal_name not in self.goals:
            return f"❌ Goal '{goal_name}' not found!"
        
        goal = self.goals[goal_name]
        percentage = (goal['current'] / goal['target']) * 100
        
        response = f"""
🎯 Goal: {goal['name'].title()}
─────────────────────
Description: {goal['description'] or 'No description'}
Category: {goal['category']}
Target: {goal['target']} | Current: {goal['current']}
Progress: {percentage:.1f}%
Status: {goal['status'].replace('_', ' ').title()}
Created: {goal['created_date'][:10]}
"""
        
        if goal['deadline']:
            response += f"Deadline: {goal['deadline']}\n"
        
        response += self._get_progress_bar(percentage)
        return response.strip()
    
    def _get_progress_bar(self, percentage):
        """Generate a visual progress bar"""
        filled = int(percentage / 5)  # 20 chars = 100%
        empty = 20 - filled
        bar = "█" * filled + "░" * empty
        return f"[{bar}] {percentage:.1f}%"
    
    def view_all_goals(self):
        """View all goals with progress"""
        if not self.goals:
            return "📋 No goals created yet. Start by creating one!"
        
        response = "🎯 All Goals:\n" + "─" * 50 + "\n"
        
        # Separate by status
        active = {k: v for k, v in self.goals.items() if v['status'] == 'in_progress'}
        completed = {k: v for k, v in self.goals.items() if v['status'] == 'completed'}
        
        if active:
            response += "📍 Active Goals:\n"
            for goal_name, goal in active.items():
                pct = (goal['current'] / goal['target']) * 100
                response += f"  • {goal_name.title()}: {pct:.0f}% ({goal['current']:.0f}/{goal['target']:.0f})\n"
        
        if completed:
            response += "\n✅ Completed:\n"
            for goal_name, goal in completed.items():
                response += f"  • {goal_name.title()}: ✓\n"
        
        return response.strip()
    
    def delete_goal(self, goal_name):
        """Delete a goal"""
        goal_name = goal_name.lower().strip()
        
        if goal_name not in self.goals:
            return f"❌ Goal '{goal_name}' not found!"
        
        del self.goals[goal_name]
        self.save_goals()
        return f"🗑️ Goal '{goal_name}' deleted!"
    
    def get_goals_summary(self):
        """Get summary of all goals"""
        if not self.goals:
            return "📊 No goals to summarize!"
        
        total = len(self.goals)
        completed = sum(1 for g in self.goals.values() if g['status'] == 'completed')
        
        response = f"📊 Goals Summary:\n" + "─" * 40 + "\n"
        response += f"Total Goals: {total}\n"
        response += f"Completed: {completed}\n"
        response += f"In Progress: {total - completed}\n\n"
        
        response += "📈 Progress Breakdown:\n"
        for goal_name, goal in sorted(self.goals.items(), 
                                     key=lambda x: (x[1]['current']/x[1]['target'])*100,
                                     reverse=True):
            pct = (goal['current'] / goal['target']) * 100
            icon = "✅" if goal['status'] == 'completed' else "📍"
            response += f"{icon} {goal_name.title()}: {pct:.0f}%\n"
        
        return response.strip()
    
    def get_progress_visualization(self, goal_name):
        """Get visual progress bar for a goal"""
        goal_name = goal_name.lower().strip()
        
        if goal_name not in self.goals:
            return f"❌ Goal '{goal_name}' not found!"
        
        goal = self.goals[goal_name]
        percentage = (goal['current'] / goal['target']) * 100
        
        # Create detailed progress visualization
        response = f"📊 {goal_name.title()} Progress\n"
        response += "─" * 40 + "\n"
        
        # Progress bar
        filled = int(percentage / 5)
        empty = 20 - filled
        bar = "█" * filled + "░" * empty
        response += f"[{bar}]\n"
        response += f"{percentage:.1f}% ({goal['current']:.0f}/{goal['target']:.0f})\n"
        
        # Days remaining if deadline set
        if goal['deadline']:
            from datetime import datetime as dt
            try:
                deadline = dt.strptime(goal['deadline'], '%Y-%m-%d')
                days_left = (deadline - dt.now()).days
                if days_left > 0:
                    response += f"\n⏰ Days remaining: {days_left} days"
                elif days_left == 0:
                    response += f"\n⏰ Due today!"
                else:
                    response += f"\n⚠️ Overdue by {abs(days_left)} days"
            except:
                pass
        
        return response.strip()
