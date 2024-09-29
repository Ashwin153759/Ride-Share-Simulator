"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from __future__ import annotations
from typing import List
from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    timestamp: A timestamp for this event.
    """

    timestamp: int

    def __init__(self, timestamp: int) -> None:
        """Initialize an Event with a given timestamp.

        Precondition: timestamp must be a non-negative integer.

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other: Event) -> bool:
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other: Event) -> bool:
        """Return True iff this Event is not equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other: Event) -> bool:
        """Return True iff this Event is less than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other: Event) -> bool:
        """Return True iff this Event is less than or equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other: Event) -> bool:
        """Return True iff this Event is greater than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other: Event) -> bool:
        """Return True iff this Event is greater than or equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    rider: The rider.
    """

    rider: Rider

    def __init__(self, timestamp: int, rider: Rider) -> None:
        """Initialize a RiderRequest event.

        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.origin)

        events = []

        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time,
                                 self.rider, driver))
        events.append(Cancellation(self.timestamp + self.rider.patience,
                                   self.rider))
        return events

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    driver: The driver.
    """

    driver: Driver

    def __init__(self, timestamp: int, driver: Driver) -> None:
        """Initialize a DriverRequest event.

        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.
        """
        # Notify the monitor about the request.

        # Request a rider from the dispatcher.
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.

        # notify the monitor of the driver's request for a rider
        monitor.notify(self.timestamp, DRIVER, REQUEST, self.driver.id,
                       self.driver.location)

        events = []

        # find the rider for the driver
        rider = dispatcher.request_rider(self.driver)

        # if a rider is found, then find how long it takes for the driver to
        # get to rider's location and send a Pickup event with that timestamp
        if rider is not None:
            travel_time = self.driver.get_travel_time(rider.origin)
            self.driver.start_drive(rider.origin)
            events.append(
                Pickup(self.timestamp + travel_time, rider, self.driver))

        return events

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):
    """ A rider cancels their ride request

    ===ATTRIBUTES===
    rider: the rider who cancelled their ride request
    """

    rider: Rider

    def __init__(self, timestamp: int, rider: Rider) -> None:
        """ Make the Cancellation Event"""
        Event.__init__(self, timestamp)
        self.rider = rider

    def __str__(self) -> str:
        """ return a string of what happened in this event"""
        return "{} -- {}: Cancel ride".format(self.timestamp, self.rider)

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """ change the status of a waiting rider to a cancelled rider """
        events = []

        # only notify the monitor of the cancellation event if
        # the rider is not already satisfied
        if self.rider.status != SATISFIED:
            monitor.notify(self.timestamp, RIDER, CANCEL, self.rider.id,
                           self.rider.origin)
            self.rider.cancelled_ride()
            dispatcher.cancel_ride(self.rider)

        return events


class Pickup(Event):
    """ make a Pickup event

    ===ATTRIBUTES===
    rider: the rider who is being picked up
    driver: the driver who is picking up the rider
    """
    rider: Rider
    driver: Driver

    def __init__(self, timestamp: int, rider: Rider, driver: Driver) -> None:
        """ initialize a pickup event"""
        Event.__init__(self, timestamp)
        self.rider = rider
        self.driver = driver

    def __str__(self) -> str:
        """ return a string of what is happening in the pickup event"""
        return "{} -- {}: Pickup {}".format(self.timestamp, self.driver,
                                            self.rider)

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """ perform the pickup event """
        events = []

        # notify monitor of rider's pickup
        monitor.notify(self.timestamp, RIDER, PICKUP, self.rider.id,
                       self.rider.origin)
        monitor.notify(self.timestamp, DRIVER, PICKUP, self.driver.id,
                       self.driver.destination)

        self.driver.end_drive()

        # if the rider is still waiting, the driver picks them up
        # and a drop-off event is scheduled making the rider satisfied
        if self.rider.status == WAITING:
            travel_time = self.driver.start_ride(self.rider)
            events.append(
                Dropoff(self.timestamp + travel_time, self.rider, self.driver))
            self.rider.satisfied()
        # if the rider canceled, then the driver requests a rider
        elif self.rider.status == CANCELLED:
            events.append(DriverRequest(self.timestamp, self.driver))
            self.driver.destination = None
            self.driver.is_idle = True

        return events


class Dropoff(Event):
    """ event of the driver dropping off the rider at their destination

    ===ATTRIBUTES===
    rider: the rider being dropped off
    driver: the driver who is dropping off rider
    """

    rider: Rider
    driver: Driver

    def __init__(self, timestamp: int, rider: Rider, driver: Driver) -> None:
        """ initialize a drop off event"""
        Event.__init__(self, timestamp)
        self.rider = rider
        self.driver = driver

    def __str__(self) -> str:
        """ give a string of what is happening in the drop off event"""
        return "{} -- {}: Drop-off {}".format(self.timestamp, self.driver,
                                              self.rider)

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """ perform the drop off event"""

        events = []

        self.driver.end_ride()

        monitor.notify(self.timestamp, RIDER, DROPOFF, self.rider.id,
                       self.rider.destination)
        monitor.notify(self.timestamp, DRIVER, DROPOFF, self.driver.id,
                       self.driver.location)

        events.append(DriverRequest(self.timestamp, self.driver))

        return events


def create_event_list(filename: str) -> List[Event]:
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    filename: The name of a file that contains the list of events.
    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]

            event = None
            # HINT: Use Location.deserialize to convert the location string to
            # a location.

            if event_type == "DriverRequest":
                # Create a DriverRequest event.
                driver_id = tokens[2]
                starting_location = deserialize_location(tokens[3])
                speed = int(tokens[4])

                event = DriverRequest(timestamp,
                                      Driver(driver_id, starting_location,
                                             speed))

            elif event_type == "RiderRequest":
                # Create a RiderRequest event.
                rider_id = tokens[2]
                origin = deserialize_location(tokens[3])
                destination = deserialize_location(tokens[4])
                patience = int(tokens[5])

                event = RiderRequest(timestamp,
                                     Rider(rider_id, patience, origin,
                                           destination))

            events.append(event)

    return events


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(
        config={
            'allowed-io': ['create_event_list'],
            'extra-imports': ['rider', 'dispatcher', 'driver',
                              'location', 'monitor']})
