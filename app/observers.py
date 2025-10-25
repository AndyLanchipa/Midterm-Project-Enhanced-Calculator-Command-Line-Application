"""Observer pattern implementation for calculator events."""

from abc import ABC, abstractmethod
from typing import List, Any
from app.calculation import Calculation


class Observer(ABC):
    """Abstract base class for observers."""
    
    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """Update method called when a calculation is performed."""
        pass
    
    @abstractmethod
    def get_observer_name(self) -> str:
        """Get the name of this observer."""
        pass


class Subject:
    """Subject class that maintains a list of observers."""
    
    def __init__(self):
        """Initialize subject with empty observer list."""
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """Attach an observer to the subject."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer from the subject."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, calculation: Calculation) -> None:
        """Notify all observers of a calculation."""
        for observer in self._observers:
            try:
                observer.update(calculation)
            except Exception as e:
                # Log error but don't stop other observers
                print(f"Error in observer {observer.get_observer_name()}: {str(e)}")
    
    def get_observer_count(self) -> int:
        """Get the number of attached observers."""
        return len(self._observers)
    
    def get_observer_names(self) -> List[str]:
        """Get names of all attached observers."""
        return [observer.get_observer_name() for observer in self._observers]
    
    def clear_observers(self) -> None:
        """Remove all observers."""
        self._observers.clear()
