"""Common API test library."""
import unittest
import database

DATABASE_MODELS = [
    database.AuthTokenBlacklist,
    database.Stuff,
    database.User
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

    def setUp(self):
        """Get database in ready state.

        Removes all data from database and insert objects outlined in
        self._DATABASE_READY_STATE.
        """
        # remove all data from database
        for model in DATABASE_MODELS:
            for entry in model.query.all():
                entry.delete()

        # insert objects outlined in self._DATABASE_READY_STATE
        for model in self._DATABASE_READY_STATE:
            if not hasattr(database, model):
                raise ValueError(f'database model {model} does not exist')
            for entry in self._DATABASE_READY_STATE.get(model):
                newEntry = getattr(database, model)(**entry)
                newEntry.save()
