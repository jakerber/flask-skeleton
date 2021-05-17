"""Database models."""
import datetime
import errors
from db import database

# Global SQLAlchemy database instance
DB = database.DB


class BaseModel(DB.Model):
    """Base model for all database objects."""

    __abstract__ = True

    created_on = DB.Column(DB.DateTime,
                           nullable=False,
                           default=datetime.datetime.utcnow())

    def save(self):
        """Save to database."""
        return database.save(self)

    def delete(self):
        """Delete from database."""
        database.delete(self)


class AuthTokenBlacklist(BaseModel):
    """Auth token blacklist database object."""

    __tablename__ = 'auth_token_blacklist'

    token = DB.Column(DB.Text, primary_key=True)

    def dict(self):
        """JSON serializable representation of entry."""
        return {'token': self.token,
                'created_on': self.created_on}


class User(BaseModel):
    """User database object."""

    __tablename__ = 'users'

    id = DB.Column(DB.BigInteger, primary_key=True, autoincrement=True)
    phone = DB.Column(DB.BigInteger, unique=True, nullable=False)
    name = DB.Column(DB.Text, nullable=False)
    password = DB.Column(DB.Text, nullable=False)
    is_admin = False  # dynamically set

    def dict(self):
        """JSON serializable representation of entry."""
        return {'id': self.id,
                'phone': self.phone,
                'name': self.name,
                'password': self.password,
                'created_on': self.created_on}


class Admin(BaseModel):
    """Admin database object."""

    __tablename__ = 'admins'

    id = DB.Column(DB.BigInteger, primary_key=True, autoincrement=True)
    user_id = DB.Column(DB.BigInteger,
                        DB.ForeignKey(User.id, ondelete='CASCADE'))

    def dict(self):
        """JSON serializable representation of entry."""
        return {'id': self.id,
                'user_id': self.user_id,
                'created_on': self.created_on}


class Stuff(BaseModel):
    """Stuff database object."""

    __tablename__ = 'stuff'

    id = DB.Column(DB.BigInteger, primary_key=True, autoincrement=True)
    description = DB.Column(DB.Text, nullable=False)
    user_id = DB.Column(DB.BigInteger,
                        DB.ForeignKey(User.id, ondelete='CASCADE'))

    def dict(self):
        """JSON serializable representation of entry."""
        return {'id': self.id,
                'description': self.description,
                'owner': self.user_id,
                'created_on': self.created_on}
