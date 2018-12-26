from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Namespace
from blwwwapi import __OPTIONPATH__
from typing import Any
import os
import yaml

def env(opt: str, local_preference: Any) -> Any:
    key = "WWWAPI_{}".format(opt)
    if key in os.environ:
        return os.environ[key]
    else:
        return local_preference

def yaml_env_constructor(loader, node):
    seq = loader.construct_sequence(node)
    return env(*seq)

def get() -> Namespace:
    with open(__OPTIONPATH__, "r") as FILE:
        yaml.add_constructor('!Env', yaml_env_constructor)
        spec = yaml.load(FILE)
    p = ArgumentParser(description=spec['program_description'],
            formatter_class = ArgumentDefaultsHelpFormatter)
    for opt in spec['options']:
        args = opt['names']
        p.add_argument(*opt['names'], **{k:v for k,v in opt.items() if k != 'names'})
    return p.parse_args()
