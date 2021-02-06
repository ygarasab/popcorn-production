import numpy as np

from ... import verificacoes
from ..subentidade import SubEntidade
from .estados import Estados


# noinspection SpellCheckingInspection
class Panela(SubEntidade):
    def __init__(self, entidade, *, tempos_de_enchimento, tempos_de_aquecimento, sempre_cheia, verboso=True):
        """
        :param entidade: simulacao.Processo
        :param tempos_de_enchimento: float
        :param verboso: bool
        """
        super().__init__(entidade, Estados, verboso)

        self.sempre_cheia = sempre_cheia

        self.tempos_de_enchimento, self.tempos_de_aquecimento = tempos_de_enchimento, tempos_de_aquecimento

        self.aquecida, self.cheia = self.ambiente.event(), self.ambiente.event()
        self.vazia = self.ambiente.event().succeed()

    @property
    def ambiente(self):
        # noinspection PyArgumentList
        return SubEntidade.ambiente.fget(self)

    @ambiente.setter
    def ambiente(self, novo_ambiente):
        # noinspection PyArgumentList
        SubEntidade.ambiente.fset(self, novo_ambiente)

        self.vazia, self.cheia = self.ambiente.event().succeed(), self.ambiente.event()
        self.aquecida = self.ambiente.event()

    @property
    def tempos_de_enchimento(self):
        return self.__tempos_de_enchimento

    @tempos_de_enchimento.setter
    def tempos_de_enchimento(self, novo_tempos_de_enchimento):
        verificacoes.verifica_numpy_ndarray(tempos_de_enchimento=novo_tempos_de_enchimento)

        self.__tempos_de_enchimento = self._filtra_outliers(novo_tempos_de_enchimento)

    @property
    def tempos_de_aquecimento(self):
        return self.__tempos_de_aquecimento

    @tempos_de_aquecimento.setter
    def tempos_de_aquecimento(self, novo_tempos_de_aquecimento):
        verificacoes.verifica_numpy_ndarray(tempos_de_aquecimento=novo_tempos_de_aquecimento)

        self.__tempos_de_aquecimento = self._filtra_outliers(novo_tempos_de_aquecimento)

    @property
    def tempo_de_enchimento(self):
        return np.random.choice(self.tempos_de_enchimento)

    @property
    def tempo_de_aquecimento(self):
        return np.random.choice(self.tempos_de_aquecimento)

    def enche(self):
        yield self.vazia

        self.vazia = self.ambiente.event()
        self.estado_atual = Estados.ENCHENDO

        yield self.ambiente.timeout(self.tempo_de_enchimento)

        self.estado_atual = Estados.CHEIA

        self.cheia.succeed()

    def aquece(self):
        yield self.cheia & self.entidade.aquecedor.ligado & self.entidade.copo.vazio

        self.cheia = self.ambiente.event()
        self.estado_atual = Estados.AQUECENDO

        yield self.ambiente.timeout(self.tempo_de_aquecimento)

        self.estado_atual = Estados.AQUECIDA
        self.aquecida.succeed()

    def esvazia(self):
        yield self.aquecida & self.entidade.copo.cheio & self.entidade.aquecedor.desligado

        self.aquecida = self.ambiente.event()
        self.estado_atual = Estados.VAZIA

        self.vazia.succeed()

        if self.sempre_cheia is True:
            self.vazia = self.ambiente.event()
            self.estado_atual = Estados.CHEIA
