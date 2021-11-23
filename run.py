#!/usr/bin/python
# -*- coding: utf-8 -*-

from server import app
from server.configuration import configuration

app.run(
    host=configuration["server"]["host"],
    port=configuration["server"]["port"],
    debug=True,
)
