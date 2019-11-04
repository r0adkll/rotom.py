#! /usr/bin/env python
"""Rotom (Dex)

Usage:
    rotom.py transform <source> <destination> [-c FILE] [-o OUTPUT] [--diffOnly]
    rotom.py images <set_code>
    rotom.py (-h | --help)
    rotom.py --version
    
Options:
    --diffOnly    Output only the difference between files
    -o --output   The output file to dump the transformed json into
    -c --config   Specify a custom config
    -h --help     Show this screen.
    --version     Show version.

"""
import os

from docopt import docopt

from commands.transform import Transform
from config import load_config_from_path, load_config
from images.malieimages import MalieImageDownloader

if __name__ == '__main__':
    args = docopt(__doc__, version='Rotom 1.0')
    print(args)

    config = load_config_from_path(args['FILE']) if args['--config'] else load_config()
    print(config)

    output = args['OUTPUT'] if args['--output'] else os.path.join(str(os.path.curdir), "rotom-output.json")
    if os.path.exists(output):
        os.remove(output)

    if args['transform']:
        Transform(config, MalieImageDownloader())\
            .run(args['<source>'], args['<destination>'], output, args['--diffOnly'])
    elif args['images']:
        set_code = args['<set_code>']
        MalieImageDownloader().download(set_code, [])
