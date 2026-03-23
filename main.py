import tkinter as tk
from tkinter import scrolledtext, messagebox
from chatbot import PersonalAssistant
import threading

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Personal Assistant Chatbot")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")
        
        self.assistant = PersonalAssistant()
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header = tk.Label(
            self.root,
            text="🤖 Personal Assistant",
            font=("Arial", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Chat display area
        chat_frame = tk.Frame(self.root, bg="white")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Arial", 10),
            bg="white",
            fg="#333",
            height=20,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for styling
        self.chat_display.tag_config("bot", foreground="#4CAF50", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("user", foreground="#2196F3", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("system", foreground="#FF9800", font=("Arial", 10))
        
        # Input frame
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bg="white",
            fg="#333",
            relief=tk.FLAT,
            bd=2
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            cursor="hand2"
        )
        send_btn.pack(side=tk.LEFT)
        
        # Help button
        help_btn = tk.Button(
            input_frame,
            text="Help",
            command=self.show_help,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=10,
            cursor="hand2"
        )
        help_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Welcome message
        self.display_message(
            "bot",
            "Welcome to your Personal Assistant! 🎉\n"
            "Type 'help' for available commands or just start chatting.\n"
            "Type 'quit' to exit."
        )
    
    def send_message(self):
        user_input = self.input_field.get().strip()
        if not user_input:
            return
        
        # Display user message
        self.display_message("user", f"You: {user_input}")
        self.input_field.delete(0, tk.END)
        
        # Check for quit command
        if user_input.lower() in ['quit', 'exit']:
            self.display_message("system", "Goodbye! 👋")
            self.root.after(1000, self.root.quit)
            return
        
        # Process command in a separate thread to keep GUI responsive
        threading.Thread(target=self._process_command, args=(user_input,), daemon=True).start()
    
    def _process_command(self, user_input):
        response = self.assistant.process_command(user_input)
        
        # Check for quit response
        if response == "QUIT":
            self.display_message("system", "Goodbye! 👋")
            self.root.after(1000, self.root.quit)
            return
        
        self.display_message("bot", response)
    
    def display_message(self, tag, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n\n", tag)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def show_help(self):
        help_text = self.assistant.utils.get_help()
        # Create a new window for help
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - Personal Assistant")
        help_window.geometry("600x500")
        
        help_display = scrolledtext.ScrolledText(
            help_window,
            wrap=tk.WORD,
            font=("Courier", 9),
            bg="white",
            fg="#333"
        )
        help_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_display.insert(tk.END, help_text)
        help_display.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    gui = ChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
