# Hotel Booking Chatbot - Web UI 🌐

This is the **frontend application** for the Hotel Booking Chatbot. It provides a modern, responsive web interface that communicates with the Rasa chatbot backend.

## 📋 Overview

This web UI is completely **separate** from the Rasa chatbot backend, allowing you to:
- Deploy the frontend and backend independently
- Scale them separately
- Use different hosting services for each
- Maintain clean separation of concerns

## 🛠️ Technology Stack

- **Framework**: Flask 3.0.0
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API Communication**: REST API (communicates with Rasa backend)

## 📁 Project Structure

```
web_ui/
├── app.py                  # Flask application server
├── templates/
│   └── index.html         # Chat interface HTML
├── static/
│   ├── style.css          # Styling
│   └── script.js          # Client-side logic
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd web_ui
pip install -r requirements.txt
```

Or if using a virtual environment:

```bash
cd web_ui
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the Web UI

```bash
python app.py
```

The server will start on: **http://localhost:5001**

### 3. Access the Interface

Open your browser and navigate to:
```
http://localhost:5001
```

## ⚙️ Configuration

### Rasa Backend URL

By default, the UI connects to Rasa at `http://localhost:5005`. You can change this using an environment variable:

```bash
export RASA_API_URL="http://your-rasa-server:5005/webhooks/rest/webhook"
python app.py
```

## 🔗 Backend Requirements

For the web UI to work, you need the **Rasa chatbot backend** running:

### Option 1: Run locally (recommended for development)

In a separate terminal:

```bash
# Terminal 1: Start Rasa server
cd ../  # Go back to chatbot root
rasa run --enable-api --cors "*"

# Terminal 2: Start Actions server
cd ../  # Go back to chatbot root
rasa run actions
```

### Option 2: Connect to remote Rasa server

Set the environment variable to point to your remote Rasa server:

```bash
export RASA_API_URL="https://your-rasa-server.com/webhooks/rest/webhook"
python app.py
```

## 📡 API Endpoints

### Frontend Endpoints

- `GET /` - Serves the chat interface
- `POST /chat` - Handles chat messages and forwards to Rasa
- `GET /health` - Health check endpoint

### Request/Response Format

**POST /chat**

Request:
```json
{
  "message": "Hi",
  "session_id": "optional-session-id"
}
```

Response:
```json
{
  "session_id": "generated-or-provided-session-id",
  "responses": ["Hello! I can help you book a hotel room. What's your name?"]
}
```

## 🎨 Features

- ✨ Modern, responsive design
- 💬 Real-time chat interface
- 📱 Mobile-friendly
- ⌨️ Keyboard shortcuts (Enter to send)
- 💭 Typing indicators
- ⏱️ Message timestamps
- 🧹 Clear conversation button
- 🎨 Beautiful gradient theme
- 🔄 Session management

## 🐛 Troubleshooting

### "Cannot connect to chatbot server"

**Problem**: The UI can't reach the Rasa backend.

**Solution**:
1. Make sure Rasa is running: `rasa run --enable-api --cors "*"`
2. Check the port (default: 5005)
3. Verify the URL in environment variable or app.py

### Port 5001 already in use

**Solution**: Change the port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Use different port
```

### CORS errors in browser console

**Solution**: Make sure Rasa is started with CORS enabled:

```bash
rasa run --enable-api --cors "*"
```

## 🚢 Deployment

### Deploy Frontend Only

The frontend can be deployed to any platform that supports Python/Flask:

- **Heroku**: `git push heroku main`
- **Railway**: Connect your GitHub repo
- **DigitalOcean**: Use App Platform
- **Vercel**: Deploy with Python runtime
- **AWS**: Use Elastic Beanstalk or EC2

Just make sure to:
1. Set `RASA_API_URL` environment variable to your Rasa backend
2. Update `CORS` settings on your Rasa server

### Production Considerations

For production, use a production-grade WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

Or with environment variable:

```bash
RASA_API_URL="https://your-backend.com/webhooks/rest/webhook" gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

## 📚 Related Documentation

- [Rasa Chatbot Backend](../README.md) - Main chatbot documentation
- [Rasa HTTP API](https://rasa.com/docs/rasa/pages/http-api) - Rasa API reference

## 🤝 Contributing

This is a standalone frontend application. To modify:

1. **UI Design**: Edit `templates/index.html` and `static/style.css`
2. **Client Logic**: Edit `static/script.js`
3. **Server Logic**: Edit `app.py`

## 📄 License

This project is for educational purposes (IU Course: Project AI Use Case).

---

**Happy Chatting! 🎉**

