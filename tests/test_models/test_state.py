#!/usr/bin/python3
"""module containing tests for the State class."""

import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import patch
from models.state import State
import models
from uuid import uuid4


class TestStateInit(unittest.TestCase):
    def setUp(self):
        self.storage_patch = patch(
            "models.storage.new", side_effect=lambda entity: None
        )
        self.mock_storage = self.storage_patch.start()
        pass

    def tearDown(self):
        self.storage_patch.stop()

    def test_initial_instance_state(self):
        state = State()
        defaults = ["id", "created_at", "updated_at"]
        self.assertTrue(all(attr in state.__dict__ for attr in defaults))
        self.assertEqual(len(state.__dict__), len(defaults))

    def test_name_cls_attr(self):
        state = State()
        self.assertTrue("name" in State.__dict__)
        self.assertEqual(state.name, "")

    @patch("uuid.uuid4")
    def test_new_state_id(self, mock_uuid):
        uu_id = uuid4()
        mock_uuid.return_value = uu_id
        state = State()
        self.assertIsInstance(state.id, str)
        self.assertEqual(state.id, str(uu_id))

    def test_id_is_unique(self):
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    def test_id_is_casted_to_string_when_updated(self):
        state1 = State()

        state1.id = 15
        self.assertEqual(state1.id, str(15))
        state1.id = [7895]
        self.assertEqual(state1.id, str([7895]))

    def test_update_valid_timestamp(self):
        state1 = State()

        new_time = datetime.fromisoformat("2023-12-09T15:30:00")
        # datetime value
        state1.created_at = new_time
        # valid iso format value
        state1.updated_at = new_time.isoformat()

        self.assertEqual(state1.created_at, new_time)
        self.assertEqual(state1.updated_at, new_time)

    def test_update_invalid_timestamp(self):
        state1 = State()
        old_timestamp = state1.created_at

        with patch("sys.stdout", new=StringIO()) as f:
            state1.created_at = "Invalid timestamp"
            printed_output = f.getvalue().strip()

        printed_err_msg = "Failed to update datetime. Invalid input."
        self.assertEqual(printed_output, printed_err_msg)
        self.assertNotEqual(state1.created_at, "Invalid timestamp")
        self.assertEqual(state1.created_at, old_timestamp)

    def test_set_other_attrs(self):
        state1 = State()
        state1.ATTR = "VALUE"

        self.assertIn("ATTR", state1.__dict__)
        self.assertEqual(state1.ATTR, "VALUE")

    def test_in_storage_on_create(self):
        with patch("models.storage.new") as nw_storage:
            state1 = State()
        nw_storage.assert_called_once_with(state1)

    def test_no_new_storage_on_keyword_args_update(self):
        with patch("models.storage.new") as nw_storage:
            State(name="foo", description="bar")

        nw_storage.assert_not_called()

    def test__class__attr_not_overwritten_on_keyword_args_update(self):
        state1 = State(__class__="who cares?")

        self.assertNotEqual(state1.__class__, "who cares?")
        self.assertEqual(state1.__class__, State)

    def test_str_representation(self):
        with patch("models.base_model.datetime") as datetime_mock:
            now = datetime.now()
            datetime_mock.now.return_value = now
            state = State()

        state.id = "1234"
        state_str = state.__str__()
        self.assertIn("[State] (1234)", state_str)
        self.assertIn("'id': '1234'", state_str)
        self.assertIn("'created_at': " + repr(now), state_str)
        self.assertIn("'updated_at': " + repr(now), state_str)


class TestStateSave(unittest.TestCase):
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
            state1 = State()

        self.assertEqual(state1.updated_at, then)

        state1.attr = "value"
        state1.save()

        self.assertNotEqual(state1.updated_at, then)
        self.assertLess(then, state1.updated_at)

    def test_changes_persisted_after_save(self):
        state1 = State()
        state1.attr = "value"
        state1.save()
        models.storage.save.assert_called_once_with()


class StateToDictionary(unittest.TestCase):

    def test_to_dict_contains_correct_keys(self):
        state = State()
        self.assertIn("id", state.to_dict())
        self.assertIn("created_at", state.to_dict())
        self.assertIn("updated_at", state.to_dict())
        self.assertIn("__class__", state.to_dict())

    def test_to_dict_timestamp_attrs_are_strs(self):
        state = State()
        state_dict = state.to_dict()
        self.assertIsInstance(state_dict["created_at"], str)
        self.assertIsInstance(state_dict["updated_at"], str)

    def test_to_dict__class__attr_is_string(self):
        state = State()
        state_dict = state.to_dict()
        self.assertIsInstance(state_dict["__class__"], str)
        self.assertEqual(state_dict["__class__"], state.__class__.__name__)
        self.assertNotEqual(state_dict["__class__"], State)

    def test_to_dict_added_attrs_are_present_in_dict(self):
        state = State()
        state.attr = "value"
        state.attr2 = [12]

        state_dict = state.to_dict()
        self.assertIn("attr", state_dict)
        self.assertIn("attr2", state_dict)
        self.assertEqual(state_dict["attr"], "value")
        self.assertEqual(state_dict["attr2"], [12])


if __name__ == "__main__":
    unittest.main()
