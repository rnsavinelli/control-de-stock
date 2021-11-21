from flask import Flask
from flask_restful import Api
from server.broker import Broker
import yaml
import os

app = Flask(__name__)
api = Api(app)

with open(os.path.dirname(app.root_path) + "/configuration.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

broker = Broker(os.path.dirname(app.root_path) + "/" + str(cfg["sqlite"]["database"]))
