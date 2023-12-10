#!/usr/bin/python3
"""module containing tests for the Place class."""

import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import patch
from models.place import Place
import models
from uuid import uuid4


class TestPlaceInit(unittest.TestCase):
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
        """Tests that the initial state of the Place instance contains certain
        expected attributes.
        """
        place = Place()
        defaults = ["id", "created_at", "updated_at"]
        self.assertTrue(all(attr in place.__dict__ for attr in defaults))
        self.assertEqual(len(place.__dict__), len(defaults))

    def test_public_cls_data_attrs(self):
        """
        Tests that the public class data attributes of Place are present and
        initialized with empty values.
        """
        place = Place()
        data_attrs = [
            "city_id",
            "user_id",
            "name",
            "description",
            "number_rooms",
            "number_bathrooms",
            "max_guest",
            "price_by_night",
            "longitude",
            "latitude",
            "amenity_ids",
        ]
        self.assertTrue(all(attr in Place.__dict__ for attr in data_attrs))
        self.assertEqual(place.name, "")

        self.assertTrue(
            all(
                {
                    k: v == ""
                    if type(v) is str
                    else v == 0
                    if type(v) is int
                    and k in [
                           "number_rooms",
                           "number_bathrooms",
                           "max_guest",
                           "price_by_night"
                       ]
                    else v == 0.0
                    if type(v) is float and k in ["longitude", "latitude"]
                    else v == [] and k in ["amenity_ids"]
                    for k, v in Place.__dict__.items()
                    if k in data_attrs
                }.values()
            )
        )

    @patch("uuid.uuid4")
    def test_new_place_id(self, mock_uuid):
        """
        Tests that a new Place instance receives a unique identifier
        upon initialization. (converted string)
        """
        uu_id = uuid4()
        mock_uuid.return_value = uu_id
        place = Place()
        self.assertIsInstance(place.id, str)
        self.assertEqual(place.id, str(uu_id))

    def test_id_is_unique(self):
        """
        Tests that two distinct instances receive different identifiers.
        """
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.id, place2.id)

    def test_id_is_casted_to_string_when_updated(self):
        """
        Tests that the id attribute of a Place instance is
        casted to a string when updated.
        """
        place1 = Place()

        place1.id = 15
        self.assertEqual(place1.id, str(15))
        place1.id = [7895]
        self.assertEqual(place1.id, str([7895]))

    def test_update_valid_timestamp(self):
        """
        Tests that the created_at and updated_at attributes of an
        instance can be updated with valid timestamp values.
        """
        place1 = Place()

        new_time = datetime.fromisoformat("2023-12-09T15:30:00")
        # datetime value
        place1.created_at = new_time
        # valid iso format value
        place1.updated_at = new_time.isoformat()

        self.assertEqual(place1.created_at, new_time)
        self.assertEqual(place1.updated_at, new_time)

    def test_update_invalid_timestamp(self):
        """
        Tests that attempting to update the created_at and updated_at
        attributes of an instance with invalid timestamp values results
        in no change.
        """
        place1 = Place()
        old_timestamp = place1.created_at

        with patch("sys.stdout", new=StringIO()) as f:
            place1.created_at = "Invalid timestamp"
            printed_output = f.getvalue().strip()

        printed_err_msg = "Failed to update datetime. Invalid input."
        self.assertEqual(printed_output, printed_err_msg)
        self.assertNotEqual(place1.created_at, "Invalid timestamp")
        self.assertEqual(place1.created_at, old_timestamp)

    def test_set_other_attrs(self):
        """
        Tests that additional arbitrary attributes can be added to an instance.
        """
        place1 = Place()
        place1.ATTR = "VALUE"

        self.assertIn("ATTR", place1.__dict__)
        self.assertEqual(place1.ATTR, "VALUE")

    def test_in_storage_on_create(self):
        """
        Tests that a new instance is stored in the database upon creation.
        """
        with patch("models.storage.new") as nw_storage:
            place1 = Place()
        nw_storage.assert_called_once_with(place1)

    def test_no_new_storage_on_keyword_args_update(self):
        """
        Tests that passing keyword arguments to the constructor
        does not trigger new storage action.
        """

        with patch("models.storage.new") as nw_storage:
            Place(name="foo", description="bar")

        nw_storage.assert_not_called()

    def test__class__attr_not_overwritten_on_keyword_args_update(self):
        """
        Tests that the __class__ attribute of an instance cannot
        be overwritten using keyword arguments passed to its constructor.
        """
        place1 = Place(__class__="who cares?")

        self.assertNotEqual(place1.__class__, "who cares?")
        self.assertEqual(place1.__class__, Place)

    def test_str_representation(self):
        """
        Tests that the string representation of an instance
        contains certain expected information.
        """
        with patch("models.base_model.datetime") as datetime_mock:
            now = datetime.now()
            datetime_mock.now.return_value = now
            place = Place()

        place.id = "1234"
        place_str = place.__str__()
        self.assertIn("[Place] (1234)", place_str)
        self.assertIn("'id': '1234'", place_str)
        self.assertIn("'created_at': " + repr(now), place_str)
        self.assertIn("'updated_at': " + repr(now), place_str)


class TestPlaceSave(unittest.TestCase):
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
            place1 = Place()

        self.assertEqual(place1.updated_at, then)

        place1.attr = "value"
        place1.save()

        self.assertNotEqual(place1.updated_at, then)
        self.assertLess(then, place1.updated_at)

    def test_changes_persisted_after_save(self):
        """
        Tests that changes made to an instance are persisted after calling
        its save method.
        """
        place1 = Place()
        place1.attr = "value"
        place1.save()
        models.storage.save.assert_called_once_with()


class PlaceToDictionary(unittest.TestCase):
    """
    Test cases to verify that the output dictionary is constructed
    correctly based on the input data.
    """

    def test_to_dict_contains_correct_keys(self):
        """
        Tests that the dictionary representation of aninstance contains
        certain expected keys.
        """
        place = Place()
        self.assertIn("id", place.to_dict())
        self.assertIn("created_at", place.to_dict())
        self.assertIn("updated_at", place.to_dict())
        self.assertIn("__class__", place.to_dict())

    def test_to_dict_timestamp_attrs_are_strs(self):
        """
        Tests that the created_at and updated_at attributes of an instance
        are strings in its dictionary representation as string
        """
        place = Place()
        place_dict = place.to_dict()
        self.assertIsInstance(place_dict["created_at"], str)
        self.assertIsInstance(place_dict["updated_at"], str)

    def test_to_dict__class__attr_is_string(self):
        """
        Tests that the __class__ attribute of an instance is a string in
        its dictionary representation.
        """
        place = Place()
        place_dict = place.to_dict()
        self.assertIsInstance(place_dict["__class__"], str)
        self.assertEqual(place_dict["__class__"], place.__class__.__name__)
        self.assertNotEqual(place_dict["__class__"], Place)

    def test_to_dict_added_attrs_are_present_in_dict(self):
        """
        Tests that additional arbitrary attributes added to an instance are
        included in its dictionary representation.
        """
        place = Place()
        place.attr = "value"
        place.attr2 = [12]

        place_dict = place.to_dict()
        self.assertIn("attr", place_dict)
        self.assertIn("attr2", place_dict)
        self.assertEqual(place_dict["attr"], "value")
        self.assertEqual(place_dict["attr2"], [12])


if __name__ == "__main__":
    unittest.main()
