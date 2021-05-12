"""Test runner."""
import app
import constants
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


@app.app.route(f'{constants.API_ROOT}/test')
def runTests():
    """Execute all tests in a seperate process."""
    multiprocessing.Process(target=unittest.main).start()
    return 'Check the console for test results.', 200


if __name__ == '__main__':
    app.app.run()
