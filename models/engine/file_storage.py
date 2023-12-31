#!/usr/bin/python3
"""
module containing the class FileStorage
"""

import json
from os import path
from models.__supported_class import supported_classes, StorableEntity
from typing import Dict, Any


SavedObjects = Dict[str, StorableEntity]

# T = TypeVar("T", bound=JsonStorableEntity)


class FileStorage:
    """
    Manages storage and retrieval of StorableEntity objects in a file.
    """
    __file_path = "db.json"
    __objects: Dict[str, StorableEntity] = {}

    def all(self):
        """
        Retrieves all stored objects.

        Return:
            dict: A dictionary containing all stored objects.
        """
        return self.__objects

    def new(self, obj: StorableEntity):
        """
        Adds a new object to storage.

        Args:
            obj: The StorableEntity object to be added.

        Raises:
            TypeError: If the object lacks required attributes.
        """
        # TODO check __class__ in __classes
        if not all([hasattr(obj, attr) for attr in ["id", "__class__"]]
                   ) or not hasattr(obj.__class__, "__name__"):
            raise TypeError(f"obj must have attributes named id, __class__")
        cls_name = obj.__class__.__name__
        key = f"{cls_name}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        Saves stored objects to a file in JSON format.
        """

        dictionaries = {
            key: obj.to_dict() for key, obj in self.__objects.items()
        }
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(dictionaries, file)

    @staticmethod
    def __from_json_str(json_str: str) -> Dict[str, Dict[str, Any]]:
        """
        Converts a JSON string to a dictionary.

        Args:
            json_str: The JSON string to be converted.

        Return:
            dict: A dictionary representation of the JSON data.
        """
        if not json_str:
            return {}
        return json.loads(json_str)

    @staticmethod
    def __instantiate_from_dict(
           cls_name: str, dic: Dict[str, Any]
    ) -> StorableEntity:
        """
        Instantiates a StorableEntity object from a dictionary.

        Args:
            cls_name: The name of the class to instantiate.
            dic: The dictionary containing object data.

        Return:
            StorableEntity: An instance that adheres to
            StorableEntity virtual class.
        """
        cls = supported_classes[cls_name]
        # cls = globals()[cls_name]
        return cls(**dic)

    def reload(self):
        """
        Reloads stored objects from the file.
        """
        if path.exists(self.__file_path):
            with open(self.__file_path, mode="r", encoding="utf-8") as file:
                json_str = file.read()

            loaded_dictionaries = self.__from_json_str(json_str)
            self.__objects = {
                key: self.__instantiate_from_dict(
                    key.split(".")[0], dictionary
                )
                for key, dictionary in loaded_dictionaries.items()
            }
