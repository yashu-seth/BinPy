from __future__ import division
"""
Contains
========

* Connector
* Bus
* make_bus

"""


class Connector:

    """
    This class is the primary medium for data transfer. Objects of this
    class can be connected to any digital object.

    Example
    =======

    >>> from BinPy import *
    >>> conn = Connector(1)  #Initializing connector with initial state = 1
    >>> conn.state
    1
    >>> gate = OR(0, 1)
    >>> conn.tap(gate, 'output')  #Tapping the connector

    Methods
    =======

    * tap
    * untap
    * isInputof
    * isOutputof
    * trigger
    """

    def __init__(self, state=None):
        self.connections = {"output": [], "input": []}
        # To store the all the taps onto this connection
        self.state = state  # To store the state of the connection
        self.oldstate = None

    def tap(self, element, mode):
        # Can't serve output for multiple devices
        if mode == "output":
            self.connections["output"] = []

        if element not in self.connections[mode]:
            self.connections[mode].append(
                element)  # Add an element to the connections list

    def untap(self, element, mode):
        if element in self.connections[mode]:
            self.connections[mode].remove(
                element)  # Delete an element from the connections list
        else:
            raise Exception(
                "ERROR:Connector is not the %s of the passed element" %
                mode)

    def isInputof(self, element):
        return element in self.connections["input"]

    def isOutputof(self, element):
        return element in self.connections["output"]

    # This function is called when the value of the connection changes
    def trigger(self):
        for i in self.connections["input"]:
            i.trigger()

    def __call__(self):
        return self.state

    # Overloads the bool method
    # For python3
    def __bool__(self):
        return True if self.state == 1 else False

    # To be compatible with Python 2.x
    __nonzero__ = __bool__

    # Overloads the int() method
    def __int__(self):
        return 1 if self.state == 1 else 0

    def __float__(self):
        return float(self.state)

    def __repr__(self):
        return str(self.state)

    def __str__(self):
        return "Connector; State: " + str(self.state)

    def __add__(self, other):
        return self.state + other.state

    def __sub__(self, other):
        return self.state - other.state

    def __mul__(self, other):
        return self.state * other.state

    def __truediv__(self, other):
        return self.state / other.state


class Bus:

    """
    This class provides an array of Connector Objects. Objects of this class can be
    used in situations where a lot of connectors are needed
    """

    def __init__(self, width=4, from_connectors=False, *connectors):
        if width <= 0:
            raise Exception("ERROR: Enter non-negative width")

        self.bus = list()
        self._width = width
        if not from_connectors:
            for i in range(width):
                temp = Connector()
                self.bus.append(temp)
        else:
            self._width = len(connectors)
            for i in connectors:
                self.bus.append(i)

    def get_state(self, index):
        if index > 0 and index < self._width:
            return self.bus[index].state
        raise Exception("ERROR: Invalid Index value")

    def set_width(self, width=None):
        if width <= 0:
            raise Exception("ERROR: Enter positive width")
        if width == self.width:
            return
        elif width < self.width:
            self.bus = self.bus[:width]
        elif width > self.width:
            for i in range(width - self._width):
                temp = Connector()
                self.bus.append(temp)
        self._width = width

    def tap(self, index, element, mode):
        if index < 0 or index > self._width:
            raise Exception("ERROR: Invalid Index Value")
        self.bus[index].tap(element, mode)

    def untap(self, index, element, mode):
        if index < 0 or index > self._width:
            raise Exception("ERROR: Invalid Index Value")
        self.bus[index].untap(element, mode)

    def __repr__(self):
        return str(self.bus)

    @property
    def width(self):
        """
        Gives width of the Bus
        """
        return self._width


def make_bus(*connectors):
    """
    This function converts a set of connectors to a Bus
    """
    return Bus(from_connectors=True, *connectors)
