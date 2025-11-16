# Hotel Room Booking Chatbot 🏨

A conversational AI chatbot built with Rasa that assists users in booking hotel rooms through natural language interactions.

## 📋 Project Overview

This chatbot collects the following information through conversation:

- Guest name (required, minimum 3 characters)
- Check-in date (required, various formats supported)
- Check-out date (required, various formats supported)
- Number of guests (required, 1-10 guests)
- Room type (Single, Double, Suite, or Deluxe)
- Breakfast inclusion (yes/no)
- Payment method (Credit Card, Debit Card, Cash, or PayPal)

After collecting all information, the bot confirms the booking summary and saves the booking to a local file (`bookings.txt`).

## ✨ Key Features

- **Smart Validation**: Validates all user inputs with helpful error messages
- **Multiple Date Formats**: Accepts dates in various formats (DD/MM/YYYY, "10th November", "tomorrow", etc.)
- **Form-Based Conversation**: Uses Rasa forms for efficient data collection
- **Flexible Room Options**: Supports Single, Double, Suite, and Deluxe rooms
- **Multiple Payment Methods**: Credit Card, Debit Card, Cash, and PayPal
- **Help System**: Users can ask for help at any time
- **Cancellation Support**: Users can cancel bookings mid-process
- **Out-of-Scope Handling**: Gracefully handles unrelated questions
- **Persistent Storage**: All bookings saved to local file with timestamps
- **Error Recovery**: Robust error handling and user-friendly messages

## 🛠️ Technology Stack

- **Framework**: Rasa 3.6.20
- **Python**: 3.10+
- **NLP**: Rasa NLU (default pipeline)
- **Storage**: Local file system (`bookings.txt`)
- **API**: Flask 2.3.2 with CORS support

## 🌐 Web Frontend + REST API

This project includes a **beautiful web interface** and a **Flask REST API** for easy integration!

### Quick Start with Web Interface

1. **Start Rasa (Terminal 1):**
   ```bash
   ./run.sh
   ```

2. **Start Web Server (Terminal 2):**
   ```bash
   cd flask_api
   ./run_api.sh
   ```

3. **Open in Browser:**
   🌐 **http://localhost:5001**

**That's it!** Start chatting in your browser! 🎉

> **Note:** Port 5001 is used because macOS reserves port 5000 for AirPlay.

For detailed instructions, see **[QUICKSTART_WEB.md](QUICKSTART_WEB.md)**

### API Endpoints

- `POST /chat` - Send messages to the chatbot
- `POST /session/new` - Create a new conversation session
- `POST /session/reset` - Reset a conversation
- `GET /bookings` - Get all bookings
- `GET /health` - Check API and bot status
- `GET /docs` - Complete API documentation

### Integration Example

```javascript
// Send a message to the bot
const response = await fetch('http://localhost:5000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "I want to book a room",
    sender: "user123"
  })
});

const data = await response.json();
console.log(data.responses); // Bot's replies
```

📚 **Full API documentation:** See [API_README.md](API_README.md)

## 📁 Project Structure

```
hotel_booking_chatbot/
├── actions/
│   ├── __init__.py
│   └── actions.py          # Custom actions for booking logic
├── data/
│   ├── nlu.yml            # Training data for NLU
│   ├── rules.yml          # Conversation rules
│   └── stories.yml        # Conversation flows
├── models/                # Trained models (generated)
├── config.yml             # Rasa NLU pipeline and policy configuration
├── domain.yml             # Intents, entities, slots, responses, and actions
├── endpoints.yml          # Action server endpoint configuration
├── credentials.yml        # Channel credentials
├── requirements.txt       # Python dependencies
├── api.py                 # Flask REST API server
├── frontend_example.html  # Sample frontend integration
├── setup.sh               # Initial setup script
├── run.sh                 # Run the chatbot
├── start_api.sh           # Start the REST API server
├── test_api.sh            # Test API endpoints
├── stop.sh                # Stop all components
├── API_README.md          # API documentation
└── README.md              # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Step 1: Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## 🏋️ Training the Model

Train the Rasa model with the provided training data:

```bash
rasa train
```

This will create a trained model in the `models/` directory.

## 🎮 Running the Chatbot

### Option 1: Quick Start (Recommended) 🚀

```bash
# First time only - setup and train
./setup.sh

# Run the chatbot
./run.sh

# To stop (in another terminal if needed)
./stop.sh
```

The `run.sh` script will:

- Activate virtual environment
- Check if model is trained
- Start the action server automatically
- Launch the Rasa shell for you to chat

### Option 2: Manual Start

You need to run TWO terminals simultaneously:

**Terminal 1 - Start the Action Server:**

```bash
rasa run actions
```

**Terminal 2 - Start the Chatbot:**

```bash
rasa shell
```

### Option 3: Interactive Learning Mode (for testing)

```bash
rasa interactive
```

## 💬 Sample Conversation

```
User: Hi
Bot: Hello! I can help you book a hotel room. What's your name?

User: My name is Nahro.
Bot: Nice to meet you, Nahro! What's your check-in date?

User: 10th November.
Bot: And your check-out date?

User: 12th November.
Bot: How many guests will stay?

User: Two.
Bot: What room type would you like? Single or double?

