"""Test runner."""
import app
import constants
import multiprocessing
import unittest
from tests import auth
from tests import stuff
from tests import user

# name -> module
TEST_MODULES = {
    'auth': auth,
    'stuff': stuff,
    'user': user
}


def load_tests(loader, tests, pattern):
    """Load tests from test modules."""
    suite = unittest.TestSuite()
    for module in TEST_MODULES:
        suite.addTests(loader.loadTestsFromModule(TEST_MODULES.get(module)))
    return suite


@app.app.route(f'{constants.API_ROOT}/test')
def runTests():
    """Execute all tests in a seperate process."""
    multiprocessing.Process(target=unittest.main).start()
    return 'Check the console for test results.', 200


if __name__ == '__main__':
    app.app.run()
