from .toy import Toy
from .cell import Cell
from .baby import Baby
from .robot import Robot
from .roller import Roller
from .reactive import Reactive
from .proactive import Proactive
from ..common import finder, AgentError

robots = [
    Reactive,
    Proactive,
]

def get_robot(name):
    return finder(robots, name, AgentError(f'Robot `{name}` implementation not found'))
