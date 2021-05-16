"""API test runner.

Runs a real Flask app instance to connect to the database.
"""
import app
import config
import multiprocessing
import unittest
from tests import auth_test
from tests import stuff_test
from tests import user_test


def load_tests(loader, tests, pattern):
    """Load tests from test modules."""
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(auth_test))
    suite.addTests(loader.loadTestsFromModule(stuff_test))
    suite.addTests(loader.loadTestsFromModule(user_test))
    return suite


if __name__ == '__main__':
    with app.app.app_context():
        unittest.main()
