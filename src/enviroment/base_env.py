from .error import EnvError

class Enviroment:
    """
    Enviroment for babys and the babysitter
    """
    def __init__(self, n, m, t, cicles=100):
        self.t      = t
        self.time   = 0
        self.agents = []
        self.data   = {}
        self.status = None
        self.size   = (n, m)
        self.end    = t * cicles
        self.clear()
        
    def clear(self):
        '''
        Create an empty world
        '''
        n, m = self.size
        self.env = [[[] for _ in range(m)] for _ in range(n)] 

    def run(self):
        '''
        Execute the enviroment pipeline
        '''
        for agent in self.agents:
            agent.action()
        self.time += 1
        if self.stop():
            return self.status
        if self.t and self.time % self.t == 0:
            self.variate(**self.data) 

    def set(self, x, y, agent):
        '''
        Set agent position to (x, y)
        '''
        pass

    def unset(self, agent):
        '''
        Remove the agent
        '''
        pass

    def get(self, x, y):
        '''
        Get the env pos (x, y)
        '''
        if not self.valid_pos(x, y):
            raise EnvError('Invalid position')
        return self.env[x][y]

    def valid_pos(self, x, y):
        n, m = self.size
        return (0 <= x < n) and (0 <= y < m)

    def variate(self, **kwargs):
        '''
        Method for define how an env varite
        '''
        pass

    def stop(self):
        '''
        Update the enviroment status 
        '''
        pass

    def __repr__(self):
        n, m = self.size
        return '\n'.join((''.join(str(self.get(i, j)) for j in range(m)) for i in range(n)))