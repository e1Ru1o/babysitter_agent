from .error import AgentError

class Agent:
    '''
    Class for enviroment entities
    '''
    def __init__(self, env=None, tag=None, enable=True):
        self.env        = env
        self.position   = None
        self.active(enable)
        self.tag(tag)

    def set_position(self, x, y):
        '''
        Set the agent env position
        '''
        self.env.set(x, y, self)
        return self

    def push(self, xdir, ydir, agent):
        '''
        Define how an agent acts when is being pushed byt otrher agent
        '''  
        return False

    def action(self):
        '''
        Defines how an agent acts
        '''
        pass

    def active(self, enable=None):
        if not enable is None:
            self.enable = enable
        return self.enable

    def tag(self, tag=None):
        if not tag is None:
            self.agent_tag = tag
        return self.agent_tag

    def lock(self, agent):
        '''
        Define what happens when an extrernal agent is trying to lock the current one
        '''
        raise AgentError("Agent can't be locked")

    def release(self, agent):
        '''
        Define what happens when an extrernal agent is trying to release the current one
        '''
        raise AgentError("Agent can't be released")

    def __repr__(self):
        name = self.agent_tag.name
        sz = 11 - len(name)
        return " %s%s " % (name, ' ' * sz)
