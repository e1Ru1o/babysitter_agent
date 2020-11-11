import random
from .utils import EnvTags
from .error import EnvError
from .base_env import Enviroment
from ..agents import Baby, Robot, Cell, Toy, Roller, DIR

class House(Enviroment):
    def __init__(self, n, m, t, babies, toys, dirty):
        super().__init__(n, m, t)
        self.babies  = babies
        
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

    def variate(self, rollers=None, toys=None, babies=None, dirty=None, bot=None):
        def generate(c, tag, sz, current):
            if current is None or len(current) != sz:
                return [c(env=self, tag=tag) for _ in range(sz)]
            return current

        n, m = self.size
        positions = [(x, y) for x in range(n) for y in range(m)]
        for pos in positions:
            Cell(env=self, tag=EnvTags.EMPTY).set_position(*pos)
        a, b = random.randint(0, n - 1), random.randint(0, m - 1)
        dir = DIR.copy()
        random.shuffle(dir)
        dir.remove((0, 0))
        amount = self.babies - 1
        rollers = generate(Roller, EnvTags.ROLLER, self.babies, rollers)
        for xdir, ydir in dir:
            if self.valid_pos(a + xdir * amount, b + ydir * amount):
                for roller in rollers:
                    roller.set_position(a, b)
                    positions.remove((a, b))
                    a += xdir
                    b += ydir
                break

        toys = generate(Toy, EnvTags.TOY, self.toys, toys)
        babies = generate(Baby, EnvTags.BABY, self.babies, babies)
        dirty = generate(Cell, EnvTags.DIRTY, self.dirty, dirty)
        bot = generate(Robot, EnvTags.BOT, 1, bot)
        all_agents = [*toys, *babies, *dirty, *bot]
        selected = random.sample(positions, len(all_agents))
        for pos, agent in zip(selected, all_agents):
            agent.set_position(*pos)
        self.build_data(rollers=rollers, toys=toys, babies=babies, dirty=dirty, bot=bot)  
        self.agents = [*bot, *babies]

    def set(self, x, y, agent):
        self.get(x, y)
        self.env[x][y] = agent
        if not agent.position is None:
             Cell(env=self, tag=EnvTags.EMPTY).set_position(*agent.position)
        agent.position = (x, y)
            

        
        

