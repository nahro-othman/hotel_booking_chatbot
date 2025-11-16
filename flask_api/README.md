# 🌐 Flask API + Frontend

This folder contains the **Flask REST API** and the **web frontend** for the hotel booking chatbot.

## 📁 Folder Structure

```
flask_api/
├── api.py                 # Flask REST API server
├── run_api.sh             # Script to start the API + Frontend
├── static/
│   └── index.html         # Web chat interface (frontend)
├── templates/             # Flask templates (if needed)
├── API_README.md          # Full API documentation
├── API_GUIDE.md           # Quick start guide
├── API_SUMMARY.md         # API overview
└── README.md              # This file
```

---

## 🚀 Quick Start

### 1. Start the Rasa Server (Required First!)

In the **root directory** of the project:

```bash
cd ..
./run.sh
```

Leave this terminal running.

### 2. Start the Flask API + Frontend

In a **new terminal**, from the `flask_api` folder:

```bash
./run_api.sh
```

Or manually:

```bash
cd flask_api
source ../.venv/bin/activate
python api.py
```

### 3. Open the Frontend in Your Browser

Once the server is running, open:

🌐 **http://localhost:5000**

That's it! You can now chat with the bot through the web interface!

---

## 🎨 The Frontend

The frontend is a **beautiful, modern chat interface** that's ready to use!

**Features:**
- 🎨 Modern gradient design
- 💬 Real-time messaging
- ⌨️ Typing indicators
- 📱 Mobile responsive
- 🔄 Reset conversation button
- ⚡ Instant message delivery
- 🎯 Connection status indicator

**Location:** `flask_api/static/index.html`

**URL:** http://localhost:5000

---

## 📡 API Endpoints

The Flask API provides these endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve the web chat interface |
| `/health` | GET | Check API and Rasa status |
| `/chat` | POST | Send messages to the bot |
| `/session/new` | POST | Create new conversation |
| `/session/reset` | POST | Reset conversation |
| `/session/active` | GET | List active sessions |
| `/bookings` | GET | Get all bookings |
| `/docs` | GET | API documentation |

---

## 🔧 How It Works

```
Browser (http://localhost:5000)
    ↓
Flask API (Port 5000)
    ├── Serves frontend (index.html)
    └── Handles API requests
        ↓
    Rasa Server (Port 5005)
        ↓
    Action Server (Port 5055)
        ↓
    bookings.txt
```

---

## 💻 Using the Frontend

### For End Users:

1. Open http://localhost:5000 in your browser
2. Type "hi" to start
3. Follow the bot's questions
4. Complete your booking!

### For Developers:

The frontend (`static/index.html`) is a **single HTML file** with embedded CSS and JavaScript. You can:

1. **Customize the design:**
   - Change colors in the `<style>` section
   - Modify the gradient colors
   - Adjust fonts and spacing

2. **Integrate into your website:**
   - Copy the HTML file
   - Or use it as an iframe: `<iframe src="http://localhost:5000" width="500" height="700"></iframe>`

3. **Use the JavaScript code:**
   - Extract the JavaScript functions
   - Integrate into React, Vue, or Angular
   - Customize the API calls

---

## 🔌 API Integration Examples

### JavaScript (from frontend)

```javascript
// Send a message
async function sendMessage(message, sessionId) {
  const response = await fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: message,
      sender: sessionId
    })
  });
  return await response.json();
}
```

### Python

```python
import requests

# Create session
session = requests.post('http://localhost:5000/session/new')
sender_id = session.json()['sender']

# Send message
response = requests.post('http://localhost:5000/chat', json={
    'message': 'I want to book a room',
    'sender': sender_id
})

print(response.json()['responses'])
```

### curl

```bash
# Create session
SESSION=$(curl -s -X POST http://localhost:5000/session/new | grep -o '"sender":"[^"]*"' | cut -d'"' -f4)

# Send message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"hi\", \"sender\": \"$SESSION\"}"
```

---

## 📚 Documentation

- **API_README.md** - Complete technical documentation (30+ pages)
- **API_GUIDE.md** - Quick start and integration guide
- **API_SUMMARY.md** - Overview of all features

---

## 🎨 Customizing the Frontend

### Change Colors

Edit `static/index.html`, find the gradient:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Replace with your colors:

```css
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
```

### Change API URL (for production)

Find this line in `static/index.html`:

```javascript
const API_URL = 'http://localhost:5000';
```

Change to your production URL:

```javascript
const API_URL = 'https://your-domain.com';
```

### Add Your Logo

Add an `<img>` tag in the chat header:

```html
<div class="chat-header">
    <img src="/static/logo.png" alt="Logo" style="height: 40px;">
    <h1>🏨 Hotel Booking Assistant</h1>
</div>
```

---

## 🐛 Troubleshooting

### "Cannot connect to chatbot server"

**Problem:** Rasa is not running

**Solution:**
```bash
cd ..
./run.sh
```

### "Port 5000 already in use"

**Problem:** Another process is using port 5000

**Solution:**
```bash
# Find the process
lsof -i :5000

# Kill it
kill -9 <PID>

# Or change the port in api.py
```

### Frontend shows blank page

**Problem:** index.html not found

**Solution:** Make sure `index.html` is in the `static` folder:
```bash
ls flask_api/static/index.html
```

### API calls failing with CORS error

**Problem:** CORS not configured

**Solution:** Flask-CORS is already configured, but make sure it's installed:
```bash
pip install flask-cors
```

---

## 🚀 Deployment

### For Production:

1. **Use gunicorn instead of Flask dev server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 api:app
   ```

2. **Set up nginx as reverse proxy**

3. **Enable HTTPS** with SSL certificate

4. **Add authentication** (API keys)

5. **Restrict CORS** to your domain:
   ```python
   CORS(app, origins=['https://yourdomain.com'])
   ```

See **API_README.md** for complete production deployment guide!

---

## ✅ Testing

### Test the API:

```bash
cd ..
./test_api.sh
```

### Test the Frontend:

1. Open http://localhost:5000
2. Type "hi"
3. Complete a booking flow
4. Check if booking is saved in `../bookings.txt`

---

## 📞 Need Help?

1. **API not starting?**
   - Check if Flask is installed: `pip show flask`
   - Make sure you're in the flask_api directory

2. **Frontend not loading?**
   - Verify the file exists: `ls static/index.html`
   - Check browser console for errors

3. **Bot not responding?**
   - Make sure Rasa is running: `curl http://localhost:5005/status`
   - Check action server: `ps aux | grep "rasa run actions"`

4. **Read the docs:**
   - API_README.md - Full technical docs
   - API_GUIDE.md - Quick start guide
   - API_SUMMARY.md - Feature overview

---

## 🎉 What You Can Do

Now that you have the Flask API + Frontend:

1. ✅ **Use the web interface** - Just open http://localhost:5000
2. ✅ **Integrate with your website** - Copy/customize the HTML
3. ✅ **Build mobile apps** - Use the REST API
4. ✅ **Connect multiple frontends** - React, Vue, Angular, etc.
5. ✅ **Deploy to production** - Follow the deployment guide
6. ✅ **Customize the design** - Match your brand

---

**Happy Coding! 🚀**

