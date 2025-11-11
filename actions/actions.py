from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
import os


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
