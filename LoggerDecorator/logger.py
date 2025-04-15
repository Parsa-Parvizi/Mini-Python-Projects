import time
import functools
import logging

class Logger:
    def __init__(self, enabled=True, log_to_file=False, filename="function_logs.log"):

        # Initialize the Logger with optional parameters
        self.enabled = enabled  # Whether logging is enabled
        self.log_to_file = log_to_file  # Whether to log to a file
        self.filename = filename  # The filename for the log file
        self._setup_logger()  # Set up the logger

    def _setup_logger(self):

        # Set up the logger configuration
        self.logger = logging.getLogger("FunctionLogger")  # Create a logger with a specific name
        self.logger.setLevel(logging.INFO)  # Set the logging level to INFO
        self.logger.propagate = False  # Prevent the log messages from being propagated to the root logger

        if self.logger.handlers:
            self.logger.handlers.clear()  # Clear any existing handlers to avoid duplicate logging

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',  # Define the log message format
            datefmt='%Y-%m-%d %H:%M:%S'  # Define the date format
        )

        # Choose the handler based on whether logging to a file is enabled
        handler = logging.FileHandler(self.filename) if self.log_to_file else logging.StreamHandler()
        handler.setFormatter(formatter)  # Set the formatter for the handler
        self.logger.addHandler(handler)  # Add the handler to the logger

    def __call__(self, func):
        """Makes the Logger instance callable, allowing it to be used as a decorator."""
        # Make the Logger instance callable to be used as a decorator
        @functools.wraps(func)  # Preserve the original function's metadata
        def wrapper(*args, **kwargs):
            """ wrapper function that logs the start and end times of the decorated function."""
            if not self.enabled:
                return func(*args, **kwargs)  # If logging is disabled, call the original function directly

            start_time = time.time()  # Record the start time
            self.logger.info(f"Started '{func.__name__}'")  # Log the start of the function

            result = func(*args, **kwargs)  # Call the original function

            end_time = time.time()  # Record the end time
            duration = end_time - start_time
            self.logger.info(f"Finished '{func.__name__}' in {duration:.4f} seconds")

            return result

        return wrapper
