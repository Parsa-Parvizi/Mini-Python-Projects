import unittest
import os
from logger import Logger


class TestLoggerDecorator(unittest.TestCase):
    # Test case to check if logging is enabled and logs are written to a file
    def test_logger_enabled_to_file(self):
        # Define the log file name
        log_file = "test_log.log"

        # Decorate the sample_function with Logger, enabling logging and setting log file
        @Logger(enabled=True, log_to_file=True, filename=log_file)
        def sample_function():
            # Sample function that returns "OK"
            return "OK"

        # Call the sample_function and store the result
        result = sample_function()
        # Assert that the result is "OK"
        self.assertEqual(result, "OK")
        # Assert that the log file exists
        self.assertTrue(os.path.exists(log_file))

        # Open the log file in read mode
        with open(log_file, "r") as f:
            # Read the content of the log file
            log_content = f.read()
            # Assert that the log contains the start message of the function
            self.assertIn("Started 'sample_function'", log_content)
            # Assert that the log contains the finish message of the function
            self.assertIn("Finished 'sample_function'", log_content)

        # Remove the log file after the test
        os.remove(log_file)

    # Test case to check if logging is disabled
    def test_logger_disabled(self):
        # Decorate the silent_func with Logger, disabling logging
        @Logger(enabled=False)
        def silent_func():
            # Sample function that returns 123
            return 123

        # Call the silent_func and assert that the result is 123
        self.assertEqual(silent_func(), 123)


if __name__ == "__main__":
    unittest.main()
