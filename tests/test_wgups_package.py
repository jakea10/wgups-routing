from src.wgups_package import Package
from src.delivery_location import DeliveryLocation
import pytest
import datetime

# def test_should_always_pass():
#     assert 2 + 2 == 4

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
        kgs=21
    )

def test_should_create_package(package: Package):
    assert package is not None
    assert package.id == 1
    assert isinstance(package.delivery_location, DeliveryLocation)
    assert isinstance(package.delivery_deadline, datetime.time)
    assert package.kgs == 21