#!/usr/bin/python3
""" containing the Console Module """

import cmd
from textwrap import dedent


class HBNBCommand(cmd.Cmd):
    """ HBNB console commands and helper functions """

    prompt = "(hbnb) "

    @staticmethod
    def do_quit(s):
        """
        Quit command to exit the program
        """
        return True

    @staticmethod
    def do_EOF(s):
        """
        EOF command to exit the program
        """
        return True

    def help_quit(self):
        """
        Display help information for the 'quit' command
        """
        help_text = self.do_quit.__doc__
        if help_text:
            print(f"{dedent(help_text)}")

    def help_EOF(self):
        """
        Display help information for the 'EOF' command
        """
        help_text = self.do_EOF.__doc__
        if help_text:
            print(f"{dedent(help_text)}")

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
