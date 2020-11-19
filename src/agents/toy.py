from .base_agent import Agent
from ..common import EnvError, EnvTags

class Toy(Agent):
    '''
    Toy agent represents an enviroment obstacle
    '''
    def push(self, xdir, ydir, agent):
        try:
            assert agent.tag() in [EnvTags.BABY, EnvTags.TOY] 
            x, y = self.position
            x, y = x + xdir, y + ydir
            assert self.env.get(x, y).push(xdir, ydir, self)
            self.set_position(x, y)
            return True
        except AssertionError: pass
        except EnvError: pass
        return False