from flask import Flask
from simulationwindow import SimulationWindow

server = Flask(__name__)

server.config.from_pyfile('config.py')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

simulation_window = SimulationWindow(server=server, external_stylesheets=external_stylesheets)
sim_app = simulation_window.app


@server.route('/')
@server.route('/dash')
def hello_world():
    return sim_app.index()


if __name__ == '__main__':
    server.run()
