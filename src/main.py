# Jacob Atencio, Student ID: 001304752
from hash_table import HashTable
from wgups import Package
import csv
import datetime


EOD_TIME = datetime.time(17, 0)  # 5:00 PM

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


# ------------------------------------------------------------------------------
# Initialize data structures
# ------------------------------------------------------------------------------
packages = HashTable(capacity=100)
# TODO: create adjaceny matrix
# TODO: create trucks

# ------------------------------------------------------------------------------
# Load package data
# ------------------------------------------------------------------------------
package_file = "wgups-routing/data/packages.csv"
load_package_data(package_file, packages)
print(packages[2])

# ------------------------------------------------------------------------------
# Handle special notes/constraints
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Initialize trucks
# ------------------------------------------------------------------------------