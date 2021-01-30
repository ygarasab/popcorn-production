import simpy as sp
from cup import Cup
from heater import Heater

class Production:

    def __init__(self, env : sp.Environment):

        self.cup = Cup(4)
        self.heater = Heater(1)

        self.fan_state = 0

        self.env = env
        self.env.process(self.run())

    def run(self):

        while True:

            print("Preparing cup to fill it up")
            self.cup.state = 1
            prepare_time = 2
            yield self.env.timeout(prepare_time)

            print("Turning fan on")
            self.fan_state = 1
            yield  self.env.timeout(1)

            print("Turning heater on")
            self.heater.state = 1
            yield  self.env.timeout(1)

            while self.heater.heat_percentage < 60:

                print("Heating up")
                self.heater.heat_up()
                self.env.timeout(1)

            while not self.cup.has_overwight():

                print("Cup is filling up")
                self.cup.fill()
                self.heater.heat_up()
                self.env.timeout(1)








