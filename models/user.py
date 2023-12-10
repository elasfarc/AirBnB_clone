#!/usr/bin/python3
"""module containing the User class"""

import models.base_model as base_model


class User(base_model.BaseModel):
    """
    Represents a user account.

    Attributes:
        email: The user's email address.
        password: The user's password.
        first_name: The user's first name.
        last_name: The user's last name.
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
