class Heater:

    def __init__(self, heating_rate):

        self.state = 0
        self.heat_percentage = 0
        self.heating_rate = heating_rate

    def heat_up(self):

        self.heat_percentage += self.heating_rate