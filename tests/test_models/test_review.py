#!/usr/bin/python3
"""module containing tests for the Review class."""

import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import patch
from models.review import Review
import models
from uuid import uuid4


class TestReviewInit(unittest.TestCase):
    def setUp(self):
        self.storage_patch = patch(
            "models.storage.new", side_effect=lambda entity: None
        )
        self.mock_storage = self.storage_patch.start()
        pass

    def tearDown(self):
        self.storage_patch.stop()

    def test_initial_instance_state(self):
        review = Review()
        defaults = ["id", "created_at", "updated_at"]
        self.assertTrue(all(attr in review.__dict__ for attr in defaults))
        self.assertEqual(len(review.__dict__), len(defaults))

    def test_user_id_cls_attr(self):
        review = Review()
        self.assertTrue("user_id" in Review.__dict__)
        self.assertEqual(review.user_id, "")

    def test_place_id_cls_attr(self):
        review = Review()
        self.assertTrue("place_id" in Review.__dict__)
        self.assertEqual(review.place_id, "")

    def test_text_cls_attr(self):
        review = Review()
        self.assertTrue("text" in Review.__dict__)
        self.assertEqual(review.text, "")

    @patch("uuid.uuid4")
    def test_new_review_id(self, mock_uuid):
        uu_id = uuid4()
        mock_uuid.return_value = uu_id
        review = Review()
        self.assertIsInstance(review.id, str)
        self.assertEqual(review.id, str(uu_id))

    def test_id_is_unique(self):
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)

    def test_id_is_casted_to_string_when_updated(self):
        review1 = Review()

        review1.id = 15
        self.assertEqual(review1.id, str(15))
        review1.id = [7895]
        self.assertEqual(review1.id, str([7895]))

    def test_update_valid_timestamp(self):
        review1 = Review()

        new_time = datetime.fromisoformat("2023-12-09T15:30:00")
        # datetime value
        review1.created_at = new_time
        # valid iso format value
        review1.updated_at = new_time.isoformat()

        self.assertEqual(review1.created_at, new_time)
        self.assertEqual(review1.updated_at, new_time)

    def test_update_invalid_timestamp(self):
        review1 = Review()
        old_timestamp = review1.created_at

        with patch("sys.stdout", new=StringIO()) as f:
            review1.created_at = "Invalid timestamp"
            printed_output = f.getvalue().strip()

        printed_err_msg = "Failed to update datetime. Invalid input."
        self.assertEqual(printed_output, printed_err_msg)
        self.assertNotEqual(review1.created_at, "Invalid timestamp")
        self.assertEqual(review1.created_at, old_timestamp)

    def test_set_other_attrs(self):
        review1 = Review()
        review1.ATTR = "VALUE"

        self.assertIn("ATTR", review1.__dict__)
        self.assertEqual(review1.ATTR, "VALUE")

    def test_in_storage_on_create(self):
        with patch("models.storage.new") as nw_storage:
            review1 = Review()
        nw_storage.assert_called_once_with(review1)

    def test_no_new_storage_on_keyword_args_update(self):
        with patch("models.storage.new") as nw_storage:
            Review(name="foo", description="bar")

        nw_storage.assert_not_called()

    def test__class__attr_not_overwritten_on_keyword_args_update(self):
        review1 = Review(__class__="who cares?")

        self.assertNotEqual(review1.__class__, "who cares?")
        self.assertEqual(review1.__class__, Review)

    def test_str_representation(self):
        with patch("models.base_model.datetime") as datetime_mock:
            now = datetime.now()
            datetime_mock.now.return_value = now
            review = Review()

        review.id = "1234"
        review_str = review.__str__()
        self.assertIn("[Review] (1234)", review_str)
        self.assertIn("'id': '1234'", review_str)
        self.assertIn("'created_at': " + repr(now), review_str)
        self.assertIn("'updated_at': " + repr(now), review_str)


class TestReviewSave(unittest.TestCase):
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
            review1 = Review()

        self.assertEqual(review1.updated_at, then)

        review1.attr = "value"
        review1.save()

        self.assertNotEqual(review1.updated_at, then)
        self.assertLess(then, review1.updated_at)

    def test_changes_persisted_after_save(self):
        review1 = Review()
        review1.attr = "value"
        review1.save()
        models.storage.save.assert_called_once_with()


class ReviewToDictionary(unittest.TestCase):

    def test_to_dict_contains_correct_keys(self):
        review = Review()
        self.assertIn("id", review.to_dict())
        self.assertIn("created_at", review.to_dict())
        self.assertIn("updated_at", review.to_dict())
        self.assertIn("__class__", review.to_dict())

    def test_to_dict_timestamp_attrs_are_strs(self):
        review = Review()
        review_dict = review.to_dict()
        self.assertIsInstance(review_dict["created_at"], str)
        self.assertIsInstance(review_dict["updated_at"], str)

    def test_to_dict__class__attr_is_string(self):
        review = Review()
        review_dict = review.to_dict()
        self.assertIsInstance(review_dict["__class__"], str)
        self.assertEqual(review_dict["__class__"], review.__class__.__name__)
        self.assertNotEqual(review_dict["__class__"], Review)

    def test_to_dict_added_attrs_are_present_in_dict(self):
        review = Review()
        review.attr = "value"
        review.attr2 = [12]

        review_dict = review.to_dict()
        self.assertIn("attr", review_dict)
        self.assertIn("attr2", review_dict)
        self.assertEqual(review_dict["attr"], "value")
        self.assertEqual(review_dict["attr2"], [12])


if __name__ == "__main__":
    unittest.main()
