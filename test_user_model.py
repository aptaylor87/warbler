"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from app import app, CURR_USER_KEY
from models import db, User, Message, Follows

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


class UserModelTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def teardown(self):
        """Clean up any fouled transaction"""

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr(self):
        """does __repr__ work"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        represenation = u.__repr__()

        self.assertIn('test@test.com',represenation)

    def test_is_following(self):
        """ test is_following method """

        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="BETTER_HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        self.assertEqual(u1.is_following(u2), False)
        self.assertEqual(u2.is_following(u1), False)

        u1.followers.append(u2)
        db.session.commit()

        self.assertEqual(u2.is_following(u1), True)
        self.assertEqual(u1.is_following(u2), False)

    def test_is_followed_by(self):

        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="BETTER_HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        self.assertEqual(u1.is_followed_by(u2), False)
        self.assertEqual(u2.is_followed_by(u1), False)

        u1.followers.append(u2)
        db.session.commit()

        self.assertEqual(u1.is_followed_by(u2), True)
        self.assertEqual(u2.is_followed_by(u1), False)


    def test_sign_up(self):
        u1 = User.signup(
            username="testuser1",
            email="test1@test.com",
            password="HASHED_PASSWORD",
            image_url="/static/images/default-pic.png"
        )

        self.assertNotIn("HASHED_PASSWORD", u1.password)
        self.assertIn("testuser1", u1.username)

        with self.assertRaises(Exception):
            User.signup(
                username="testuser1",
                password="HASHED_PASSWORD",
                image_url="/static/images/default-pic.png"
                )
            

    def test_authenticate(self):

        u1 = User.signup(
            username="testuser1",
            email="test1@test.com",
            password="HASHED_PASSWORD",
            image_url="/static/images/default-pic.png"
        )

        db.session.add(u1)
        db.session.commit()

        auth_user = User.authenticate("testuser1", "HASHED_PASSWORD")

        self.assertEqual(auth_user.username, "testuser1")
        self.assertNotEqual(auth_user.password, "HASHED_PASSWORD")

        bad_username = User.authenticate("bestuser1", "HASHED_PASSWORD")

        self.assertEqual(bad_username, False)

        bad_password = User.authenticate("testuser1", "MASHED_PASSWORD")

        self.assertEqual(bad_password, False)
