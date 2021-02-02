from ..entidade import Entidade
from .estados import Estados

from ..aquecedor import Aquecedor
from ..copo import Copo
from ..panela import Panela


# noinspection SpellCheckingInspection
class Processo(Entidade):
    def __init__(self, ambiente, tempos, verboso=True):
        super().__init__(ambiente, Estados, verboso)

        self.aquecedor = Aquecedor(ambiente, tempos[:, 1][tempos[:, 1] < 180])
        self.copo = Copo(ambiente, tempos[:, 3], tempos[:, 4])
        self.panela = Panela(ambiente, tempos[:, 0], tempos[:, 2])

    def executa(self, ate=None):
        iteracoes = 0
        etapas = {
            "enche panela": self.panela.enche,
            "liga aquecedor": self.aquecedor.liga,
            "aquece panela": self.panela.aquece,
            "enche copo": self.copo.enche,
            "despeja copo": self.copo.despeja
        }

        while True:
            print(f"[Tempo: {round(self.ambiente.now, 2)}] Processo começou.")

            for nome, processo in etapas.items():
                self.ambiente.process(processo())

                self.ambiente.run()

                print(f" - [Tempo: {round(self.ambiente.now, 2)}] Etapa '{nome}' concluída.")

            iteracoes += 1

            if ate is not None and self.ambiente.now >= ate:
                break

        print(f"[Tempo: {round(self.ambiente.now, 2)}] Processo finalizado. {iteracoes} pipocas foram produzidas.")
