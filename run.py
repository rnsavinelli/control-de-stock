#!/usr/bin/python
# -*- coding: utf-8 -*-

from server import app

app.run(
    host="0.0.0.0",
    port=80,
    debug=True,
)
