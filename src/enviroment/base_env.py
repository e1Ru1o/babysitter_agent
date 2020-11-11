from .error import EnvError

class Enviroment:
    """
    Enviroment for babys and the babysitter
    """
    def __init__(self, n, m, t, cicles=100):
        self.t      = t
        self.time   = 0
        self.agents = []
        self.size   = (n, m)
        self.end    = t * cicles
        self.env    = [[None] * m for _ in range(n)] 
        
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
            self.variate() 

    def set_agents(self, agents):
        self.agents = [agent(env=self) for agent in agents]

    def set(self, x, y, agent):
        '''
        Set agent position to (x, y)
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
        return '\n'.join(str(l) for l in self.env)