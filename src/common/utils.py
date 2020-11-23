import random
from enum import Enum

class EnvTags(Enum):
    EMPTY, DIRTY, TOY, ROLLER, FULL_ROLLER, BABY, BOT = range(7) 
    
DIR = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
ALL_DIR = [*DIR, (1, 1), (1, -1), (-1, 1), (-1, -1)]

def random_dir(data=DIR):
    return random.choice(data)

def finder(data, name, error):
    for element in data:
        if element.__name__.lower() == name.lower():
            return element
    raise error

def fill_with(data, callback):
    for x in data:
        yield x
    while True:
        yield callback()
        