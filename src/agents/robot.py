from .utils import bfs
from .base_agent import Agent
from ..common import EnvTags as Tags

valid = [Tags.EMPTY, Tags.DIRTY, Tags.ROLLER]
all_valid = [*valid, Tags.BABY]
options = [valid, all_valid]

class Robot(Agent):
    '''
    Enviroment babysitter robot
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carry       = None
        self.top         = float('inf')
        self.saved_pos   = None
        self.time        = 0
        self.last_change = 0

    def see(self):
        return self.env.env

    def perceive(self):
        if self.saved_pos:
            if self.saved_pos != self.position:
                self.top = min(self.top, self.time - self.last_change)
                self.last_change = self.time
        return bfs(self.position, self.see(), options[self.carry is None], self.top)
    