from flask import Flask

server = Flask(__name__)

server.config.from_pyfile('config.py')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


@server.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    server.run()
