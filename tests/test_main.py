"""Test cases for main application entry point."""

import pytest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO


class TestMainApplication:
    """Test main application functionality."""
    
    @patch('main.CalculatorConfig')
    @patch('sys.stdout', new_callable=StringIO)
    def test_setup_environment_success(self, mock_stdout, mock_config_class):
        """Test successful environment setup."""
        # Mock config instance
        mock_config = MagicMock()
        mock_config.log_dir.mkdir = MagicMock()
        mock_config.history_dir.mkdir = MagicMock()
        mock_config.log_dir.__str__ = MagicMock(return_value="logs")
        mock_config.history_dir.__str__ = MagicMock(return_value="history")
        mock_config_class.return_value = mock_config
        
        # Import and test setup_environment
        from main import setup_environment
        result = setup_environment()
        
        assert result == True
        output = mock_stdout.getvalue()
        assert "Environment setup complete" in output
    
    @patch('main.CalculatorConfig')
    @patch('sys.stdout', new_callable=StringIO)
    def test_setup_environment_config_error(self, mock_stdout, mock_config_class):
        """Test environment setup with configuration error."""
        from app.exceptions import ConfigurationError
        
        # Mock config to raise ConfigurationError
        mock_config_class.side_effect = ConfigurationError("Test config error")
        
        # Import and test setup_environment
        from main import setup_environment
        result = setup_environment()
        
        assert result == False
        output = mock_stdout.getvalue()
        assert "Configuration error" in output
    
    @patch('main.CalculatorConfig')
    @patch('sys.stdout', new_callable=StringIO)
    def test_setup_environment_general_error(self, mock_stdout, mock_config_class):
        """Test environment setup with general error."""
        # Mock config to raise general Exception
        mock_config_class.side_effect = Exception("Test general error")
        
        # Import and test setup_environment
        from main import setup_environment
        result = setup_environment()
        
        assert result == False
        output = mock_stdout.getvalue()
        assert "Setup error" in output
    
    @patch('main.repl_main')
    @patch('main.setup_environment', return_value=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_success(self, mock_stdout, mock_setup, mock_repl):
        """Test successful main execution."""
        from main import main
        
        main()
        
        mock_setup.assert_called_once()
        mock_repl.assert_called_once()
        output = mock_stdout.getvalue()
        assert "Starting Advanced Calculator" in output
        assert "Thank you for using" in output
    
    @patch('main.setup_environment', return_value=False)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_setup_failure(self, mock_stdout, mock_setup):
        """Test main execution with setup failure."""
        from main import main
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
        output = mock_stdout.getvalue()
        assert "Failed to setup environment" in output
    
    @patch('main.repl_main')
    @patch('main.setup_environment', return_value=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_keyboard_interrupt(self, mock_stdout, mock_setup, mock_repl):
        """Test main execution with keyboard interrupt."""
        mock_repl.side_effect = KeyboardInterrupt()
        
        from main import main
        main()
        
        output = mock_stdout.getvalue()
        assert "terminated by user" in output
    
    @patch('main.repl_main')
    @patch('main.setup_environment', return_value=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_general_exception(self, mock_stdout, mock_setup, mock_repl):
        """Test main execution with general exception."""
        mock_repl.side_effect = Exception("Test exception")
        
        from main import main
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
        output = mock_stdout.getvalue()
        assert "Application error" in output
