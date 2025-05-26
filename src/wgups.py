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
    """
    Represents a WGUPS delivery truck.
    """
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
            route: list[int],
            delivery_log: list[tuple[int, time]]
        ):
        """
        Initializes a new Truck instance.
        
        Args:
            id (int): Unique identifier for the truck
            capacity (int): Maximum number of packages the truck can carry
            speed_mph (int): Average speed of the truck in miles per hour
            current_location_id (int): Current address ID where the truck is located
            packages_on_board (list[Package]): List of packages currently on the truck
            mileage_traveled (float): Total miles traveled by the truck
            current_time (time): Current time for the truck
            is_available (bool): Whether the truck is available for new assignments
            return_to_hub_needed (bool): Whether the truck needs to return to hub
            route (list[int]): Planned route as list of address IDs
            delivery_log (list[tuple[int, time]]): Log of delivered packages with times
        """
        self.id = id
        self.capacity = capacity
        self.speed_mph = speed_mph
        self.current_location_id = current_location_id
        self.packages_on_board = packages_on_board
        self.mileage_traveled = mileage_traveled
        self.current_time = current_time
        self.is_available = is_available
        self.route = route
        self.delivery_log = delivery_log
    
    def add_package(self, package: Package) -> None:
        """
        Adds a package to the truck.

        Args:
            package (Package): The package to add to the truck
        
        Raises:
            ValueError: If the truck is at capacity or package already exists
        """
        if len(self.packages_on_board) >= self.capacity:
            raise ValueError(f"Truck {self.id} is at max package capacity")
        
        if package in self.packages_on_board:
            raise ValueError(f"Truck {self.id} already contains {repr(package)}")
        
        self.packages_on_board.append(package)
    
    def remove_package(self, package: Package) -> None:
        """
        Removes a package from the truck.
        
        Args:
            package (Package): The package to remove from the truck
            
        Raises:
            ValueError: If package is not found on the truck
        """
        try:
            self.packages_on_board.remove(package)
        except ValueError:
            raise ValueError(f"Not found on Truck {self.id}: {repr(package)}")

    def list_packages(self) -> None:
        """
        Prints a list of all packages currently on the truck.
        """
        if len(self.packages_on_board) > 0:
            print(f"Packages on board Truck {self.id}:")
            for package in self.packages_on_board:
                print(f"  - {repr(package)}")
        else:
            print(f"Packages on board Truck {self.id}: None")

    def deliver_package(self, package: Package, delivery_time: time) -> None:
        """
        Delivers a package and updates its status.
        
        Args:
            package (Package): The package to deliver
            delivery_time (time): The time the package was delivered
        """
        package.status = PackageStatus.DELIVERED
        package.delivery_time = delivery_time
        self.delivery_log.append((package.id, delivery_time))
        self.packages_on_board.remove(package)
    
    def get_next_destination(self, distance_matrix: list[list], address_to_id_map: dict) -> int | None:
        """
        Gets the next destination using nearest neighbor logic.
        
        Args:
            distance_matrix (list[list]): 2D matrix of distances between addresses
            address_to_id_map (dict): Maps addresses to their matrix indices
            
        Returns:
            int | None: The address ID of the nearest undelivered package, or None if no packages
        """
        if not self.packages_on_board:
            return None
        
        nearest_distance = float('inf')
        nearest_destination = None

        for package in self.packages_on_board:
            dest_id = address_to_id_map[package.address]
            distance = distance_matrix[self.current_location_id][dest_id]

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_destination = dest_id
        
        return nearest_destination
    
    def get_packages_at_address(self, address_id: int, address_to_id_map: dict) -> list[Package]:
        """
        Gets all packages on the truck that need to be delivered to the given address.

        Args:
            address_id (int): The address ID to check for packages
            address_to_id_map (dict): Maps addresses to their matrix indices

        Returns:
            list[Package]: List of packages that need to be delivered to the given address
        """
        packages_at_address = []
        for package in self.packages_on_board:
            if address_to_id_map[package.address] == address_id:
                packages_at_address.append(package)
        
        return packages_at_address
    
    def __str__(self):
        """
        Returns a string representation of the Truck.
        """
        return (f"Truck {self.id}: Location {self.current_location_id}, "
                f"Packages: {len(self.packages_on_board)}/{self.capacity}, "
                f"Miles: {self.mileage_traveled:.1f}, Time: {self.current_time}")


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

    # print(my_package)
    
    truck_1 = Truck(
        id=1,
        capacity=16,
        speed_mph=18,
        current_location_id=0,
        packages_on_board=[],
        mileage_traveled=0.0,
        current_time=datetime.time(8, 0),
        is_available=True,
        return_to_hub_needed=False,
        route=[],
        delivery_log=[]
    )

    truck_1.add_package(my_package)
    truck_1.add_package(my_package)
    truck_1.list_packages()
    truck_1.remove_package(my_package)
    truck_1.list_packages()
    truck_1.remove_package(my_package)