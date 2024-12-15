from src.wgups_package import Package
import pytest
import datetime

# def test_should_always_pass():
#     assert 2 + 2 == 4

@pytest.fixture
def package() -> Package:
    return Package(
        id=1,
        address="195 W Oakland Ave",
        city="Salt Lake City",
        state="UT",
        zip_code="84115",
        delivery_deadline=datetime.datetime.strptime("10:30 AM", "%I:%M %p").time(),
        kgs=21
    )

def test_should_create_package(package):
    assert package is not None