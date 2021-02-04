import numpy as np

from ... import verificacoes
from ..subentidade import SubEntidade
from .estados import Estados


# noinspection SpellCheckingInspection
class Aquecedor(SubEntidade):
    def __init__(self, entidade, *, tempos_de_ligacao, quantidade, verboso=True):
        """
        :param entidade: simulacao.Processo
        :param tempos_de_ligacao: numpy.ndarray
        :param verboso: bool
        """
        super().__init__(entidade, Estados, quantidade, verboso)

        self.tempos_de_ligacao = tempos_de_ligacao
        self.desligado, self.ligado = self.ambiente.event().succeed(), self.ambiente.event()

    @property
    def ambiente(self):
        # noinspection PyArgumentList
        return SubEntidade.ambiente.fget(self)

    @ambiente.setter
    def ambiente(self, novo_ambiente):
        # noinspection PyArgumentList
        SubEntidade.ambiente.fset(self, novo_ambiente)

        self.desligado, self.ligado = self.ambiente.event().succeed(), self.ambiente.event()

    @property
    def tempos_de_ligacao(self):
        return self.__tempos_de_ligacao

    @tempos_de_ligacao.setter
    def tempos_de_ligacao(self, novo_tempos_de_ligacao):
        verificacoes.verifica_numpy_ndarray(tempos_de_ligacao=novo_tempos_de_ligacao)

        self.__tempos_de_ligacao = self._filtra_outliers(novo_tempos_de_ligacao)

    @property
    def tempo_de_ligacao(self):
        return np.random.choice(self.tempos_de_ligacao)

    def liga(self):
        yield self.desligado & self.entidade.panela.cheia

        self.desligado = self.ambiente.event()
        self.estado_atual = Estados.LIGANDO

        yield self.ambiente.timeout(self.tempo_de_ligacao)

        self.estado_atual = Estados.LIGADO

        self.ligado.succeed()

    def desliga(self):
        yield self.ligado & self.entidade.copo.cheio

        self.ligado = self.ambiente.event()
        self.estado_atual = Estados.DESLIGADO

        self.desligado.succeed()
