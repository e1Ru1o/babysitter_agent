from .base_agent import Agent

class Cell(Agent):
    '''
    Define an enviroment empty cell
    '''
    def push(xdir, ydir):
        return True
    