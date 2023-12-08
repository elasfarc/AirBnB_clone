import unittest
from unittest.mock import patch, mock_open
import json

from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestStorage(unittest.TestCase):
    def test_storage_attributes(self):
        storage = FileStorage()
        self.assertIsInstance(storage.all(), dict)
        self.assertTrue(storage._FileStorage__file_path)
        self.assertEqual(storage._FileStorage__file_path, "db.json")


class TestAddToStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage()
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        del self.storage

    def test_storage_after_init(self):
        stored_objs = self.storage.all()
        self.assertEqual(stored_objs, {})

    def test_adding_valid_object_to_storage(self):
        obj = BaseModel()
        obj_id = obj.id
        expected_key = f"{BaseModel.__name__}.{obj_id}"

        self.storage.new(obj)
        stored_objs = self.storage.all()

        self.assertEqual(len(stored_objs), 1)
        self.assertIn(expected_key, stored_objs.keys())
        self.assertIsInstance(stored_objs[expected_key], BaseModel)
        self.assertIs(stored_objs[expected_key], obj)

    def test_cannot_add_object_without_id(self):
        class TestNoIdObject:
            pass

        invalid_obj = TestNoIdObject()
        self.assertFalse(hasattr(invalid_obj, "id"))

        with self.assertRaises(TypeError) as context:
            self.storage.new(invalid_obj)
        self.assertEqual(
            str(context.exception),
            "obj must have attributes named id, __class__"
        )

    def test_cannot_add_object_without_class_name(self):
        class TestInvalidObject:
            id = "123"

            @property
            def __class__(self):
                return 100

        invalid_object = TestInvalidObject()
        self.assertFalse(hasattr(invalid_object.__class__, "__name__"))

        with self.assertRaises(TypeError) as context:
            self.storage.new(invalid_object)
        self.assertEqual(
            str(context.exception),
            "obj must have attributes named id, __class__"
        )


class TestSaveStorageToJSON(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage()

    def test_save_an_empty_storage(self):
        filename = "db.json"

        self.assertEqual(self.storage.all(), {})
        expected_written_json = json.dumps(self.storage.all())

        mocked_open = mock_open()
        with patch("builtins.open", mocked_open):
            self.storage.save()
        mocked_open.assert_called_once_with(filename, "w", encoding="utf-8")

        mocked_open = mock_open(read_data=expected_written_json)
        with patch("builtins.open", mocked_open):
            with open(f"{filename}", "r", encoding="utf") as rf:
                self.assertEqual(rf.read(), expected_written_json)

    def test_save_non_empty_storage(self):
        self.storage.new(BaseModel())
        self.storage.new(BaseModel())
        self.storage.new(BaseModel())

        self.assertEqual(len(self.storage.all()), 3)

        expected_written_json = json.dumps(
            {k: obj.to_dict() for k, obj in self.storage.all().items()}
        )

        mocked_open = mock_open()
        with patch("builtins.open", mocked_open):
            self.storage.save()
        mocked_open.assert_called_once_with("db.json", "w", encoding="utf-8")

        mocked_open = mock_open(read_data=expected_written_json)
        with patch("builtins.open", mocked_open):
            with open("db.json", "r", encoding="utf-8") as rf:
                self.assertEqual(rf.read(), expected_written_json)


class TestReloadStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage()
        self.storage._FileStorage__objects = {}

    def test_with_storage_file_not_exist(self):
        mocked_file = mock_open()

        with patch("builtins.open", mocked_file):
            with patch("os.path.exists", return_value=False):
                self.storage.reload()

        mocked_file.assert_not_called()

    def test_empty_file(self):
        self.storage.FileStorage__file_path = "empty_file.json"
        self.storage.__objects = {}
        expected_objects = {}
        expected_json_str = ""

        with patch("builtins.open", mock_open(read_data=expected_json_str)):
            self.storage.reload()

        self.assertEqual(self.storage.__objects, expected_objects)

    def test_valid_dictionaries(self):
        self.storage._FileStorage__file_path = "valid_file.json"
        self.storage._FileStorage__objects = {}
        expected_objects = {
            "BaseModel.1": BaseModel(),
            "BaseModel.2": BaseModel(),
        }
        expected_json_str = json.dumps(
            {
                "BaseModel.1": {"id": "1", "attr1": "value1"},
                "BaseModel.2": {"id": "2", "attr1": "value2"},
            }
        )

        fs_model = "models.engine.file_storage.FileStorage"

        mocked_file = mock_open(read_data=expected_json_str)
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mocked_file):
                with patch(
                    f"{fs_model}._FileStorage__instantiate_from_dict"
                ) as mocked_instantiate_from_dict:
                    mocked_instantiate_from_dict.side_effect = list(
                        expected_objects.values()
                    )
                    self.storage.reload()

        mocked_file.assert_called_once_with(
            "valid_file.json", mode="r", encoding="utf-8"
        )
        self.assertEqual(self.storage.all(), expected_objects)


if __name__ == "__main__":
    unittest.main()
