from .robot import Robot
from .utils import get_path
from ..logging import Logger
from ..common import EnvTags as Tags, DIR

class Proactive(Robot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = Logger('App').getChild('Proactive')
        self.plan   = None

    def action(self):
        steps = 1 if self.carry is None else 2
        self.logger.debug(f'Bot action started, {steps} steps available', 'action')
        for _ in range(steps):
            try:
                while True:
                    # current position action
                    assert not self.cur_pos_action()

                    # use planed actions
                    if self.plan:
                        assert not self.do_planned_action()
                    
                    # New plan needed
                    assert self.build_new_plan()
            except AssertionError: pass
            self.saved_pos = self.position
            if self.carry is None: break
        self.time += 1
        
    def cur_pos_action(self):
        agent = self.env.get(*self.position, -2)
        if self.carry and (agent.tag() == Tags.ROLLER):
            self.logger.info('Leaving the baby...', 'action')
            self.carry = None
            agent.lock(self)
            return True
        if agent.tag() == Tags.DIRTY:
            self.logger.info('Cleaning the dirty...', 'action')
            self.env.dirty -= 1
            agent.tag(Tags.EMPTY)
            return True
        return False

    def do_planned_action(self):
        pos, tag = self.plan.pop(0)
        agent = self.env.get(*pos)
        adyacent = [(pos[0] + x, pos[1] + y) for x, y in DIR[1:]]
        if (agent.tag() != tag) or (not self.position in adyacent):
            self.logger.info('Agent planification failure', 'action')
            return False
        self.set_position(*pos)
        if tag == Tags.BABY:
            self.logger.info('Picking up a baby', 'action')
            self.carry = agent
            agent.lock(self)
        return True

    def build_new_plan(self):
        #perception
        perception = self.perceive()
        try:
            #goal layers
            assert not self.do_roller(perception)
            assert not self.do_baby(perception)
            assert not self.do_dirty(perception)
            return False
        except AssertionError:
            return True

    def find(self, data, dis):
        # Select the nearest agent
        a, b = data[0]
        for x, y in data:
            if dis[x][y] < dis[a][b]:
                a, b = x, y
        agent = self.env.get(a, b)
        self.logger.info(f'Nearest {str(agent).strip()} found', 'action')
        return self.env.get(a, b)

    def do_roller(self, perception):
        # Precondition
        if self.carry is None:
            return False

        # Body
        data, dis, step = perception
        data = data[Tags.ROLLER]
        if not data:
            self.logger.debug('Search for a roller failed', 'action')
            return False        
        
        roller = self.find(data, dis)
        self.save_plan(roller.position, step)
        return True
            
    def do_baby(self, perception):
        # Precondition 
        data, dis, step = perception
        if self.carry or (not data[Tags.BABY]):
            return False

        # Body
        data = data[Tags.BABY]
        baby = self.find(data, dis)
    
        self.save_plan(baby.position, step)
        return True

    def do_dirty(self, perception):
         # Precondition 
        data, dis, step = perception
        if not data[Tags.DIRTY]:
            return False

        # Body
        data = data[Tags.DIRTY]
        dirty = self.find(data, dis)
    
        self.save_plan(dirty.position, step)
        return True

    def save_plan(self, pos, step):
        self.plan = []
        x, y = self.position
        for xdir, ydir in get_path(pos, step): 
            x, y = x + xdir, y + ydir
            self.plan.append(((x, y), self.env.get(x, y).tag()))
