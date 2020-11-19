from .toy import Toy
from .cell import Cell
from .baby import Baby
from .robot import Robot
from .roller import Roller
from .reactive import Reactive
from .proactive import Proactive

robots = [
    Reactive,
    Proactive,
]

def get_robot(name):
    for robot in robots:
        if robot.__name__.lower() == name.lower():
            return robot
    raise AgentError(f'Robot `{name}` implementation not found')