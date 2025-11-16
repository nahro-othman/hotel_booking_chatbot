# 🚀 Quick Start: Web Frontend

This guide shows you how to run the hotel booking chatbot **in your web browser**!

---

## ⚡ 3-Step Quick Start

### Step 1: Start Rasa (Terminal 1)

```bash
./run.sh
```

**What this does:**
- Starts the Rasa server (Port 5005)
- Starts the action server (Port 5055)
- Loads the trained chatbot model

**Wait until you see:** "Rasa server is up and running"

---

### Step 2: Start the Web Server (Terminal 2)

```bash
cd flask_api
./run_api.sh
```

**What this does:**
- Starts Flask API server (Port 5000)
- Serves the web chat interface
- Connects to Rasa

**Wait until you see:** "Running on http://0.0.0.0:5000"

---

### Step 3: Open in Browser

Open your web browser and go to:

**🌐 http://localhost:5001**

That's it! Start chatting with the bot! 🎉

> **Note:** We use port 5001 instead of 5000 because macOS uses port 5000 for AirPlay Receiver.

---

## 🎨 Using the Web Interface

### What You'll See:

A beautiful purple chat interface with:
- Modern gradient design
- Message bubbles (yours on right, bot on left)
- Typing indicators when bot is "thinking"
- Status indicator (green = online)
- Reset button to start over

### How to Use:

1. **Type "hi" in the message box** at the bottom
2. **Press Enter** or click "Send"
3. **Follow the bot's questions:**
   - Your name
   - Check-in date
   - Check-out date (this is now fixed!)
   - Number of guests
   - Room type
   - Breakfast preference
   - Payment method
4. **Confirm your booking** when the bot shows the summary
5. **Done!** Your booking is saved

### Example Conversation:

```
You: hi
Bot: Hello! I can help you book a hotel room. What's your name?

You: John Smith
Bot: Nice to meet you, John Smith! What's your check-in date?

You: tomorrow
Bot: How many guests will stay?

You: 2
Bot: And your check-out date?

You: in 3 days
Bot: What room type would you like? Single, Double, Suite, or Deluxe?

You: double
Bot: Do you want breakfast included?

You: yes
Bot: How would you like to pay? Credit Card, Debit Card, Cash, or PayPal?

You: credit card
Bot: Here's your summary: John Smith, Double room, 2 guests, from tomorrow to in 3 days, breakfast included, payment by Credit Card. Confirm?

You: yes
Bot: Great! Your booking is confirmed. Thank you for choosing our hotel.
```

---

## 🔄 Reset Conversation

If you make a mistake or want to start over:

1. Click the **"Reset Chat"** button at the top
2. Or refresh the browser page
3. Start a new conversation from scratch!

---

## 🐛 Troubleshooting

### Problem: "Cannot connect to chatbot server"

**Solution:** Rasa is not running. Go back to Terminal 1 and run:
```bash
./run.sh
```

### Problem: "Offline" or "Bot Offline" status

**Solution:** 
1. Check Terminal 1 - is Rasa running?
2. Check Terminal 2 - is Flask running?
3. Try restarting both

### Problem: Page won't load

**Solution:**
1. Make sure you're using the correct URL: http://localhost:5000
2. Check if Flask is running in Terminal 2
3. Check browser console for errors (F12)

### Problem: Bot not responding

**Solution:**
1. Check if the status indicator is green
2. Click the "Reset Chat" button
3. Refresh the page
4. Check Terminal 2 for error messages

---

## 💻 For Different Devices

### Desktop/Laptop:
Open http://localhost:5000 in:
- Chrome
- Firefox
- Safari
- Edge

### Mobile (on same network):
1. Find your computer's IP address:
   ```bash
   # Mac/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Or
   hostname -I
   ```
2. On your phone, open: http://YOUR_IP:5000
   (e.g., http://192.168.1.100:5000)

### Tablet:
Same as mobile - use your computer's IP address

---

## 🎨 Customize the Look

The web interface is in: `flask_api/static/index.html`

### Change Colors:

Find this line and change the colors:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Try these color combinations:
- Blue: `#4158D0 0%, #C850C0 100%`
- Green: `#0BA360 0%, #3CBA92 100%`
- Orange: `#FA8BFF 0%, #2BD2FF 100%`
- Red: `#E44D26 0%, #F16529 100%`

### Add Your Logo:

Edit `flask_api/static/index.html` and add:
```html
<img src="your-logo.png" alt="Logo" style="height: 40px;">
```

---

## 📊 View Your Bookings

All confirmed bookings are saved in: `bookings.txt`

To view them:
```bash
cat bookings.txt
```

Or through the API:
```bash
curl http://localhost:5000/bookings
```

Or in your browser:
http://localhost:5000/bookings

---

## 🚀 What's Next?

### For End Users:
- Just use the web interface!
- No installation needed (after initial setup)
- Works on any device with a browser

### For Developers:
- Integrate the API into your app
- Customize the frontend design
- Deploy to production server
- Add more features

**See:** `flask_api/README.md` for more details

---

## 📞 Quick Commands Reference

```bash
# Start everything (need 2 terminals)

# Terminal 1: Start Rasa
./run.sh

# Terminal 2: Start Web Server
cd flask_api
./run_api.sh

# Then open: http://localhost:5000

# Stop everything
# Terminal 1 & 2: Press Ctrl+C

# Or use the stop script
./stop.sh
```

---

## ✅ Checklist

Before you start:
- [ ] Python 3.10+ installed
- [ ] Virtual environment created (run `./setup.sh` if not)
- [ ] Rasa model trained (run `rasa train` if needed)
- [ ] Flask installed (included in requirements.txt)

To run:
- [ ] Terminal 1: `./run.sh` ✓
- [ ] Terminal 2: `cd flask_api && ./run_api.sh` ✓
- [ ] Browser: http://localhost:5000 ✓

---

## 🎉 You're All Set!

**The web interface is the easiest way to use the chatbot:**
- ✅ No command line needed (after starting servers)
- ✅ Beautiful, modern UI
- ✅ Works on any device
- ✅ Real-time chat experience
- ✅ Easy to share with others

**Enjoy chatting with your bot! 🏨**

---

**Need more help?**
- See `flask_api/README.md` for Flask/Frontend details
- See `README.md` for complete project documentation
- See `flask_api/API_README.md` for API documentation

