// ========== MAIN CHAT FUNCTIONALITY ==========

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded, initializing chat...');
    
    const messageInput = document.getElementById('messageInput');
    if (!messageInput) {
        console.error('Message input not found!');
        return;
    }
    
    messageInput.focus();
    
    // Handle Enter key to send message
    messageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
    
    // Load conversations after page is fully ready
    setTimeout(loadConversations, 1000);
});

// ========== SEND MESSAGE FUNCTION ==========

function sendMessage() {
    console.log('sendMessage called');
    
    const input = document.getElementById('messageInput');
    if (!input) {
        console.error('Input element not found');
        return;
    }
    
    const message = input.value.trim();
    if (!message) {
        console.warn('Empty message');
        return;
    }

    console.log('Sending message:', message);
    
    // Clear input immediately
    input.value = '';
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Show typing indicator
    showTypingIndicator();

    // Send to server
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => {
        console.log('Response received:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Got data:', data);
        removeTypingIndicator();
        
        if (data.bot_response) {
            addMessage(data.bot_response, 'bot');
        } else if (data.error) {
            addMessage('Error: ' + data.error, 'bot');
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        removeTypingIndicator();
        addMessage('Error connecting to server: ' + error.message, 'bot');
    });
    
    input.focus();
}

// ========== MESSAGE DISPLAY ==========

function addMessage(text, sender) {
    console.log('Adding message:', sender, text.substring(0, 50));
    
    const messagesDiv = document.getElementById('messages');
    if (!messagesDiv) {
        console.error('Messages div not found');
        return;
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    if (sender === 'bot') {
        contentDiv.innerHTML = formatBotMessage(text);
    } else {
        contentDiv.textContent = text;
    }

    messageDiv.appendChild(contentDiv);
    messagesDiv.appendChild(messageDiv);

    // Scroll to bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function formatBotMessage(text) {
    let html = escapeHtml(text);
    html = html.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\n/g, '<br>');
    return html;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showTypingIndicator() {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = 'typing-indicator';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content typing-indicator';
    contentDiv.innerHTML = '<span></span><span></span><span></span>';

    messageDiv.appendChild(contentDiv);
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// ========== HELP MODAL ==========

async function toggleHelp() {
    const modal = document.getElementById('helpModal');
    if (!modal) return;
    
    if (modal.classList.contains('active')) {
        modal.classList.remove('active');
    } else {
        modal.classList.add('active');
        
        const helpContent = document.getElementById('helpContent');
        if (helpContent && helpContent.textContent === 'Loading help...') {
            try {
                const response = await fetch('/help');
                const data = await response.json();
                helpContent.innerHTML = `<pre>${escapeHtml(data.help)}</pre>`;
            } catch (error) {
                helpContent.innerHTML = '<p>Error loading help</p>';
            }
        }
    }
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('helpModal');
    if (modal && event.target === modal) {
        modal.classList.remove('active');
    }
}

// Close modal on Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modal = document.getElementById('helpModal');
        if (modal && modal.classList.contains('active')) {
            toggleHelp();
        }
    }
});

// ========== CONVERSATION MANAGEMENT ==========

async function loadConversations() {
    console.log('Loading conversations...');
    try {
        const response = await fetch('/conversations');
        if (!response.ok) {
            console.warn('Conversations endpoint returned:', response.status);
            document.getElementById('conversationsList').innerHTML = 
                '<p class="empty-state">Chat history unavailable</p>';
            return;
        }
        
        const data = await response.json();
        console.log('Loaded conversations:', data.conversations.length);
        displayConversations(data.conversations);
    } catch (error) {
        console.error('Error loading conversations:', error);
        document.getElementById('conversationsList').innerHTML = 
            '<p class="empty-state">No conversations yet</p>';
    }
}

function displayConversations(conversations) {
    const list = document.getElementById('conversationsList');
    if (!list) return;
    
    if (!conversations || conversations.length === 0) {
        list.innerHTML = '<p class="empty-state">No conversations yet</p>';
        return;
    }
    
    list.innerHTML = '';
    
    conversations.forEach(conv => {
        const item = document.createElement('div');
        item.className = 'conversation-item';
        
        const date = new Date(conv.started_at);
        const timeStr = date.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
        });
        const dateStr = date.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric' 
        });
        
        item.innerHTML = `
            <div class="conversation-info" onclick="loadConversationHistory('${conv.id}')">
                <div class="conversation-title">${escapeHtml(conv.title)}</div>
                <div class="conversation-meta">
                    <span>${dateStr} ${timeStr}</span>
                    <span>${conv.message_count} messages</span>
                </div>
            </div>
            <button class="conversation-delete" onclick="deleteConversation('${conv.id}', event)">
                <i class="fas fa-trash-alt"></i>
            </button>
        `;
        
        list.appendChild(item);
    });
}

