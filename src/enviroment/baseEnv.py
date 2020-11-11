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
        
    def run(*args, **kwargs):
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

    def set_agents(agents):
        self.agents = [agent(env=self) for agent in agents]

    def vaid_pos(x, y):
        n, m = self.size
        return (0 <= x < n) and (0 <= y < m)

    def variate(*args, **kwargs):
        '''
        Method for define how an env varite
        '''
        pass

    def stop():
        '''
        Update the enviroment status 
        '''
        pass