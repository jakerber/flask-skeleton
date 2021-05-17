"""Database operations."""
import flask_sqlalchemy
import errors

# Global database instance
DB = flask_sqlalchemy.SQLAlchemy()


def delete(entry, commit=True):
    """Delete entry from the database.

    :param entry [BaseModel]: database entry model
    :param commit [bool]: immediately commit the operation
    """
    DB.session.delete(entry)
    if commit:
        _commit()


def save(entry, commit=True):
    """Save entry to the database.

    :param entry [BaseModel]: database entry model
    :param commit [bool]: immediately commit the operation
    :returns [BaseModel]: the entry
    """
    DB.session.add(entry)
    if commit:
        _commit()
    return entry


def _commit():
    """Commit database transaction.

    :raises DatabaseError: if unable to commit
    """
    try:
        DB.session.commit()
    except Exception as error:
        raise errors.DatabaseError(f'{str(error)}')
