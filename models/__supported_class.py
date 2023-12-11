from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models.city import City

from models.virtual import StorableEntity

from typing import Dict, Type


supported_classes: Dict[str, Type[StorableEntity]] = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }
