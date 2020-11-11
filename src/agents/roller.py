from .error import AgentError
from .base_agent import Agent
from ..enviroment import EnvTags

class Roller(Agent):
    def lock(self, agent):
        try:
            assert self.active(), 'Agent is already locked'
            assert agent.tag() != EnvTags.BOT, 'Invalid lock attempt'
            self.tag(EnvTags.FULL_ROLLER)
            self.active(False)
        except AssertionError as e:
            raise AgentError(str(e))

