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

    phone = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.Text, nullable=False)
    password = DB.Column(DB.Text, nullable=False)

    def dict(self):
        """JSON serializable representation of entry."""
        return {'phone': self.phone, 'name': self.name, 'password': self.password, 'created_on': self.created_on}

class Item(BaseModel):
    """Item database object."""

    __tablename__ = 'items'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    value = DB.Column(DB.Text, nullable=False)
    owner = DB.Column(DB.BigInteger, DB.ForeignKey(User.phone))

    def dict(self):
        """JSON serializable representation of entry."""
        return {'id': self.id, 'value': self.value, 'owner': self.owner, 'created_on': self.created_on}
