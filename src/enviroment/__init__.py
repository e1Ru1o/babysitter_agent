from .house import House
from ..common import finder, EnvError

envs = [
    House,
]

def get_env(name):
    return finder(envs, name, EnvError(f'Enviroment `{name}` implementation not found'))
