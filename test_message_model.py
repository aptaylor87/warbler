"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


import os
from unittest import TestCase
from app import app, CURR_USER_KEY
from models import db, User, Message, Follows
from datetime import datetime

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

# Use test database and don't clutter tests with SQL
app.config['DATABASE_URL'] = "postgresql:///warbler-test"
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

class MessageModelTestCase(TestCase):
    """Test views for messages"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def teardown(self):
        """Clean up any fouled transaction"""

    def test_message_model(self):
        """Does the basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.messages), 0)

        message = Message(
            text = "Test text",
            timestamp = datetime.utcnow(),
            user_id = u.id
        )

        db.session.add(message)
        db.session.commit()

        messages = Message.query.all()

        self.assertEqual(len(messages), 1)


    def test_message_user(self):

        """Does the basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.messages), 0)

        message = Message(
            text = "Test text",
            timestamp = datetime.utcnow(),
            user_id = u.id
        )

        db.session.add(message)
        db.session.commit()

        self.assertEqual(message.user, u)