function loadConversationHistory(sessionId) {
    console.log('Loading conversation:', sessionId);
    fetch(`/conversation/${sessionId}`)
    .then(response => response.json())
    .then(conv => {
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML = '';
        
        if (conv.messages) {
            conv.messages.forEach(msg => {
                addMessage(msg.user, 'user');
                addMessage(msg.bot, 'bot');
            });
        }
        
        const sidebar = document.getElementById('sidebar');
        if (sidebar && sidebar.classList.contains('active')) {
            toggleSidebar();
        }
    })
    .catch(error => console.error('Error loading conversation:', error));
}

function deleteConversation(sessionId, event) {
    event.stopPropagation();
    
    if (!confirm('Delete this conversation?')) {
        return;
    }
    
    fetch(`/conversation/${sessionId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            loadConversations();
        } else {
            alert('Error deleting conversation');
        }
    })
    .catch(error => console.error('Error:', error));
}

function startNewConversation() {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML = `
        <div class="message bot-message">
            <div class="message-content">
                <p>Starting fresh conversation...</p>
            </div>
        </div>
    `;
    
    const sidebar = document.getElementById('sidebar');
    if (sidebar && sidebar.classList.contains('active')) {
        toggleSidebar();
    }
}

function clearAllConversations() {
    if (!confirm('Delete ALL conversations? This cannot be undone.')) {
        return;
    }
    
    fetch('/conversations/clear', {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            loadConversations();
            startNewConversation();
        } else {
            alert('Error clearing conversations');
        }
    })
    .catch(error => console.error('Error:', error));
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
}

// Close sidebar when clicking outside
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.querySelector('.mobile-menu-toggle');
    
    if (sidebar && 
        !sidebar.contains(event.target) && 
        toggle && !toggle.contains(event.target) && 
        window.innerWidth <= 768) {
        sidebar.classList.remove('active');
    }
});

// ========== CALENDAR PICKER FUNCTIONALITY ==========

let currentCalendarDate = new Date();
let selectedDate = null;

// Initialize calendar on page load
document.addEventListener('DOMContentLoaded', function() {
    renderCalendar();
});

function renderCalendar() {
    const year = currentCalendarDate.getFullYear();
    const month = currentCalendarDate.getMonth();
    
    // Update month/year display
    const monthYearEl = document.getElementById('monthYear');
    if (monthYearEl) {
        const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                           'July', 'August', 'September', 'October', 'November', 'December'];
        monthYearEl.textContent = `${monthNames[month]} ${year}`;
    }
    
    const grid = document.getElementById('calendarGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    // Add day headers
    const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    dayNames.forEach(day => {
        const dayHeader = document.createElement('div');
        dayHeader.className = 'calendar-day header';
        dayHeader.textContent = day;
        grid.appendChild(dayHeader);
    });
    
    // Get first day of month and number of days
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const daysInPrevMonth = new Date(year, month, 0).getDate();
    
    // Add previous month's days
    for (let i = firstDay - 1; i >= 0; i--) {
        const dayDiv = document.createElement('div');
        dayDiv.className = 'calendar-day other-month';
        dayDiv.textContent = daysInPrevMonth - i;
        grid.appendChild(dayDiv);
    }
    
    // Add current month's days
    const today = new Date();
    for (let day = 1; day <= daysInMonth; day++) {
        const dayDiv = document.createElement('div');
        dayDiv.className = 'calendar-day';
        dayDiv.textContent = day;
        
        const cellDate = new Date(year, month, day);
        const cellDateString = cellDate.toISOString().split('T')[0];
        
        // Check if today
        if (cellDate.toDateString() === today.toDateString()) {
            dayDiv.classList.add('today');
        }
        
        // Check if selected
        if (selectedDate === cellDateString) {
            dayDiv.classList.add('selected');
        }
        
        // Add click handler
        dayDiv.addEventListener('click', function() {
            selectDate(cellDateString, dayDiv);
        });
        
        grid.appendChild(dayDiv);
    }
    
    // Add next month's days
    const totalCells = grid.children.length - 7; // Subtract header row
    const remainingCells = 42 - totalCells; // 6 weeks * 7 days
    for (let day = 1; day <= remainingCells; day++) {
        const dayDiv = document.createElement('div');
        dayDiv.className = 'calendar-day other-month';
        dayDiv.textContent = day;
        grid.appendChild(dayDiv);
    }
}

function selectDate(dateString, element) {
    selectedDate = dateString;
    document.getElementById('eventDate').value = dateString;
    
    // Update visual selection
    document.querySelectorAll('.calendar-day.selected').forEach(day => {
        day.classList.remove('selected');
    });
    element.classList.add('selected');
    
    // Update display
    const dateObj = new Date(dateString + 'T00:00:00');
    const formatter = new Intl.DateTimeFormat('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    document.getElementById('selectedDateDisplay').textContent = formatter.format(dateObj);
}

function previousMonth() {
    currentCalendarDate.setMonth(currentCalendarDate.getMonth() - 1);
    renderCalendar();
}

function nextMonth() {
    currentCalendarDate.setMonth(currentCalendarDate.getMonth() + 1);
    renderCalendar();
}

// ========== EVENT MODAL FUNCTIONS ==========

function openEventModal() {
    const modal = document.getElementById('eventModal');
    if (modal) {
        modal.classList.add('active');
        document.addEventListener('keydown', handleModalEscape);
    }
}

function closeEventModal() {
    const modal = document.getElementById('eventModal');
    if (modal) {
        modal.classList.remove('active');
        resetEventForm();
        document.removeEventListener('keydown', handleModalEscape);
    }
}

function handleModalEscape(event) {
    if (event.key === 'Escape') {
        closeEventModal();
    }
}

function resetEventForm() {
    document.getElementById('eventName').value = '';
    document.getElementById('eventDate').value = '';
    document.getElementById('eventTime').value = '12:00';
    selectedDate = null;
    document.getElementById('selectedDateDisplay').textContent = 'None';
    document.querySelectorAll('.calendar-day.selected').forEach(day => {
        day.classList.remove('selected');
    });
}

function submitEvent() {
    const eventName = document.getElementById('eventName').value.trim();
    const eventDate = document.getElementById('eventDate').value;
    const eventTime = document.getElementById('eventTime').value;
    
    if (!eventName) {
        alert('Please enter an event name!');
        return;
    }
    
    if (!eventDate) {
        alert('Please select a date!');
        return;
    }
    
    // Format date to YYYY-MM-DD
    const message = `add event ${eventName} on ${eventDate}`;
    
    // Clear form and close modal
    closeEventModal();
    
    // Send message to chatbot
    sendEventMessage(message);
}

function sendEventMessage(message) {
    const input = document.getElementById('messageInput');
    const messagesDiv = document.getElementById('messages');
    
    // Add user message
    addMessage(message, 'user');
    
    // Show typing indicator
    showTypingIndicator();
    
    // Send to server
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        removeTypingIndicator();
        
        if (data.bot_response) {
            addMessage(data.bot_response, 'bot');
        } else if (data.error) {
            addMessage('Error: ' + data.error, 'bot');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        removeTypingIndicator();
        addMessage('Error connecting to server: ' + error.message, 'bot');
    });
}

// Click outside modal to close
window.addEventListener('click', function(event) {
    const eventModal = document.getElementById('eventModal');
    const goalsModal = document.getElementById('goalsModal');
    if (eventModal && event.target === eventModal) {
        closeEventModal();
    }
    if (goalsModal && event.target === goalsModal) {
        closeGoalsPanel();
    }
});

// ========== VOICE INPUT FUNCTIONALITY ==========

let isListening = false;

function toggleVoiceInput() {
    const voiceBtn = document.getElementById('voiceBtn');
    const voiceStatus = document.getElementById('voiceStatus');
    
    if (isListening) {
        stopVoiceInput();
    } else {
        startVoiceInput();
    }
}

function startVoiceInput() {
    isListening = true;
    const voiceBtn = document.getElementById('voiceBtn');
    const voiceStatus = document.getElementById('voiceStatus');
    const statusText = document.getElementById('voiceStatusText');
    
    voiceBtn.classList.add('listening');
    voiceStatus.style.display = 'block';
    statusText.textContent = '🎤 Listening...';
    
    // Call backend voice API
    fetch('/voice/listen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.text) {
            // Put the recognized text in the message input
            document.getElementById('messageInput').value = data.text;
            showNotification('Voice Input', data.text, 'success');
        } else if (data.error) {
            showNotification('Voice Error', data.error, 'error');
        }
        stopVoiceInput();
    })
    .catch(error => {
        console.error('Voice error:', error);
        showNotification('Voice Error', 'Failed to process voice input', 'error');
        stopVoiceInput();
    });
}

function stopVoiceInput() {
    isListening = false;
    const voiceBtn = document.getElementById('voiceBtn');
    const voiceStatus = document.getElementById('voiceStatus');
    
    voiceBtn.classList.remove('listening');
    voiceStatus.style.display = 'none';
}

// ========== GOALS MANAGEMENT ==========

function openGoalsPanel() {
    const modal = document.getElementById('goalsModal');
    if (modal) {
        modal.classList.add('active');
        loadGoals();
    }
}

function closeGoalsPanel() {
    const modal = document.getElementById('goalsModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

function createGoal() {
    const name = document.getElementById('goalName').value.trim();
    const target = document.getElementById('goalTarget').value.trim();
    const deadline = document.getElementById('goalDeadline').value;
    
    if (!name || !target) {
        showNotification('Invalid Input', 'Please fill in goal name and target', 'warning');
        return;
    }
    
    fetch('/goals/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            target: parseInt(target),
            deadline: deadline || null
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showNotification('Goal Created', `"${name}" created! 🎯`, 'success');
            document.getElementById('goalName').value = '';
            document.getElementById('goalTarget').value = '';
            document.getElementById('goalDeadline').value = '';
            loadGoals();
        } else {
            showNotification('Error', data.message || 'Failed to create goal', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error', 'Failed to create goal', 'error');
    });
}

function loadGoals() {
    fetch('/goals/list', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        displayGoals(data.goals || []);
        displayGoalsSummary(data.summary || null);
    })
    .catch(error => {
        console.error('Error loading goals:', error);
    });
}

function displayGoals(goals) {
    const goalsList = document.getElementById('goalsList');
    
    if (!goals || goals.length === 0) {
        goalsList.innerHTML = '<p class="empty-state">No goals yet. Create one to get started! 🎯</p>';
        return;
    }
    
    goalsList.innerHTML = goals.map(goal => {
        const progress = (goal.progress / goal.target) * 100;
        return `
            <div class="goal-item">
                <div class="goal-info">
                    <div class="goal-title">${escapeHtml(goal.name)}</div>
                    <div class="goal-progress-bar">
                        <div class="goal-progress-fill" style="width: ${progress}%"></div>
                    </div>
                    <div class="goal-text">${goal.progress}/${goal.target} • ${goal.status}</div>
                </div>
                <div class="goal-actions">
                    <button class="goal-btn goal-update-btn" onclick="updateGoalProgress(${goal.id})">+1</button>
                    <button class="goal-btn goal-delete-btn" onclick="deleteGoal(${goal.id})">🗑️</button>
                </div>
            </div>
        `;
    }).join('');
}

function displayGoalsSummary(summary) {
    const summaryDiv = document.getElementById('goalsSummary');
    
    if (!summary) {
        summaryDiv.innerHTML = '<p>No data available</p>';
        return;
    }
    
    summaryDiv.innerHTML = `
        <div class="summary-card">
            <div class="number">${summary.total || 0}</div>
            <div class="label">Total Goals</div>
        </div>
        <div class="summary-card">
            <div class="number">${summary.completed || 0}</div>
            <div class="label">Completed</div>
        </div>
        <div class="summary-card">
            <div class="number">${summary.in_progress || 0}</div>
            <div class="label">In Progress</div>
        </div>
    `;
}

function updateGoalProgress(goalId) {
    fetch(`/goals/update/${goalId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showNotification('Progress Updated', data.message, 'success');
            loadGoals();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error', 'Failed to update goal', 'error');
    });
}

