import os
import yaml


config = {}

with open('config.yaml', 'r') as stream:
    config = yaml.load(stream)['game-engine'] 
    config['full-path'] = os.path.join(config['path'], config['executable'])