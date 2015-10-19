from flask import Flask

web_app = Flask(__name__)

@web_app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    web_app.run(host='0.0.0.0',debug=True)
