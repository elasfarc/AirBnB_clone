#!/usr/bin/python3
"""module containing tests for the Amenity class."""

import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import patch
from models.amenity import Amenity
import models
from uuid import uuid4


class TestAmenityInit(unittest.TestCase):
    """
    Test cases for init a new instance.
    """
    def setUp(self):
        """Sets up the necessary mocks and variables needed for testing."""
        self.storage_patch = patch(
            "models.storage.new", side_effect=lambda entity: None
        )
        self.mock_storage = self.storage_patch.start()
        pass

    def tearDown(self):
        """Stops the started mocks."""
        self.storage_patch.stop()

    def test_initial_instance_state(self):
        """
        Tests that the initial state of the Place instance contains
        certain expected attributes.
        """
        amenity = Amenity()
        defaults = ["id", "created_at", "updated_at"]
        self.assertTrue(all(attr in amenity.__dict__ for attr in defaults))
        self.assertEqual(len(amenity.__dict__), len(defaults))

    def test_name_cls_attr(self):
        """
        Tests that the name public class data attribute of Amenity
        is present and initialized with empty values.
        """
        amenity = Amenity()
        self.assertTrue("name" in Amenity.__dict__)
        self.assertEqual(amenity.name, "")

    @patch("uuid.uuid4")
    def test_new_amenity_id(self, mock_uuid):
        """
        Tests that a new Amenity instance receives a unique identifier
        upon initialization. (converted string)
        """
        uu_id = uuid4()
        mock_uuid.return_value = uu_id
        amenity = Amenity()
        self.assertIsInstance(amenity.id, str)
        self.assertEqual(amenity.id, str(uu_id))

    def test_id_is_unique(self):
        """
        Tests that two distinct instances receive different identifiers.
        """
        amenity = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity.id, amenity2.id)

    def test_id_is_casted_to_string_when_updated(self):
        """
        Tests that the id attribute of a Place instance is
        casted to a string when updated.
        """
        amenity = Amenity()

        amenity.id = 15
        self.assertEqual(amenity.id, str(15))
        amenity.id = [7895]
        self.assertEqual(amenity.id, str([7895]))

    def test_update_valid_timestamp(self):
        """
        Tests that the created_at and updated_at attributes of an
        instance can be updated with valid timestamp values.
        """
        amenity = Amenity()

        new_time = datetime.fromisoformat("2023-12-09T15:30:00")
        # datetime value
        amenity.created_at = new_time
        # valid iso format value
        amenity.updated_at = new_time.isoformat()

        self.assertEqual(amenity.created_at, new_time)
        self.assertEqual(amenity.updated_at, new_time)

    def test_update_invalid_timestamp(self):
        """
        Tests that attempting to update the created_at and updated_at
        attributes of an instance with invalid timestamp values results
        in no change.
        """
        amenity = Amenity()
        old_timestamp = amenity.created_at

        with patch("sys.stdout", new=StringIO()) as f:
            amenity.created_at = "Invalid timestamp"
            printed_output = f.getvalue().strip()

        printed_err_msg = "Failed to update datetime. Invalid input."
        self.assertEqual(printed_output, printed_err_msg)
        self.assertNotEqual(amenity.created_at, "Invalid timestamp")
        self.assertEqual(amenity.created_at, old_timestamp)

    def test_set_other_attrs(self):
        """
        Tests that additional arbitrary attributes can be added to an instance.
        """
        amenity = Amenity()
        amenity.ATTR = "VALUE"

        self.assertIn("ATTR", amenity.__dict__)
        self.assertEqual(amenity.ATTR, "VALUE")

    def test_in_storage_on_create(self):
        """
        Tests that a new instance is stored in the database upon creation.
        """
        with patch("models.storage.new") as nw_storage:
            amenity = Amenity()
        nw_storage.assert_called_once_with(amenity)

    def test_no_new_storage_on_keyword_args_update(self):
        """
        Tests that passing keyword arguments to the constructor
        does not trigger new storage action.
        """
        with patch("models.storage.new") as nw_storage:
            Amenity(name="foo", description="bar")

        nw_storage.assert_not_called()

    def test__class__attr_not_overwritten_on_keyword_args_update(self):
        """
        Tests that the __class__ attribute of an instance cannot
        be overwritten using keyword arguments passed to its constructor.
        """
        amenity = Amenity(__class__="who cares?")

        self.assertNotEqual(amenity.__class__, "who cares?")
        self.assertEqual(amenity.__class__, Amenity)

    def test_str_representation(self):
        """
        Tests that the string representation of an instance
        contains certain expected information.
        """
        with patch("models.base_model.datetime") as datetime_mock:
            now = datetime.now()
            datetime_mock.now.return_value = now
            amenity = Amenity()

        amenity.id = "1234"
        amenity_str = amenity.__str__()
        self.assertIn("[Amenity] (1234)", amenity_str)
        self.assertIn("'id': '1234'", amenity_str)
        self.assertIn("'created_at': " + repr(now), amenity_str)
        self.assertIn("'updated_at': " + repr(now), amenity_str)


