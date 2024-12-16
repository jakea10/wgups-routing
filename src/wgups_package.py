# package.py

from src.delivery_location import DeliveryLocation
from datetime import time


class Package:
    def __init__(
        self,
        id: int,
        delivery_location: DeliveryLocation,
        delivery_deadline: time,
        kgs: int,
        notes: str | None = None,
    ):
        self.id = id
        self.delivery_location = delivery_location
        self.delivery_deadline = delivery_deadline
        self.kgs = kgs
        self.notes = notes


    def __str__(self):
        return (
            f"Package ID: {self.id}\n"
            f"Delivery Location: {self.delivery_location}\n"
            f"Deadline: {self.delivery_deadline.strftime('%I:%M %p')}\n"
            f"Weight: {self.kgs} kgs\n"
            f"Notes: {self.notes}"
        )


    def __repr__(self):
        return (
            f"Package(id={self.id}, "
            f"delivery_location={repr(self.delivery_location)}, "
            f"delivery_deadline={repr(self.delivery_deadline)}, "
            f"kgs={self.kgs}, notes='{self.notes}')"
        )


    def __eq__(self, other):
        if not isinstance(other, Package):
            return False
        return (
            self.id == other.id
            and self.delivery_location == other.delivery_location
            and self.delivery_deadline == other.delivery_deadline
            and self.kgs == other.kgs
            and self.notes == other.notes
        )