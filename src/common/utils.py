import random
from enum import Enum

class EnvTags(Enum):
    EMPTY, DIRTY, TOY, ROLLER, FULL_ROLLER, BABY, BOT = range(7) 
    
DIR = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
ALL_DIR = [*DIR, (1, 1), (1, -1), (-1, 1), (-1, -1)]

def random_dir(data=DIR):
    return random.choice(data)