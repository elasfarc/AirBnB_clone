"""
module containing the class BaseModel
"""

import uuid
from datetime import datetime
from typing import Any, Dict, TypedDict


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

        for key, value in kwargs.items():
            self[key] = value

        now = datetime.now()
        u_id = uuid.uuid4() if "id" not in kwargs else kwargs["id"]
        self.id = str(u_id)

        # TODO check string is iso-format before converting
        self.created_at = now if "created_at" not in kwargs else (
            datetime.fromisoformat(kwargs["created_at"]))

        missing_timestamps = any([key not in kwargs for key in
                                  ["updated_at", "created_at"]])
        self.updated_at = now if missing_timestamps else (
            datetime.fromisoformat(kwargs["updated_at"]))

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
        if key not in ["__class__", "created_at", "updated_at", "id"]:
            setattr(self, key, value)

    def save(self):
        """
        Update the 'updated_at' attribute to the current date and time.

        This method is called to mark the instance as updated,
        refreshing the 'updated_at' timestamp to the current date and time.
        """
        self.updated_at = datetime.now()

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
