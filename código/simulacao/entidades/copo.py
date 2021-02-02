# noinspection SpellCheckingInspection
class Copo:

    def __init__(self, limite_de_peso: int, taxa_de_enchimento: float):

        self.estado = 0
        self.peso = 0
        self.limite_de_peso = limite_de_peso
        self.taxa_de_enchimento = taxa_de_enchimento

    def tem_sobrepeso(self):

        return self.peso > self.limite_de_peso

    def enche(self):

        self.peso += self.taxa_de_enchimento
