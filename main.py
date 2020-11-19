from src import House, Logger, get_robot
from collections import defaultdict

def get_level(level):
    try:
        return int(level)
    except ValueError:
        return level.upper()

def main(args):
    # Setting up the app logger
    logger = Logger('App', args.log_file)
    level = get_level(args.level)
    try:
        logger.setLevel(level)
    except ValueError:
        logger.setLevel('INFO')
        logger.error(f'`{level}` is not a valid logging level, setting the level to INFO', 'main')

    # Running the env
    data = defaultdict(lambda: 0)
    for _ in range(args.repetitions):
        env = House(args.rows, args.columns, args.time, args.babies, \
            args.toys, args.dirty, args.cicles, get_robot(args.robot))
        status = env.run()
        data['DIRTY-MEAN'] += env.dirty
        data[status.name]  += 1

    # Computing the result
    logger.debug(f"Acumulated dirty amount is {data['DIRTY-MEAN']}", 'main')
    data['DIRTY-MEAN'] /= args.repetitions
    print('\n'.join(f'{key}: {value}' for key, value in data.items()))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser('Enviroment simulator')
    # cmd = parser.add_subparsers('cmd', 'Command line Arguments')
    parser.add_argument('-n',   '--rows',        type=int,   required=True,      help='Number of row of the enviroment')
    parser.add_argument('-m',   '--columns',     type=int,   required=True,      help='Number of columns of the enviroment')
    parser.add_argument('-b',   '--babies',      type=int,   required=True,      help='Number of babies in the enviroment')
    parser.add_argument('-o',   '--toys',        type=float, required=True,      help='Percent of obstacles(toys) in the enviroment')
    parser.add_argument('-d',   '--dirty',       type=float, required=True,      help='Percent of dirty cells in the enviroment')
    parser.add_argument('-t',   '--time',        type=int,   required=True,      help='Enviroment life cicle duration')
    parser.add_argument('-c',   '--cicles',      type=int,   default=100,        help='Number of cicles to run')
    parser.add_argument('-rep', '--repetitions', type=int,   default=30,         help='Number of times to run the env')
    parser.add_argument('-lvl', '--level',       type=str,   default='notset',   help='Number of cicles to run')
    parser.add_argument('-f',   '--log-file',    type=str,   default='',         help='File to write the logs')
    parser.add_argument('-bot', '--robot',       type=str,   default='reactive', help='File to write the logs')

    args = parser.parse_args()
    main(args)