User: Suite.
Bot: Do you want breakfast included?

User: Yes.
Bot: How would you like to pay? Credit Card, Debit Card, Cash, or PayPal?

User: Credit card.
Bot: Here's your summary: Nahro, Suite room, Two guests, from 10th November to 12th November, breakfast included, payment by Credit Card. Confirm?

User: Yes.
Bot: Great! Your booking is confirmed. Thank you for choosing our hotel.
```

## 📝 Booking Records

All confirmed bookings are saved to `bookings.txt` in the project root directory with the following format:

```
============================================================
BOOKING CONFIRMATION - 2024-11-11 14:30:45
============================================================
Guest Name: Nahro
Check-in Date: 10th November
Check-out Date: 12th November
Number of Guests: Two
Room Type: Double
Breakfast: Yes
Payment Method: Credit card
============================================================
```

## 🧪 Testing

### Test NLU Model

```bash
rasa test nlu --nlu data/nlu.yml
```

This will test the intent classification and entity extraction accuracy.

### Test Stories and Dialogue

```bash
rasa test
```

This tests the entire dialogue management system.

### Test Specific Scenarios

Use `rasa shell` to test these scenarios:

1. **Complete Booking Flow**: Test a full booking from greeting to confirmation
2. **Help Request**: Type "help" during booking to test help system
3. **Cancellation**: Type "cancel" mid-booking to test cancellation
4. **Out-of-Scope**: Ask "what's the weather" to test out-of-scope handling
5. **Invalid Inputs**: Test validation by providing invalid names, dates, or numbers
6. **Edge Cases**: Test with 1 guest, 10 guests, various date formats

### Interactive Testing Mode

```bash
rasa interactive
```

This allows you to test and correct the bot's behavior in real-time.

## 🔧 Customization

### Adding More Intents

1. Add intent examples to `data/nlu.yml`
2. Add intent to `domain.yml`
3. Update stories in `data/stories.yml`
4. Retrain the model: `rasa train`

### Modifying Responses

Edit the `responses` section in `domain.yml` and retrain the model.

### Adding Custom Actions

1. Add new action classes to `actions/actions.py`
2. Register the action in `domain.yml` under `actions`
3. Use the action in your stories
4. Restart the action server

## 📊 Intents & Entities

### Intents

- `greet` - Initial greeting
- `provide_name` - User provides their name
- `provide_checkin_date` - Check-in date
- `provide_checkout_date` - Check-out date
- `provide_num_guests` - Number of guests
- `provide_room_type` - Room type preference
- `provide_breakfast` - Breakfast inclusion
- `provide_payment_method` - Payment method
- `affirm` - Confirmation (yes)
- `deny` - Denial (no)
- `goodbye` - End conversation
- `ask_help` - User requests help or information
- `ask_cancel` - User wants to cancel the booking
- `out_of_scope` - Questions unrelated to hotel booking
- `thank` - User expresses gratitude

### Entities

- `name` - Guest name
- `checkin_date` - Check-in date
- `checkout_date` - Check-out date
- `num_guests` - Number of guests
- `room_type` - Room type (single/double)
- `breakfast` - Breakfast preference
- `payment_method` - Payment method

## 🐛 Troubleshooting

### Action Server Not Connecting

- Ensure the action server is running: `rasa run actions`
- Check that `endpoints.yml` points to `http://localhost:5055/webhook`
- Verify no firewall blocking port 5055

### Model Not Training

- Ensure you have enough training examples (minimum 2-5 per intent)
- Check YAML syntax in configuration files
- Verify Python version is 3.10+

### Slots Not Being Filled

- Check entity extraction in NLU training data
- Verify entity-to-slot mappings in `domain.yml`
- Test with: `rasa shell nlu`

## 🎯 Best Practices Implemented

This project follows Rasa best practices:

1. **Form-Based Slot Filling**: Efficient data collection using Rasa forms
2. **Comprehensive Validation**: All user inputs are validated before acceptance
3. **Error Handling**: Graceful error handling with user-friendly messages
4. **Conversation Recovery**: Users can restart or cancel at any time
5. **Intent Separation**: Clear separation between different user intents
6. **Rich Training Data**: Over 260+ training examples across 14 intents
7. **Multiple Conversation Paths**: Various story flows to handle different scenarios
8. **Entity Extraction**: Proper entity recognition and slot mapping
9. **Fallback Handling**: Out-of-scope intent for unrelated queries
10. **Documentation**: Comprehensive README with setup and usage instructions

## 📈 Project Statistics

- **14 Intents**: Covering all booking scenarios and edge cases
- **7 Entities**: For extracting booking information
- **7 Slots**: For storing booking details
- **8 Stories**: Diverse conversation flows
- **8 Rules**: For consistent responses
- **3 Custom Actions**: For validation and booking confirmation
- **260+ Training Examples**: Ensuring robust NLU performance

## 📚 Resources

- [Rasa Documentation](https://rasa.com/docs/rasa/)
- [Rasa Community Forum](https://forum.rasa.com/)
- [Rasa YouTube Channel](https://www.youtube.com/c/RasaHQ)

## 👨‍💻 Author

Created for IU Course: Project AI Use Case - Task 1

## 📄 License

This project is for educational purposes.

---

**Happy Booking! 🎉**
