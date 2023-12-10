#!/usr/bin/python3
"""module containing tests for the User class."""

import unittest
from unittest.mock import patch
from time import sleep
from datetime import datetime

from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """Class for testing User class."""
    @patch("uuid.uuid4", return_value="1234")
    @patch("models.storage.new")
    def test_new_instance(self, storage_new, mock_uuid4):
        """Test the creation of a new instance of the User class"""
        mocked_now = datetime.fromisoformat("2024-01-01")

        with patch("models.base_model.datetime") as mock_datetime:
            mock_datetime.now.return_value = mocked_now
            user = User()

        self.assertTrue(isinstance(user, User))
        self.assertTrue(isinstance(user, BaseModel))
        self.assertEqual(user.id, "1234")
        self.assertEqual(user.created_at, mocked_now)
        self.assertEqual(user.updated_at, mocked_now)
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")
        self.assertEqual(user.email, "")
        self.assertEqual(user.password, "")

        storage_new.assert_called_once_with(user)

    @patch("models.storage.new")
    def test_no_new_storage_entity_created_on_object_update(self, storage_new):
        """
        Test that updating an object does not create a new storage entity.
        """

        updated_attributes = {
            "first_name": "foo",
            "last_name": "bar",
        }
        User(**updated_attributes)
        storage_new.assert_not_called()

    def test_id_uniqueness(self):
        """Test the uniqueness of User IDs."""
        self.assertNotEqual(User().id, User().id)

    def test_created_at(self):
        """Test the creation timestamps of User instances."""
        u1 = User()
        sleep(0.1)
        u2 = User()
        self.assertNotEqual(u1.created_at, u2.created_at)
        self.assertLess(u1.created_at, u2.created_at)

    def test__str__(self):
        """Test the string representation of User instances."""

        mocked_now = datetime.fromisoformat("2024-01-01")
        with patch("models.base_model.datetime") as mock_datetime:
            mock_datetime.now.return_value = mocked_now
            user = User()

        user.id = "1234"
        user.first_name = "foo"

        self.assertIn("[User] (1234)", str(user))
        self.assertIn("'id': '1234'", str(user))
        self.assertIn("'created_at': " + repr(mocked_now), str(user))
        self.assertIn("'updated_at': " + repr(mocked_now), str(user))

    def test_updated_at_on_save(self):
        """
        Test that the 'updated_at' attribute is updated on calling the
        'save' method.
        """
        user = User()
        old_updated_at = user.updated_at
        with patch("models.storage.save", side_effect=lambda: None):
            user.save()

        sleep(0.01)
        new_updated_at = user.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertLess(old_updated_at, new_updated_at)

    def test_to_dict_keys(self):
        """Test the keys returned by the 'to_dict' method."""
        user = User()
        self.assertIn("id", user.to_dict())
        self.assertIn("created_at", user.to_dict())
        self.assertIn("updated_at", user.to_dict())
        self.assertIn("__class__", user.to_dict())
        self.assertEqual(User.__name__, user.to_dict()["__class__"])


if __name__ == "__main__":
    unittest.main()
