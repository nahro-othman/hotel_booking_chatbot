from __future__ import annotations

import os
from typing import Any, Dict, List, Text, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import ValidationAction


class ActionStoreBooking(Action):
    def name(self) -> Text:
        return "action_store_booking"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        guest_name = (tracker.get_slot("name") or "").strip()
        checkin_date = (tracker.get_slot("checkin_date") or "").strip()
        checkout_date = (tracker.get_slot("checkout_date") or "").strip()
        guests = (tracker.get_slot("guests") or "").strip()
        room_type = (tracker.get_slot("room_type") or "").strip()
        breakfast = (tracker.get_slot("breakfast") or "").strip()
        payment_method = (tracker.get_slot("payment_method") or "").strip()

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bookings_path = os.path.join(project_root, "bookings.txt")

        record = (
            f"Name: {guest_name}\n"
            f"Check-in: {checkin_date}\n"
            f"Check-out: {checkout_date}\n"
            f"Guests: {guests}\n"
            f"Room type: {room_type}\n"
            f"Breakfast: {breakfast}\n"
            f"Payment: {payment_method}\n"
            "---\n"
        )

        with open(bookings_path, "a", encoding="utf-8") as f:
            f.write(record)

        dispatcher.utter_message(text="Great! Your booking is confirmed. Thank you for choosing our hotel.")
        return []


class ValidateBookingForm(ValidationAction):
    def name(self) -> Text:
        return "validate_booking_form"

    @staticmethod
    def _normalize_yes_no(value: Optional[str]) -> Optional[str]:
        if not value:
            return value
        v = value.strip().lower()
        yes_values = {"y", "yes", "yeah", "yep", "sure", "affirm", "true"}
        no_values = {"n", "no", "nope", "nah", "false"}
        if v in yes_values:
            return "yes"
        if v in no_values:
            return "no"
        return value

    @staticmethod
    def _normalize_room_type(value: Optional[str]) -> Optional[str]:
        if not value:
            return value
        v = value.strip().lower()
        if "double" in v:
            return "double"
        if "single" in v:
            return "single"
        return value

    @staticmethod
    def _normalize_payment(value: Optional[str]) -> Optional[str]:
        if not value:
            return value
        v = value.strip().lower()
        if "card" in v or "credit" in v or "visa" in v or "master" in v:
            return "credit card"
        if "cash" in v:
            return "cash"
        return value

    @staticmethod
    def _normalize_guests(value: Optional[str]) -> Optional[str]:
        if not value:
            return value
        v = value.strip().lower()
        words_to_nums = {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
            "ten": "10",
        }
        if v in words_to_nums:
            return words_to_nums[v]
        # keep digits-only as-is
        if v.isdigit():
            return v
        return value

    async def extract_breakfast(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> Dict[Text, Any]:
        value = tracker.latest_message.get("text") or tracker.get_slot("breakfast")
        return {"breakfast": self._normalize_yes_no(value)}

    async def validate_breakfast(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        normalized = self._normalize_yes_no(value)
        if normalized in {"yes", "no"}:
            return {"breakfast": normalized}
        dispatcher.utter_message(text="Please answer with yes or no for breakfast.")
        return {"breakfast": None}

    async def validate_room_type(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        normalized = self._normalize_room_type(value)
        if normalized in {"single", "double"}:
            return {"room_type": normalized}
        dispatcher.utter_message(text="Please choose 'single' or 'double'.")
        return {"room_type": None}

    async def validate_payment_method(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        normalized = self._normalize_payment(value)
        if normalized in {"credit card", "cash"}:
            return {"payment_method": normalized}
        dispatcher.utter_message(text="Payment can be 'credit card' or 'cash'.")
        return {"payment_method": None}

    async def validate_guests(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        normalized = self._normalize_guests(value)
        if normalized and (normalized.isdigit() and int(normalized) > 0):
            return {"guests": normalized}
        dispatcher.utter_message(text="How many guests? (e.g., 1, 2, three)")
        return {"guests": None}


