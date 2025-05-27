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


# ANSI color codes for printing colored text
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'  # Reset to default


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
    wrong_address = []  # Packages that have the wrong address and must wait to be corrected
    regular_packages = []  # All other packages

    # Separate packages per constraints
    for package in packages.values:
        if package.notes and "Can only be on truck 2" in package.notes:
            truck2_only.append(package)
        elif package.notes and "Delayed on flight" in package.notes:
            delayed_packages.append(package)
        elif package.id in [13, 14, 15, 16, 19, 20]:
            grouped_packages.append(package)
        elif package.delivery_deadline < EOD_TIME:
            early_deadline.append(package)
        elif package.notes and "Wrong address" in package.notes:
            wrong_address.append(package)
        else:
            regular_packages.append(package)
    
    # Assign truck 2 only packages
    for package in truck2_only:
        trucks[1].add_package(package)
        packages[package.id].status = PackageStatus.EN_ROUTE

    # Assign delayed packages to truck 2 (departs after 9:05 AM)
    for package in delayed_packages:
        trucks[1].add_package(package)
        packages[package.id].status = PackageStatus.EN_ROUTE
    
    # Assign early deadline packages to truck 1 (departs first)
    for package in early_deadline:
        if len(trucks[0].packages_on_board) < TRUCK_CAPACITY:
            trucks[0].add_package(package)
            packages[package.id].status = PackageStatus.EN_ROUTE

    # Handle grouped packages (13, 14, 15, 16, 19, and 20)
    for package in grouped_packages:
        if len(trucks[0].packages_on_board) < TRUCK_CAPACITY:
            trucks[0].add_package(package)
            packages[package.id].status = PackageStatus.EN_ROUTE

    # Assign wrong address packages to truck 3
    for package in wrong_address:
        if len(trucks[2].packages_on_board) < TRUCK_CAPACITY:
            trucks[2].add_package(package)
            packages[package.id].status = PackageStatus.EN_ROUTE
    
    # Distribute remaining packages
    truck_index = 2
    for package in regular_packages:
        if package.status == PackageStatus.EN_ROUTE:
            continue

        # Find truck with available capacity
        while len(trucks[truck_index].packages_on_board) >= TRUCK_CAPACITY:
            truck_index = (truck_index + 1) % 3  # there are only 3 trucks, so wrap around if necessary
        
        trucks[truck_index].add_package(package)
        packages[package.id].status = PackageStatus.EN_ROUTE
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


def deliver_packages(
        truck: Truck,
        distance_matrix: list[list],
        address_to_id_map: dict,
        packages: HashTable
    ) -> None:
    """
    Simulate package delivery for a truck following its optimized route.

    Args:
        truck: The truck making package deliveries
        distance_matrix: 2D list of distances between addresses
        address_to_id_map: Maps addresses to their matrix indices
        packages: Hash table containing all packages
    """
    # Generate optimized route
    truck.route = nearest_neighbor_route(truck, distance_matrix, address_to_id_map)

    current_location = truck.current_location_id
    current_time = truck.current_time

    for destination_id in truck.route:
        # Calculate travel time to destination
        distance = distance_matrix[current_location][destination_id]
        travel_time = calculate_time_from_distance(distance, truck.speed_mph)

        # Update truck's location and time
        truck.mileage_traveled += distance
        current_time = add_time(current_time, travel_time)
        truck.current_location_id = destination_id
        truck.current_time = current_time

        # Deliver all packages for this address
        for package in truck.get_packages_at_address(destination_id, address_to_id_map):
            truck.deliver_package(package, current_time)
            # Update package status in main hash table
            packages[package.id].status = PackageStatus.DELIVERED
            packages[package.id].delivery_time = current_time

        current_location = destination_id
    
    # All packages delviered, return to hub
    distance_to_hub = distance_matrix[truck.current_location_id][HUB_ADDRESS_ID]
    travel_time_to_hub = calculate_time_from_distance(distance_to_hub, truck.speed_mph)
    truck.mileage_traveled += distance_to_hub
    truck.current_time = add_time(truck.current_time, travel_time_to_hub)
    truck.current_location_id = HUB_ADDRESS_ID


def print_package_status(packages: HashTable, current_time: datetime.time | None = None) -> None:
    """Print status of all packages, optionally filtered by time."""
    print("\n" + f"{Colors.BOLD}={Colors.END}" * 80)
    print(f"\t{Colors.BOLD}PACKAGE STATUS REPORT{Colors.END}")
    print(f"{Colors.BOLD}={Colors.END}" * 80)
    if current_time:
        print(f"Status as of: {current_time.strftime('%I:%M %p')}")

    for package_id in sorted(packages.keys):
        package = packages[package_id]
        deadline_str = package.delivery_deadline.strftime('%I:%M %p') if package.delivery_deadline != EOD_TIME else 'EOD'
        delivery_str = package.delivery_time.strftime('%I:%M %p') if package.delivery_time else 'Not delivered'
        if 'Not delivered' in delivery_str:
            deadline_color = Colors.YELLOW
        else:
            deadline_color = Colors.GREEN if package.delivery_time < package.delivery_deadline else Colors.RED
        print(f"Package {package.id:2d}: {package.address:<40} | "
              f"Deadline: {deadline_str:8} | Status: {package.status:<12} | "
              f"Delivered: {deadline_color}{delivery_str}{Colors.END}")


