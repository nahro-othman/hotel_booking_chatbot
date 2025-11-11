# 🏗️ Project Architecture

This document explains the separation between the **chatbot backend** and the **web UI frontend**.

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                      (Web Browser)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP Requests
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    WEB UI (Frontend)                        │
│                     Port: 5001                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Flask Server (app.py)                                │ │
│  │  - Serves HTML/CSS/JS                                 │ │
│  │  - Handles user sessions                              │ │
│  │  - Proxies requests to Rasa                           │ │
│  └───────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API Calls
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              CHATBOT BACKEND (Rasa)                         │
│                     Port: 5005                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Rasa Server                                          │ │
│  │  - NLU: Intent & Entity Recognition                   │ │
│  │  - Dialogue Management                                │ │
│  │  - Form Handling (booking_form)                       │ │
│  └────────────────────┬──────────────────────────────────┘ │
│                       │ Calls Custom Actions               │
│                       ▼                                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Action Server (Port: 5055)                           │ │
│  │  - action_show_booking_summary                        │ │
│  │  - action_confirm_booking                             │ │
│  │  - Saves bookings to bookings.txt                     │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Directory Structure

```
hotel_booking_chatbot/
│
├── 🎨 web_ui/                    # FRONTEND (Separate Application)
│   ├── app.py                    # Flask server
│   ├── templates/
│   │   └── index.html           # Chat interface
│   ├── static/
│   │   ├── style.css            # Styling
│   │   └── script.js            # Client logic
│   ├── requirements.txt         # Frontend dependencies
│   ├── README.md                # Frontend documentation
│   └── .gitignore
│
├── 🤖 Chatbot Backend Files     # BACKEND (Rasa Application)
│   ├── actions/
│   │   ├── __init__.py
│   │   └── actions.py           # Custom actions
│   ├── data/
│   │   ├── nlu.yml              # Training data
│   │   ├── rules.yml            # Conversation rules
│   │   └── stories.yml          # Conversation flows
│   ├── models/                  # Trained models
│   ├── config.yml               # Rasa configuration
│   ├── domain.yml               # Domain definition
│   ├── endpoints.yml            # Endpoints config
│   ├── credentials.yml          # Channel credentials
│   └── requirements.txt         # Backend dependencies
│
└── 📚 Documentation
    ├── README.md                # Main documentation
    ├── ARCHITECTURE.md          # This file
    └── START_WEB_UI.md          # Quick start guide
```

## 🔌 Communication Flow

### 1. User Sends Message

```
User Browser → POST /chat → Flask Server (web_ui/app.py)
```

### 2. Flask Forwards to Rasa

```
Flask Server → POST http://localhost:5005/webhooks/rest/webhook → Rasa Server
```

**Payload:**

```json
{
  "sender": "session_12345",
  "message": "Hi"
}
```

### 3. Rasa Processes Message

- **NLU**: Extracts intent (`greet`) and entities
- **Dialogue**: Determines next action (form activation)
- **Forms**: Manages slot filling for booking_form
- **Actions**: Calls custom actions when needed

### 4. Rasa Calls Action Server (if needed)

```
Rasa Server → POST http://localhost:5055/webhook → Action Server
```

### 5. Response Flow

```
Action Server → Rasa Server → Flask Server → User Browser
```

## 🚀 Running Components Separately

### Frontend Only

```bash
cd web_ui
pip install -r requirements.txt
python app.py
# Runs on http://localhost:5001
```

**Note**: Needs Rasa backend to be accessible.

### Backend Only (Rasa)

```bash
# Terminal 1: Rasa Server
rasa run --enable-api --cors "*"
# Runs on http://localhost:5005

# Terminal 2: Action Server
rasa run actions
# Runs on http://localhost:5055
```

**Note**: Can be tested via API without the web UI.

## 🌐 Deployment Strategies

### Strategy 1: Separate Hosting

**Frontend**: Deploy to Vercel, Netlify, or Heroku
**Backend**: Deploy to AWS EC2, DigitalOcean, or Rasa X

**Pros**:

- Scale independently
- Use different hosting providers
- Clear separation of concerns

**Cons**:

- Need to configure CORS
- Manage two deployments

### Strategy 2: Same Server, Different Ports

Both run on the same server but on different ports.

**Pros**:

- Simpler deployment
- No CORS issues
- Lower hosting cost

**Cons**:

- Tightly coupled
- Scale together

### Strategy 3: Docker Containers

Each component in its own container:

- `chatbot-ui` (Port 5001)
- `chatbot-rasa` (Port 5005)
- `chatbot-actions` (Port 5055)

**Pros**:

- Easy to orchestrate with docker-compose
- Portable
- Easy to scale with Kubernetes

## 🔒 Security Considerations

### In Production:

1. **API Authentication**: Add API keys between frontend and backend
2. **HTTPS**: Use SSL certificates for both frontend and backend
3. **Rate Limiting**: Prevent abuse on both servers
4. **CORS**: Configure properly (don't use `*` in production)
5. **Environment Variables**: Store sensitive config in .env files

## 📊 Benefits of Separation

### ✅ Independent Development

- Frontend and backend teams can work independently
- Different release cycles
- Easier testing

### ✅ Scalability

- Scale frontend and backend separately based on load
- Frontend can be on CDN
- Backend can have multiple instances

### ✅ Technology Flexibility

- Can replace frontend (React, Vue, etc.) without touching backend
- Can swap Rasa with another NLU engine without changing frontend
- Use different hosting optimized for each

### ✅ Maintainability

- Clear boundaries
- Easier debugging
- Simpler to understand

## 🔄 Alternative Frontends

Since the backend is separate, you can create multiple frontends:

- **Web UI** (current): Flask + HTML/CSS/JS
- **Mobile App**: React Native, Flutter
- **Desktop App**: Electron
- **Voice Interface**: Integrate with Alexa, Google Assistant
- **Messaging**: WhatsApp, Telegram, Slack

All using the same Rasa backend!

## 📝 API Contract

The interface between frontend and backend:

**Endpoint**: `POST /webhooks/rest/webhook`

**Request**:

```json
{
  "sender": "unique-session-id",
  "message": "user message text"
}
```

**Response**:

```json
[
  {
    "recipient_id": "unique-session-id",
    "text": "bot response message"
  }
]
```

This contract allows any frontend to communicate with the Rasa backend!

---

**This architecture provides flexibility, scalability, and maintainability! 🎉**
