#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import yaml

pwd = os.path.dirname(os.path.realpath(__file__))

with open("configuration.yml", "r") as ymlfile:
    configuration = yaml.safe_load(ymlfile)

configuration["sqlite"]["file"] = pwd + "/../" + configuration["sqlite"]["file"]

del pwd, ymlfile
