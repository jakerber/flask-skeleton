"""Test runner."""
import argparse
import constants
import sys
import unittest
from tests import auth
from tests import stuff
from tests import user

# name -> module
TEST_MODULES = {
    'auth': auth,
    'item': stuff,
    'user': user
}

parser = argparse.ArgumentParser(description='API test runner.')
parser.add_argument('--name', type=str, default=None, action='store',
                    help='Name of test module to run')
args = parser.parse_args()


def load_tests(loader, tests, pattern):
    """Load tests from test modules."""
    suite = unittest.TestSuite()
    if args.name:
        testModule = TEST_MODULES.get(args.name)
        if not testModule:
            raise ValueError(f'test module {args.name} not found')
        suite.addTests(loader.loadTestsFromModule(TEST_MODULES.get(testModule)))
    else:
        for module in TEST_MODULES:
            suite.addTests(loader.loadTestsFromModule(TEST_MODULES.get(module)))
    return suite


if __name__ == '__main__':
    input('Warning: this will delete all data in test database '
          f'{constants.SQLALCHEMY_DATABASE_URI}. Press enter to continue.')
    unittest.main(argv=sys.argv[:1])
