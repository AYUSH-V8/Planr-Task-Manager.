# 🤖 Personal Assistant Chatbot

A Python-based personal assistant chatbot with **both GUI and Web versions** for managing daily tasks, reminders, notes, calendar events, and more - **no external APIs required!**

You can now share it with friends via a web link! 🚀

## Features

✅ **To-Do Task Management** - Add, view, and mark tasks as complete  
✅ **Reminders** - Set reminders at specific times  
✅ **Calendar & Events** - Schedule and track events  
✅ **Notes** - Create and organize notes  
✅ **Time Tracking** - Track activities and get summaries  
✅ **Calculator** - Perform mathematical calculations  
✅ **Dictionary** - Search word definitions  
✅ **Journal** - Write and view journal entries  
✅ **Web Search** - Open web searches  
✅ **Unit Conversion** - Convert between units (km to miles, C to F, etc.)  
✅ **Utilities** - Current time, date, and more  
✅ **Natural Conversation** - Chat like real ChatGPT  

## Requirements

- Python 3.12+ (you already have it!)
- tkinter (comes with Python) - for GUI version
- Flask (installed automatically) - for Web version

## Quick Start

### 🌐 Web Version (Recommended - Share with Friends!)

**Easiest way - Double-click:**
```
run_web.bat
```

**Or command line:**
```bash
cd "c:\Users\abhij\AppData\Local\Programs\Python\Python312\Class XII TUITION\personal chatbot"
pip install flask     # (one-time only)
python app.py
```

**Then open in your browser:**
```
http://localhost:5000
```

**Share with friends on same network:**
1. Find your IP: Open PowerShell and type `ipconfig`
2. Look for "IPv4 Address" (e.g., 192.168.1.100)
3. Share: `http://[YOUR-IP]:5000`

---

### 💻 GUI Version (Desktop App)

**Double-click:**
```
run.bat
```

**Or command line:**
```bash
python main.py
```

---

## Usage Guide

### 💬 Natural Conversations

Just chat naturally! The chatbot understands:
```
hello                    # Greeting
how are you             # Small talk
what can you do         # Questions
thanks                  # Appreciation
bye                     # Say goodbye
```

### 📋 Todo Management

```
add task [task name]           # Add a task
add task high [task name]      # Add high-priority task
show tasks                      # View all tasks
mark task 1 done               # Mark task #1 as complete
delete task 1                  # Delete task #1
```

### 🔔 Reminders

```
set reminder [text] at 15:30   # Set reminder for 3:30 PM
show reminders                 # View all reminders
```

### 📅 Calendar

```
add event [name] on 2024-03-20          # Add event
show events                              # View all events
upcoming events                          # Next 7 days
show calendar                            # Display calendar
```

### 📝 Notes

```
add note [title] | [content]   # Create a note
show notes                      # View all notes
read note 1                     # View note #1
delete note 1                  # Delete note #1
```

### ⏱️ Time Tracking

```
start tracking [activity]      # Start tracking
stop tracking                  # Stop tracking
activity summary               # View summary
```

### 🧮 Calculator

```
calculate 5+3*2                # = 11
calculate 100/4                # = 25
```

### 📖 Dictionary

```
define python                  # Search definition
dictionary                     # List all words
```

### 📔 Journal

```
journal [your entry]           # Write journal entry
view journal                   # View recent entries
view journal today             # Today's entries
```

### 🔧 Utilities

```
what time                      # Current time
what date                      # Current date
search [query]                 # Web search on Google
convert 5 km to miles          # Unit conversion
```

Type **"help"** in the chat for the complete command list!

## File Structure

```
personal chatbot/
├── main.py                 # GUI launcher (Tkinter)
├── app.py                  # Web server (Flask) ⭐ NEW
├── chatbot.py             # Chatbot logic
├── run.bat                # Quick GUI launcher
├── run_web.bat            # Quick web launcher ⭐ NEW
├── requirements.txt       # Dependencies
├── templates/             # Web templates ⭐ NEW
│   └── index.html        # Modern web interface
├── static/                # Web assets ⭐ NEW
│   ├── style.css         # Sleek styling
│   └── script.js         # Chat interactions
├── features/
│   ├── todo.py           # Task management
│   ├── reminders.py      # Reminders
│   ├── calendar.py       # Calendar & events
│   ├── notes.py          # Notes
│   ├── time_tracker.py   # Time tracking
│   ├── calculator.py     # Calculator
│   ├── dictionary.py     # Dictionary
│   ├── journal.py        # Journal
│   └── utilities.py      # Utilities
└── data/                  # JSON storage
    ├── todos.json        # Your tasks
    ├── reminders.json    # Your reminders
    ├── events.json       # Calendar events
    ├── notes.json        # Your notes
    ├── time_tracking.json
    └── journal.json      # Journal entries
```

## Data Persistence

All your data is saved locally in JSON files in the `data/` folder:
- Tasks, reminders, events, notes, time logs, and journal entries persist between sessions
- Data is only stored on your computer (no cloud)

## Tips & Tricks

1. **High Priority Tasks**: Use "add task high [task]" for important tasks
2. **Smart Search**: Type partial commands and the assistant will suggest options
3. **Date Format**: Use YYYY-MM-DD format for dates (e.g., 2024-03-20)
4. **Time Format**: Use 24-hour HH:MM format for times (e.g., 15:30)
5. **Unit Conversion**: Supports km↔miles, kg↔lbs, °C↔°F
6. **Web Sharing**: Make sure both devices are on the same WiFi network

## Web Version Features

🎨 **Modern UI** - Beautiful gradient design with smooth animations  
⚡ **Real-time Chat** - Instant message feedback  
📱 **Responsive** - Works on mobile and desktop  
🔗 **Shareable** - Share link with friends on same network  
🎭 **Typing Indicator** - See when bot is "thinking"  
📖 **Help Modal** - Easy access to all commands  

## Troubleshooting

**Port 5000 already in use?**
```bash
python app.py --port 5001
```

**Can't access from other device?**
- Make sure firewall allows port 5000
- Check both devices are on same WiFi
- Use full IP address with port: `http://192.168.1.100:5000`

**Data not saving?**
- Check `data/` folder exists with write permissions
- Clear browser cache if using web version

**Flask not found?**
```bash
pip install flask
```

## Future Enhancements

- Voice input/output support
- System notifications
- Habit tracking
- Goal setting with progress
- Mobile app version
- Cloud sync option

## License

Open source - Modify and extend as you like!

---

**Made with ❤️ for productivity. Enjoy your personal assistant! 🚀**
