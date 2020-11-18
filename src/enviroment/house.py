import random
from .error import EnvError
from .base_env import Enviroment
from ..agents import Baby, Robot, Cell, Toy, Roller, DIR
from .utils import EnvTags, EnvStatus, generate, fill_agents, agent_maker as maker
from ..logging import Logger

class House(Enviroment):
    def __init__(self, n, m, t, babies, toys, dirty, cicles):
        super().__init__(n, m, t, cicles, 'House')
        self.babies  = babies
        
        self.logger.debug("Checking if the env is feasible", 'init')
        cells       = n * m
        self.dirty  = int((dirty * cells) / 100)
        self.toys   = int((toys * cells)  / 100)
        try:
            assert 2 * babies + self.dirty + self.toys + 1 <= cells
            assert babies <= n or babies <= m
        except AssertionError:
            raise EnvError('Initial env is not feasible')
        self.variate()

    def build_data(self, **kwargs):
        self.data = kwargs

    def run(self):
        self.logger.debug('Setting the status to RUNNING', 'run')
        self.status = EnvStatus.RUNNING
        return super().run()

    def variate(self, rollers=None, toys=None, babies=None, dirty=None, bot=None):
        # New empty table
        self.clear()

        # Generate all the positions
        n, m = self.size
        positions = [(x, y) for x in range(n) for y in range(m)]
        random.shuffle(positions)

        # Set the rollers
        dir = DIR[1:]
        random.shuffle(dir)
        a, b = random.randint(0, n - 1), random.randint(0, m - 1)
        rollers = generate(maker(Roller, self, EnvTags.ROLLER), self.babies, rollers)
        amount = self.babies - 1
        for xdir, ydir in dir:
            x, y = (min(n - 1, a + xdir * amount), min(m - 1, b + ydir * amount))
            r = amount - (x - a + y - b)
            first = (a - xdir * r, b - ydir * r)
            if self.valid_pos(*first) and self.valid_pos(x, y):
                a, b = first
                for roller in rollers:
                    roller.set_position(a, b)
                    positions.remove((a, b))
                    a += xdir
                    b += ydir
                break

        # Genarate all the objects
        toys = generate(maker(Toy, self, EnvTags.TOY), self.toys, toys)
        babies = generate(maker(Baby, self, EnvTags.BABY), self.babies, babies)
        dirty = generate(maker(Cell, self, EnvTags.DIRTY), self.dirty, dirty)
        bot = generate(maker(Robot, self, EnvTags.BOT), 1, bot)
        callback = lambda: Cell(env=self, tag=EnvTags.EMPTY)
        all_agents = fill_agents([*toys, *babies, *dirty, *bot], callback)
        
        # Assign positions
        for pos, agent in zip(positions, all_agents):
            agent.set_position(*pos)

        # Update the env
        self.build_data(rollers=rollers, toys=toys, babies=babies, dirty=dirty, bot=bot)  
        self.agents = [*bot, *babies]

        # Add empty cells in the agents positions
        for x in self.agents:
            callback().set_position(*x.position)

    def set(self, x, y, agent):
        self.unset(agent)
        self.logger.debug(f'Setting {str(agent).strip()} agent position to {(x, y)}', 'set')
        cell = self._get(x, y)
        cell.append(agent)
        cell.sort(key=lambda x: x.tag().value)
        agent.position = (x, y)

    def unset(self, agent):
        if agent.position:
            self.logger.debug(f'Unsetting {str(agent).strip()} agent at position {agent.position}', 'unset')
            self._get(*agent.position).remove(agent)
            agent.position = None

    def _get(self, x, y):
        return super().get(x, y)
            
    def get(self, x, y):
        return super().get(x, y)[-1]

    def stop(self):
        n, m = self.size
        cells = n * m
        rollers = sum(r.tag() == EnvTags.FULL_ROLLER for r in self.data['rollers'])
        if (not self.dirty) and (rollers == self.babies):
            self.logger.debug('CLEAN status reached', 'stop')
            self.status = EnvStatus.CLEAN
        elif self.time > self.end:
            self.logger.debug('Time Limit Exceded status reached', 'stop')
            self.status = EnvStatus.TLE
        elif (self.dirty * 100) / cells >= 60:
            self.logger.debug('Bot Fired status reached', 'stop')
            self.status = EnvStatus.FIRED
        return self.status != EnvStatus.RUNNING 
            


