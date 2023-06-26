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


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_add_message(self):
        """Can use add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")
    def FollowPages(self):
        """Can see if your following page is logged in"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                resp = c.get("/users/1/following")

                self.assertEqual(resp.status_code, 200)
                self.assert_template_used('user/following.html')

    def followPagesLoggedOut(self):
        """Can't see following page is logged out"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = None
                resp = c.get("/users/1/following")

                self.assertEqual(resp.status_code, 302)
                self.assertTrue(resp.search('Access unauthorized',
                    resp.get_data(as_text=True)))
                
    def addMessageNoLogged(self):
        """Can't post a message if you're not logged in"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = None
                resp = c.post("/messages/new", data={"text": "Hello"})
                self.assertEqual(resp.status_code, 302)
                self.assertTrue(resp.search('Access unauthorized',
                    resp.get_data(as_text=True)))
                
    def deleteMessage(self):
        """Delete a messsage"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.post("/messages/1/delete", data={"text": "Hello"})

            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg, [])

    def addMessageNoLogged(self):
        """Can't delete a message if you're not logged in"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = None
                resp = c.post("/messages/1/delete", data={"text": "Hello"})
                self.assertEqual(resp.status_code, 302)
                self.assertTrue(resp.search('Access unauthorized',
                    resp.get_data(as_text=True)))
                
    def addSomeOtherUserMessage(self):
        """Can't add a message to someone's else account"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                resp = c.post("/messages/new", data={"text": "Hello", "user_id": 2})
                self.assertEqual(resp.status_code, 302)
                self.assertTrue(resp.search('Access unauthorized',
                    resp.get_data(as_text=True)))
                
    def deleteSomeOtherUserMessage(self):
        """Can't delete another user's message"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                resp = c.post("/messages/1/delete", data={"text": "Hello", "user_id": 2})
                self.assertEqual(resp.status_code, 302)
                self.assertTrue(resp.search('Access unauthorized',
                    resp.get_data(as_text=True)))

