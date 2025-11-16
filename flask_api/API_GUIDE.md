# 🎯 Quick Start Guide: Using the API

## What is this?

This is a REST API that lets you connect your hotel booking chatbot to **any frontend** - React, Vue, Angular, plain HTML, mobile apps, or even other backend services!

---

## ⚡ 3-Step Quick Start

### Step 1: Start Everything

```bash
# Terminal 1: Start Rasa (if not already running)
./run.sh

# Terminal 2: Start the API
./start_api.sh
```

### Step 2: Test the API

```bash
# In Terminal 3
./test_api.sh
```

### Step 3: See It in Action

Open `frontend_example.html` in your browser and start chatting!

---

## 🎨 What You Get

### 1. **Beautiful Frontend Example** (`frontend_example.html`)

A complete, production-ready chat interface with:
- Modern gradient design
- Typing indicators
- Real-time messaging
- Session management
- Error handling
- Mobile responsive

**Just open it in your browser!** No build tools needed.

### 2. **REST API** (`api.py`)

7 powerful endpoints:
- Send messages
- Manage sessions
- Get bookings
- Health checks
- Reset conversations

### 3. **Complete Documentation** 

- `API_README.md` - Full technical docs
- `API_GUIDE.md` - This quick start guide

---

## 💡 Common Use Cases

### Use Case 1: Add to Your Website

```html
<iframe src="frontend_example.html" width="400" height="700"></iframe>
```

Or integrate the JavaScript code directly into your site!

### Use Case 2: React/Vue/Angular App

```javascript
import axios from 'axios';

const chatWithBot = async (message, sessionId) => {
  const response = await axios.post('http://localhost:5000/chat', {
    message,
    sender: sessionId
  });
  return response.data.responses;
};
```

### Use Case 3: Mobile App

Use the API with any HTTP client:
- React Native: `fetch` or `axios`
- Flutter: `http` package
- Swift: `URLSession`
- Kotlin: `Retrofit` or `OkHttp`

### Use Case 4: Connect Multiple Frontends

The API supports multiple concurrent users, so you can have:
- Web app
- Mobile app
- Desktop app
- WhatsApp/Telegram bot

All using the same chatbot backend!

---

## 🧪 Testing Your Integration

### Test with curl

```bash
# 1. Create a session
curl -X POST http://localhost:5000/session/new

# Copy the sender ID from response, then:

# 2. Send a message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hi", "sender": "YOUR_SENDER_ID"}'

# 3. Continue the conversation
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "John Doe", "sender": "YOUR_SENDER_ID"}'
```

### Test with JavaScript Console

Open `frontend_example.html` and try in browser console:

```javascript
// Send a test message
fetch('http://localhost:5000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "I want to book a room",
    sender: "test123"
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 🔧 Customization

### Change API Port

In `api.py`, change the last line:

```python
app.run(host='0.0.0.0', port=5000, debug=True)
# Change 5000 to your desired port
```

### Customize Frontend

Edit `frontend_example.html`:

```javascript
// Change colors
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);

// Change API URL (for production)
const API_URL = 'https://your-production-domain.com';
```

### Add Authentication

In `api.py`:

```python
@app.route('/chat', methods=['POST'])
def chat():
    # Add this at the start
    api_key = request.headers.get('X-API-Key')
    if api_key != 'your-secret-key':
        return jsonify({"error": "Unauthorized"}), 401
    
    # Rest of the code...
```

---

## 📱 Example Integrations

### React Component

```jsx
import React, { useState, useEffect } from 'react';

