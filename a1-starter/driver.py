"""Drivers for the simulation"""
from typing import Optional
from location import Location, manhattan_distance
from rider import Rider


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    id: A unique identifier for the driver.
    location: The current location of the driver.
    is_idle: True if the driver is idle and False otherwise.
    destination: the destination the driver is traveling to
    _speed: the driver's speed
    """

    id: str
    location: Location
    is_idle: bool
    destination: Optional[Location]
    _speed: int

    def __init__(self, identifier: str, location: Location, speed: int) -> None:
        """Initialize a Driver.

        """
        self.id = identifier
        self.location = location
        self.is_idle = True

        self.destination = None
        self._speed = speed

    def __str__(self) -> str:
        """Return a string representation. """

        return (f"Driver({self.id}, {self.location}, {self.is_idle},"
                f" {self._speed}, {self.destination})")

    def __eq__(self, other: object) -> bool:
        """Return True if self equals other, and false otherwise.

        >>> driver1 = Driver("Ashwin", Location(1,2), 1)
        >>> driver2 = Driver("Kyle", Location(1,2), 1)
        >>> driver1.__eq__(driver2)
        False
        """

        if not isinstance(other, Driver):
            return False

        return self.id == other.id

    def get_travel_time(self, destination: Location) -> int:
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        >>> driver1 = Driver("Ashwin", Location(1,2), 1)
        >>> driver1.get_travel_time(Location(1,3))
        1
        """
        distance = manhattan_distance(self.location, destination)
        travel_time = round(distance / self._speed)

        return travel_time

    def start_drive(self, location: Location) -> int:
        """Start driving to the location.
        Return the time that the drive will take.

        >>> driver1 = Driver("Ashwin", Location(1,2), 1)
        >>> new_location = Location(1,3)
        >>> driver1.start_drive(new_location)
        1
        >>> driver1.destination.row
        1
        >>> driver1.destination.column
        3
        """
        self.is_idle = False

        time_to_rider_location = self.get_travel_time(location)

        self.destination = location
        return time_to_rider_location

    def end_drive(self) -> None:
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        >>> driver1 = Driver("Ashwin", Location(1,2), 1)
        >>> new_location = Location(1,3)
        >>> time = driver1.start_drive(new_location)
        >>> driver1.end_drive()
        >>> driver1.location.column
        3
        """
        self.location = self.destination
        self.destination = None

    def start_ride(self, rider: Rider) -> int:
        """Start a ride and return the time the ride will take.

        >>> driver1 = Driver("Ashwin", Location(1,2), 1)
        >>> rider1 = Rider("Kyle", 1, Location(1,3), Location(1,4))
        >>> time = driver1.start_drive(rider1.origin)
        >>> driver1.end_drive()
        >>> final_time = driver1.start_ride(rider1)
        >>> driver1.destination.column
        4
        """
        self.is_idle = False
        self.destination = rider.destination

        return self.get_travel_time(rider.destination)

    def end_ride(self) -> None:
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        >>> driver1 = Driver("Ashwin", Location(1,2), 1)
        >>> rider1 = Rider("Kyle", 1, Location(1,3), Location(1,4))
        >>> time = driver1.start_drive(rider1.origin)
        >>> driver1.end_drive()
        >>> final_time = driver1.start_ride(rider1)
        >>> driver1.end_ride()
        >>> driver1.location.column
        4
        """
        self.is_idle = True
        self.location = self.destination
        self.destination = None


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(
        config={'extra-imports': ['location', 'rider']})
