"""API test runner.

Runs a real Flask app instance to connect to the database.
"""
import app
import config
import multiprocessing
import unittest
from tests import admin_endpoints_test
from tests import auth_endpoints_test
from tests import stuff_endpoints_test
from tests import user_endpoints_test


def load_tests(loader, tests, pattern):
    """Load tests from test modules."""
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(admin_endpoints_test))
    suite.addTests(loader.loadTestsFromModule(auth_endpoints_test))
    suite.addTests(loader.loadTestsFromModule(stuff_endpoints_test))
    suite.addTests(loader.loadTestsFromModule(user_endpoints_test))
    return suite


if __name__ == '__main__':
    with app.app.app_context():
        unittest.main()
