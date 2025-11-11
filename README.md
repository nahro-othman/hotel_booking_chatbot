# Hotel Room Booking Chatbot 🏨

A conversational AI chatbot built with Rasa that assists users in booking hotel rooms through natural language interactions.

## 📋 Project Overview

This chatbot collects the following information through conversation:

- Guest name (required)
- Check-in date (required)
- Check-out date (required)
- Number of guests (required)
- Room type (single/double)
- Breakfast inclusion (yes/no)
- Payment method (credit card/cash)

After collecting all information, the bot confirms the booking summary and saves the booking to a local file (`bookings.txt`).

## 🛠️ Technology Stack

- **Framework**: Rasa 3.6.20
- **Python**: 3.10+
- **NLP**: Rasa NLU (default pipeline)
- **Storage**: Local file system (`bookings.txt`)

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
├── start_all.sh           # Script to start all components
├── stop_all.sh            # Script to stop all components
└── README.md             # This file
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

Use the provided script to start all components automatically:

```bash
./start_all.sh
```

This will:
- Auto-train the model if needed
- Start the Rasa server
- Start the Action server
- Wait for everything to be ready

Then interact with the bot:

```bash
rasa shell
```

To stop all components:

```bash
./stop_all.sh
```

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

User: Double.
Bot: Do you want breakfast included?

User: Yes.
Bot: How would you like to pay? Credit card or cash?

User: Credit card.
Bot: Here's your summary: Nahro, Double room, Two guests, from 10th November to 12th November, breakfast included, payment by credit card. Confirm?

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

To test the NLU model:

```bash
rasa test nlu --nlu data/nlu.yml
```

To test stories:

```bash
rasa test
```

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
