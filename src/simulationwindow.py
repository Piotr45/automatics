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

        self.__figure__ = make_subplots(rows=3, cols=2)

        self.app.layout = self.create_layout()

    @staticmethod
    def create_config(params=None) -> dict:
        if params is None:
            return {
                'K': 0.06,
                'Kp': 110,
                'Ki': 0.05,
                'Kd': 5,
                'Tp': 0.1,
                'Ti': 110 / 0.05,
                'Td': 5 / 110,
                'Current water temperature': 20,
                'Temperature goal': 50,
                'Ambient temperature': 20,
                'Thermal capacity': 555 / 0.06,
                'Quantity minimum': 10,
                'Quantity maximum': 2200,
                'Heat gain minimum': 0,
                'Heat gain maximum': 41900,
                'Simulation cycles': 300
            }
        return {
            'K': params[0],
            'Kp': params[1],
            'Ki': params[2],
            'Kd': params[3],
            'Tp': params[4],
            'Ti': params[1] / params[2],
            'Td': params[3] / params[1],
            'Current water temperature': params[5],
            'Temperature goal': params[6],
            'Ambient temperature': params[7],
            'Thermal capacity': 555 / params[0],
            'Quantity minimum': 10,
            'Quantity maximum': 2200,
            'Heat gain minimum': 0,
            'Heat gain maximum': 41900,
            'Simulation cycles': 300
        }

    # @staticmethod
    # def create_dataframe(params) -> DataFrame:
    #     return DataFrame({
    #         'Delivered heat': params[0],
    #         'Heat loss': params[1],
    #         'Errors': params[2],
    #         'Quantity': params[3],
    #         'Temperature': params[4],
    #         'Sum of errors': params[5]
    #     })

    def create_layout(self) -> html.Div:
        return html.Div([
            html.H1(children="Water heater", style={'text-align': 'center',
                                                    'color': 'white',
                                                    'background-color': 'darkslategrey'
                                                    }),
            # html.Link(rel='stylesheet', href='stylesheet.css'),
            html.Div(children=[
                html.Div(children=[
                    html.Label('K'),
                    dcc.Input(value=0.06, type='number', step=0.01, id='k', min=0.01, style={'text-align': 'center'}),

                    html.Label('Kp'),
                    dcc.Input(value=110, type='number', step=5, id='kp', min=50, style={'text-align': 'center'}),

                    html.Label('Ki'),
                    dcc.Input(value=0.05, type='number', step=0.01, id='ki', min=0.01, style={'text-align': 'center'}),

                    html.Label('Kd'),
                    dcc.Input(value=5, type='number', step=1, id='kd', style={'text-align': 'center'}),

                    html.Label('Tp'),
                    dcc.Input(value=0.1, type='number', step=0.001, id='tp', min=0.001, style={'text-align': 'center'}),

                    html.Label('Current water temperature'),
                    dcc.Input(value=20, type='number', step=1, id='current-temperature', min=0,
                              style={'text-align': 'center'}),

                    html.Label('Temperature goal'),
                    dcc.Input(value=50, type='number', step=5, id='goal', min=0, style={'text-align': 'center'}),

                    html.Label('Ambient temperature'),
                    dcc.Input(value=20, type='number', step=1, id='ambient', min=0, style={'text-align': 'center'}),

                    html.Label('Simulation time (minutes)'),
                    dcc.Input(value=20, type='number', step=5, id='time', min=5, style={'text-align': 'center'}),

                ], id='user-input', style={
                    'text-align': 'center',
                    'font-size': '14px',
                    'padding': '12px',
                    'width': '25%',
                    'box-sizing': 'border-box',
                    'border': '2px solid  # 0088a9',

                    'border-radius': '4px',
                    'background-color': 'darkslategrey',
                    'text-decoration-color': 'azure',
                    'color': 'white',
                    'display': 'inline-block'
                }),

                # style={'columnCount': 2}

                html.Div(children=[
                    dcc.Graph(figure=self.generate_plots(), animate=True, id='graph')
                ], id='output-graphs', style={'width': '75%', 'height': 'auto', 'display': 'inline-block'})
            ], id='sub-main-div', )
        ])

    def _add_subplots(self):
        figure_titles = ['Delivered heat', 'Heat loss', 'Error', 'Quantity', 'Water temperature']
        keys = self.__dataframe__.keys()[:-1]
        for i in range(1, 6):
            # print(f"i: {i} row: {i // 2 + 1} col: {i % 2 + 1}")
            self.__figure__.add_trace(
                go.Scatter(
                    x=self.__dataframe__['Time'],
                    y=self.__dataframe__[keys[i - 1]],
                    name=figure_titles[i - 1],
                ),
                row=i // 2 + 1,
                col=i % 2 + 1
            )
        self.set_plot_info()

    def set_plot_info(self):
        self.__figure__['layout']['xaxis']['title'] = 'Time [s]'
        self.__figure__['layout']['xaxis2']['title'] = 'Time [s]'
        self.__figure__['layout']['xaxis3']['title'] = 'Time [s]'
        self.__figure__['layout']['xaxis4']['title'] = 'Time [s]'
        self.__figure__['layout']['xaxis5']['title'] = 'Time [s]'
        self.__figure__['layout']['yaxis']['title'] = 'Delivered heat [J]'
        self.__figure__['layout']['yaxis2']['title'] = 'Heat loss [J]'
        self.__figure__['layout']['yaxis3']['title'] = 'Error [*C]'
        self.__figure__['layout']['yaxis4']['title'] = 'Power (Quantity) [W]'
        self.__figure__['layout']['yaxis5']['title'] = 'Water temperature [*C]'

    def generate_plots(self, params=None):
        self.__figure__ = make_subplots(rows=3, cols=2)
        self.simulation = Simulation(self.create_config(params))
        self.__dataframe__ = DataFrame(self.simulation.simulation())

        self._add_subplots()
        self.__figure__.update_layout({'legend': {'orientation': 'h', }})
        return self.__figure__

    # def generate_graph_div(self, params=None):
    #     return dcc.Graph(figure=self.generate_plots(params), animate=True, id='graph')

    # def generate_graph_div(self, params=None):
    #     return html.Div(children=[
    #                 dcc.Graph(figure=self.generate_plots(params), animate=True, id='graph'),
    #             ], id='output-graphs', style={'width': '75%', 'height': 'auto', 'display': 'inline-block'})

