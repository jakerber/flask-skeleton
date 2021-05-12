"""Test runner."""
import argparse
import unittest
from tests import auth
from tests import item
from tests import user

parser = argparse.ArgumentParser(description='Test runner')
parser.add_argument('--name', type=str, default=None, help='Name of test module to run')
args = parser.parse_args()

# name -> module
TEST_MODULES = {
    'auth': auth,
    'item': item,
    'user': user
}

def load_tests(loader, tests, pattern):
    """Load tests from test modules."""
    suite = unittest.TestSuite()
    if args.name:
        testModule = TEST_MODULES.get(args.name)
        if not testModule:
            raise ValueError(f'test module {args.name} not found')
        suite.addTests(loader.loadTestsFromModule(TEST_MODULES.get()))
    else:
        suite.addTests(loader.loadTestsFromModule(auth))
        suite.addTests(loader.loadTestsFromModule(item))
        suite.addTests(loader.loadTestsFromModule(user))
    return suite

if __name__ == '__main__':
    unittest.main()
