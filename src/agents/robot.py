from .utils import bfs
from .base_agent import Agent
from ..common import EnvTags as Tags

valid = [Tags.EMPTY, Tags.DIRTY, Tags.ROLLER]
all_valid = [*valid, Tags.BABY]

class Robot(Agent):
    '''
    Enviroment babysitter robot
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carry = None

    def see(self):
        return self.env.env

    def perceive(self):
        return bfs(self.position, self.see(), [valid, all_valid][self.carry is None])
        

    