#!/usr/bin/python3
"""
module containing tests for the BaseModel class.
"""
import unittest
from unittest.mock import patch, mock_open
import json

from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestStorage(unittest.TestCase):
    """
    A TestCase class for testing the functionality of the FileStorage class.
    """
    def test_storage_attributes(self):
        """tests the attributes of the FileStorage class."""
        storage = FileStorage()
        self.assertIsInstance(storage.all(), dict)
        self.assertTrue(storage._FileStorage__file_path)
        self.assertEqual(storage._FileStorage__file_path, "db.json")


class TestAddToStorage(unittest.TestCase):
    """Test suite for testing the addition of objects to the storage."""
    def setUp(self):
        """
        Setup method for creating a new FileStorage
        instance and setting it to the storage variable.
        sets the _FileStorage__objects attribute to an empty dictionary.
        """
        self.storage = FileStorage()
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Teardown method for deleting the storage variable."""
        del self.storage

    def test_storage_after_init(self):
        """Test case for checking that the storage has no objects after init.
        """
        stored_objs = self.storage.all()
        self.assertEqual(stored_objs, {})

    def test_adding_valid_object_to_storage(self):
        """Test case for adding a valid object to the storage.
        """
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
        """Test case for adding an object without an id attribute.
        """
        class TestNoIdObject:
            """testing class"""
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
        """Test case for adding an object without a class name.
        """
        class TestInvalidObject:
            """TestModel - testing class """
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
    """tests the save functionality of the Storage class."""
    def setUp(self):
        """Set up the test environment."""
        self.storage = FileStorage()

    def test_save_an_empty_storage(self):
        """Test that an empty storage is saved correctly."""
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
        """Test that a non-empty storage is saved correctly."""
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
    """the reload functionality of the FileStorage class."""
    def setUp(self):
        """Set up the test environment."""
        self.storage = FileStorage()
        self.storage._FileStorage__objects = {}

    def test_with_storage_file_not_exist(self):
        """Test that the reload method does not attempt to load a storage
        file that does not exist.
        """
        mocked_file = mock_open()

        with patch("builtins.open", mocked_file):
            with patch("os.path.exists", return_value=False):
                self.storage.reload()

        mocked_file.assert_not_called()

    def test_empty_file(self):
        """Test that the reload method can handle an empty storage file.
        """
        self.storage.FileStorage__file_path = "empty_file.json"
        self.storage.__objects = {}
        expected_objects = {}
        expected_json_str = ""

        with patch("builtins.open", mock_open(read_data=expected_json_str)):
            self.storage.reload()

        self.assertEqual(self.storage.__objects, expected_objects)

    def test_valid_dictionaries(self):
        """Test that the reload method can successfully instantiate
        objects from valid dictionaries.
        """
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
