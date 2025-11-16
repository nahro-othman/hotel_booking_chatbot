# 🚀 Hotel Booking Chatbot API Documentation

A complete REST API for integrating the Rasa-powered hotel booking chatbot with any frontend application.

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Integration Examples](#integration-examples)
- [Frontend Example](#frontend-example)
- [Error Handling](#error-handling)
- [Security Considerations](#security-considerations)

---

## 🎯 Overview

This Flask API provides RESTful endpoints to interact with the hotel booking chatbot. It handles:

- **Message routing** between frontend and Rasa
- **Session management** for multiple concurrent users
- **CORS support** for cross-origin requests
- **Booking retrieval** from the database
- **Health monitoring** of the chatbot service

### Tech Stack

- **Flask 2.3.2** - Web framework
- **Flask-CORS 4.0.0** - Cross-origin support
- **Requests 2.31.0** - HTTP client for Rasa communication
- **Rasa 3.6.20** - Chatbot backend

---

## ⚡ Quick Start

### 1. Install Dependencies

```bash
pip install flask flask-cors requests
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Start the Rasa Server

First, make sure Rasa is running:

```bash
./run.sh
```

### 3. Start the API Server

```bash
./start_api.sh
```

Or manually:

```bash
python api.py
```

The API will be available at: **http://localhost:5000**

### 4. Test the API

```bash
./test_api.sh
```

Or use curl:

```bash
curl http://localhost:5000/health
```

---

## 📡 API Endpoints

### 1. **Health Check**

Check if the API and Rasa server are running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-11-16T13:45:00",
  "rasa_status": "running"
}
```

**Example:**
```bash
curl http://localhost:5000/health
```

---

### 2. **Send Message to Chatbot**

Send a user message and receive bot responses.

**Endpoint:** `POST /chat`

**Request Body:**
```json
{
  "message": "I want to book a room",
  "sender": "user123"
}
```

**Parameters:**
- `message` (required) - The user's message
- `sender` (optional) - Session ID. If not provided, a new session is created

**Response:**
```json
{
  "sender": "user123",
  "responses": [
    {
      "text": "Hello! I can help you book a hotel room. What's your name?"
    }
  ],
  "timestamp": "2024-11-16T13:45:00"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hi", "sender": "test-user-123"}'
```

---

### 3. **Create New Session**

Create a new conversation session for a user.

**Endpoint:** `POST /session/new`

**Response:**
```json
{
  "sender": "abc123-def456-ghi789",
  "message": "New session created successfully"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/session/new
```

---

### 4. **Reset Session**

Reset an existing conversation and start fresh.

**Endpoint:** `POST /session/reset`

**Request Body:**
```json
{
  "sender": "user123"
}
```

**Response:**
```json
{
  "sender": "user123",
  "message": "Session reset successfully"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/session/reset \
  -H "Content-Type: application/json" \
  -d '{"sender": "user123"}'
```

---

### 5. **Get Active Sessions**

Retrieve list of all active conversation sessions.

**Endpoint:** `GET /session/active`

**Response:**
```json
{
  "active_sessions": 3,
  "sessions": {
    "user123": {
      "last_message": "hi",
      "timestamp": "2024-11-16T13:45:00"
    }
  }
}
```

**Example:**
```bash
curl http://localhost:5000/session/active
```

---

### 6. **Get All Bookings**

Retrieve all confirmed bookings from the system.

**Endpoint:** `GET /bookings`

**Response:**
```json
{
  "bookings": [
    "BOOKING CONFIRMATION - 2024-11-16 13:40:26\n..."
  ],
  "total": 5
}
```

**Example:**
```bash
curl http://localhost:5000/bookings
```

---

### 7. **API Documentation**

Get complete API documentation in JSON format.

**Endpoint:** `GET /docs`

**Example:**
```bash
curl http://localhost:5000/docs
```

---

## 💻 Integration Examples

### JavaScript (Fetch API)

```javascript
// Initialize session
async function initChat() {
  const response = await fetch('http://localhost:5000/session/new', {
    method: 'POST'
  });
  const data = await response.json();
  return data.sender; // Session ID
}

// Send message
async function sendMessage(sessionId, message) {
  const response = await fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: message,
      sender: sessionId
    })
  });
  
  const data = await response.json();
  return data.responses;
}

// Usage
const sessionId = await initChat();
const responses = await sendMessage(sessionId, "I want to book a room");
console.log(responses);
```

### Python (requests)

```python
import requests

API_URL = "http://localhost:5000"

# Create session
response = requests.post(f"{API_URL}/session/new")
session_id = response.json()["sender"]

# Send message
response = requests.post(f"{API_URL}/chat", json={
    "message": "I want to book a room",
    "sender": session_id
})

bot_responses = response.json()["responses"]
for resp in bot_responses:
    print(resp["text"])
```

### React Example

```jsx
import { useState, useEffect } from 'react';

function ChatBot() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  useEffect(() => {
    // Initialize session
    fetch('http://localhost:5000/session/new', { method: 'POST' })
      .then(res => res.json())
      .then(data => setSessionId(data.sender));
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    setMessages([...messages, { text: input, sender: 'user' }]);

    // Send to API
    const response = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: input,
        sender: sessionId
      })
    });

    const data = await response.json();
    
    // Add bot responses
    const botMessages = data.responses.map(r => ({
      text: r.text,
      sender: 'bot'
    }));
    
    setMessages([...messages, { text: input, sender: 'user' }, ...botMessages]);
    setInput('');
  };

  return (
    <div>
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={msg.sender}>
            {msg.text}
          </div>
        ))}
      </div>
      <input 
        value={input} 
        onChange={e => setInput(e.target.value)}
        onKeyPress={e => e.key === 'Enter' && sendMessage()}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
```

---

## 🌐 Frontend Example

A complete HTML/CSS/JavaScript frontend example is provided in `frontend_example.html`.

**To use it:**

1. Start the Rasa server: `./run.sh`
2. Start the API server: `./start_api.sh`
3. Open `frontend_example.html` in your browser

**Features:**
- Modern, responsive UI
- Real-time messaging
- Typing indicators
- Session management
- Error handling
- Reset conversation

---

## ⚠️ Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "error": "Missing 'message' in request body"
}
```

#### 503 Service Unavailable
```json
{
  "error": "Cannot connect to chatbot server. Please ensure Rasa is running."
}
```

#### 504 Gateway Timeout
```json
{
  "error": "Request timeout - chatbot is taking too long to respond"
}
```

### Error Handling in Code

```javascript
try {
  const response = await fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: "hi", sender: sessionId })
  });

  if (!response.ok) {
    const error = await response.json();
    console.error('API Error:', error.error);
    return;
  }

  const data = await response.json();
  // Process responses...

} catch (error) {
  console.error('Network Error:', error);
}
```

---

## 🔒 Security Considerations

### For Development

The current setup is configured for development with:
- `debug=True` in Flask
- Open CORS policy
- No authentication
- Running on `0.0.0.0`

### For Production

Before deploying to production, implement:

1. **Authentication & Authorization**
   ```python
   from flask import request
   
   def require_api_key():
       api_key = request.headers.get('X-API-Key')
       if api_key != 'your-secret-key':
           return jsonify({"error": "Unauthorized"}), 401
   ```

2. **Rate Limiting**
   ```python
   from flask_limiter import Limiter
   
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   
   @app.route('/chat', methods=['POST'])
   @limiter.limit("10 per minute")
   def chat():
       # ...
   ```

3. **HTTPS Only**
   - Use SSL certificates
   - Redirect HTTP to HTTPS

4. **CORS Restrictions**
   ```python
   CORS(app, origins=['https://yourdomain.com'])
   ```

5. **Input Validation**
   ```python
   from flask import escape
   
   message = escape(data['message'])
   ```

6. **Environment Variables**
   ```python
   import os
   
   RASA_API_URL = os.getenv('RASA_API_URL', 'http://localhost:5005')
   SECRET_KEY = os.getenv('SECRET_KEY')
   ```

7. **Production Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 api:app
   ```

