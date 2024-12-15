# package.py

from datetime import time


class Package:
    def __init__(
        self,
        id: int,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        delivery_deadline: time,
        kgs: int,
        notes: str,
    ):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.kgs = kgs
        self.notes = notes