def print_truck_summary(trucks: list[Truck]) -> None:
    """Print summary of all trucks."""
    print("\n" + f"{Colors.BOLD}={Colors.END}" * 80)
    print(f"\t{Colors.BOLD}TRUCK SUMMARY{Colors.END}")
    print(f"{Colors.BOLD}={Colors.END}" * 80)
    total_mileage = 0
    
    for truck in trucks:
        print(f"Truck {truck.id}: {truck.mileage_traveled:.1f} miles | "
              f"Delivered: {len(truck.delivery_log)} packages | "
              f"Final time: {truck.current_time.strftime('%I:%M %p')}")
        total_mileage += truck.mileage_traveled
    
    color = Colors.GREEN if total_mileage < 140 else Colors.RED
    print(f"\nTotal mileage for all trucks: {color}{total_mileage:.1f} miles{Colors.END}")


def lookup_package_at_time(package_id: int, lookup_time: datetime.time, packages: HashTable) -> str:
    """
    Look up a package's status at a specific time.
    
    Args:
        package_id: ID of the package to look up
        lookup_time: Time to check the package status
        packages: Hash table containing all packages
        
    Returns:
        String describing the package status at the given time
    """
    if package_id not in packages:
        return f"Package {package_id} not found"
    
    package = packages[package_id]

    # If package hasn't been delivered yet or delivery time is after lookup time
    if not package.delivery_time or package.delivery_time > lookup_time:
        if package.loaded_time < lookup_time:
            return f"Package {package_id} is en route"
        else:
            return f"Package {package_id} is at the hub"
    else:
        return f"Package {package_id} delivered at {package.delivery_time.strftime('%I:%M %p')}"


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

    # Assign packages
    assign_packages_to_trucks(packages, trucks, address_to_id_map)
    for truck in trucks:
        print(f"Truck {truck.id} loaded with {len(truck.packages_on_board)} / {TRUCK_CAPACITY} packages")

    # Simulate deliveries truck 1
    print(f"Delivering packages for Truck {trucks[0].id} (start time: {trucks[0].current_time})...")
    deliver_packages(trucks[0], distance_matrix, address_to_id_map, packages)

    # Simulate deliveries truck 2
    trucks[1].current_time = datetime.time(9, 5)
    print(f"Delivering packages for Truck {trucks[1].id} (start time: {trucks[1].current_time})...")
    deliver_packages(trucks[1], distance_matrix, address_to_id_map, packages)

    # Handle special case: Package 9 has wrong address until 10:20 AM
    packages[9].address = "410 S State St"  # Correct address

    # Truck 1 departs at 8:00 AM
    # Truck 2 departs at 9:05 AM
    # Truck 3 departs after truck 1 or 2 returns (only two drivers)
    trucks[2].current_time = min(trucks[0].current_time, trucks[1].current_time)
    print(f"Delivering packages for Truck {trucks[2].id} (start time: {trucks[2].current_time})...")
    deliver_packages(trucks[2], distance_matrix, address_to_id_map, packages)

    # Print final results
    print_package_status(packages)
    print_truck_summary(trucks)

    # Interactive lookup interface
    print("\n" + f"{Colors.BOLD}={Colors.END}" * 80)
    print(f"{Colors.BOLD}\tINTERACTIVE PACKAGE LOOKUP{Colors.END}")
    print(f"{Colors.BOLD}={Colors.END}" * 80)

    while True:
        try:
            print(f"\n{Colors.BOLD}Options:{Colors.END}")
            print(f"  {Colors.BOLD}1.{Colors.END} Look up package status at specific time")
            print(f"  {Colors.BOLD}2.{Colors.END} View all packages at specific time") 
            print(f"  {Colors.BOLD}3.{Colors.END} Look up specific package current status")
            print(f"  {Colors.BOLD}4.{Colors.END} View truck delivery logs")
            print(f"  {Colors.BOLD}5.{Colors.END} Exit")
            
            choice = input("\nEnter choice (1-5): ").strip()

            if choice == '1':
                package_id = int(input("Enter package ID: "))
                time_str = input("Enter time (HH:MM AM/PM): ")
                lookup_time = datetime.datetime.strptime(time_str, "%I:%M %p").time()
                result = lookup_package_at_time(package_id, lookup_time, packages)
                print(result)

            elif choice == '2':
                time_str = input("Enter time (HH:MM AM/PM): ")
                lookup_time = datetime.datetime.strptime(time_str, "%I:%M %p").time()
                for package_id in sorted(packages.keys):
                    result = lookup_package_at_time(package_id, lookup_time, packages)
                    print(result)
            
            elif choice == '3':
                package_id = int(input("Enter package ID: "))
                if package_id in packages:
                    result = lookup_package_at_time(package_id, EOD_TIME, packages)
                    print(result)
                else:
                    print(f"Package {package_id} not found")

            elif choice == '4':
                for truck in trucks:
                    package_ids = sorted([delivery[0] for delivery in truck.delivery_log])
                    print(f"Truck {truck.id} delivery log:")
                    for pkg_id in package_ids:
                        print(f"  - Package {pkg_id}")

            elif choice == '5':
                break

        except ValueError:
            print("Invalid input. Please try again.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()