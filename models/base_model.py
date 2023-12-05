"""
module containing the class BaseModel
"""

import uuid
from datetime import datetime


class BaseModel:
    """
    A base class representing a model with unique identifier and timestamp attributes.
    """

    def __init__(self):
        """
        Initialize a new instance of the BaseModel class.

        Attributes:
        - id (str): A unique identifier generated using the UUID4 algorithm.
        - created_at (datetime): The timestamp indicating when the instance is created.
        - updated_at (datetime): The timestamp indicating when the instance is last updated.
        """
        now = datetime.now()
        self.id = str(uuid.uuid4())
        self.created_at = now
        self.updated_at = now

    def save(self):
        """
        Update the 'updated_at' attribute to the current date and time.

        This method is called to mark the instance as updated, refreshing the 'updated_at'
        timestamp to the current date and time.
        """
        self.updated_at = datetime.now()
