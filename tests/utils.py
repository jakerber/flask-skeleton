"""API testing utility library."""
import unittest
from db import models

# Will be cleared before each test
DATABASE_MODELS = [
    models.AuthTokenBlacklist,
    models.Stuff,
    models.User
]


class APITestBase(unittest.TestCase):
    """Base class for API integration tests."""

    # Model name -> list of database entries to add
    _DATABASE_READY_STATE = {
        'User': [
            {
                'id': 1,
                'phone': 1111111111,
                'name': 'josh',
                'password': '1a0a41d838bbff454688436ff593508dab2c55722bae0f32d6ba50975a6a46a3',
            }
        ],
        'Stuff': [
            {
                'id': 1,
                'description': 'stuff-josh-owns',
                'user_id': 1,
            }
        ]
    }

    @classmethod
    def tearDownClass(cls):
        """Clear database after tests are executed."""
        cls.clearDatabase()

    @classmethod
    def clearDatabase(cls):
        """Remove all data from the database."""
        for model in DATABASE_MODELS:
            for entry in model.query.all():
                entry.delete()

    def setUp(self):
        """Get database in ready state.

        Removes all data from database and insert objects outlined in
        self._DATABASE_READY_STATE.
        """
        self.clearDatabase()

        # Insert objects outlined in self._DATABASE_READY_STATE
        for model in self._DATABASE_READY_STATE:
            if not hasattr(models, model):
                raise RuntimeError(f'database model {model} does not exist')
            for entry in self._DATABASE_READY_STATE.get(model):
                newEntry = getattr(models, model)(**entry)
                newEntry.save()
