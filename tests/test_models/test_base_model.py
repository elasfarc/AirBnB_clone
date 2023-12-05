"""
module containing tests for the BaseModel class.
"""

import unittest
from unittest.mock import patch
from datetime import timedelta
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    A TestCase class for testing the functionality of the BaseModel class.
    """

    def test_id_type(self):
        """
        Test the data type of the 'id' attribute in the BaseModel class.

        This test ensures that the 'id' attribute of a BaseModel instance is of type str.
        """
        base = BaseModel()
        self.assertIsInstance(base.id, str)

    def test_unique_id(self):
        """
        Test the uniqueness of the 'id' attribute in different BaseModel instances.

        This test checks that the 'id' attribute of different BaseModel instances is unique.
        """
        base_model1 = BaseModel()
        base_model2 = BaseModel()
        base_model3 = BaseModel()
        assert base_model1.id != base_model2.id != base_model3.id

    def test_object_timestamps(self):
        """
        Test the equality of 'created_at' and 'updated_at' attributes in a BaseModel instance.

        This test checks that the 'created_at' and 'updated_at' attributes are equal upon
        initialization of a BaseModel instance.
        """
        base = BaseModel()
        self.assertEqual(base.created_at, base.updated_at)

    def test_objects_timestamps(self):
        """
        Test the ordering of 'created_at' attributes in different BaseModel instances.

        This test ensures that the 'created_at' attribute of a second BaseModel instance is
        greater than that of the first BaseModel instance.
        """
        base = BaseModel()
        base2 = BaseModel()
        self.assertGreater(base2.created_at, base.created_at)

    def test_save(self):
        """
        Test the 'save' method in the BaseModel class.

        This test checks that the 'save' method updates the 'updated_at' attribute to the
        current date and time.
        """
        base = BaseModel()
        current_updated = base.updated_at
        delta = timedelta(days=2)

        with patch("models.base_model.datetime") as mock_datetime:
            mock_datetime.now.return_value = current_updated + delta
            base.save()

        self.assertNotEqual(base.updated_at, current_updated)
        self.assertGreater(base.updated_at, current_updated)
