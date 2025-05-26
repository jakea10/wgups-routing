# Jacob Atencio, Student ID: 001304752
from hash_table import HashTable
from wgups import Package, PackageStatus, Truck
import csv
import datetime


EOD_TIME: datetime.time = datetime.time(17, 0)
HUB_ADDRESS_ID: int = 0
TRUCK_CAPACITY: int = 16
TRUCK_SPEED_MPH: int = 18
START_TIME: datetime.time = datetime.time(8, 0)
ADDRESS_CHANGE_TIME: datetime.time = datetime.time(10, 20)


def load_package_data(package_file: str, hash_table: HashTable) -> None:
    """
    Parses package data from a CSV file into the provided hash table.

    Args:
        package_file (str): The path to the packages.csv file.
        hash_table (HashTable): The custom HashTable instance to populate.
    """
    with open(package_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert delivery_deadline string to datetime.time as expected by Package class constructor
            if row['delivery_deadline'] == 'EOD':
                parsed_deadline = EOD_TIME
            else:
                parsed_deadline = datetime.datetime.strptime(
                    row['delivery_deadline'], "%I:%M %p").time()
            row['delivery_deadline'] = parsed_deadline

            # Convert weight to float as expected by Package class constructor
            row['weight'] = float(row['weight'])

            # Handle potentially empty notes string
            row['notes'] = row['notes'] if row['notes'] else None

            # Create the Package object using the transformed dict
            package = Package.from_dict(row)

            # Insert the package into the provided hash_table
            hash_table[package.id] = package


def load_address_data(address_file: str) -> tuple[dict, list]:
    """
    Parses address data from a CSV file.
    Maps addresses to their corresponding IDs and provides reverse lookup.

    Args:
        address_file (str): The path to the addresses.csv file.
    
    Returns:
        tuple[dict, list]: A tuple containing the address_to_id_map (dict) and the id_to_address_map (list).
    """
    address_to_id_map = {}  # Maps addresses to corresponding indices in distance matrix
    id_to_address_map = []  # For reverse lookup (i.e. lookup address by ID)

    with open(address_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            id = int(row['id'])
            address = row['address']

            address_to_id_map[address] = id
            id_to_address_map.insert(id, address)

    return (address_to_id_map, id_to_address_map)


def load_distance_data(distance_file: str, num_addresses: int, header_row: bool = False) -> list[list]:
    """
    Parses distance data from a CSV file.

    Args:
        distance_file (str): The path to the distances.csv file.
        num_addresses (int): The total number of addresses (size of the square matrix).
        header_row (bool): Whether or not there is a header row in the distance_file. Defaults to False.

    Returns:
        list[list]: A 2D list representing the distance matrix.
    """
    # Initialize a 2D matrix based on num_addresses with zeros as a placeholder
    distance_matrix = [[0.0 for _ in range(num_addresses)] for _ in range(num_addresses)]

    with open(distance_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        if header_row:
            reader.__next__()  # Skip header row

        current_row_index = 0
        for row in reader:
            for col_index in range(len(row)):
                distance_value = float(row[col_index])

                # The distance matrix is symmetric, i.e. distance(A,B) == distance(B,A)
                distance_matrix[current_row_index][col_index] = distance_value
                distance_matrix[col_index][current_row_index] = distance_value

            current_row_index += 1

    return distance_matrix


def create_trucks() -> list[Truck]:
    """Create and return a list of 3 trucks with default settings."""
    trucks = []
    for i in range(1, 4):
        truck = Truck(
            id=i,
            capacity=TRUCK_CAPACITY,
            speed_mph=TRUCK_SPEED_MPH,
            current_location_id=HUB_ADDRESS_ID,
            packages_on_board=[],
            mileage_traveled=0.0,
            current_time=START_TIME,
            is_available=True,
            return_to_hub_needed=False,
            route=[],
            delivery_log=[]
        )
        trucks.append(truck)

    return trucks


def assign_packages_to_trucks(packages: HashTable, trucks: list[Truck], address_to_id_map: dict) -> None:
    """
    Assign packages to trucks based on delivery constraints and efficiency.
    """
    # Groupd packages by sepcial reqs
    truck2_only = []  # Packages that can only be on truck 2
    early_deadline = []  # Packages with early deadlines
    delayed_packages = []  # Packages delayed until 9:05 AM
    grouped_packages = []  # Packages that must be delivered together
    regular_packages = []  # All other packages

    # Separate packages per constraints
    for package in packages.values:
        if package.notes and "Can only be on truck 2" in package.notes:
            truck2_only.append(package)
        elif package.notes and "Delayed on flight" in package.notes:
            delayed_packages.append(package)
        elif package.id in [13, 14, 15, 16, 19, 20]:
            grouped_packages.append(package)
        elif package.delivery_deadline < datetime.time(10, 30):
            early_deadline.append(package)
        else:
            regular_packages.append(package)
    
    # Assign truck 2 only packages
    for package in truck2_only:
        trucks[1].add_package(package)
        package.status = PackageStatus.EN_ROUTE
    
    # Assign early deadline packages to truck 1 (departs first)
    for package in early_deadline:
        if len(trucks[0].packages_on_board) < TRUCK_CAPACITY:
            trucks[0].add_package(package)
            package.status = PackageStatus.EN_ROUTE

    # Handle grouped packages (13, 14, 15, 16, 19, and 20)
    for package in grouped_packages:
        if len(trucks[0].packages_on_board) < TRUCK_CAPACITY:
            trucks[0].add_package(package)
            package.status = PackageStatus.EN_ROUTE

    # Assign delayed packages to truck 3 (departs after 9:05 AM)
    for package in delayed_packages:
        if len(trucks[2].packages_on_board) < TRUCK_CAPACITY:
            trucks[2].add_package(package)
            package.status = PackageStatus.EN_ROUTE
    
    # Distribute remaining packages
    truck_index = 0
    for package in regular_packages:
        if package.status == PackageStatus.EN_ROUTE:
            continue

        # Find truck with available capacity
        while len(trucks[truck_index].packages_on_board) >= TRUCK_CAPACITY:
            truck_index = (truck_index + 1) % 3  # there are only 3 trucks, so wrap around if necessary
        
        trucks[truck_index].add_package(package)
        package.status = PackageStatus.EN_ROUTE
        truck_index = (truck_index + 1) % 3


def nearest_neighbor_route(truck: Truck, distance_matrix: list[list], address_to_id_map: dict) -> list[int]:
    """
    Generate an optimized route using the nearest neighbor algorithm.

    Args:
        truck (Truck): The truck to generate a route for
        distance_matrix (list[list]): 2D list of distances between addresses
        address_to_id_map: Maps addresses to their matrix indices
    
    Returns:
        List of address IDs representing the optimal route
    """
    # Unloaded truck guard
    if not truck.packages_on_board:
        return []
    
    # Get destination addresses for packages on truck
    destinations = set()
    for package in truck.packages_on_board:
        dest_id = address_to_id_map[package.address]
        destinations.add(dest_id)
    
    route = []
    current_location = truck.current_location_id
    unvisited = destinations.copy()  # All destinations start off unvisited

    # Nearest neighbor algorithm
    while unvisited:
        nearest_distance = float('inf')
        nearest_destination = None

        for destination in unvisited:
            distance = distance_matrix[current_location][destination]
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_destination = destination

        route.append(nearest_destination)
        unvisited.remove(nearest_destination)
        current_location = nearest_destination

    return route


def calculate_time_from_distance(distance: float, speed_mph: int) -> datetime.timedelta:
    """Calculate travel time based on distance and speed."""
    hours = distance / speed_mph
    return datetime.timedelta(hours=hours)


def add_time(time_obj: datetime.time, delta: datetime.timedelta) -> datetime.time:
    """Add a timedelta to a time object."""
    # Convert time to datetime, add the delta, and convert back to time obj
    dummy_date = datetime.datetime.combine(datetime.date.today(), time_obj)
    new_datetime = dummy_date + delta
    return new_datetime.time()


# ------------------------------------------------------------------------------
#       Main
# ------------------------------------------------------------------------------
def main():
    # Init packages ht
    packages = HashTable(capacity=100)

    # Load package data
    package_file = "wgups-routing/data/packages.csv"
    load_package_data(package_file, packages)

    # Load address data
    address_file = "wgups-routing/data/addresses.csv"
    address_to_id_map, id_to_address_map = load_address_data(address_file)
    num_addresses = len(id_to_address_map)

    # Load distance data
    distance_file = "wgups-routing/data/distances.csv"
    distance_matrix = load_distance_data(distance_file, num_addresses)

    # Create trucks
    trucks = create_trucks()

    # TODO: Handle special case: Package 9 has wrong address until 10:20 AM

    # Assign packages
    assign_packages_to_trucks(packages, trucks, address_to_id_map)
    for truck in trucks:
        print(f"Truck {truck.id} loaded with {len(truck.packages_on_board)} / {TRUCK_CAPACITY} packages")

    # Truck 1 and 2 depart at 8:00 AM
    # Truck 3 departs at 9:05 AM after delayed packages arrive
    trucks[2].current_time = datetime.time(9, 5)

    # TODO: Simulate deliveries for all trucks

    # TODO: Print final results

    # TODO: Interactive lookup interface


if __name__ == "__main__":
    main()