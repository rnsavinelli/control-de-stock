import os
import yaml

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)

with open(dir_path + "/../configuration.yml", "r") as ymlfile:
    configuration = yaml.safe_load(ymlfile)
