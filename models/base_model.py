#!/usr/bin/python3
"""
module containing the class BaseModel
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Union
import models


def handle_timestamp_update(timestamp: Any) -> Union[None, datetime]:
    """
    Handle timestamp update.

    Args:
    - timestamp (Any): The timestamp to be handled.
    It can be of any type.

    Returns:
    - Any: The handled timestamp.
        Returns None if the input timestamp is not a valid datetime object
        or a valid ISO format string.

    Example:
    >>> handle_timestamp_update(datetime.now())
    datetime.datetime(...)

    >>> handle_timestamp_update("2024-01-01T12:34:56")
    datetime.datetime(...)

    >>> handle_timestamp_update("invalid_timestamp")
    None
    """
    if not isinstance(timestamp, type(datetime.now())):
        try:
            timestamp = datetime.fromisoformat(str(timestamp))
        except ValueError:
            return None
    return timestamp


class BaseModel:
    """
    A base class representing a model with unique identifier and timestamp
    attributes.
    """

    def __init__(self, **kwargs):
        """
        Initialize a new instance of the BaseModel class.

        Args:
            @kwargs: Keyword arguments

        Attributes:
        - id (str): A unique identifier generated using the UUID4 algorithm.
        - created_at (datetime): The timestamp indicating
            when the instance is created.
        - updated_at (datetime): The timestamp indicating
            when the instance is last updated.


        Description:
         This method iterates over the keyword arguments and sets the instance
         attributes accordingly. If "id" is not provided, it is generated using
         the UUID4 algorithm. If "created_at" is not provided,
         it is set to the current timestamp.
         If "updated_at" is provided, but "created_at" is not, "updated_at"
         is set to the value of "created_at". If neither "updated_at" nor
         "created_at" is provided, both are set to the current timestamp.
        """

        is_new_instance = not bool(len(kwargs))
        if is_new_instance:
            now = datetime.now()
            u_id = uuid.uuid4()
            self.id = str(u_id)

            # TODO check string is iso-format before converting
            self.created_at = now
            self.updated_at = now

            models.storage.new(self)

        else:
            for key, value in kwargs.items():
                self[key] = value

    def __setitem__(self, key, value):
        """
        Set the value of an attribute in the instance

        Args:
            @key: The key specifying the attribute to be set
            @value: The value to be assigned to the specified attribute

        Description:
            This method sets the value of the specified attribute in the
            instance, excluding reserved keys like "__class__", "created_at",
            "updated_at", and "id".

        """

        if key != "__class__":
            if key == "created_at" or key == "updated_at":
                self._set_timestamp(key, value)
            else:
                setattr(self, key, value)

    def __setattr__(self, name, value):
        """
        Set attribute value.

        This method is called when an attribute value is assigned
        to an instance.
            - If the attribute is 'created_at' or 'updated_at', it delegates
                to the _set_timestamp method.
            - If the attribute is 'id', it converts the value to a string.
            - For other attributes, it uses
                the default behavior (object.__setattr__)

        Args:
        - self: The instance itself.
        - name (str): The name of the attribute being set.
        - value: The value to be assigned to the attribute.

        """
        if name == "created_at" or name == "updated_at":
            return self._set_timestamp(name, value)
        if name == "id":
            value = str(value)

        object.__setattr__(self, name, value)

    def _set_timestamp(self, timestamp_key: str, timestamp_value: Any):
        """
        Set timestamp attribute value. ('created_at' or 'updated_at').
            - If the timestamp is valid,
                it updates the attribute with the new value.
            - If the timestamp is not valid, it prints an error message.

        Args:
        - self: The instance itself.
        - timestamp_key (str): ('created_at' or 'updated_at').
        - timestamp_value (Any):
            The value to be assigned to the timestamp attribute.
        """
        updated_timestamp = handle_timestamp_update(timestamp_value)
        if updated_timestamp:
            object.__setattr__(self, timestamp_key, updated_timestamp)
        else:
            print("Failed to update datetime. Invalid input.")

    def save(self):
        """
        Update the 'updated_at' attribute to the current date and time.

        This method is called to mark the instance as updated,
        refreshing the 'updated_at' timestamp to the current date and time.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self) -> Dict[str, Any]:
        """
        to_dict - Converts the object to a dictionary.

        Description:
        This method converts the object to a dictionary representation.
        It iterates through the instance's attributes,
        handling timestamp keys by converting their values to ISO format using
        the `to_iso_format` function. The resulting dictionary includes all
        instance attributes and the class name.

        Return:
        A dictionary representation of the object,
        where timestamp values are converted to ISO format.

        """
        def to_iso_format(dt: datetime) -> str:
            """
            to_iso_format - Converts a datetime object to ISO format.

            Parameters:
            - dt: A datetime object.

            Return:
            A string representing the ISO format of the input datetime.

            """
            return dt.isoformat()
        timestamp_keys = ["created_at", "updated_at"]

        obj_dict = {
            key: value if key not in timestamp_keys else to_iso_format(value)
            for key, value in self.__dict__.items()
        }

        obj_dict.update(__class__=self.__class__.__name__)

        return obj_dict

    def __str__(self):
        """
        __str__ - Returns a string representation of the object.

        Return:
        A string representing the object, formatted as
        "[ClassName] (ObjectID) {__dict__}".
        """
        cls_name = self.__class__.__name__
        return f"[{cls_name}] ({self.id}) {self.__dict__}"
