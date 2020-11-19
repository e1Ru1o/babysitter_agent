from .agents import robots

def config(callback, args):
    from configparser import ConfigParser

    parser = ConfigParser()
    parser.read(args.path)
    # required args
    args.rows         = parser.getint('env',   'rows')
    args.columns      = parser.getint('env',   'columns')
    args.babies       = parser.getint('env',   'babies')
    args.time         = parser.getint('env',   'time')
    args.toys         = parser.getfloat('env', 'toys')
    args.dirty        = parser.getfloat('env', 'dirty')

    # optional args
    args.level        = parser.get('log',    'level',       fallback='notset')
    args.log_file     = parser.get('log',    'file',        fallback='')
    args.robot        = parser.get('robot',  'name',        fallback='reactive')
    args.cicles       = parser.getint('env', 'cicles',      fallback=100)
    args.repetitions  = parser.getint('app', 'repetitions', fallback=30)
    callback(args)    

def info(callback, args):
    robots_list = '\n'.join(f'+ {bot.__name__}' for bot in robots)
    available_bots = f'Robots:\n{robots_list}\n'
    print(available_bots)

def parse_arguments(main):
    import argparse

    parser = argparse.ArgumentParser('Enviroment simulator')
    subparsers = parser.add_subparsers()

    cmd_parser = subparsers.add_parser('cmd', help='Used for command line arguments')
    cmd_parser.add_argument('-n',   '--rows',        type=int,   required=True,      help='Number of row of the enviroment')
    cmd_parser.add_argument('-m',   '--columns',     type=int,   required=True,      help='Number of columns of the enviroment')
    cmd_parser.add_argument('-b',   '--babies',      type=int,   required=True,      help='Number of babies in the enviroment')
    cmd_parser.add_argument('-o',   '--toys',        type=float, required=True,      help='Percent of obstacles(toys) in the enviroment')
    cmd_parser.add_argument('-d',   '--dirty',       type=float, required=True,      help='Percent of dirty cells in the enviroment')
    cmd_parser.add_argument('-t',   '--time',        type=int,   required=True,      help='Enviroment life cicle duration')
    cmd_parser.add_argument('-c',   '--cicles',      type=int,   default=100,        help='Number of cicles to run')
    cmd_parser.add_argument('-rep', '--repetitions', type=int,   default=30,         help='Number of times to run the env')
    cmd_parser.add_argument('-lvl', '--level',       type=str,   default='notset',   help='Number of cicles to run')
    cmd_parser.add_argument('-f',   '--log-file',    type=str,   default='',         help='File to write the logs')
    cmd_parser.add_argument('-bot', '--robot',       type=str,   default='reactive', help='File to write the logs')
    cmd_parser.set_defaults(command=lambda _, args: main(args))

    info_parser = subparsers.add_parser('info', help='Show available agents and enviroments')
    info_parser.set_defaults(command=info)

    config_parser = subparsers.add_parser('config', help='Take the configuration from a file')
    config_parser.add_argument('-p', '--path', type=str, default='config.ini', help='Path to the configuration file')
    config_parser.set_defaults(command=config)

    args = parser.parse_args()
    if not hasattr(args, 'command'):
        parser.print_help()
    else:
        args.command(main, args)