# wgups.py

from datetime import time
from enum import StrEnum


# Using a StrEnum for package status for a cleaner way to handle discrete states
class PackageStatus(StrEnum):
    AT_HUB = "At the hub"
    EN_ROUTE = "En route"
    DELIVERED = "Delivered"


class Package:
    """
    Represents a WGUPS package.
    """
    def __init__(
        self,
        id: int,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        delivery_deadline: time,
        weight: float,
        notes: str | None = None,
        status: PackageStatus = PackageStatus.AT_HUB,
        delivery_time: time | None = None
    ):
        """
        Initializes a new Package instance.

        Args:
            id (int): A unique identifier for the package.
            address (str): The address where the package needs to be delivered.
            city (str): The city where the package needs to be delivered.
            state (str): The state where the package needs to be delivered.
            zip_code (str): The zip_code where the package needs to be delivered.
            delivery_deadline (time): The deadline for the package delivery.
            weight (float): The weight of the package in kilograms.
            notes (str | None): Optional additional notes for the package.
            status (PackageStatus): The current delivery status of the package.
            delivery_time(time | None): If applicable, the time the package was delivered.
        """
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.delivery_time = delivery_time


    def __str__(self):
        """
        Returns a string representation of the Package.
        """
        return (f"Package ID: {self.id}, Address: {self.address}, City: {self.city}, "
                f"Zip: {self.zip_code}, Deadline: {self.delivery_deadline}, Weight: {self.weight}, "
                f"Notes: {self.notes}, Status: {self.status}, Delivered: {self.delivery_time}")


    def __repr__(self):
        """
        Returns a developer-friendly string representation of the Package.
        """
        cls = self.__class__.__name__
        # return f"{cls}.from_dict({str(self)})"
        return (f"{cls}({self.id}, '{self.address}', '{self.city}', "
                f"'{self.zip_code}', {self.delivery_deadline}, '{self.weight}', "
                f"'{self.notes}', '{self.status}', '{self.delivery_time}')")


    def __eq__(self, other):
        """
        Compares two Package objects for equality.
        """
        if not isinstance(other, Package):
            return False
        return (
            self.id == other.id
            and self.address == other.address
            and self.city == other.city
            and self.zip_code == other.zip_code
            and self.delivery_deadline == other.delivery_deadline
            and self.weight == other.weight
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
            self.address,
            self.city,
            self.state,
            self.zip_code,
            self.delivery_deadline,
            self.weight,
            self.notes
        ))
    
    @classmethod
    def from_dict(cls, dictionary: dict):
        """
        Creates a Package instance from a given dictionary.

        Args:
            dictionary(dict): The dictionary to populate the hash table with.
        """
        return cls(
            id=int(dictionary['package_id']),
            address=dictionary['address'],
            city=dictionary['city'],
            state=dictionary['state'],
            zip_code=dictionary['zip_code'],
            delivery_deadline=dictionary['delivery_deadline'],
            weight=dictionary['weight'],
            notes=dictionary['notes']
        )


class Truck:
    def __init__(
            self,
            id: int,
            capacity: int,
            speed_mph: int,
            current_location_id: int,
            packages_on_board: list[Package],
            mileage_traveled: float,
            current_time: time,
            is_available: bool,
            return_to_hub_needed: bool,
            route: list[int],
            delivery_log: list[tuple[int, time]]
        ):
        self.id = id
        self.capacity = capacity
        self.speed_mph = speed_mph
        self.current_location_id = current_location_id
        self.packages_on_board = packages_on_board
        self.mileage_traveled = mileage_traveled
        self.current_time = current_time
        self.is_available = is_available
        self.return_to_hub_needed = return_to_hub_needed
        self.route = route
        self.delivery_log = delivery_log


if __name__ == "__main__":
    import datetime

    my_package = Package(
        id=1,
        address="195 W Oakland Ave",
        city="Salt Lake City",
        state="UT",
        zip_code="84115",
        delivery_deadline=datetime.datetime.strptime("10:30 AM", "%I:%M %p").time(),
        weight=21,
        notes="Handle with care"
    )

    print(my_package)
    print(repr(my_package))