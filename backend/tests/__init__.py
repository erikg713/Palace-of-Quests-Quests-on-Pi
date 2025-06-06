"""
Initializes the test suite for the backend.

You can place global fixtures, environment setup, or logging configuration here.
"""

import pytest
import logging
import os

def setUpModule():
    """Set up any state specific to the execution of the test module."""
    # Example: configure logging for test output clarity
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    # Example: set up environment variables for tests
    os.environ.setdefault("TESTING", "1")
    logging.info("Test suite setup complete.")

def tearDownModule():
    """Tear down any state that was previously set up for the test module."""
    # Example: clean up environment variables or other global states
    os.environ.pop("TESTING", None)
    logging.info("Test suite teardown complete.")
