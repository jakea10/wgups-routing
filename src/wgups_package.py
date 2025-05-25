# package.py

from src.delivery_location import DeliveryLocation
from datetime import time


class Package:
    """
    Represents a package with an ID, delivery details, weight, and optional notes.
    """
    def __init__(
        self,
        id: int,
        delivery_location: DeliveryLocation,
        delivery_deadline: time,
        kgs: int,
        notes: str | None = None,
    ):
        """
        Initializes a new Package instance.

        Args:
            id (int): A unique identifier for the package.
            delivery_location (DeliveryLocation): The location where the package needs to be delivered.
            delivery_deadline (time): The deadline for the package delivery.
            kgs (int): The weight of the package in kilograms.
            notes (str | None): Optional additional notes for the package.
        """
        self.id = id
        self.delivery_location = delivery_location
        self.delivery_deadline = delivery_deadline
        self.kgs = kgs
        self.notes = notes


    def __str__(self):
        """
        Returns a string representation of the Package.
        """
        return (
            f"Package ID: {self.id}\n"
            f"Delivery Location: {self.delivery_location}\n"
            f"Deadline: {self.delivery_deadline.strftime('%I:%M %p')}\n"
            f"Weight: {self.kgs} kgs\n"
            f"Notes: {self.notes}"
        )


    def __repr__(self):
        """
        Returns a developer-friendly string representation of the Package.
        """
        return (
            f"Package(id={self.id}, "
            f"delivery_location={repr(self.delivery_location)}, "
            f"delivery_deadline={repr(self.delivery_deadline)}, "
            f"kgs={self.kgs}, notes='{self.notes}')"
        )


    def __eq__(self, other):
        """
        Compares two Package objects for equality.
        """
        if not isinstance(other, Package):
            return False
        return (
            self.id == other.id
            and self.delivery_location == other.delivery_location
            and self.delivery_deadline == other.delivery_deadline
            and self.kgs == other.kgs
            and self.notes == other.notes
        )
    
    def __hash__(self):
        """
        Computes a hash value for the Package object.

        This method makes Package objects hashable, allowing them to be used
        as keys in dictionaries or elements in sets.
        """
        return hash((
            self.id,
            self.delivery_location,
            self.delivery_deadline,
            self.kgs,
            self.notes
        ))
    
if __name__ == "__main__":
    from delivery_location import DeliveryLocation
    import datetime

    location = DeliveryLocation(
    address="195 W Oakland Ave",
    city="Salt Lake City",
    state="UT",
    zip_code="84115"
    )

    my_package = Package(
        id=1,
        delivery_location=location,
        delivery_deadline=datetime.datetime.strptime("10:30 AM", "%I:%M %p").time(),
        kgs=21,
        notes="Handle with care"
    )

    print(hash(my_package) % 8)