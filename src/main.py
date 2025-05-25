from hash_table import HashTable
from wgups import Package, Truck
import csv
import datetime


EOD = "5:00 PM"

# ------------------------------------------------------------------------------
# Initialize data structures
# ------------------------------------------------------------------------------
packages = HashTable(capacity=100)
# TODO: create adjaceny matrix
# TODO: create trucks

# ------------------------------------------------------------------------------
# Load package data
# ------------------------------------------------------------------------------
package_file = "wgups-routing/data/wgups-package-file.csv"
with open(package_file, encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # print(row)
        if row['delivery_deadline'] == 'EOD':
            # print(row)
            row['delivery_deadline'] = EOD
        else:
            row['delivery_deadline'] = datetime.datetime.strptime(row['delivery_deadline'], "%I:%M %p").time()
        package = Package.from_dict(row)
        packages[package.id] = package

print(packages[6])

# ------------------------------------------------------------------------------
# Handle special notes/constraints
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Initialize trucks
# ------------------------------------------------------------------------------