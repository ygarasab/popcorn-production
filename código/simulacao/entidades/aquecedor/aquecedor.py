import numpy as np

from ... import verificacoes
from ..entidade import Entidade
from .estados import Estados


# noinspection SpellCheckingInspection
class Aquecedor(Entidade):
    def __init__(self, ambiente, tempos_de_ligacao, verboso=True):
        """
        :param ambiente: simpy.Environment
        :param tempos_de_ligacao: numpy.ndarray
        :param verboso: bool
        """
        super().__init__(ambiente, Estados, verboso)

        self.tempos_de_ligacao = tempos_de_ligacao
        self.aquecedor_desligado, self.aquecedor_ligado = self.ambiente.event().succeed(), self.ambiente.event()

    @property
    def tempos_de_ligacao(self):
        return self.__tempos_de_ligacao

    @tempos_de_ligacao.setter
    def tempos_de_ligacao(self, novo_tempos_de_ligacao):
        verificacoes.verifica_numpy_ndarray(tempos_de_ligacao=novo_tempos_de_ligacao)

        self.__tempos_de_ligacao = novo_tempos_de_ligacao

    @property
    def tempo_de_ligacao(self):
        return np.random.choice(self.tempos_de_ligacao)

    def liga(self):
        yield self.aquecedor_desligado

        self.aquecedor_desligado = self.ambiente.event()

        yield self.ambiente.timeout(self.tempo_de_ligacao)

        self.estado_atual = Estados.LIGADO

        self.aquecedor_ligado.succeed()

    def desliga(self):
        yield self.aquecedor_ligado

        self.aquecedor_ligado = self.ambiente.event()
        self.estado_atual = Estados.DESLIGADO

        self.aquecedor_desligado.succeed()
