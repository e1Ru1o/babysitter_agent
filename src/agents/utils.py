import random

DIR = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
ALL_DIR = [*DIR, (1, 1), (1, -1), (-1, 1), (-1, -1)]

def random_dir(data=DIR):
    return random.choice(data)

def select(agents, tag):
    return [x for x in agents if x.tag() == tag]