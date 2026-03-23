class Dictionary:
    def __init__(self):
        # Local dictionary with common words and definitions
        self.words = {
            'python': 'A high-level programming language known for simplicity.',
            'code': 'Instructions written in a programming language for computers.',
            'algorithm': 'Step-by-step procedure for solving a problem.',
            'variable': 'A named location in memory to store data.',
            'function': 'A reusable block of code that performs a specific task.',
            'loop': 'A control structure that repeats a block of code.',
            'conditional': 'An if-else statement that controls program flow.',
            'data': 'Information used by programs.',
            'database': 'Organized collection of data.',
            'server': 'A computer that provides resources to other computers.',
            'client': 'A computer or application that requests services.',
            'network': 'Connected computers that can share resources.',
            'internet': 'Global system of interconnected networks.',
            'api': 'Interface for applications to communicate.',
            'framework': 'Collection of libraries and tools for development.',
            'library': 'Collection of reusable code modules.',
            'bug': 'An error in computer code.',
            'debug': 'Process of finding and fixing errors.',
            'compile': 'Convert source code to executable form.',
            'syntax': 'Rules for writing correct code.',
            'robot': 'A machine designed to perform automated tasks.',
            'artificial intelligence': 'Technology that enables machines to simulate human intelligence.',
            'automation': 'Using technology to perform tasks with minimal human intervention.',
            'productivity': 'Effectiveness of effort measured by the rate of output per unit of input.',
            'efficiency': 'Ability to accomplish a task with minimal waste of resources.',
            'organization': 'Arranging tasks or items in a structured manner.',
            'priority': 'Importance or urgency of a task or item.',
            'schedule': 'Plan of activities or events arranged in order of time.',
            'reminder': 'Notification to remember something at a specific time.',
            'deadline': 'Final time or date for completing a task.',
            'task': 'A piece of work to be done or undertaken.',
            'goal': 'Desired result or outcome you aim to achieve.',
            'milestone': 'Significant event or stage in progress towards a goal.',
        }
    
    def search_word(self, word):
        word = word.lower().strip()
        if word in self.words:
            return f"📖 {word.upper()}: {self.words[word]}"
        
        # Simple suggestions for similar words
        similar = [w for w in self.words if word in w or w in word]
        if similar:
            result = f"Word '{word}' not found. Did you mean:\n"
            for w in similar[:3]:
                result += f"  • {w}\n"
            return result
        return f"Word '{word}' not found in dictionary."
    
    def add_word(self, word, definition):
        word = word.lower().strip()
        self.words[word] = definition
        return f"Added '{word}' to dictionary!"
    
    def list_words(self):
        result = "📚 Available Words:\n"
        for i, word in enumerate(sorted(self.words.keys()), 1):
            result += f"{i}. {word}\n"
            if i >= 20:
                result += f"... and {len(self.words) - 20} more words\n"
                break
        return result
