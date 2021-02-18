import dash
import dash_html_components as html
import dash_core_components as dcc
from pandas import DataFrame
import plotly.graph_objects as go
from plotly.graph_objs.scatter import Line
from plotly.subplots import make_subplots
from simulation import Simulation


class SimulationWindow:
    def __init__(self, server, external_stylesheets, url_path='/dash/'):
        self.app = dash.Dash(
            __name__,
            server=server,
            external_stylesheets=external_stylesheets,
            url_base_pathname=url_path
        )
        self.__config__ = self.create_config()
        self.__config__['Ti'] = self.__config__['Kp'] / self.__config__['Ki']
        self.__config__['Td'] = self.__config__['Kd'] / self.__config__['Kp']
        self.__config__['Thermal capacity'] = 555 / self.__config__['K']

        self.__figure__ = make_subplots(rows=2, cols=3)
        self.__dataframe__ = self.create_dataframe()
        self.app.layout = self.create_layout()

        # self.simulation = Simulation(self.__config__, self.__dataframe__)
        # self.simulation.simulation()

    @staticmethod
    def create_config() -> dict:
        return {
            'K': 0.06,
            'Kp': 110,
            'Ki': 0.05,
            'Kd': 5,
            'Tp': 0.1,
            'Ti': None,
            'Td': None,
            'Current water temperature': 20,
            'Temperature goal': 50,
            'Ambient temperature': 20,
            'Thermal capacity': 555 / 1,
            'Quantity minimum': 10,
            'Quantity maximum': 2200,
            'Heat gain minimum': 0,
            'Heat gain maximum': 41900,
            'Simulation cycles': 300
        }

    @staticmethod
    def create_dataframe(params) -> DataFrame:
        return DataFrame({
            'Delivered heat': params[0],
            'Heat loss': params[1],
            'Errors': params[2],
            'Quantity': params[3],
            'Temperature': params[4],
            'Sum of errors': params[5]
        })

    @staticmethod
    def create_layout() -> html.Div:
        return html.Div([
            html.H1(children="Water heater", style={'text-align': 'center'}),

            html.Div(children=[
                html.Label('K'),
                dcc.Input(value=0.06, type='number', step=0.01, id='k', min=0.01, max=0.25),

                html.Label('Kp'),
                dcc.Input(value=110, type='number', step=5, id='kp', min=50, max=250),

                html.Label('Ki'),
                dcc.Input(value=0.05, type='number', step=0.01, id='ki', min=0.01, max=0.25),

                html.Label('Kd'),
                dcc.Input(value=5, type='number', step=1, id='kd', min=1),

                html.Label('Tp'),
                dcc.Input(value=0.1, type='number', step=0.001, id='tp', min=0.001, max=1.0),

                html.Label('Current water temperature'),
                dcc.Input(value=20, type='number', step=1, id='current-temperature', min=0, max=100),

                html.Label('Temperature goal'),
                dcc.Input(value=50, type='number', step=5, id='goal', min=0, max=100),

                html.Label('Ambient temperature'),
                dcc.Input(value=20, type='number', step=1, id='ambient', min=0, max=100),

                html.Label('Simulation time (minutes)'),
                dcc.Input(value=20, type='number', step=5, id='time', min=5),

            ], id='user-input'),

            # style={'columnCount': 2}

            html.Div(children=[

            ], id='output-graphs')
        ])
