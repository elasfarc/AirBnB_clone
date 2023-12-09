#!/usr/bin/python3
"""
module containing tests for the BaseModel class.
"""

import unittest
from unittest.mock import patch
from datetime import timedelta, datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    A TestCase class for testing the functionality of the BaseModel class.
    """

    def test_id_type(self):
        """
        Test the data type of the 'id' attribute in the BaseModel class.

        This test ensures that the 'id' attribute of a BaseModel instance
        is of type str.
        """
        base = BaseModel()
        self.assertIsInstance(base.id, str)

    def test_unique_id(self):
        """
        Test the uniqueness of the 'id' attribute in different BaseModel
        instances.

        This test checks that the 'id' attribute of different BaseModel
        instances is unique.
        """
        base_model1 = BaseModel()
        base_model2 = BaseModel()
        base_model3 = BaseModel()
        assert base_model1.id != base_model2.id != base_model3.id

    def test_object_timestamps(self):
        """
        Test the equality of 'created_at' and 'updated_at' attributes
        in a BaseModel instance.

        This test checks that the 'created_at' and 'updated_at' attributes
        are equal upon initialization of a BaseModel instance.
        """
        base = BaseModel()
        self.assertEqual(base.created_at, base.updated_at)

    def test_objects_timestamps(self):
        """
        Test the ordering of 'created_at' attributes in different BaseModel
        instances.

        This test ensures that the 'created_at' attribute of a second
        BaseModel instance is greater than that of the first BaseModel
        instance.
        """
        base = BaseModel()
        base2 = BaseModel()
        self.assertGreater(base2.created_at, base.created_at)

    def test_save(self):
        """
        Test the 'save' method in the BaseModel class.

        This test checks that the 'save' method updates the 'updated_at'
        attribute to the current date and time.
        """
        base = BaseModel()
        current_updated = base.updated_at
        delta = timedelta(days=2)

        with patch("models.base_model.datetime") as mock_datetime:
            mock_datetime.now.return_value = current_updated + delta
            base.save()

        self.assertNotEqual(base.updated_at, current_updated)
        self.assertGreater(base.updated_at, current_updated)

    def test_string_representation_with_class_name_id_and_attributes(self):
        """
        test_string_representation_with_class_name_id_and_attributes
            Test the string representation with class name, ID,
            and attributes.

        Description:
        This test case creates an instance of the BaseModel class,
        retrieves its string representation, and compares it
        with the expected string.
        The expected string is formatted as "[BaseModel] (ObjectID) {__dict__}"

        """
        obj = BaseModel()
        expected = f"[BaseModel] ({obj.id}) {obj.__dict__}"
        self.assertEqual(str(obj), expected)

    #  The string representation includes all attributes of the object.
    def test_string_representation_includes_all_attributes(self):
        """
        test_string_representation_includes_all_attributes
            Test that the string representation includes all attributes.

        Description:
        This test case defines a TestModel class that inherits from BaseModel,
        initializes some attributes, creates an instance, retrieves its string
        representation, and compares it with the expected string.
        The expected string is formatted as "[TestModel] (ObjectID) {__dict__}"
        """
        class TestModel(BaseModel):
            """
            TestModel - A subclass of BaseModel for testing purposes.
            """
            def __init__(self):
                super().__init__()
                self.attribute1 = "value1"
                self.attribute2 = "value2"

        obj = TestModel()
        expected = f"[TestModel] ({obj.id}) {obj.__dict__}"
        self.assertEqual(str(obj), expected)


class TestDictionaryConversion(unittest.TestCase):
    """
    TestDictionaryConversion - Test case for the dictionary conversion
    methods in the BaseModel class.
    """
    def test_timestamps(self):
        """
        test_timestamps - Test handling of timestamps in the to_dict method.

        Description:
        This test method uses the unittest.TestCase `patch` functionality
        to mock the datetime module, setting a fixed date for testing.
        It creates an instance of the BaseModel class, converts it to
        a dictionary, and then asserts that the timestamp attributes in the
        resulting dictionary are of type string and have the expected values.

        """
        with patch("models.base_model.datetime") as mock_datetime:
            mock_datetime.now.return_value =\
                datetime.fromisoformat("2024-01-01")
            obj = BaseModel()
            dic = obj.to_dict()

        self.assertIsInstance(dic["created_at"], str)
        self.assertIsInstance(dic["updated_at"], str)
        self.assertEqual(dic["created_at"], obj.created_at.isoformat())
        self.assertEqual(dic["created_at"], obj.created_at.isoformat())
        # expected =

    def test_returns_dictionary_with_attributes_and_cls_name(self):
        """
        test_returns_dictionary_with_attributes_and_cls_name
            Test that to_dict returns a dictionary with attributes and
            class name.

        Description:
        This test method creates an instance of the BaseModel class,
        converts it to a dictionary, and asserts that the resulting
        dictionary includes attributes such as '__class__', 'id', 'created_at',
        and 'updated_at', with correct values.

        """
        obj = BaseModel()
        dic = obj.to_dict()

        self.assertIsInstance(dic, dict)
        self.assertEqual(dic["__class__"], obj.__class__.__name__)
        self.assertEqual(dic["id"], obj.id)
        self.assertEqual(dic["created_at"], obj.created_at.isoformat())
        self.assertEqual(dic["created_at"], obj.created_at.isoformat())

    def test_works_with_attributes_of_different_types(self):
        """
        test_works_with_attributes_of_different_types
            Test that to_dict works with attributes of different types.

        Description:
        This test method defines a TestModel class that inherits from BaseModel
        and initializes attributes of various types.
        It creates an instance of TestModel, converts it to a dictionary,
        and asserts that the resulting dictionary contains attributes with
        their correct values.

        """
        class TestModel(BaseModel):
            """
            TestModel - A subclass of BaseModel for testing purposes.
            """
            def __init__(self):
                super().__init__()
                self.name = "Test"
                self.age = 20
                self.is_active = True

        obj = TestModel()
        dic = obj.to_dict()

        self.assertEqual(dic["name"], obj.name)
        self.assertEqual(dic["age"], obj.age)
        self.assertEqual(dic["is_active"], obj.is_active)


class Test(unittest.TestCase):
    """
    Test case for the instantiation and behavior of the BaseModel class.
    """
    def setUp(self):
        """
        Set up the test case with initial instances.
        """
        self.obj = BaseModel()
        self.dic = self.obj.to_dict()
        self.obj2 = BaseModel(**self.dic)

    def test_kwargs_instantiation(self):
        """
        Test instantiation of the BaseModel class using keyword arguments.
        """
        self.assertDictEqual(self.obj.to_dict(), self.obj2.to_dict())

        self.obj.name = "Test"
        self.obj.age = None

        obj3 = BaseModel(**self.obj.to_dict())
        self.assertDictEqual(self.obj.to_dict(), obj3.to_dict())
        self.assertEqual(obj3.name, "Test")
        self.assertIsNone(obj3.age)

    def test_dict_manipulation(self):
        """
        Test manipulation of the BaseModel instance's dictionary representation
        """
        dic = self.obj.to_dict()
        del dic["updated_at"]
        del dic["id"]
        self.assertNotIn("updated_at", dic)
        self.assertNotIn("id", dic)

        with patch("models.base_model.datetime") as mocked_datetime:
            with patch("uuid.uuid4", return_value="123"):
                now = datetime.now()
                mocked_datetime.now.return_value = now
                obj2 = BaseModel(**dic)

        self.assertIn("updated_at", obj2.to_dict())
        self.assertIsInstance(obj2.updated_at, datetime)
        self.assertEqual(obj2.updated_at, now)

        self.assertIn("id", obj2.to_dict())
        self.assertIsInstance(obj2.id, str)
        self.assertEqual(obj2.id, "123")

    def test_non_str_id(self):
        dic = {"id": 123456}
        obj = BaseModel(**dic)
        self.assertIsInstance(obj.id, str)
        self.assertEqual(obj.id, "123456")

    def test_class_attribute(self):
        """
        Test class attribute "__class__" in the BaseModel instance's dictionary
        """
        class_name = BaseModel.__name__

        # obj = BaseModel()
        # dic = obj.to_dict()
        # obj2 = BaseModel(**dic)

        self.assertIn("__class__", self.dic)
        self.assertEqual(self.dic["__class__"], class_name)

        self.assertEqual(self.obj2.__class__, BaseModel)
        self.assertNotEqual(self.obj2.__class__, class_name)

    def test_timestamps_are_datetime(self):
        """
        Test that timestamps in the BaseModel instance are of type datetime.
        """

        # obj = BaseModel()
        # dic = obj.to_dict()
        #
        # obj2 = BaseModel(**dic)

        self.assertIsInstance(self.obj.created_at, datetime)
        self.assertIsInstance(self.obj.updated_at, datetime)
        self.assertIsInstance(self.dic["created_at"], str)
        self.assertIsInstance(self.dic["updated_at"], str)

        self.assertIsInstance(self.obj2.created_at, datetime)
        self.assertIsInstance(self.obj2.updated_at, datetime)
        self.assertEqual(self.obj2.created_at, self.obj.created_at)
        self.assertEqual(self.obj2.updated_at, self.obj.updated_at)

    def test_updated_at_when_no_created_at(self):
        """
        Test the behavior of updated_at when created_at is not provided.
        """
        mocked_update_stamp = datetime.fromisoformat("2014-01-01")
        dic = {
            "id": "123",
            "updated_at": datetime.isoformat(mocked_update_stamp)
        }

        with patch("models.base_model.datetime") as mocked_datetime:
            now = datetime.now()
            mocked_datetime.now.return_value = now
            obj = BaseModel(**dic)

        self.assertEqual(obj.created_at, now)
        self.assertNotEqual(obj.updated_at, mocked_update_stamp)
        self.assertEqual(obj.updated_at, now)

    def test_updated_at_when_created_at(self):
        """
        Test the behavior of updated_at when created_at is provided.
        """
        mocked_create_stamp = datetime.fromisoformat("2014-01-01")
        dic = {
            "id": "123",
            "created_at": datetime.isoformat(mocked_create_stamp)
        }

        with patch("models.base_model.datetime") as mocked_datetime:
            now = datetime.now()
            mocked_datetime.now.return_value = now
            mocked_datetime.fromisoformat.return_value = mocked_create_stamp
            obj = BaseModel(**dic)

        self.assertEqual(obj.created_at, mocked_create_stamp)
        self.assertEqual(obj.updated_at, now)
