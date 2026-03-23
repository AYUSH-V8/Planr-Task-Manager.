# 📋 Planr - AI Task Manager

A Python-based intelligent task management chatbot with **both GUI and Web versions** for organizing daily tasks, reminders, notes, calendar events, and more - **no external APIs required!**

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

## Requirements

- Python 3.12+ (you already have it!)
- tkinter (comes with Python)
- No external API required!

## Installation & Running

### Version 1: GUI Application (Desktop)

#### 1. Navigate to the project directory:
```bash
cd "c:\Users\abhij\AppData\Local\Programs\Python\Python312\Class XII TUITION\personal chatbot"
```

#### 2. Run the GUI version:
```bash
python main.py
```

Or double-click **`run.bat`** - The GUI window will open. You're ready to chat!

---

### Version 2: Web Application (Modern, Shareable) ⭐ **NEW**

#### 1. Install Flask (one-time):
```bash
pip install flask
```

#### 2. Run the web version:
```bash
python app.py
```

Or double-click **`run_web.bat`** - The web server will start!

#### 3. Open in your browser:
```
http://localhost:5000
```

#### 4. Share with friends:
```
http://[YOUR-IP]:5000
```
Find your IP address:
```powershell
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

---

## Installation & Running (Old Section - Keep Below)

### Version 1: GUI Application (Desktop)

#### 1. Navigate to the project directory:

## Usage Guide

### Quick Commands

**Todo Management:**
```
add task [task name]           # Add a task
add task high [task name]      # Add high-priority task
show tasks                      # View all tasks
mark task 1 done               # Mark task #1 as complete
delete task 1                  # Delete task #1
```

**Reminders:**
```
set reminder [text] at 15:30   # Set reminder for 3:30 PM
show reminders                 # View all reminders
```

**Calendar:**
```
add event [name] on 2024-03-20          # Add event
show events                              # View all events
upcoming events                          # Next 7 days
show calendar                            # Display calendar
```

**Notes:**
```
add note [title] | [content]   # Create a note
show notes                      # View all notes
read note 1                     # View note #1
delete note 1                   # Delete note #1
```

**Time Tracking:**
```
start tracking [activity]      # Start tracking
stop tracking                  # Stop tracking
activity summary               # View summary
```

**Calculator:**
```
calculate 5+3*2                # = 11
calculate 100/4                # = 25
```

**Dictionary:**
```
define python                  # Search definition
dictionary                     # List all words
```

**Journal:**
```
journal [your entry]           # Write journal entry
view journal                   # View recent entries
view journal today             # Today's entries
```

**Utilities:**
```
what time                      # Current time
what date                      # Current date
search [query]                 # Web search on Google
convert 5 km to miles          # Unit conversion
```

### Type "help" in the chat for the complete command reference!

## File Structure

```
personal chatbot/
├── main.py                 # GUI entry point
├── chatbot.py             # Main chatbot logic
├── features/
│   ├── todo.py           # Task management
│   ├── reminders.py      # Reminders
│   ├── calendar.py       # Calendar & events
│   ├── notes.py          # Notes management
│   ├── time_tracker.py   # Time tracking
│   ├── calculator.py     # Calculator
│   ├── dictionary.py     # Dictionary
│   ├── journal.py        # Journal entries
│   └── utilities.py      # Helper utilities
└── data/                 # JSON storage
    ├── todos.json
    ├── reminders.json
    ├── events.json
    ├── notes.json
    ├── time_tracking.json
    └── journal.json
```

## Data Persistence

All your data is saved locally in JSON files in the `data/` folder:
- **todos.json** - Your tasks
- **reminders.json** - Your reminders
- **events.json** - Calendar events
- **notes.json** - Your notes
- **time_tracking.json** - Time tracking sessions
- **journal.json** - Journal entries

Data persists between sessions!

## Tips & Tricks

1. **High Priority Tasks**: Use "add task high [task]" for important tasks
2. **Smart Search**: Type partial commands and the assistant will suggest options
3. **Date Format**: Use YYYY-MM-DD format for dates (e.g., 2024-03-20)
4. **Time Format**: Use 24-hour HH:MM format for times (e.g., 15:30)
5. **Unit Conversion**: Supports km↔miles, kg↔lbs, °C↔°F

## Troubleshooting

**Issue**: GUI doesn't appear
- **Solution**: Make sure tkinter is installed: `python -m tkinter`

**Issue**: Data not saving
- **Solution**: Check that the `data/` folder exists and has write permissions

**Issue**: Commands not recognized
- **Solution**: Type "help" to see exact command syntax

## Future Enhancements

- Voice input/output
- Notifications using system notifications
- Weather integration (local weather calculation)
- Habit tracking
- Goal setting
- Email integration

## License

Open source - Feel free to modify and extend!

---

**Enjoy Planr! 🚀**
