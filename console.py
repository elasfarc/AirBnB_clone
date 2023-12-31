#!/usr/bin/python3
""" containing the Console Module """

import cmd
import shlex
from textwrap import dedent
import re
import ast

from models import storage
from models.__supported_class import supported_classes, StorableEntity
from typing import Dict, List, Callable, Literal, Pattern, Any


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

    prompt = "(hbnb) "

    @format_docstring
    def do_create(self, s: str):
        """
        create command - Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        ex: create [className]
        """
        args = shlex.split(s)
        if self.has_valid_class(args):
            class_name = args[0]
            cls = supported_classes[class_name]
            new_instance = cls()
            new_instance.save()
            print(new_instance.id)

    @format_docstring
    def do_show(self, s: str):
        """
        show command - Prints the string representation of an instance
        based on the class name and id. Ex: $ show [className] [object_id].
        """
        self.operate_on_entity_if_valid(
            s, lambda stored_obj_key: print(storage.all()[stored_obj_key])
        )

    @format_docstring
    def do_destroy(self, s: str):
        """
        destroy command - Deletes an instance based on the class name and id
        Ex: $ destroy [className] [object_id].
        """

        def remove_object_and_save(storage_key: str):
            """
            Removes an object with the specified key from storage and
            saves the changes.

            Args:
            - storage_key (str):
                The key of the object to be removed from the storage.
            """
            storage.all().pop(storage_key)
            storage.save()

        self.operate_on_entity_if_valid(s, remove_object_and_save)

    @format_docstring
    def do_all(self, s: str):
        """
        all command - all: Prints all string representation of all instances
        based or not on the class name. Ex: $ all BaseModel or $ all.
        """
        if dic := self._get_all(s):
            print([str(entity) for entity in dic.values()])

    @format_docstring
    def do_update(self, s: str):
        """
        update: Updates an instance based on the class name and id
        by adding or updating attribute.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """

        def update_object_attribute(storage_key: str):
            """
            Updates the attribute of an object in storage
            with the specified key.
            Prints error message If the attribute name or value is missing.

            Args:
            - storage_key (str): The key of the object to be updated.
            """
            args = shlex.split(s)
            if len(args) < 3:
                print("** attribute name missing **")
            elif len(args) < 4:
                print("** value missing **")
            else:
                attr_name = args[2]
                value = str(args[3])
                # TODO correctly cast value
                obj = storage.all()[storage_key]
                obj[attr_name] = value
                storage.save()

        self.operate_on_entity_if_valid(s, update_object_attribute)

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

    @staticmethod
    def has_valid_class(args: List[str]) -> bool:
        """
        Check if the first element in the list of strings is a valid class name

        Args:
            args: The list of strings to check.

        Return: Whether the first element in the list is a valid class name.
        """
        if len(args) < 1:
            print("** class name missing **")
            return False
        if args[0] not in supported_classes:
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

    def operate_on_entity_if_valid(
            self, cmd_line: str, operation_fn: Callable[[str], None]
    ):
        """
        Executes an operation on a stored entity if the command line is valid.

        Args:
        - command_line:
            A string representing the command line input.
        - operation_function:
            A callable function to execute the operation on the stored entity.
            (stored_entity_key: str) -> None
        """
        args = shlex.split(cmd_line)
        if self.has_valid_class(args) and self.has_id(args):
            entity_key = self.get_entity_storing_key(args[0], args[1])
            if self.is_stored(key=entity_key):
                operation_fn(entity_key)

    def precmd(self, line):
        """
        Preprocess the command line before executing it.

        Args:
            line(str): The command line to process.

        Returns: The processed command line.
        """
        special_line = line.split(maxsplit=0)[0] if len(line.strip()) else ""
        special_cmds_pattern = \
            re.compile(
                r"([a-zA-Z0-9])*\.(all|show|destroy|update|count)\(.*?\)$"
            )
        match = special_cmds_pattern.fullmatch(special_line)
        if match:
            return self._parse_special_command(special_line)

        else:
            return cmd.Cmd.precmd(self, line)

    def _parse_special_command(self, line: str):
        """
            Parses a special command and returns the appropriate response.

            Args:
                line(str): The special command to parse.

            Returns: The response to the special command. (str)
        """

        cls_pattern = re.compile(r"^[a-zA-Z0-9]*\.")
        cmd_pattern = re.compile(r'.[a-zA-Z]*\(')
        args_pattern = re.compile(r'\(.*?\)$')

        cls = self.__parse_part(line, cls_pattern, "cls")
        command = self.__parse_part(line, cmd_pattern, "cmd")
        args = self.__parse_part(line, args_pattern, "args")
        formatted_args = " ".join(args.split(", "))

        parsed = f"{command} {cls} {formatted_args}"

        ##
        multi_updates_ptrn = re.compile(r'(?<=,)\s*\{.*?\}')
        if command == "update" and (match := multi_updates_ptrn.search(args)):
            raw_dict = match.group().strip()
            try:
                parsed_dict: Dict[str, Any] = ast.literal_eval(raw_dict)
                for k, v in parsed_dict.items():
                    object_id = args.split(',')[0]
                    self.do_update(f"{cls} {object_id} {k} {v}")
            except Exception:
                print("** Error: The multiple update command"
                      "is not used correctly. ** \n"
                      "<class name>.update(<id>, <dictionary representation>)"
                      )
        elif command == "count":
            self._do_count(cls)
        else:
            return parsed

        return ""

    @staticmethod
    def __parse_part(
        special_cmd: str, ptrn: Pattern, target: Literal["cmd", "cls", "args"]
    ):
        """
        Helper function to parse a part of a special command.

        Args:
            special_cmd : str
                The special command to parse.
            ptrn : Pattern
                The pattern to search for in the special command.
            target : Literal["cmd", "cls", "args"]
                The part of the special command to retrieve.

        Returns: The requested part of the special command. (str)
        """
        match = ptrn.search(special_cmd)
        if match:
            if target == "cmd" or target == "args":
                # substring_inside_match
                return special_cmd[match.start() + 1: match.end() - 1]
            elif target == "cls":
                # substring_before_match_end
                return special_cmd[:match.end() - 1]

        return ''

    def _get_all(self, s: str):
        """
        Get all objects of a certain class or all objects
        if no class is provided.

        Args:
            s (str): The command string.

        Returns:
            Dict: A dictionary mapping object IDs to objects.
            None: If there is no valid class provided.
        """
        args = shlex.split(s)
        is_class = bool(len(args))

        if is_class:
            if self.has_valid_class(args):
                class_name = args[0]
                dic = self.__filter_by_prefix(storage.all(), class_name)
            else:
                return None
        else:
            dic = storage.all()

        return dic

    def _do_count(self, s):
        """
        Print the Count the number of objects of a certain class or
        all objects if no class is provided.

        Args:
            s (str): The command string.

        Returns:
            None
        """
        dic = self._get_all(s)
        if dic:
            print(len(dic))


if __name__ == "__main__":
    HBNBCommand().cmdloop()
