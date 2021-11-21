import os
from flask import Flask
from flask_restful import Api

from server.broker import Broker
from server.configuration import configuration

app = Flask(__name__)
api = Api(app)

broker = Broker(os.path.dirname(app.root_path) + configuration["sqlite"]["file"])
