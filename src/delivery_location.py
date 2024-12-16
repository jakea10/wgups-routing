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