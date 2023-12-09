#!/usr/bin/python3
""" containing the Console Module """

import cmd
from textwrap import dedent
from models.base_model import BaseModel
from models.virtual import StorableEntity
from models import storage
from typing import Dict, Type, Union


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
        if factory := self.__get_cls_arg(s):
            new_instance = factory()
            new_instance.save()
            print(new_instance.id)

    @format_docstring
    def do_show(self, s: str):
        """
        show command - Prints the string representation of an instance
        based on the class name and id. Ex: $ show [className] [object_id].
        """
        key = self.__get_entity_key(s)
        if key:
            if key in (objects := storage.all()):
                print(f"{objects[key]}")
            else:
                print("** no instance found **")

    @format_docstring
    def do_destroy(self, s: str):
        """
        destroy command - Deletes an instance based on the class name and id
        Ex: $ destroy [className] [object_id].
        """
        key = self.__get_entity_key(s)
        if key:
            if key in (objects := storage.all()):
                objects.pop(key)
                storage.save()
            else:
                print("** no instance found **")

    @format_docstring
    def do_all(self, s: str = None):
        """
        all command - all: Prints all string representation of all instances
        based or not on the class name. Ex: $ all BaseModel or $ all.
        """

        is_class = bool(len(s.split()))

        if is_class:
            if cls := self.__get_cls_arg(s):
                prefix = cls.__name__
                dic = self.filter_by_prefix(storage.all(), prefix)
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

    @classmethod
    def __get_cls_arg(cls, s: str) -> Union[Type[StorableEntity], None]:
        """Return the class object corresponding to the given string argument.

        If the class does not exist, in the supported classes dictionary
        this method will print an error message and return `None`.

        Args:
            s: A string representing the whole provided line to the console.

        Returns:
            The class object corresponding to the given string argument,
            or `None` if the class does not exist.
        """
        args = s.split()
        if len(args) < 1:
            return print("** class name missing **")
        elif (first_arg := args[0]) not in cls.__classes:
            return print("** class doesn't exist **")
        else:
            return cls.__classes[first_arg]

    @staticmethod
    def __get_instance_id_arg(s: str):
        """Extract the instance ID from the given string argument.

        Assuming the object_id is the second arg
        "<class_name> <instance_id> <other arguments>"
        where `<instance_id>` is the unique identifier of the instance.
        This method returns the extracted instance ID as a string,
        or prints an error message and returns `None`
        if no valid instance ID was found.

        Args:
            s: A string representing the whole provided line to the console.

        Returns:
            The extracted instance ID as a string,
            or `None` if no valid instance ID was found.
        """
        args = s.split()
        if len(args) < 2:
            print("** instance id missing **")
            return None
        else:
            return args[1]

    @classmethod
    def __get_entity_key(cls, s: str) -> str | None:
        """Generate a key for the entity based on its type and ID.

        The generated key has the format "<type>.<ID>",
        where `<type>` is the fully qualified name of the entity's class,
        and `<ID>` is the entity's unique identifier within that class.

        Args:
            s: A string representation of the entity, including its type and ID

        Returns:
            The generated entity key,
            or `None`if the entity could not be identified.
        """
        if not (cls_arg := cls.__get_cls_arg(s)):
            return None
        if not (obj_id := cls.__get_instance_id_arg(s)):
            return None

        return f"{cls_arg.__name__}.{obj_id}"

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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
