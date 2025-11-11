# 🎯 Separated UI and Chatbot Setup Guide

The project is now **completely separated** into two independent applications:

## 📦 Two Applications

### 1. 🤖 **Chatbot Backend** (Rasa)
- **Location**: Root directory
- **Purpose**: NLU, dialogue management, custom actions
- **Ports**: 5005 (Rasa), 5055 (Actions)
- **Dependencies**: `requirements.txt` (root)

### 2. 🌐 **Web UI Frontend** (Flask)
- **Location**: `web_ui/` directory
- **Purpose**: User interface, session management
- **Port**: 5001
- **Dependencies**: `web_ui/requirements.txt`

---

## 🚀 Quick Start (Both Together)

### Option 1: Automated Script

```bash
./start_all.sh
```

This starts all three components automatically!

To stop:
```bash
./stop_all.sh
```

### Option 2: Manual Start

**Terminal 1 - Rasa Server:**
```bash
source venv/bin/activate
rasa run --enable-api --cors "*"
```

**Terminal 2 - Action Server:**
```bash
source venv/bin/activate
rasa run actions
```

**Terminal 3 - Web UI:**
```bash
cd web_ui
python app.py
```

Then open: **http://localhost:5001**

---

## 🎯 Running Separately

### Run Backend Only (API Testing)

Start only the chatbot backend:

```bash
# Terminal 1
source venv/bin/activate
rasa run --enable-api --cors "*"

# Terminal 2
source venv/bin/activate
rasa run actions
```

Test via API:
```bash
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "test_user",
    "message": "Hi"
  }'
```

### Run Frontend Only (With Remote Backend)

If you have Rasa deployed elsewhere:

```bash
cd web_ui
export RASA_API_URL="https://your-rasa-server.com/webhooks/rest/webhook"
python app.py
```

---

## 📁 File Structure

```
hotel_booking_chatbot/
│
├── 🌐 web_ui/                    # FRONTEND APPLICATION (Separate)
│   ├── app.py                    # Flask server
│   ├── templates/                # HTML templates
│   ├── static/                   # CSS & JavaScript
│   ├── requirements.txt          # Frontend dependencies only
│   ├── README.md                 # Frontend documentation
│   └── .gitignore
│
├── 🤖 Backend Files              # RASA CHATBOT (Separate)
│   ├── actions/                  # Custom actions
│   ├── data/                     # Training data
│   ├── models/                   # Trained models
│   ├── config.yml
│   ├── domain.yml
│   ├── endpoints.yml
│   └── requirements.txt          # Backend dependencies
│
├── 📜 Scripts
│   ├── start_all.sh              # Start everything
│   └── stop_all.sh               # Stop everything
│
└── 📚 Documentation
    ├── README.md                 # Main documentation
    ├── ARCHITECTURE.md           # System architecture
    ├── SEPARATED_SETUP.md        # This file
    └── START_WEB_UI.md           # UI quick start
```

---

## 🔧 Installation

### Backend Setup

```bash
# In root directory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
rasa train
```

### Frontend Setup

```bash
# In web_ui directory
cd web_ui
pip install -r requirements.txt
# Or create separate venv for frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🌐 Deployment Options

### Option 1: Both on Same Server

```
Server (e.g., AWS EC2)
├── Backend: Port 5005, 5055
└── Frontend: Port 5001
```

### Option 2: Separate Servers

```
Frontend Server (e.g., Vercel)
└── Port 80/443 → Points to Backend

Backend Server (e.g., DigitalOcean)
└── Port 5005 (Rasa API)
```

### Option 3: Docker Containers

```yaml
version: '3.8'
services:
  rasa:
    build: .
    ports:
      - "5005:5005"
  
  actions:
    build: ./actions
    ports:
      - "5055:5055"
  
  web_ui:
    build: ./web_ui
    ports:
      - "5001:5001"
    environment:
      - RASA_API_URL=http://rasa:5005/webhooks/rest/webhook
```

---

## 🔄 Communication Flow

```
User Browser (Port 5001)
    ↓
Flask Web UI (web_ui/app.py)
    ↓ HTTP POST
Rasa Server (Port 5005)
    ↓ Webhook
Action Server (Port 5055)
    ↓
Returns Response
```

---

## ✅ Benefits of Separation

1. **Independent Deployment**: Deploy frontend and backend separately
2. **Technology Flexibility**: Replace frontend (React, Vue) without touching backend
3. **Scalability**: Scale each component independently
4. **Development**: Frontend and backend teams work independently
5. **Multiple Frontends**: Create mobile app, desktop app using same backend
6. **Easier Testing**: Test backend via API, frontend with mock data

---

## 🎨 Multiple Frontend Options

Since backend is separate, you can create:

- ✅ **Web UI** (current): Flask + HTML/CSS/JS
- 📱 **Mobile App**: React Native, Flutter
- 💬 **Messaging**: WhatsApp, Telegram, Slack
- 🎙️ **Voice**: Alexa, Google Assistant
- 🖥️ **Desktop**: Electron

All using the same Rasa backend!

---

## 📝 Configuration

### Backend Configuration

Edit `endpoints.yml`:
```yaml
action_endpoint:
  url: "http://localhost:5055/webhook"
```

### Frontend Configuration

Edit `web_ui/app.py`:
```python
RASA_API_URL = os.getenv('RASA_API_URL', 'http://localhost:5005/webhooks/rest/webhook')
```

Or use environment variable:
```bash
export RASA_API_URL="http://your-server:5005/webhooks/rest/webhook"
```

---

## 🐛 Troubleshooting

### Frontend can't connect to backend

1. Check Rasa is running: `curl http://localhost:5005`
2. Check CORS is enabled: `rasa run --enable-api --cors "*"`
3. Verify URL in `web_ui/app.py`

### Port conflicts

Change ports in respective files:
- **Rasa**: Default 5005 (can't easily change)
- **Actions**: `endpoints.yml` port 5055
- **Web UI**: `web_ui/app.py` port 5001

---

## 📚 Documentation Links

- [Main README](README.md) - Full project documentation
- [Architecture](ARCHITECTURE.md) - System design and communication flow
- [Web UI README](web_ui/README.md) - Frontend-specific documentation
- [Rasa Docs](https://rasa.com/docs/) - Official Rasa documentation

---

**The separation is complete! You can now develop, deploy, and scale each component independently! 🎉**

