"""Dispatcher for the simulation"""

from typing import Optional
from driver import Driver
from rider import Rider


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.

    ===ATTRIBUTES===
    all_drivers: a list of all the drivers who have registered
    waiting_riders: a list of all the riders who have requested a ride, but no
                    driver was available at the time
    """

    all_drivers: list[Driver]
    waiting_riders: list[Rider]

    def __init__(self) -> None:
        """ Initialize a Dispatcher """
        self.all_drivers = []
        self.waiting_riders = []

    def __str__(self) -> str:
        """ Return a string representation of driver contents """
        return (f"Dispatcher(All drivers: {len(self.all_drivers)}, "
                f"Available riders: {len(self.waiting_riders)})")

    def request_driver(self, rider: Rider) -> Optional[Driver]:
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        >>> from location import Location
        >>> rider1 = Rider("Kyle", 10, Location(3,3), Location(3,4))
        >>> dispatch = Dispatcher()
        >>> driver = Driver("Ashwin", Location(3,2), 1)
        >>> dispatch.all_drivers.append(driver)
        >>> requested = dispatch.request_driver(rider1)
        >>> requested.id
        'Ashwin'
        """
        closest_driver = None
        riders_location = rider.origin

        for i in range(len(self.all_drivers)):
            # check if the driver is idle, has no destination
            # (to make sure they are free to drive someone else)
            if self.all_drivers[i].is_idle and (
                    self.all_drivers[i].destination is None):
                # find out who is closest to the rider
                if (closest_driver is None) or (
                        self.all_drivers[i].get_travel_time(
                            riders_location)
                        < closest_driver.get_travel_time(riders_location)):
                    closest_driver = self.all_drivers[i]

        # return the closest driver
        if closest_driver is None:
            self.waiting_riders.append(rider)
            return None
        else:
            return closest_driver

    def request_rider(self, driver: Driver) -> Optional[Rider]:
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        >>> from location import Location
        >>> driver2 = Driver("Ashwin", Location(3,2), 1)
        >>> dispatch = Dispatcher()
        >>> dispatch.waiting_riders
        []
        >>> rider1=dispatch.request_rider(driver2)
        >>> rider1 is None
        True
        """
        if driver not in self.all_drivers:
            self.all_drivers.append(driver)

        if len(self.waiting_riders) == 0:
            return None
        else:
            waiting_rider = self.waiting_riders.pop(0)
            return waiting_rider

    def cancel_ride(self, rider: Rider) -> None:
        """Cancel the ride for rider.

        >>> from location import Location
        >>> rider1 = Rider("Kyle", 10, Location(3,3), Location(3,4))
        >>> dispatch = Dispatcher()
        >>> driver1= dispatch.request_driver(rider1)
        >>> driver1 is None
        True
        >>> dispatch.cancel_ride(rider1)
        >>> rider1.status
        'cancelled'
        """
        # if the rider is in the wait list
        # and doesn't want a ride anymore, remove them from wait list
        if rider in self.waiting_riders:
            self.waiting_riders.remove(rider)

        # change the rider status to cancelled
        rider.cancelled_ride()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing', 'driver', 'rider']})
