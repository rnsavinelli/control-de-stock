#!/usr/bin/python
# -*- coding: utf-8 -*-

import yaml


class Configuration:
    def __init__(self, _configuration_file):
        with open(_configuration_file, "r") as ymlfile:
            self.configuration = yaml.safe_load(ymlfile)

    def database(self):
        return self.configuration["sqlite"]["file"]
