#!/usr/bin/python3
""" containing the Console Module """

import cmd
from textwrap import dedent


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

    prompt = "(hbnb) "

    @format_docstring
    def do_quit(self, _):
        """
        Quit command to exit the program
        """
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
