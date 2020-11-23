from .robot import Robot
from .utils import get_path
from ..logging import Logger
from ..common import EnvTags as Tags

class Reactive(Robot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = Logger('App').getChild('Reactive')

    def action(self):
        steps = 1 if self.carry is None else 2
        self.logger.debug(f'Bot action started, {steps} steps available', 'action')
        for _ in range(steps):
            try:
                #perception
                perception = self.perceive()
                
                # action layers
                assert not self.cur_pos_action()
                assert not self.do_roller(perception)
                assert not self.do_baby(perception)
                assert not self.do_dirty(perception)
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
        self.move(roller.position, step)
        return True
            
    def do_baby(self, perception):
        # Precondition 
        data, dis, step = perception
        if self.carry or (not data[Tags.BABY]):
            return False

        # Body
        data = data[Tags.BABY]
        baby = self.find(data, dis)
    
        self.move(baby.position, step)
        # pick up the baby
        if self.position == baby.position:
            self.logger.info('Picking up a baby', 'action')
            self.carry = baby
            baby.lock(self)
        return True

    def do_dirty(self, perception):
         # Precondition 
        data, dis, step = perception
        if not data[Tags.DIRTY]:
            return False

        # Body
        data = data[Tags.DIRTY]
        dirty = self.find(data, dis)
    
        self.move(dirty.position, step)
        return True

    def move(self, pos, step):
        # do one move
        x, y = self.position
        (xdir, ydir) = get_path(pos, step)[0]
        self.set_position(x + xdir, y + ydir)
