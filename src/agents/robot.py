from .base_agent import Agent
from .utils import bfs, get_path
from ..enviroment import EnvTags as Tags

valid = [Tags.EMPTY, Tags.DIRTY, Tags.ROLLER, Tags.BABY]

class Robot(Agent):
    '''
    Enviroment babysitter robot
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carry = None

    def see(self):
        return self.env.data

    def perceive(self):
        return bfs(self.position, self.see(), valid)
        

    