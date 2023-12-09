#!/usr/bin/python3
""" containing the Console Module """

import cmd
from textwrap import dedent
from models.base_model import BaseModel
from models.virtual import StorableEntity
from models import storage
from typing import Dict, Type, List


def format_docstring(fn):
    """
    a decorator to format the docstring
    removes leading whitespace

    Args:
        fn (function): the function to be formatted
    """
    fn.__doc__ = dedent(fn.__doc__).strip() + "\n"
    return fn


class HBNBCommand(cmd.Cmd):
    """HBNB console commands and helper functions"""

    __classes: Dict[str, Type[StorableEntity]] = {
        'BaseModel': BaseModel
    }

    prompt = "(hbnb) "

    @format_docstring
    def do_create(self, s: str):
        """
        create command - Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        ex: create [className]
        """
        args = s.split()
        if self.has_valid_class(args):
            class_name = args[0]
            cls = self.__classes[class_name]
            new_instance = cls()
            new_instance.save()
            print(new_instance.id)

    @format_docstring
    def do_show(self, s: str):
        """
        show command - Prints the string representation of an instance
        based on the class name and id. Ex: $ show [className] [object_id].
        """
        args = s.split()
        if self.has_valid_class(args) and self.has_id(args):
            key = self.get_entity_storing_key(args[0], args[1])
            if self.is_stored(key=key):
                print(storage.all()[key])

    @format_docstring
    def do_destroy(self, s: str):
        """
        destroy command - Deletes an instance based on the class name and id
        Ex: $ destroy [className] [object_id].
        """
        args = s.split()
        if self.has_valid_class(args) and self.has_id(args):
            key = self.get_entity_storing_key(args[0], args[1])
            if self.is_stored(key=key):
                storage.all().pop(key)
                storage.save()

    @format_docstring
    def do_all(self, s: str):
        """
        all command - all: Prints all string representation of all instances
        based or not on the class name. Ex: $ all BaseModel or $ all.
        """

        args = s.split()
        is_class = bool(len(args))

        if is_class:
            if self.has_valid_class(args):
                class_name = args[0]
                dic = self.__filter_by_prefix(storage.all(), class_name)
            else:
                return
        else:
            dic = storage.all()
        print([str(entity) for entity in dic.values()])

    @format_docstring
    def do_quit(self, _):
        """Quit command to exit the program"""
        return True

    @format_docstring
    def do_EOF(self, _):
        """
        EOF command to exit the program
        """
        return True

    def emptyline(self):
        """
        emptyline - Handle an empty input line

        Description:
            called when an empty line is entered. It overrides the default
            behavior to do nothing.
        """
        pass

    @staticmethod
    def __filter_by_prefix(dictionary: Dict[str, StorableEntity], prefix: str):
        """Filter a dictionary by a given prefix.

        Return a new dictionary containing only the items whose
        keys start with the given prefix.

        Parameters:
            dictionary : The original dictionary to filter.
            prefix: The prefix to search for in the keys of the dictionary.

        Returns:
            dict: A filtered version of the original dictionary containing
            only the items whose keys start with the given prefix.
        """
        return {k: v for k, v in dictionary.items() if k.startswith(prefix)}

    def has_valid_class(self, args: List[str]) -> bool:
        """
        Check if the first element in the list of strings is a valid class name

        Args:
            args: The list of strings to check.

        Return: Whether the first element in the list is a valid class name.
        """
        if len(args) < 1:
            print("** class name missing **")
            return False
        if args[0] not in self.__classes:
            print("** class doesn't exist **")
            return False
        return True

    @staticmethod
    def has_id(args: List[str]) -> bool:
        """
        Check if the second element in the list of strings is an instance id.

        Args:
            args: The list of strings to check.

        Return: Whether the second element in the list is an instance id.
        """
        if len(args) < 2:
            print("** instance id missing **")
            return False
        else:
            return True

    @staticmethod
    def get_entity_storing_key(entity_cls: str, entity_id: str):
        """
        Return the storing key for an entity.

        Args:
            entity_cls: The class of the entity.
            entity_id: The id of the entity.
        """
        return f"{entity_cls}.{entity_id}"

    @classmethod
    def is_stored(cls, **kwargs) -> bool:
        """
        Check if an entity is stored in the database.

        Args:
            kwargs: Keyword arguments specifying the entity to check.
            ["key", "entity_cls", "entity_id"]
        """
        if "key" in kwargs:
            key = kwargs["key"]
        else:
            key = cls.get_entity_storing_key(
                kwargs["entity_cls"], kwargs["entity_id"]
            )

        if key not in (storage.all()):
            print("** no instance found **")
            return False
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
