"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

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

    def isFollowing(self):
        """Test to see if User1 is following User2"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        

        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        u.following.append(u2)

        following = u.is_following(self, u2)

        self.assertEqual(following, 1)

    def isNotFollowing(self):
        """Test to see if User1 is not following User2"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        following = u.is_following(self, u2)
        self.assertEqual(following, 0)

    def isFollowedBy(self):
        """To see if user1 is followed by user2"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        u.following.append(u2)
        followed_by = u2.is_followed_by(self,u)
        self.assertEqual(followed_by, 1)

    def isNotFollowedBy(self):
        """To see if user1 is not followed user2"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        followed_by = u2.is_followed_by(self,u)
        self.assertEqual(followed_by, 0)

    def newUser(self):
        """To see if the signup works successfully"""
        u = User.signup("testuser", "testuser@gmail.com", "password", "image.com")
        self.assertEqual(u, User)

    def noNewUser(self):
        """Won't signup if it isn't used properly"""
        u = User.signup("aw09djwad")
        self.assertNotEqual(u, User)

    def testAuthenticate(self):
        u = User.signup("testuser", "testuser@gmail.com", "password", "image.com")
        db.session.add(u)
        db.sesison.commit()
        logged_u = User.authenticate("testuser", "password")
        self.assertEqual(logged_u, User)

    def invalidUsername(self):
        u = User.signup("testuser", "testuser@gmail.com", "password", "image.com")
        db.session.add(u)
        db.sesison.commit()
        logged_u = User.authenticate("asfawefaw", "password")
        self.assertNotEqual(logged_u, User)

    def invalidPassword(self):
        u = User.signup("testuser", "testuser@gmail.com", "password", "image.com")
        db.session.add(u)
        db.sesison.commit()
        logged_u = User.authenticate("testuser", "oiuhjfwoawihjf")
        self.assertNotEqual(logged_u, User)



