# wgups.py

from datetime import time


class DeliveryLocation():
    def __init__(
        self,
        address: str,
        city: str,
        state: str,
        zip_code: str,
                 
    ):
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    
    def __str__(self):
        """
        Returns a string representation of the delivery location.
        """
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"
    

    def __repr__(self):
        """
        Returns a developer-friendly string representation of the delivery location.
        """
        return (
            f"DeliveryLocation(address='{self.address}', city='{self.city}', "
            f"state='{self.state}', zip_code='{self.zip_code}')"
        )
    

    def __eq__(self, other):
        """Compares two DeliveryLocation instances for equality."""
        if self is other:
            return True
        if not isinstance(other, DeliveryLocation):
            return False
        return (
            self.address == other.address
            and self.city == other.city
            and self.state == other.state
            and self.zip_code == other.zip_code

        )
    
    def __hash__(self):
        """Hashes the DeliveryLocation based on its attributes."""
        return hash((self.address, self.city, self.state, self.zip_code))


class Package:
    """
    Represents a package with an ID, delivery details, weight, and optional notes.
    """
    def __init__(
        self,
        id: int,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        # delivery_location: DeliveryLocation,
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
        # self.address = address
        # self.city = city
        # self.state = state
        # self.zip_code = zip_code
        self.delivery_location = DeliveryLocation(
            address, city, state, zip_code
        )
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
            # self.address,
            # self.city,
            # self.state,
            # self.zip_code,
            self.delivery_location,
            self.delivery_deadline,
            self.kgs,
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
            kgs=dictionary['kgs'],
            notes=dictionary['notes']
        )


class Truck:
    def __init__(
            self, 
            capacity: int, 
            speed: int, 
            packages: list, 
            mileage: float, 
            depart_time: time
        ):
        self.capacity = capacity
        self.speed = speed
        self.packages = packages
        self.mileage = mileage
        self.depart_time = depart_time
        self.time = depart_time


if __name__ == "__main__":
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