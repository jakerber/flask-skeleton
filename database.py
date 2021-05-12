"""Database operations."""
import datetime
import flask_sqlalchemy

# global SQLAlchemy database instance
DB = flask_sqlalchemy.SQLAlchemy()

"""
Data models.
"""

class BaseModel(DB.Model):
    """Base model for all database objects."""

    __abstract__ = True

    created_on = DB.Column(DB.DateTime, nullable=False, default=datetime.datetime.utcnow())

    def save(self):
        """Save to database."""
        DB.session.add(self)
        DB.session.commit()
        return self

    def delete(self):
        """Delete from database."""
        DB.session.delete(self)
        DB.session.commit()

class User(BaseModel):
    """User database object."""

    __tablename__ = 'users'

    id = DB.Column(DB.BigInteger, primary_key=True, autoincrement=True)
    phone = DB.Column(DB.BigInteger, unique=True, nullable=False)
    name = DB.Column(DB.Text, nullable=False)
    password = DB.Column(DB.Text, nullable=False)

    def dict(self):
        """JSON serializable representation of entry."""
        return {'id': self.id,
                'phone': self.phone,
                'name': self.name,
                'password': self.password,
                'created_on': self.created_on}

class Stuff(BaseModel):
    """Stuff database object."""

    __tablename__ = 'stuff'

    id = DB.Column(DB.BigInteger, primary_key=True, autoincrement=True)
    description = DB.Column(DB.Text, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(User.id))

    def dict(self):
        """JSON serializable representation of entry."""
        return {'id': self.id,
                'description': self.description,
                'owner': self.user_id,
                'created_on': self.created_on}
