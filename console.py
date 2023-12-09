#!/usr/bin/python3
""" containing the Console Module """

import cmd
from textwrap import dedent
from models.base_model import BaseModel
from models.virtual import JsonStorableEntity
from models import storage
from typing import Dict, Type


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
    """ HBNB console commands and helper functions """

    __classes: Dict[str, Type[JsonStorableEntity]] = {
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
        if len(args) < 1:
            print("** class name missing **")
        elif (cls_name := args[0]) not in self.__classes:
            print("** class doesn't exist **")
        else:
            obj = self.__classes[cls_name]()
            obj.save()
            print(obj.id)

    @format_docstring
    def do_show(self, s: str):
        """
        show command - Prints the string representation of an instance
        based on the class name and id. Ex: $ show [className] [object_id].
        """
        args = s.split()
        if len(args) < 1:
            print("** class name missing **")
        elif (cls_name := args[0]) not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            obj_id = args[1]
            key = f"{cls_name}.{obj_id}"
            objects = storage.all()
            print("** no instance found **" if key not in objects else
                  f"{objects[key]}")

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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
