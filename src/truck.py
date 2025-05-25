from datetime import time

class Truck:
    def __init__(
            self, 
            capacity: int, 
            speed: int, 
            packages: list, 
            mileage: float, 
            depart_time: time
        ):
        self.capacity = capacity
        self.speed = speed
        self.packages = packages
        self.mileage = mileage
        self.depart_time = depart_time
        self.time = depart_time