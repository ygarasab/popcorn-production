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

    def executa(self):
        etapas = [self.panela.enche, self.aquecedor.liga, self.panela.aquece, self.copo.enche, self.copo.despeja]

        while True:
            for etapa in etapas:
                self.ambiente.process(etapa())

            self.ambiente.run()