function deleteGoal(goalId) {
    if (confirm('Delete this goal?')) {
        fetch(`/goals/delete/${goalId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showNotification('Goal Deleted', 'Goal removed', 'success');
                loadGoals();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error', 'Failed to delete goal', 'error');
        });
    }
}

// ========== THEME TOGGLE ==========

function toggleTheme() {
    const body = document.body;
    const isDarkMode = body.classList.toggle('dark-mode');
    
    // Update button text and icon
    const themeIcon = document.getElementById('themeIcon');
    const themeBtn = document.getElementById('themeToggleBtn');
    
    if (isDarkMode) {
        themeIcon.textContent = '☀️';
        themeBtn.querySelector('span:last-child').textContent = 'Light';
        localStorage.setItem('theme', 'dark');
    } else {
        themeIcon.textContent = '🌙';
        themeBtn.querySelector('span:last-child').textContent = 'Dark';
        localStorage.setItem('theme', 'light');
    }
}

// Load theme preference on page load
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        const themeIcon = document.getElementById('themeIcon');
        const themeBtn = document.getElementById('themeToggleBtn');
        if (themeIcon) themeIcon.textContent = '☀️';
        if (themeBtn) themeBtn.querySelector('span:last-child').textContent = 'Light';
    }
});

// ========== KEYBOARD SHORTCUTS ==========

document.addEventListener('keydown', function(event) {
    // Only trigger shortcuts when not typing in input field (except for search)
    const isInput = document.activeElement.tagName === 'INPUT' && document.activeElement.id !== 'searchInput';
    const isTextarea = document.activeElement.tagName === 'TEXTAREA';
    
    // Ctrl+T: Quick Task
    if (event.ctrlKey && event.key === 't' && !isInput && !isTextarea) {
        event.preventDefault();
        document.getElementById('messageInput').focus();
        document.getElementById('messageInput').placeholder = '📝 Type a quick task...';
    }
    
    // Ctrl+N: New Note
    if (event.ctrlKey && event.key === 'n' && !isInput && !isTextarea) {
        event.preventDefault();
        openNotesModal();
    }
    
    // Ctrl+S: Search (already handled by input, but allow focus)
    if (event.ctrlKey && event.key === 's' && !isInput && !isTextarea) {
        event.preventDefault();
        document.getElementById('searchInput').focus();
    }
    
    // Ctrl+K: Goals
    if (event.ctrlKey && event.key === 'k' && !isInput && !isTextarea) {
        event.preventDefault();
        openGoalsPanel();
    }
    
    // Ctrl+M: Toggle Theme
    if (event.ctrlKey && event.key === 'm' && !isInput && !isTextarea) {
        event.preventDefault();
        toggleTheme();
    }
    
    // Escape: Close modals
    if (event.key === 'Escape') {
        closeAllModals();
    }
});

// ========== NOTES MODAL FUNCTIONS ==========

function openNotesModal() {
    const modal = document.getElementById('notesModal');
    if (modal) {
        modal.classList.add('active');
        document.getElementById('noteTitle').focus();
    }
}

function closeNotesModal() {
    const modal = document.getElementById('notesModal');
    if (modal) {
        modal.classList.remove('active');
        // Clear form
        document.getElementById('noteTitle').value = '';
        document.getElementById('noteContent').value = '';
        document.getElementById('attachedFiles').innerHTML = '';
        attachedFilesList = [];
    }
}

let attachedFilesList = [];

function handleFileDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    
    const dragDropZone = document.getElementById('dragDropZone');
    dragDropZone.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    handleFiles(files);
}

function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    const dragDropZone = document.getElementById('dragDropZone');
    dragDropZone.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    const dragDropZone = document.getElementById('dragDropZone');
    dragDropZone.classList.remove('dragover');
}

function handleFileSelect(event) {
    const files = event.target.files;
    handleFiles(files);
}

function handleFiles(files) {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const maxSize = 5 * 1024 * 1024; // 5MB
    
    for (let file of files) {
        // Validate file type
        if (!allowedTypes.includes(file.type)) {
            showNotification('Invalid File', `${file.name} is not supported`, 'warning');
            continue;
        }
        
        // Validate file size
        if (file.size > maxSize) {
            showNotification('File Too Large', `${file.name} is larger than 5MB`, 'warning');
            continue;
        }
        
        // Add to list
        attachedFilesList.push({
            name: file.name,
            type: file.type,
            size: file.size
        });
    }
    
    displayAttachedFiles();
}

function displayAttachedFiles() {
    const container = document.getElementById('attachedFiles');
    container.innerHTML = '';
    
    attachedFilesList.forEach((file, index) => {
        const fileTag = document.createElement('div');
        fileTag.className = 'file-tag';
        
        const icon = file.type.startsWith('image/') ? '🖼️' : '📄';
        
        fileTag.innerHTML = `
            ${icon} ${file.name}
            <button type="button" class="file-tag-remove" onclick="removeAttachedFile(${index})">×</button>
        `;
        
        container.appendChild(fileTag);
    });
}

function removeAttachedFile(index) {
    attachedFilesList.splice(index, 1);
    displayAttachedFiles();
}

function saveNote() {
    const title = document.getElementById('noteTitle').value.trim();
    const content = document.getElementById('noteContent').value.trim();
    
    if (!title || !content) {
        showNotification('Empty Note', 'Please add a title and content', 'warning');
        return;
    }
    
    // For now, just add as a message
    addMessage(`📝 Note: ${title}\n\n${content}`, 'user');
    
    showNotification('Note Saved', `"${title}" has been saved`, 'success');
    closeNotesModal();
}

// ========== SEARCH FUNCTIONALITY ==========

function performSearch(query) {
    const searchResults = document.getElementById('searchResults');
    
    if (query.length < 2) {
        searchResults.style.display = 'none';
        return;
    }
    
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        displaySearchResults(data.results || []);
    })
    .catch(error => {
        console.error('Search error:', error);
        searchResults.innerHTML = '<div class="search-result-item">Search error</div>';
    });
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('searchResults');
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="search-result-item">No results found</div>';
        searchResults.style.display = 'block';
        return;
    }
    
    searchResults.innerHTML = results.map(result => `
        <div class="search-result-item" onclick="selectSearchResult('${result.type}', '${result.id}')">
            <div class="search-result-type">${result.type}</div>
            <div class="search-result-text">${result.text}</div>
        </div>
    `).join('');
    
    searchResults.style.display = 'block';
}

function selectSearchResult(type, id) {
    const searchInput = document.getElementById('searchInput');
    searchInput.value = '';
    document.getElementById('searchResults').style.display = 'none';
    
    // Show selected result
    showNotification('Search Result', `Selected ${type}: ${id}`, 'info');
}

// Close modals when clicking outside
document.addEventListener('click', function(event) {
    const helpModal = document.getElementById('helpModal');
    const eventModal = document.getElementById('eventModal');
    const goalsModal = document.getElementById('goalsModal');
    const notesModal = document.getElementById('notesModal');
    
    if (event.target === helpModal) helpModal.classList.remove('active');
    if (event.target === eventModal) eventModal.classList.remove('active');
    if (event.target === goalsModal) goalsModal.classList.remove('active');
    if (event.target === notesModal) notesModal.classList.remove('active');
});

function closeAllModals() {
    document.getElementById('helpModal').classList.remove('active');
    document.getElementById('eventModal').classList.remove('active');
    document.getElementById('goalsModal').classList.remove('active');
    document.getElementById('notesModal').classList.remove('active');
}

// ========== NOTIFICATIONS SYSTEM ==========

function showNotification(title, message, type = 'info', duration = 4000) {
    const container = document.getElementById('notificationsContainer');
    if (!container) return;
    
    const notificationId = 'notif-' + Date.now();
    const notification = document.createElement('div');
    notification.id = notificationId;
    notification.className = `notification ${type}`;
    
    const icons = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️'
    };
    
    notification.innerHTML = `
        <div class="notification-icon">${icons[type] || 'ℹ️'}</div>
        <div class="notification-content">
            <div class="notification-title">${escapeHtml(title)}</div>
            <div class="notification-message">${escapeHtml(message)}</div>
        </div>
        <button class="notification-close" onclick="closeNotification('${notificationId}')">✕</button>
    `;
    
    container.appendChild(notification);
    
    // Auto-remove after duration
    setTimeout(() => {
        closeNotification(notificationId);
    }, duration);
}

function closeNotification(notificationId) {
    const notification = document.getElementById(notificationId);
    if (notification) {
        notification.style.animation = 'slideOutRight 0.3s ease forwards';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }
}

// Add slide out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
`;
document.head.appendChild(style);
