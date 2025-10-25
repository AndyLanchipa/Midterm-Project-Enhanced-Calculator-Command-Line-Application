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


class LoggingObserver(Observer):
    """Observer that logs calculations to a file."""
    
    def __init__(self, logger):
        """Initialize with a logger instance."""
        from app.logger import CalculatorLogger
        self.logger = logger
    
    def update(self, calculation: Calculation) -> None:
        """Log the calculation when notified."""
        self.logger.log_calculation(calculation)
    
    def get_observer_name(self) -> str:
        """Get observer name."""
        return "LoggingObserver"


class AutoSaveObserver(Observer):
    """Observer that automatically saves calculation history to CSV."""
    
    def __init__(self, history_manager):
        """Initialize with a history manager instance."""
        from app.history import CalculationHistory
        self.history_manager = history_manager
    
    def update(self, calculation: Calculation) -> None:
        """Auto-save history when a calculation is performed."""
        try:
            self.history_manager.save_to_csv()
        except Exception as e:
            # Don't raise exception to avoid interrupting calculation flow
            print(f"Auto-save failed: {str(e)}")
    
    def get_observer_name(self) -> str:
        """Get observer name."""
        return "AutoSaveObserver"


class CalculationEvent:
    """Event class for calculation notifications."""
    
    def __init__(self, calculation: Calculation, event_type: str = "calculation_performed"):
        """Initialize calculation event."""
        self.calculation = calculation
        self.event_type = event_type
        self.timestamp = calculation.timestamp
    
    def __str__(self) -> str:
        """String representation of the event."""
        return f"{self.event_type}: {self.calculation}"
