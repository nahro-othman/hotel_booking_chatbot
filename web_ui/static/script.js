// Session management
let sessionId = null;

// Generate unique session ID
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Initialize session
if (!sessionId) {
    sessionId = generateSessionId();
}

// Get current time in HH:MM format
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

// Add message to chat
function addMessage(message, isUser = false) {
    const messagesContainer = document.getElementById('messages');
    
    // Remove welcome message if it exists
    const welcomeMessage = messagesContainer.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    
    const avatarSvg = isUser 
        ? '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z" fill="white"/></svg>'
        : '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 5C13.66 5 15 6.34 15 8C15 9.66 13.66 11 12 11C10.34 11 9 9.66 9 8C9 6.34 10.34 5 12 5ZM12 19.2C9.5 19.2 7.29 17.92 6 15.98C6.03 13.99 10 12.9 12 12.9C13.99 12.9 17.97 13.99 18 15.98C16.71 17.92 14.5 19.2 12 19.2Z" fill="#4F46E5"/></svg>';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            ${avatarSvg}
        </div>
        <div class="message-content">
            <div class="message-bubble">${escapeHtml(message)}</div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Add typing indicator
function addTypingIndicator() {
    const messagesContainer = document.getElementById('messages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot typing';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 5C13.66 5 15 6.34 15 8C15 9.66 13.66 11 12 11C10.34 11 9 9.66 9 8C9 6.34 10.34 5 12 5ZM12 19.2C9.5 19.2 7.29 17.92 6 15.98C6.03 13.99 10 12.9 12 12.9C13.99 12.9 17.97 13.99 18 15.98C16.71 17.92 14.5 19.2 12 19.2Z" fill="#4F46E5"/>
            </svg>
        </div>
        <div class="message-content">
            <div class="message-bubble">
                <div class="typing-indicator">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
            </div>
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Scroll to bottom of messages
function scrollToBottom() {
    const messagesContainer = document.getElementById('messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Send message to backend
async function sendMessage(event) {
    event.preventDefault();
    
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Disable input while processing
    input.disabled = true;
    document.getElementById('send-btn').disabled = true;
    
    // Add user message to chat
    addMessage(message, true);
    input.value = '';
    
    // Show typing indicator
    addTypingIndicator();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (response.ok) {
            // Update session ID if provided
            if (data.session_id) {
                sessionId = data.session_id;
            }
            
            // Add bot responses
            if (data.responses && data.responses.length > 0) {
                data.responses.forEach((botMessage, index) => {
                    setTimeout(() => {
                        addMessage(botMessage, false);
                    }, index * 500); // Stagger responses by 500ms
                });
            } else {
                addMessage("I'm having trouble responding right now. Please try again.", false);
            }
        } else {
            addMessage("Sorry, I encountered an error. Please try again.", false);
        }
    } catch (error) {
        removeTypingIndicator();
        console.error('Error:', error);
        addMessage("Sorry, I couldn't connect to the server. Please make sure the Rasa server is running.", false);
    } finally {
        // Re-enable input
        input.disabled = false;
        document.getElementById('send-btn').disabled = false;
        input.focus();
    }
}

// Send quick message
function sendQuickMessage(message) {
    const input = document.getElementById('user-input');
    input.value = message;
    const form = document.getElementById('chat-form');
    form.dispatchEvent(new Event('submit'));
}

// Clear chat
function clearChat() {
    if (confirm('Are you sure you want to clear the conversation?')) {
        const messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML = `
            <div class="welcome-message">
                <div class="bot-avatar-large">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 5C13.66 5 15 6.34 15 8C15 9.66 13.66 11 12 11C10.34 11 9 9.66 9 8C9 6.34 10.34 5 12 5ZM12 19.2C9.5 19.2 7.29 17.92 6 15.98C6.03 13.99 10 12.9 12 12.9C13.99 12.9 17.97 13.99 18 15.98C16.71 17.92 14.5 19.2 12 19.2Z" fill="#4F46E5"/>
                    </svg>
                </div>
                <h2>Welcome to Hotel Booking! 🏨</h2>
                <p>I'm here to help you book your perfect stay. Let's get started!</p>
                <div class="quick-actions">
                    <button class="quick-btn" onclick="sendQuickMessage('Hi')">👋 Start Booking</button>
                </div>
            </div>
        `;
        // Generate new session
        sessionId = generateSessionId();
    }
}

// Focus input on load
window.addEventListener('load', () => {
    document.getElementById('user-input').focus();
});

