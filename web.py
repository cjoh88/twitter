from flask import Flask

web_app = Flask(__name__)

@web_app.route('/')
def index():
    return 'Hello World'
