from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from datetime import datetime
import os
import re


class ActionShowBookingSummary(Action):
    """Custom action to show booking summary before confirmation"""

    def name(self) -> Text:
        return "action_show_booking_summary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get all slot values
        guest_name = tracker.get_slot("guest_name")
        checkin_date = tracker.get_slot("checkin_date")
        checkout_date = tracker.get_slot("checkout_date")
        num_guests = tracker.get_slot("num_guests")
        room_type = tracker.get_slot("room_type")
        breakfast = tracker.get_slot("breakfast")
        payment_method = tracker.get_slot("payment_method")
        
        # Format breakfast text
        breakfast_text = "breakfast included" if breakfast and breakfast.lower() in ["yes", "y", "yeah", "yep", "sure"] else "no breakfast"
        
        # Create summary message
        summary = (
            f"Here's your summary: {guest_name}, {room_type} room, {num_guests} guests, "
            f"from {checkin_date} to {checkout_date}, {breakfast_text}, "
            f"payment by {payment_method}. Confirm?"
        )
        
        dispatcher.utter_message(text=summary)
        
        return []


class ValidateBookingForm(FormValidationAction):
    """Validates the booking form slots"""

    def name(self) -> Text:
        return "validate_booking_form"

    def validate_guest_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate guest name"""
        
        if not slot_value or len(slot_value.strip()) < 2:
            dispatcher.utter_message(text="Please provide a valid name (at least 2 characters).")
            return {"guest_name": None}
        
        # Check if name contains only letters and spaces
        if not re.match(r"^[a-zA-Z\s]+$", slot_value):
            dispatcher.utter_message(text="Please provide a valid name (letters only).")
            return {"guest_name": None}
        
        return {"guest_name": slot_value.strip()}

    def validate_checkin_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate check-in date"""
        
        # Simple date pattern matching (DD/MM/YYYY, DD-MM-YYYY, or natural like "10th November")
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{4}',  # 10/11/2024 or 10-11-2024
            r'\d{1,2}(st|nd|rd|th)?\s+(january|february|march|april|may|june|july|august|september|october|november|december)',  # 10th November
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}',  # November 10
        ]
        
        slot_value_lower = str(slot_value).lower()
        
        for pattern in date_patterns:
            if re.search(pattern, slot_value_lower):
                return {"checkin_date": slot_value}
        
        dispatcher.utter_message(text="Please provide a valid date (e.g., 10/11/2024 or 10th November).")
        return {"checkin_date": None}

    def validate_checkout_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate check-out date"""
        
        # Use same validation as check-in date
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{4}',
            r'\d{1,2}(st|nd|rd|th)?\s+(january|february|march|april|may|june|july|august|september|october|november|december)',
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}',
        ]
        
        slot_value_lower = str(slot_value).lower()
        
        for pattern in date_patterns:
            if re.search(pattern, slot_value_lower):
                return {"checkout_date": slot_value}
        
        dispatcher.utter_message(text="Please provide a valid date (e.g., 12/11/2024 or 12th November).")
        return {"checkout_date": None}

    def validate_num_guests(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate number of guests"""
        
        # Extract numbers from text
        numbers = re.findall(r'\d+', str(slot_value))
        
        if not numbers:
            # Check for word numbers
            word_to_num = {
                'one': '1', 'two': '2', 'three': '3', 'four': '4', 
                'five': '5', 'six': '6', 'seven': '7', 'eight': '8'
            }
            
            slot_lower = str(slot_value).lower()
            for word, num in word_to_num.items():
                if word in slot_lower:
                    return {"num_guests": num}
            
            dispatcher.utter_message(text="Please provide a valid number of guests (e.g., 2 or two).")
            return {"num_guests": None}
        
        num = int(numbers[0])
        
        if num < 1 or num > 10:
            dispatcher.utter_message(text="Please provide a number between 1 and 10 guests.")
            return {"num_guests": None}
        
        return {"num_guests": str(num)}

    def validate_room_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate room type"""
        
        valid_rooms = ['single', 'double', 'suite', 'deluxe']
        slot_lower = str(slot_value).lower()
        
        for room in valid_rooms:
            if room in slot_lower:
                return {"room_type": room.capitalize()}
        
        dispatcher.utter_message(
            text="Please choose a valid room type: Single, Double, Suite, or Deluxe."
        )
        return {"room_type": None}

    def validate_breakfast(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate breakfast choice"""
        
        slot_lower = str(slot_value).lower()
        
        if any(word in slot_lower for word in ['yes', 'y', 'yeah', 'yep', 'sure', 'ok', 'okay']):
            return {"breakfast": "Yes"}
        elif any(word in slot_lower for word in ['no', 'n', 'nope', 'nah']):
            return {"breakfast": "No"}
        else:
            dispatcher.utter_message(text="Please answer with Yes or No.")
            return {"breakfast": None}

    def validate_payment_method(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate payment method"""
        
        valid_methods = ['credit card', 'debit card', 'cash', 'paypal']
        slot_lower = str(slot_value).lower()
        
        for method in valid_methods:
            if method in slot_lower or method.replace(' ', '') in slot_lower:
                return {"payment_method": method.title()}
        
        dispatcher.utter_message(
            text="Please choose a valid payment method: Credit Card, Debit Card, Cash, or PayPal."
        )
        return {"payment_method": None}


class ActionConfirmBooking(Action):
    """Custom action to confirm booking and save to file"""

    def name(self) -> Text:
        return "action_confirm_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get all slot values
        guest_name = tracker.get_slot("guest_name")
        checkin_date = tracker.get_slot("checkin_date")
        checkout_date = tracker.get_slot("checkout_date")
        num_guests = tracker.get_slot("num_guests")
        room_type = tracker.get_slot("room_type")
        breakfast = tracker.get_slot("breakfast")
        payment_method = tracker.get_slot("payment_method")
        
        # Create booking record
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        booking_record = (
            f"\n{'='*60}\n"
            f"BOOKING CONFIRMATION - {timestamp}\n"
            f"{'='*60}\n"
            f"Guest Name: {guest_name}\n"
            f"Check-in Date: {checkin_date}\n"
            f"Check-out Date: {checkout_date}\n"
            f"Number of Guests: {num_guests}\n"
            f"Room Type: {room_type}\n"
            f"Breakfast: {breakfast}\n"
            f"Payment Method: {payment_method}\n"
            f"{'='*60}\n"
        )
        
        # Save to bookings.txt file
        try:
            bookings_file = "bookings.txt"
            with open(bookings_file, "a", encoding="utf-8") as f:
                f.write(booking_record)
            print(f"Booking saved to {bookings_file}")
        except Exception as e:
            print(f"Error saving booking: {e}")
        
        return []
