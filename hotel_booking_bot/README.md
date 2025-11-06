# Hotel Booking Chatbot (Rasa)

This project is a simple hotel room booking assistant for the IU course: Project AI Use Case - Task 1. It collects booking details and confirms the reservation, storing it locally in `bookings.txt`.

## Requirements
- Python 3.10+
- Rasa 3.x and Rasa SDK 3.x

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install "rasa==3.6.*" "rasa-sdk==3.6.*"
```

## Train the model
```bash
rasa train
```

## Run the action server (terminal 1)
```bash
rasa run actions --actions actions.actions --port 5055
```

## Run the bot in shell (terminal 2)
```bash
rasa shell
```

## Conversation Example
User: Hi

Bot: Hello! I can help you book a hotel room. What’s your name?

User: My name is Nahro.

Bot: Nice to meet you, Nahro! What’s your check-in date?

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

Bot: Here’s your summary: Nahro, Double room, 2 guests, from 10th to 12th November, breakfast included, payment by credit card. Confirm?

User: Yes.

Bot: Great! Your booking is confirmed. Thank you for choosing our hotel.

## Notes
- Bookings are appended to `bookings.txt` at the project root.
- This demo uses simple slot filling via entities and stories; no forms are used.
- For non-English dates or better date parsing, enhance NLU or use a form with validation.


