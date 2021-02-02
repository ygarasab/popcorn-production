# noinspection SpellCheckingInspection
class Aquecedor:

    def __init__(self, limite_de_temperatura: int, taxa_de_aquecimento: float):

        self.estado: int = 0
        self.temperatura: int = 0

        self.limite_de_temperatura: int = limite_de_temperatura
        self.taxa_de_aquecimento: float = taxa_de_aquecimento

    def aquece(self):

        self.temperatura += self.taxa_de_aquecimento
