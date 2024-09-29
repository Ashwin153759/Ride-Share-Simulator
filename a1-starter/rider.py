"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
WAITING: A constant used for the waiting rider status.
CANCELLED: A constant used for the cancelled rider status.
SATISFIED: A constant used for the satisfied rider status
"""
from location import Location

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """A rider for a ride-sharing service.

    ===ATTRIBUTES===
    id: the riders id
    patience: the patience level the rider has before canceling a ride
    origin: the location the rider is currently at
    destination: the location the rider wants to go
    status: the current status of the rider (the constants above)
    """

    id: str
    patience: int
    origin: Location
    destination: Location
    status: str

    def __init__(self, identifier: str, patience: int, origin: Location,
                 destination: Location) -> None:
        """Initialize a Rider.

        """
        self.id = identifier
        self.patience = patience
        self.origin = origin
        self.destination = destination
        self.status = WAITING

    def __str__(self) -> str:
        """ return a string representation of the rider's attributes"""
        return (f"Rider({self.id}, {self.patience}, {self.origin},"
                f" {self.destination}, {self.status})")

    def __eq__(self, other: object) -> bool:
        """Return true is self equals other, else return false

        >>> rider1 = Rider("Ashwin", 1, Location(1,2), Location(1,3))
        >>> rider2 = Rider("Ashwin", 1, Location(1,2), Location(1,3))
        >>> rider1.__eq__(rider2)
        True
        """
        if not isinstance(other, Rider):
            return False

        return self.id == other.id

    def cancelled_ride(self) -> None:
        """ set the rider's status to canceled

        >>> rider1 = Rider("Ashwin", 1, Location(1,2), Location(1,3))
        >>> rider1.cancelled_ride()
        >>> rider1.status
        'cancelled'
        """
        self.status = CANCELLED

    def satisfied(self) -> None:
        """ set the rider's status to satisfied

        >>> rider1 = Rider("Ashwin", 1, Location(1,2), Location(1,3))
        >>> rider1.satisfied()
        >>> rider1.status
        'satisfied'
        """
        self.status = SATISFIED


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['location']})
