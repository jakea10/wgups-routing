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
