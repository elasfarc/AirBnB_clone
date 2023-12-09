#!/usr/bin/python3
"""
init FileStorage instance for the application
"""
from models.engine.file_storage import FileStorage

storage = FileStorage()

storage.reload()