class TestAmenitySave(unittest.TestCase):
    """Test cases to test saving an instance functionality """
    def setUp(self):
        """Sets up the necessary mocks and variables needed for testing."""
        self.storage_patch = patch.multiple(
            "models.storage",
            new=patch("models.storage.new",
                      side_effect=lambda entity: None).start(),
            save=patch(target="models.storage.save",
                       side_effect=lambda: None).start()
        )
        self.storage_patch.start()

    def tearDown(self):
        """Stops the started mocks."""
        self.storage_patch.stop()

    def test_updated_at(self):
        """
        Tests that the updated_at attribute of an instance is updated after
        calling its save method.
        """
        with patch("models.base_model.datetime") as mocked_time:
            then = datetime.now()
            mocked_time.now.return_value = then
            amenity = Amenity()

        self.assertEqual(amenity.updated_at, then)

        amenity.attr = "value"
        amenity.save()

        self.assertNotEqual(amenity.updated_at, then)
        self.assertLess(then, amenity.updated_at)

    def test_changes_persisted_after_save(self):
        """
        Tests that changes made to an instance are persisted after
        calling its save method.
        """
        amenity = Amenity()
        amenity.attr = "value"
        amenity.save()
        models.storage.save.assert_called_once_with()


class AmenityToDictionary(unittest.TestCase):
    """
    Test cases to verify that the output dictionary is constructed
    correctly based on the input data.
    """

    def test_to_dict_contains_correct_keys(self):
        """
        Tests that the dictionary representation of aninstance contains
        certain expected keys.
        """
        amenity = Amenity()
        self.assertIn("id", amenity.to_dict())
        self.assertIn("created_at", amenity.to_dict())
        self.assertIn("updated_at", amenity.to_dict())
        self.assertIn("__class__", amenity.to_dict())

    def test_to_dict_timestamp_attrs_are_strs(self):
        """
        Tests that the created_at and updated_at attributes of an instance
        are strings in its dictionary representation as string
        """
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertIsInstance(amenity_dict["created_at"], str)
        self.assertIsInstance(amenity_dict["updated_at"], str)

    def test_to_dict__class__attr_is_string(self):
        """
        Tests that the __class__ attribute of an instance is a string in
        its dictionary representation.
        """
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertIsInstance(amenity_dict["__class__"], str)
        self.assertEqual(amenity_dict["__class__"], amenity.__class__.__name__)
        self.assertNotEqual(amenity_dict["__class__"], Amenity)

    def test_to_dict_added_attrs_are_present_in_dict(self):
        """
        Tests that additional arbitrary attributes added to an instance are
        included in its dictionary representation.
        """
        amenity = Amenity()
        amenity.attr = "value"
        amenity.attr2 = [12]

        amenity_dict = amenity.to_dict()
        self.assertIn("attr", amenity_dict)
        self.assertIn("attr2", amenity_dict)
        self.assertEqual(amenity_dict["attr"], "value")
        self.assertEqual(amenity_dict["attr2"], [12])


if __name__ == "__main__":
    unittest.main()
