#!/usr/bin/env python3
"""
Advanced Calculator Application
Main entry point for the calculator with dynamic help system.
"""

import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

from app.repl import main as repl_main
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def setup_environment():
    """Set up the application environment."""
    try:
        # Initialize configuration to create necessary directories
        config = CalculatorConfig()
        
        # Ensure directories exist
        config.log_dir.mkdir(exist_ok=True)
        config.history_dir.mkdir(exist_ok=True)
        
        print(f"✅ Environment setup complete")
        print(f"📁 Log directory: {config.log_dir}")
        print(f"📁 History directory: {config.history_dir}")
        
        return True
        
    except ConfigurationError as e:
        print(f"❌ Configuration error: {e}")
        return False
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False


def main():
    """Main application entry point."""
    print("🚀 Starting Advanced Calculator Application...")
    print("=" * 50)
    
    # Setup environment
    if not setup_environment():
        print("❌ Failed to setup environment. Exiting.")
        sys.exit(1)
    
    print("🔧 All systems ready!")
    print("=" * 50)
    
    try:
        # Start the REPL interface
        repl_main()
        
    except KeyboardInterrupt:
        print("\n👋 Calculator application terminated by user.")
    except Exception as e:
        print(f"❌ Application error: {e}")
        sys.exit(1)
    
    print("👋 Thank you for using Advanced Calculator!")


if __name__ == "__main__":
    main()
