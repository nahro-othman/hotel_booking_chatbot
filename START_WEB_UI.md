# 🚀 Quick Start Guide - Web Interface

Follow these steps to run the Hotel Booking Chatbot with the web interface.

## Prerequisites

Make sure you've already:

1. ✅ Installed all dependencies: `pip install -r requirements.txt`
2. ✅ Trained the model: `rasa train`

## Running the Web Interface

You need **3 terminals** open at the same time. Follow these steps:

### Terminal 1: Rasa Server

```bash
cd /Users/nahro/Documents/my_projects/iu_projects/hotel_booking_chatbot
source venv/bin/activate
rasa run --enable-api --cors "*"
```

**Wait for:** "Rasa server is up and running"

---

### Terminal 2: Action Server

```bash
cd /Users/nahro/Documents/my_projects/iu_projects/hotel_booking_chatbot
source venv/bin/activate
rasa run actions
```

**Wait for:** "Action endpoint is up and running"

---

### Terminal 3: Flask Web App

```bash
cd /Users/nahro/Documents/my_projects/iu_projects/hotel_booking_chatbot
source venv/bin/activate
python app.py
```

**Wait for:** "Running on http://127.0.0.1:5001"

---

## 🌐 Access the Chatbot

Open your browser and go to:

```
http://localhost:5001
```

## 🎉 Start Chatting!

Click the **"👋 Start Booking"** button and begin your hotel booking conversation!

---

## 💡 Tips

- Keep all 3 terminals running while using the web interface
- To stop a server, press `Ctrl+C` in its terminal
- If port 5000 or 5005 is already in use, you'll need to stop the process using that port
- Check the terminal logs if you encounter any issues

---

## 🐛 Troubleshooting

### "Connection Error" in browser

- Make sure all 3 servers are running
- Check that Terminal 1 shows: "Rasa server is up and running"
- Check that Terminal 2 shows: "Action endpoint is up and running"

### Port Already in Use

```bash
# Find and kill process on port 5001 (Flask)
lsof -ti:5001 | xargs kill -9

# Find and kill process on port 5005 (Rasa)
lsof -ti:5005 | xargs kill -9

# Find and kill process on port 5055 (Actions)
lsof -ti:5055 | xargs kill -9
```

### Alternative: Disable AirPlay Receiver on macOS

If you want to use port 5000, you can disable AirPlay Receiver:

1. Go to **System Settings** (or System Preferences)
2. Click **General** → **AirDrop & Handoff**
3. Turn off **AirPlay Receiver**

---

## 📸 What You'll See

The web interface features:

- ✨ Modern, responsive design
- 💬 Real-time chat interface
- 🎨 Beautiful gradient colors
- 📱 Mobile-friendly
- ⌨️ Keyboard shortcuts (Enter to send)
- 🧹 Clear conversation button
- ⏱️ Message timestamps
- 💭 Typing indicators

Enjoy booking your hotel room! 🏨
