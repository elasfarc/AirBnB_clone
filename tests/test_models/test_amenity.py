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
    def setUp(self):
        self.storage_patch = patch(
            "models.storage.new", side_effect=lambda entity: None
        )
        self.mock_storage = self.storage_patch.start()
        pass

    def tearDown(self):
        self.storage_patch.stop()

    def test_initial_instance_amenity(self):
        amenity = Amenity()
        defaults = ["id", "created_at", "updated_at"]
        self.assertTrue(all(attr in amenity.__dict__ for attr in defaults))
        self.assertEqual(len(amenity.__dict__), len(defaults))

    def test_name_cls_attr(self):
        amenity = Amenity()
        self.assertTrue("name" in Amenity.__dict__)
        self.assertEqual(amenity.name, "")

    @patch("uuid.uuid4")
    def test_new_amenity_id(self, mock_uuid):
        uu_id = uuid4()
        mock_uuid.return_value = uu_id
        amenity = Amenity()
        self.assertIsInstance(amenity.id, str)
        self.assertEqual(amenity.id, str(uu_id))

    def test_id_is_unique(self):
        amenity = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity.id, amenity2.id)

    def test_id_is_casted_to_string_when_updated(self):
        amenity = Amenity()

        amenity.id = 15
        self.assertEqual(amenity.id, str(15))
        amenity.id = [7895]
        self.assertEqual(amenity.id, str([7895]))

    def test_update_valid_timestamp(self):
        amenity = Amenity()

        new_time = datetime.fromisoformat("2023-12-09T15:30:00")
        # datetime value
        amenity.created_at = new_time
        # valid iso format value
        amenity.updated_at = new_time.isoformat()

        self.assertEqual(amenity.created_at, new_time)
        self.assertEqual(amenity.updated_at, new_time)

    def test_update_invalid_timestamp(self):
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
        amenity = Amenity()
        amenity.ATTR = "VALUE"

        self.assertIn("ATTR", amenity.__dict__)
        self.assertEqual(amenity.ATTR, "VALUE")

    def test_in_storage_on_create(self):
        with patch("models.storage.new") as nw_storage:
            amenity = Amenity()
        nw_storage.assert_called_once_with(amenity)

    def test_no_new_storage_on_keyword_args_update(self):
        with patch("models.storage.new") as nw_storage:
            Amenity(name="foo", description="bar")

        nw_storage.assert_not_called()

    def test__class__attr_not_overwritten_on_keyword_args_update(self):
        amenity = Amenity(__class__="who cares?")

        self.assertNotEqual(amenity.__class__, "who cares?")
        self.assertEqual(amenity.__class__, Amenity)

    def test_str_representation(self):
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
    def setUp(self):
        self.storage_patch = patch.multiple(
            "models.storage",
            new=patch("models.storage.new",
                      side_effect=lambda entity: None).start(),
            save=patch(target="models.storage.save",
                       side_effect=lambda: None).start()
        )
        self.storage_patch.start()

    def tearDown(self):
        self.storage_patch.stop()

    def test_updated_at(self):
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
        amenity = Amenity()
        amenity.attr = "value"
        amenity.save()
        models.storage.save.assert_called_once_with()


class AmenityToDictionary(unittest.TestCase):

    def test_to_dict_contains_correct_keys(self):
        amenity = Amenity()
        self.assertIn("id", amenity.to_dict())
        self.assertIn("created_at", amenity.to_dict())
        self.assertIn("updated_at", amenity.to_dict())
        self.assertIn("__class__", amenity.to_dict())

    def test_to_dict_timestamp_attrs_are_strs(self):
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertIsInstance(amenity_dict["created_at"], str)
        self.assertIsInstance(amenity_dict["updated_at"], str)

    def test_to_dict__class__attr_is_string(self):
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertIsInstance(amenity_dict["__class__"], str)
        self.assertEqual(amenity_dict["__class__"], amenity.__class__.__name__)
        self.assertNotEqual(amenity_dict["__class__"], Amenity)

    def test_to_dict_added_attrs_are_present_in_dict(self):
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
