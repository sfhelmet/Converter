from abc import ABC, abstractmethod

class StateInterface(ABC):
    @property
    @abstractmethod
    def name(self):
        """Get the name of the state."""
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        """Set the name of the state."""
        pass

    @property
    @abstractmethod
    def superstate(self):
        """Get the superstate of the state."""
        pass

    @superstate.setter
    @abstractmethod
    def superstate(self, value):
        """Set the superstate of the state."""
        pass