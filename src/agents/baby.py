import random
from .error import AgentError
from .base_agent import Agent
from ..enviroment import EnvTags, EnvError
from .utils import random_dir, select, ALL_DIR
from ..logging import Logger

class Baby(Agent):
    '''
    Baby represent the enviroment baby
    '''
    def __init__(self, **kwargs):
        kwargs['logger'] = 'Baby'
        super().__init__(**kwargs)
        self.carrier = None

    def lock(self, agent):
        try:
            assert self.active(), "Agent is already locked"
            assert agent.tag() == EnvTags.BOT, "Agent can't be locked by a %s" % str(agent)
        except AssertionError as e:
            raise AgentError(str(e))
        self.logger.info('Baby locked succesfully', 'lock')
        self.carrier = agent
        self.active(False)
        self.env.unset(self)

    def release(self, agent):
        try:
            assert not self.active(), "Agent is not locked"
            assert self.carrier != agent, "Agent can't be released"
        except AssertionError as e:
            raise AgentError(str(e))
        self.logger.info('Baby realeased succesfully', 'realease')
        self.carrier = None
        self.active(True)
        self.set_position(*agent.position)

    def set_position(self, x, y):
        if self.active():
            super().set_position(x, y)

    def action(self):
        if not self.active():
            return
        xdir, ydir = random_dir()
        x, y = self.position
        old_pos = self.position
        x, y = x + xdir, y + ydir
        try:
            assert self.env.get(x, y).push(xdir, ydir, self)
            self.set_position(x, y)
        except AssertionError: pass
        except EnvError: pass
        x, y = old_pos
        neighbors = []
        for xdir, ydir in ALL_DIR:
            pos = [x + xdir, y + ydir]
            if self.env.valid_pos(*pos):
                neighbors.append(self.env.get(*pos))
        empty = select(neighbors, EnvTags.EMPTY)
        baby_cant = len(select(neighbors, EnvTags.BABY))
        dirty = [0, 1, 3, 6][min(baby_cant, 3)]
        dirty = random.randint(0, min(dirty, len(empty)))
        self.logger.debug(f'Adding {dirty} new dirties', 'action')
        for cell in random.sample(empty, dirty):
            cell.tag(EnvTags.DIRTY)
        self.env.dirty += dirty



