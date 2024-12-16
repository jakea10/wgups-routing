# test_delivery_location.py

from src.delivery_location import DeliveryLocation
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
