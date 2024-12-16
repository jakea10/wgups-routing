from src.wgups_package import Package
from src.delivery_location import DeliveryLocation
import pytest
import datetime


@pytest.fixture
def package() -> Package:
    delivery_location = DeliveryLocation(
        address="195 W Oakland Ave",
        city="Salt Lake City",
        state="UT",
        zip_code="84115"
    )
    return Package(
        id=1,
        delivery_location=delivery_location,
        delivery_deadline=datetime.datetime.strptime("10:30 AM", "%I:%M %p").time(),
        kgs=21,
        notes="Handle with care"
    )


def test_should_create_package(package: Package):
    assert package is not None
    assert package.id == 1
    assert isinstance(package.delivery_location, DeliveryLocation)
    assert isinstance(package.delivery_deadline, datetime.time)
    assert package.kgs == 21


def test_wgups_package_str(package: Package):
    """Test the __str__ method of the WGUPS Package class."""
    expected_str = (
        "Package ID: 1\n"
        "Delivery Location: 195 W Oakland Ave, Salt Lake City, UT 84115\n"
        "Deadline: 10:30 AM\n"
        "Weight: 21 kgs\n"
        "Notes: Handle with care"
    )
    assert str(package) == expected_str


def test_wgups_package_repr(package: Package):
    """Test the __repr__ method of the WGUPS Package class."""
    expected_repr = (
        "Package(id=1, "
        "delivery_location=DeliveryLocation(address='195 W Oakland Ave', city='Salt Lake City', state='UT', zip_code='84115'), "
        "delivery_deadline=datetime.time(10, 30), "
        "kgs=21, notes='Handle with care')"
    )
    assert repr(package) == expected_repr


def test_wgups_package_eq(package: Package):
    """Test the __eq__ method of the WGUPS Package class."""
    # Identical package
    package2 = Package(
        id=1,
        delivery_location=DeliveryLocation(
            address="195 W Oakland Ave",
            city="Salt Lake City",
            state="UT",
            zip_code="84115",
        ),
        delivery_deadline=datetime.time(hour=10, minute=30),
        kgs=21,
        notes="Handle with care",
    )
    assert package == package2

    # Different package
    package3 = Package(
        id=2,  # Different ID
        delivery_location=DeliveryLocation(
            address="195 W Oakland Ave",
            city="Salt Lake City",
            state="UT",
            zip_code="84115",
        ),
        delivery_deadline=datetime.time(hour=10, minute=30),
        kgs=5, # Different kgs
        notes="Handle with care",
    )
    assert package != package3

