import simpy as sp

from código.simulacao.entidades.copo import Copo
from código.simulacao.entidades.aquecedor import Aquecedor


# noinspection SpellCheckingInspection
class Producao:

    def __init__(self, ambiente: sp.Environment):

        self.copo = Copo(4)
        self.aquecedor = Aquecedor(1)

        self.estado_do_ventilador = 0

        self.ambiente = ambiente
        self.ambiente.process(self.executa())

    def executa(self):

        while True:

            print("Preparing cup to fill it up")
            self.copo.estado = 1
            prepare_time = 2
            yield self.ambiente.timeout(prepare_time)

            print("Turning fan on")
            self.estado_do_ventilador = 1
            yield self.ambiente.timeout(1)

            print("Turning heater on")
            self.aquecedor.estado = 1
            yield self.ambiente.timeout(1)

            while self.aquecedor.temperatura < 60:
                print("Heating up")
                self.aquecedor.aquece()
                self.ambiente.timeout(1)

            while not self.copo.tem_sobrepeso():
                print("Cup is filling up")
                self.copo.enche()
                self.aquecedor.aquece()
                self.ambiente.timeout(1)
