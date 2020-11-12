from .base_agent import Agent

class Robot(Agent):
    '''
    Enviroment babysitter robot
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carry = None

    def action(self):
        # //TODO: Implement
        pass

    