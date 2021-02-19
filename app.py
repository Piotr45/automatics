from flask import Flask
from src.simulationwindow import SimulationWindow
from dash.dependencies import Output, Input

server = Flask(__name__)

server.config.from_pyfile('config.py')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

simulation_window = SimulationWindow(server=server, external_stylesheets=external_stylesheets)
sim_app = simulation_window.app


@sim_app.callback(Output('graph', 'figure'),
                  Input('k', 'value'),
                  Input('kp', 'value'),
                  Input('ki', 'value'),
                  Input('kd', 'value'),
                  Input('tp', 'value'),
                  Input('current-temperature', 'value'),
                  Input('goal', 'value'),
                  Input('ambient', 'value'),
                  Input('time', 'value')
                  )
def update_plots(k, kp, ki, kd, tp, current_temperature, goal, ambient_temperature, time):
    return simulation_window.generate_plots([k, kp, ki, kd, tp, current_temperature, goal, ambient_temperature, time])


@server.route('/')
@server.route('/dash')
def simulation_web():
    return sim_app.index()


if __name__ == '__main__':
    server.run()
