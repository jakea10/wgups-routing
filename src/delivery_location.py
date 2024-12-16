# delivery_location.py

class DeliveryLocation():
    def __init__(
        self,
        address: str,
        city: str,
        state: str,
        zip_code: str,
                 
    ):
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    
    def __str__(self):
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"
    

    def __repr__(self):
        return (
            f"DeliveryLocation(address='{self.address}', city='{self.city}', "
            f"state='{self.state}', zip_code='{self.zip_code}')"
        )
    

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, DeliveryLocation):
            return False
        return (
            self.address == other.address
            and self.city == other.city
            and self.state == other.state
            and self.zip_code == other.zip_code

        )
