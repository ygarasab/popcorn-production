import numpy as np

from ... import verificacoes
from ..subentidade import SubEntidade
from .estados import Estados


# noinspection SpellCheckingInspection
class Copo(SubEntidade):
    def __init__(self, entidade, tempos_de_enchimento, tempos_de_despejo, verboso=True):
        """
        :param entidade: simulacao.Processo
        :param tempos_de_enchimento: float
        :param verboso: bool
        """
        super().__init__(entidade, Estados, verboso)

        self.tempos_de_enchimento, self.tempos_de_despejo = tempos_de_enchimento, tempos_de_despejo
        self.copo_vazio, self.copo_cheio = self.ambiente.event().succeed(), self.ambiente.event()

    @property
    def tempos_de_enchimento(self):
        return self.__tempos_de_enchimento

    @tempos_de_enchimento.setter
    def tempos_de_enchimento(self, novo_tempos_de_enchimento):
        verificacoes.verifica_numpy_ndarray(tempos_de_enchimento=novo_tempos_de_enchimento)

        self.__tempos_de_enchimento = self._filtra_outliers(novo_tempos_de_enchimento)

    @property
    def tempos_de_despejo(self):
        return self.__tempos_de_despejo

    @tempos_de_despejo.setter
    def tempos_de_despejo(self, novo_tempos_de_despejo):
        verificacoes.verifica_numpy_ndarray(tempos_de_despejo=novo_tempos_de_despejo)

        self.__tempos_de_despejo = self._filtra_outliers(novo_tempos_de_despejo)

    @property
    def tempo_de_enchimento(self):
        return np.random.choice(self.tempos_de_enchimento)

    @property
    def tempo_de_despejo(self):
        return np.random.choice(self.tempos_de_despejo)

    def enche(self):
        yield self.copo_vazio & self.entidade.panela.panela_aquecida

        self.copo_vazio = self.ambiente.event()
        self.estado_atual = Estados.ENCHENDO

        yield self.ambiente.timeout(self.tempo_de_enchimento)

        self.estado_atual = Estados.CHEIO

        self.copo_cheio.succeed()
        self.entidade.panela.esvazia()

    def despeja(self):
        yield self.copo_cheio & self.entidade.panela.panela_vazia & self.entidade.aquecedor.aquecedor_desligado

        self.copo_cheio = self.ambiente.event()
        self.estado_atual = Estados.DESPEJANDO

        yield self.ambiente.timeout(self.tempo_de_despejo)

        self.estado_atual = Estados.VAZIO

        self.copo_vazio.succeed()