---

## 🧪 Testing

### Manual Testing

Use the provided test script:
```bash
./test_api.sh
```

### Automated Testing

Create a test file `test_api.py`:

```python
import unittest
import requests

class TestAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"
    
    def test_health(self):
        response = requests.get(f"{self.BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
    
    def test_chat(self):
        # Create session
        session = requests.post(f"{self.BASE_URL}/session/new")
        sender_id = session.json()["sender"]
        
        # Send message
        response = requests.post(f"{self.BASE_URL}/chat", json={
            "message": "hi",
            "sender": sender_id
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("responses", response.json())

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python test_api.py
```

---

## 📊 Monitoring & Logging

The API logs all conversations:

```
INFO:__main__:User [abc123]: I want to book a room
INFO:__main__:Bot [abc123]: Great! What's your name?
```

Monitor logs in real-time:
```bash
tail -f action_server.log
```

---

## 🎓 Best Practices

1. **Always handle errors** - Check response status codes
2. **Use session IDs** - Maintain conversation context
3. **Implement timeouts** - Don't wait indefinitely
4. **Cache session IDs** - Store in localStorage or cookies
5. **Show loading states** - Improve user experience
6. **Validate inputs** - Sanitize user messages
7. **Monitor health** - Periodically check `/health` endpoint
8. **Reset when needed** - Provide option to restart conversation

---

## 🆘 Troubleshooting

### API won't start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill process using port 5000
kill -9 <PID>
```

### Cannot connect to Rasa
```bash
# Check if Rasa is running
curl http://localhost:5005/status

# Restart Rasa
./stop.sh && ./run.sh
```

### CORS errors in browser
- Ensure Flask-CORS is installed
- Check browser console for specific error
- Verify API is running on `0.0.0.0`

---

## 📞 Support

For issues or questions:
1. Check the logs in `action_server.log`
2. Review the API documentation at `/docs`
3. Test with `./test_api.sh`

---

## 📄 License

This API is part of the Hotel Booking Chatbot project.

---

**Built with ❤️ for seamless chatbot integration**

