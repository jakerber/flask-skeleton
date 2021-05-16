"""Database operations."""
import flask_sqlalchemy
import errors

# Global database instance
DB = flask_sqlalchemy.SQLAlchemy()


def save(entry):
    """Save entry to the database.

    :param entry [BaseModel]: database entry model
    :returns [BaseModel]: the entry
    :raises DatabaseError: if unable to save entry
    """
    DB.session.add(entry)
    try:
        DB.session.commit()
    except Exception as error:
        raise errors.DatabaseError(f'unable to save entry: {str(error)}')
    return entry


def delete(entry):
    """Delete entry from the database.

    :param entry [BaseModel]: database entry model
    :raises DatabaseError: if unable to save entry
    """
    DB.session.delete(entry)
    try:
        DB.session.commit()
    except Exception as error:
        raise errors.DatabaseError(f'unable to save entry: {str(error)}')
