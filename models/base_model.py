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

    def __init__(self):
        """
        Initialize a new instance of the BaseModel class.

        Attributes:
        - id (str): A unique identifier generated using the UUID4 algorithm.
        - created_at (datetime): The timestamp indicating
            when the instance is created.
        - updated_at (datetime): The timestamp indicating
            when the instance is last updated.
        """
        now = datetime.now()
        self.id = str(uuid.uuid4())
        self.created_at = now
        self.updated_at = now

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
