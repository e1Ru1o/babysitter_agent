from .base_agent import Agent
from ..enviroment import EnvTags

class Cell(Agent):
    '''
    Define an enviroment empty/dirty cell
    '''
    def push(*args):
        return self.tag() == EnvTags.EMPTY
    