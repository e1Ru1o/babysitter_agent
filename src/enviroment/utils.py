from enum import Enum

class EnvTags(Enum):
    EMPTY, BABY, BOT, TOY, DIRTY, ROLLER, FULL_ROLLER = range(7) 

class EnvStatus(Enum):
    RUNNING, FIRED, CLEAN, TLE = range(4) 
