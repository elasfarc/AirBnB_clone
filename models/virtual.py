#!/usr/bin/python3
"""
module containing virtual abstract classes.
"""
from typing import Protocol, Dict, Any


class StorableEntity(Protocol):
    """
    (virtual class)
    Represents an entity that can be stored in JSON format.
    Classes that adhere to this class should implement at least these methods
    """
    id: str

    def __init__(self, **kwargs):
        """
        Initialize a new instance.
        Classes that adhere to this class should implement this method
        and support keyword-args to instantiate new instances
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the entity to a dictionary.

        Return:
            dict: A dictionary representation of the entity.
        """
        pass

    def save(self):
        """
        provides a mechanism to save the entity object
        """
        pass
