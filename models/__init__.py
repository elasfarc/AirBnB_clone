#!/usr/bin/python3
"""
init FileStorage instance for the application
"""
from models.engine.file_storage import FileStorage

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models.city import City

storage = FileStorage()

storage.reload()