function ChatBot() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // Create session on mount
    fetch('http://localhost:5000/session/new', { method: 'POST' })
      .then(r => r.json())
      .then(data => setSessionId(data.sender));
  }, []);

  const sendMessage = async (text) => {
    const response = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, sender: sessionId })
    });
    const data = await response.json();
    setMessages([...messages, ...data.responses]);
  };

  return (
    <div>
      {messages.map(msg => <div>{msg.text}</div>)}
      <input onKeyPress={e => e.key === 'Enter' && sendMessage(e.target.value)} />
    </div>
  );
}
```

### Vue Component

```vue
<template>
  <div class="chat">
    <div v-for="msg in messages" :key="msg.id">{{ msg.text }}</div>
    <input v-model="input" @keyup.enter="sendMessage" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      sessionId: null,
      messages: [],
      input: ''
    }
  },
  async mounted() {
    const res = await fetch('http://localhost:5000/session/new', { method: 'POST' });
    const data = await res.json();
    this.sessionId = data.sender;
  },
  methods: {
    async sendMessage() {
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: this.input, 
          sender: this.sessionId 
        })
      });
      const data = await response.json();
      this.messages.push(...data.responses);
      this.input = '';
    }
  }
}
</script>
```

### Python Client

```python
import requests

class ChatBotClient:
    def __init__(self, api_url="http://localhost:5000"):
        self.api_url = api_url
        self.session_id = self.create_session()
    
    def create_session(self):
        response = requests.post(f"{self.api_url}/session/new")
        return response.json()["sender"]
    
    def send_message(self, message):
        response = requests.post(f"{self.api_url}/chat", json={
            "message": message,
            "sender": self.session_id
        })
        return response.json()["responses"]
    
    def reset(self):
        requests.post(f"{self.api_url}/session/reset", json={
            "sender": self.session_id
        })

# Usage
bot = ChatBotClient()
responses = bot.send_message("I want to book a room")
for resp in responses:
    print(resp["text"])
```

---

## 🚀 Deployment Tips

### Deploy to Production

1. **Use a production server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 api:app
   ```

2. **Set up HTTPS:**
   Use nginx or Apache as reverse proxy with SSL certificate

3. **Add environment variables:**
   ```bash
   export RASA_API_URL=https://your-rasa-server.com
   export SECRET_KEY=your-secret-key
   ```

4. **Enable CORS for your domain only:**
   ```python
   CORS(app, origins=['https://yourdomain.com'])
   ```

5. **Add rate limiting:**
   ```bash
   pip install flask-limiter
   ```

### Deploy Rasa Separately

You can deploy Rasa on a different server and point the API to it:

```python
# In api.py
RASA_API_URL = "https://your-rasa-server.com"
```

---

## 🐛 Troubleshooting

### "Cannot connect to chatbot server"

**Solution:** Make sure Rasa is running on port 5005
```bash
curl http://localhost:5005/status
```

### "CORS error in browser"

**Solution:** Ensure Flask-CORS is installed
```bash
pip install flask-cors
```

### "Port 5000 already in use"

**Solution:** Kill the process or change the port
```bash
lsof -i :5000
kill -9 <PID>
```

### Messages not getting responses

**Solution:** Check action server is running
```bash
ps aux | grep "rasa run actions"
```

---

## ✅ Checklist for Production

- [ ] Add authentication (API keys or OAuth)
- [ ] Enable HTTPS only
- [ ] Add rate limiting
- [ ] Set up monitoring/logging
- [ ] Use production WSGI server (gunicorn)
- [ ] Restrict CORS to your domains
- [ ] Add input validation
- [ ] Set up error tracking (Sentry)
- [ ] Load test the API
- [ ] Back up bookings to database
- [ ] Add health check monitoring
- [ ] Set up CI/CD pipeline

---

## 📞 Need Help?

1. Check the full documentation: `API_README.md`
2. Test with the test script: `./test_api.sh`
3. Review the example frontend: `frontend_example.html`
4. Check logs: `tail -f action_server.log`

---

## 🎉 What's Next?

Now that you have the API running, you can:

1. **Customize the frontend** to match your brand
2. **Integrate with your existing website**
3. **Build a mobile app** using the API
4. **Connect to messaging platforms** (WhatsApp, Telegram, Slack)
5. **Add analytics** to track conversations
6. **Store bookings in a database** (PostgreSQL, MongoDB)
7. **Add payment processing** integration
8. **Build an admin dashboard** to manage bookings

The API is your gateway to unlimited possibilities! 🚀

---

**Happy Coding! 🎊**

