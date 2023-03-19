"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for users"""
    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser1 = User.signup(username="testuser1",
                                    email="test1@test.com",
                                    password="testuser1",
                                    image_url=None)
        
        self.testuser2 = User.signup(username="testuser2",
                                    email="test2@test.com",
                                    password="testuser2",
                                    image_url=None)
        

        db.session.commit()

        self.testuser1.followers.append(self.testuser2)

        db.session.commit()

    def tearDown(self):
        """Clean up and fouled transaction"""

        db.session.rollback()

    def test_list_users(self):
        """Does this view show users"""

        resp = self.client.get("/users")
        
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('testuser1', html)

    def test_show_user_profile(self):

        resp = self.client.get(f"/users/{self.testuser1.id}")
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('testuser1', html)
        
    def test_show_following(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

            resp = c.get(f"/users/{self.testuser1.id}/following")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testuser1', html)

    def test_show_followers(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

            resp = c.get(f"/users/{self.testuser1.id}/followers")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testuser2', html)

    def test_follow_other_user(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

            user2 = User.query.filter(User.username =='testuser2')

            resp = c.post(f"/users/follow/{user2.id}")
            # html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)









    

