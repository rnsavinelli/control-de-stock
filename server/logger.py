#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime


def log(message):
    _output = "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + str(message)

    with open("server.log", "a") as log_file:
        log_file.write(_output)
        log_file.write("\n")

    print(_output)
