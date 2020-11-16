import random

DIR = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
ALL_DIR = [*DIR, (1, 1), (1, -1), (-1, 1), (-1, -1)]

def random_dir(data=DIR):
    return random.choice(data)

def select(agents, tag):
    return [x for x in agents if x.tag() == tag]

def bfs(start, table, valid_tags):
    q, idx = [start], 0
    step = [[None] * len(x) for x in table]
    visited = [[False] * len(x) for x in table]
    distance = [[float('inf')] * len(x) for x in table]
    x, y = start
    distance[x][y] = 0
    visited[x][y] = True
    data = {tag:[] for tag in valid_tags}
    while idx < len(q):
        x, y = q[idx]
        for xdir, ydir in DIR:
            nx, ny = x + xdir, y + ydir
            try:
                assert nx >= 0 and ny >= 0
                assert not visited[nx][ny]
                tag = table[nx][ny].tag()
                assert tag in valid_tags
                d = distance[nx][ny] = distance[x][y] + 1
                data[tag].append((nx, ny))
                visited[nx][ny] = True
                step[nx][ny] = (xdir, ydir)
                q.append((nx, ny))
            except IndexError: pass
            except AssertionError: pass
        idx += 1
    return data, distance, step
    
def get_path(end, steps):
    l = []
    x, y = end
    while steps[x][y]:
        l.append(step[x][y])
        xdir, ydir = step[x][y]
        x -= xdir
        y -= xdir
    l.reverse()
    return l