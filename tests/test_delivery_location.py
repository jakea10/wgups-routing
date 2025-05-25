# test_delivery_location.py

from src.wgups import DeliveryLocation
import pytest


@pytest.fixture
def location() -> DeliveryLocation:
    return DeliveryLocation(
        address="195 W Oakland Ave",
        city="Salt Lake City",
        state="UT",
        zip_code="84115"
    )


def test_should_create_delivery_location(location: DeliveryLocation):
    assert location is not None
    assert location.address == "195 W Oakland Ave"
    assert location.city == "Salt Lake City"
    assert location.state == "UT"
    assert location.zip_code == "84115"


def test_delivery_location_str(location: DeliveryLocation):
    """Test the __str__ method of the DeliveryLocation class."""
    assert str(location) == "195 W Oakland Ave, Salt Lake City, UT 84115"


def test_delivery_location_repr(location: DeliveryLocation):
    """Test the __repr__ method of the DeliveryLocation class."""
    expected_repr = (
        "DeliveryLocation(address='195 W Oakland Ave', city='Salt Lake City', "
        "state='UT', zip_code='84115')"
    )
    assert repr(location) == expected_repr


def test_delivery_location_eq():
    """Test the __eq__ method of the DeliveryLocation class."""
    location1 = DeliveryLocation("123 Main St", "Anytown", "CA", "12345")
    location2 = DeliveryLocation("123 Main St", "Anytown", "CA", "12345")
    location3 = DeliveryLocation("456 Oak Ave", "Anytown", "CA", "12345")

    assert location1 == location2
    assert location1 != location3
