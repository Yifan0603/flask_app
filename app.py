from flask import Flask
from controller.FlaskAppWrapper import FlaskAppWrapper
import os

flask_app = Flask(__name__)
obj = {
    'SQLALCHEMY_DATABASE_URI': 'mysql://root:123456@127.0.0.1:3336/employeedb',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'MAX_CONTENT_LENGTH': 500 * 1000 * 1000
}

app = FlaskAppWrapper(flask_app, obj)
db = app.db
#import controller
from controller.EmpController import *
#import model
from model.Employee import *

if __name__ == "__main__":
    app.run(port=6969, debug=True)


