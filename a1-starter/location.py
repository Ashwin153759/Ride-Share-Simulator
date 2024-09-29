"""Locations for the simulation"""

from __future__ import annotations


class Location:
    """A two-dimensional location.

    ===ATTRIBUTES===
    row: the row coordinate of the location
    column: the column coordinate of the location

    """

    row: int
    column: int

    def __init__(self, row: int, column: int) -> None:
        """ Initialize a location. """
        self.row = row
        self.column = column

    def __str__(self) -> str:
        """ Return a string representation. """
        return f"{self.row},{self.column}"

    def __eq__(self, other: Location) -> bool:
        """ Return True if self equals other, and false otherwise.

        >>> location1 = Location(1,2)
        >>> location2 = Location(1,2)
        >>> location1.__eq__(location2)
        True
        """
        return self.row == other.row and self.column == other.column


def manhattan_distance(origin: Location, destination: Location) -> int:
    """Return the Manhattan distance between the origin and the destination.

    >>> location1 = Location(1,2)
    >>> location2 = Location(1,3)
    >>> manhattan_distance(location1, location2)
    1
    """
    row_distance = abs(origin.row - destination.row)
    column_distance = abs(origin.column - destination.column)

    return row_distance + column_distance


def deserialize_location(location_str: str) -> Location:
    """Deserialize a location.

    location_str: A location in the format 'row,col'

    >>> location= deserialize_location("1,2")
    >>> location.row
    1
    >>> location.column
    2
    """
    coordinates = location_str.split(",")
    return Location(int(coordinates[0]), int(coordinates[1]))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all()
