# Jacob Atencio, Student ID: 001304752
from hash_table import HashTable
from wgups import Package
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


# ------------------------------------------------------------------------------
#       Initialize data structures and load data
# ------------------------------------------------------------------------------
packages = HashTable(capacity=100)
# TODO: create trucks

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
