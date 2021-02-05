import numpy as np

from ..entidade import Entidade
from .estados import Estados

from ..aquecedor import Aquecedor
from ..copo import Copo
from ..panela import Panela


# noinspection SpellCheckingInspection
class Processo(Entidade):
    def __init__(
            self, tempos, *, aquecedor_sempre_ligado=False, panela_sempre_cheia=False, ambiente=None, verboso=True
    ):
        super().__init__(ambiente, Estados, verboso)

        self.aquecedor_sempre_ligado, self.panela_sempre_cheia = aquecedor_sempre_ligado, panela_sempre_cheia

        self.aquecedor = Aquecedor(self, tempos_de_ligacao=tempos[:, 1], verboso=verboso)
        self.copo = Copo(self, tempos_de_enchimento=tempos[:, 3], tempos_de_despejo=tempos[:, 4], verboso=verboso)
        self.panela = Panela(
            self,
            tempos_de_enchimento=tempos[:, 0],
            tempos_de_aquecimento=tempos[:, 2],
            sempre_cheia=panela_sempre_cheia,
            verboso=verboso
        )

        self.porcoes_produzidas = None

    @property
    def ambiente(self):
        # noinspection PyArgumentList
        return Entidade.ambiente.fget(self)

    @ambiente.setter
    def ambiente(self, novo_ambiente):
        # noinspection PyArgumentList
        Entidade.ambiente.fset(self, novo_ambiente)

        for entidade in ["aquecedor", "copo", "panela"]:
            if hasattr(self, entidade):
                exec(f"self.{entidade}.ambiente = novo_ambiente")

    def recria_ambiente(self):
        super().recria_ambiente()

        for entidade in ["aquecedor", "copo", "panela"]:
            if hasattr(self, entidade):
                exec(f"self.{entidade}.ambiente = self.ambiente")

        self.porcoes_produzidas = 0

    def executa(self, ate=None):
        self.porcoes_produzidas, tempos_de_execucao = 0, np.empty(0)

        etapas = [
            self.panela.enche,
            self.aquecedor.liga,
            self.panela.aquece,
            self.copo.enche,
            self.copo.despeja,
            self.panela.esvazia,
            (self.aquecedor.desliga if self.aquecedor_sempre_ligado is False else None),
        ]

        while self.ambiente.now < ate if ate is not None else True:
            if self.verboso is True:
                print(f"[Tempo: {round(self.ambiente.now, 2)}] Produção da porção {self.porcoes_produzidas + 1}:")

            self.estado_atual = Estados.EXECUTANDO

            for etapa in etapas:
                if etapa is not None:
                    self.ambiente.process(etapa())

            self.ambiente.run()

            self.porcoes_produzidas += 1

            tempos_de_execucao = np.append(tempos_de_execucao, self.ambiente.now)

            self.estado_atual = Estados.PARADO

            if self.aquecedor_sempre_ligado is True and self.porcoes_produzidas == 1:
                self.aquecedor.desligado.succeed()
                del etapas[1]

            if self.panela_sempre_cheia is True:
                self.panela.cheia.succeed()

                if self.porcoes_produzidas == 1:
                    del etapas[0]

        return tempos_de_execucao
