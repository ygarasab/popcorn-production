from ..entidade import Entidade
from .estados import Estados

from ..aquecedor import Aquecedor
from ..copo import Copo
from ..panela import Panela


# noinspection SpellCheckingInspection
class Processo(Entidade):
    def __init__(self, tempos, ambiente=None, verboso=True):
        super().__init__(ambiente, Estados, verboso)

        self.aquecedor = Aquecedor(self, tempos[:, 1])
        self.copo = Copo(self, tempos[:, 3], tempos[:, 4])
        self.panela = Panela(self, tempos[:, 0], tempos[:, 2])

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

    def executa(self, ate=None):
        self.porcoes_produzidas, etapas = 0, {
            "enche panela": self.panela.enche,
            "liga aquecedor": self.aquecedor.liga,
            "aquece panela": self.panela.aquece,
            "enche copo": self.copo.enche,
            "despeja copo": self.copo.despeja,
            "esvazia panela": self.panela.esvazia,
            "desliga aquecedor": self.aquecedor.desliga
        }

        while self.ambiente.now < ate if ate is not None else True:
            if (
                    self.panela.panela_vazia.triggered is True and
                    self.aquecedor.aquecedor_desligado.triggered is True and
                    self.copo.copo_vazio.triggered is True
            ):
                print(f"[Tempo: {round(self.ambiente.now, 2)}] Produção da porção {self.porcoes_produzidas + 1}:")

                self.estado_atual = Estados.EXECUTANDO

                for etapa in etapas.values():
                    self.ambiente.process(etapa())

                self.ambiente.run()

                self.porcoes_produzidas += 1

                self.estado_atual = Estados.PARADO
            else:
                raise Exception()
