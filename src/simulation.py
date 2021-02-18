class Simulation:
    def __init__(self, config):
        self.__config__ = config
        self.__data__ = {
            'Delivered heat': [0] * self.__config__['Simulation cycles'],
            'Heat loss': [0] * self.__config__['Simulation cycles'],
            'Errors': [0] * self.__config__['Simulation cycles'],
            'Quantity': [0] * self.__config__['Simulation cycles'],
            'Temperature': [0] * self.__config__['Simulation cycles'],
            'Time': [_ for _ in range(0, self.__config__['Simulation cycles'])]
        }
        self.sum_of_errors = 0

    @staticmethod
    def minmax(minimum, maximum, value):
        return max(minimum, min(maximum, value))

    def find_error(self, index) -> None:
        self.__data__['Errors'][index] = self.__config__['Temperature goal'] - self.__config__[
            'Current water temperature']

    def find_delta_error(self, index) -> float:
        if index == 0:
            return self.__data__['Errors'][0]
        return self.__data__['Errors'][index] - self.__data__['Errors'][index - 1]

    def sum_errors(self, index) -> None:
        self.sum_of_errors += self.__data__['Errors'][index]

    def new_control_quantity_value(self, index) -> float:
        return self.__config__['Kp'] * (
                self.__data__['Errors'][index] + (self.__config__['Tp'] / self.__config__['Ti']) *
                self.sum_of_errors + (
                        self.__config__['Td'] / self.__config__['Tp']) * self.find_delta_error(index))

    def append_element_to_control_quantity_list(self, index) -> None:
        self.__data__['Quantity'][index] = self.minmax(self.__config__['Quantity minimum'],
                                                       self.__config__['Quantity maximum'],
                                                       self.new_control_quantity_value(index))

    def count_heat_gain(self, index) -> None:
        self.__data__['Delivered heat'][index] = (
                self.__config__['Heat gain maximum'] - self.__config__['Heat gain minimum'] / (self.__config__[
            'Quantity maximum']) - self.__config__['Quantity minimum'] * self.__data__['Quantity'][index])

    def count_heat_loss(self, index):
        self.__data__['Heat loss'][index] = (self.__config__['Current water temperature'] - self.__config__[
            'Ambient temperature']) / self.__config__['K']

    def update_temperature(self, index):
        self.__data__['Temperature'][index + 1] = ((self.__data__['Delivered heat'][index] -
                                                    self.__data__['Heat loss'][index] / self.__config__[
                                                             'Thermal capacity']) * self.__config__['Tp'] +
                                                   self.__data__['Temperature'][index])
        self.__config__['Current water temperature'] = self.__data__['Temperature'][index + 1]

    def simulation(self):
        for index in range(0, self.__config__['Simulation cycles']):
            self.find_error(index)
            self.sum_errors(index)
            self.append_element_to_control_quantity_list(index)
            self.count_heat_gain(index)
            self.count_heat_loss(index)
            if index == self.__config__['Simulation cycles']-1:
                pass
            else:
                self.update_temperature(index)
        return self.__data__


# tmp = Simulation({
#             'K': 0.06,
#             'Kp': 110,
#             'Ki': 0.05,
#             'Kd': 5,
#             'Tp': 0.1,
#             'Ti': 110/0.05,
#             'Td': 5/110,
#             'Current water temperature': 20,
#             'Temperature goal': 50,
#             'Ambient temperature': 20,
#             'Thermal capacity': 555 / 1,
#             'Quantity minimum': 10,
#             'Quantity maximum': 2200,
#             'Heat gain minimum': 0,
#             'Heat gain maximum': 41900,
#             'Simulation cycles': 300
#         })
#
# tmp.simulation()
