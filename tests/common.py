"""Common test module."""
import app

class APITestBase(unittest.TestCase):
    """Base class for API endpoint testing."""

    def setUp(self):
        """Put database in test-ready state."""
        NotImplementedError
