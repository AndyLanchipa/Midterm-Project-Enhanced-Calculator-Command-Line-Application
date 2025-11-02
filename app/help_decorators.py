"""Dynamic help menu system using Decorator Design Pattern."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Callable
from functools import wraps
from app.operations import OperationFactory

# Make colorama optional
try:
    import colorama
    from colorama import Fore, Style, Back
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


class HelpSection(ABC):
    """Abstract base class for help sections."""
    
    @abstractmethod
    def generate_content(self) -> str:
        """Generate help content for this section."""
        pass
    
    @abstractmethod
    def get_section_name(self) -> str:
        """Get the name of this help section."""
        pass


class OperationsHelpSection(HelpSection):
    """Help section for available operations."""
    
    def generate_content(self) -> str:
        """Generate operations help content dynamically."""
        content = []
        content.append(f"{Fore.CYAN}🔢 Arithmetic Operations:{Style.RESET_ALL}")
        
        # Get operations dynamically from factory
        operations = OperationFactory.get_available_operations()
        
        for op_name in sorted(operations):
            try:
                operation = OperationFactory.create_operation(op_name)
                symbol = operation.symbol
                description = operation.description
                content.append(f"  {Fore.GREEN}{op_name:<12}{Style.RESET_ALL} ({symbol:<3}) - {description}")
            except Exception:
                # Fallback if operation can't be created
                content.append(f"  {Fore.GREEN}{op_name:<12}{Style.RESET_ALL} - Perform {op_name} operation")
        
        return "\n".join(content)
    
    def get_section_name(self) -> str:
        return "operations"


class HistoryHelpSection(HelpSection):
    """Help section for history commands."""
    
    def generate_content(self) -> str:
        """Generate history help content."""
        content = []
        content.append(f"{Fore.YELLOW}📚 History Commands:{Style.RESET_ALL}")
        
        commands = [
            ("history", "Show calculation history"),
            ("clear", "Clear calculation history"),
            ("undo", "Undo last calculation"),
            ("redo", "Redo last undone calculation"),
        ]
        
        for cmd, desc in commands:
            content.append(f"  {Fore.GREEN}{cmd:<15}{Style.RESET_ALL} - {desc}")
        
        return "\n".join(content)
    
    def get_section_name(self) -> str:
        return "history"


class FileHelpSection(HelpSection):
    """Help section for file operations."""
    
    def generate_content(self) -> str:
        """Generate file operations help content."""
        content = []
        content.append(f"{Fore.MAGENTA}💾 File Operations:{Style.RESET_ALL}")
        
        commands = [
            ("save [filename]", "Save history to CSV file"),
            ("load [filename]", "Load history from CSV file"),
        ]
        
        for cmd, desc in commands:
            content.append(f"  {Fore.GREEN}{cmd:<15}{Style.RESET_ALL} - {desc}")
        
        return "\n".join(content)
    
    def get_section_name(self) -> str:
        return "file"


class SystemHelpSection(HelpSection):
    """Help section for system commands."""
    
    def generate_content(self) -> str:
        """Generate system commands help content."""
        content = []
        content.append(f"{Fore.BLUE}🔧 System Commands:{Style.RESET_ALL}")
        
        commands = [
            ("info", "Show calculator information"),
            ("help", "Show this help message"),
            ("help <section>", "Show help for specific section"),
            ("exit/quit", "Exit the calculator"),
        ]
        
        for cmd, desc in commands:
            content.append(f"  {Fore.GREEN}{cmd:<15}{Style.RESET_ALL} - {desc}")
        
        return "\n".join(content)
    
    def get_section_name(self) -> str:
        return "system"


class HelpMenuDecorator:
    """Decorator for enhancing help menu functionality."""
    
    def __init__(self):
        """Initialize help menu decorator."""
        colorama.init()  # Initialize colorama for cross-platform color support
        self.sections: Dict[str, HelpSection] = {}
        self._register_default_sections()
    
    def _register_default_sections(self) -> None:
        """Register default help sections."""
        self.register_section(OperationsHelpSection())
        self.register_section(HistoryHelpSection())
        self.register_section(FileHelpSection())
        self.register_section(SystemHelpSection())
    
    def register_section(self, section: HelpSection) -> None:
        """Register a new help section."""
        self.sections[section.get_section_name()] = section
    
    def unregister_section(self, section_name: str) -> None:
        """Unregister a help section."""
        if section_name in self.sections:
            del self.sections[section_name]
    
    def generate_full_help(self) -> str:
        """Generate complete help menu."""
        content = []
        
        # Header
        content.append(f"\n{Back.BLUE}{Fore.WHITE}📖 Advanced Calculator Help Menu{Style.RESET_ALL}\n")
        
        # Generate each section
        for section_name in ["operations", "history", "file", "system"]:
            if section_name in self.sections:
                content.append(self.sections[section_name].generate_content())
                content.append("")  # Add spacing between sections
        
        # Footer with examples
        content.append(f"{Fore.CYAN}💡 Usage Examples:{Style.RESET_ALL}")
        content.append(f"  {Fore.YELLOW}add 5 3{Style.RESET_ALL}        - Calculate 5 + 3")
        content.append(f"  {Fore.YELLOW}power 2 8{Style.RESET_ALL}      - Calculate 2^8")
        content.append(f"  {Fore.YELLOW}help operations{Style.RESET_ALL} - Show only operations help")
        
        return "\n".join(content)
    
    def generate_section_help(self, section_name: str) -> str:
        """Generate help for a specific section."""
        if section_name not in self.sections:
            available = ", ".join(self.sections.keys())
            return f"{Fore.RED}❌ Unknown help section: {section_name}{Style.RESET_ALL}\nAvailable sections: {available}"
        
        content = []
        content.append(f"\n{Back.BLUE}{Fore.WHITE}📖 Help: {section_name.title()}{Style.RESET_ALL}\n")
        content.append(self.sections[section_name].generate_content())
        
        return "\n".join(content)
    
    def get_available_sections(self) -> List[str]:
        """Get list of available help sections."""
        return list(self.sections.keys())


def dynamic_help_decorator(func: Callable) -> Callable:
    """Decorator function to enhance help functionality."""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the instance (self) from args
        if args and hasattr(args[0], '_help_decorator'):
            instance = args[0]
            help_decorator = instance._help_decorator
            
            # If this is a help command, use dynamic help
            if len(args) > 1 and args[1].strip().startswith('help'):
                parts = args[1].strip().split()
                
                if len(parts) == 1:
                    # Show full help
                    print(help_decorator.generate_full_help())
                    return
                elif len(parts) == 2:
                    # Show section-specific help
                    section_name = parts[1].lower()
                    print(help_decorator.generate_section_help(section_name))
                    return
        
        # For non-help commands, execute normally
        return func(*args, **kwargs)
    
    return wrapper


class DynamicHelpMixin:
    """Mixin class to add dynamic help functionality."""
    
    def __init__(self):
        """Initialize dynamic help functionality."""
        self._help_decorator = HelpMenuDecorator()
    
    def get_dynamic_help(self, section: str = None) -> str:
        """Get dynamic help content."""
        if section:
            return self._help_decorator.generate_section_help(section)
        else:
            return self._help_decorator.generate_full_help()
    
    def register_help_section(self, section: HelpSection) -> None:
        """Register a custom help section."""
        self._help_decorator.register_section(section)
