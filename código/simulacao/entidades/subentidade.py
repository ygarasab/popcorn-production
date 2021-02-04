import numpy as np
import simpy as sp

from .entidade import Entidade


# noinspection SpellCheckingInspection
class SubEntidade(Entidade):
    def __init__(self, entidade, estados, quantidade, verboso):
        """
        :param entidade: simpy.Environment
        :param estados: enum.Enum
        :param quantidade: int
        :param verboso: bool
        """
        super().__init__(entidade.ambiente, estados, verboso)

        self.entidade, self.quantidade = entidade, quantidade
        self.recurso = sp.Resource(self.ambiente, self.quantidade)

    @property
    def ambiente(self):
        # noinspection PyArgumentList
        return Entidade.ambiente.fget(self)

    @ambiente.setter
    def ambiente(self, novo_ambiente):
        # noinspection PyArgumentList
        Entidade.ambiente.fset(self, novo_ambiente)

        if self.quantidade is not None:
            self.recurso = sp.Resource(self.ambiente, self.quantidade)

    @property
    def entidade(self):
        return self.__entidade

    @entidade.setter
    def entidade(self, novo_entidade):
        if hasattr(self, "_SubEntidade_entidade"):
            raise AttributeError("O atributo entidade só pode ser definido na inicialização do objeto.")
        elif not isinstance(novo_entidade, Entidade):
            raise TypeError("O atributo entidade precisa receber um objeto do tipo Entidade. Tipo recebido: "
                            f"{type(novo_entidade)}.")

        self.__entidade = novo_entidade

    @property
    def quantidade(self):
        return self.__quantidade if hasattr(self, "_SubEntidade__quantidade") else None

    @quantidade.setter
    def quantidade(self, novo_quantidade):
        if not isinstance(novo_quantidade, int):
            raise TypeError("O atributo quantidade precisa receber um objeto do tipo int. Tipo do objeto recebido: "
                            f"{type(novo_quantidade)}.")

        self.__quantidade = novo_quantidade

        if self.ambiente is not None:
            self.recurso = sp.Resource(self.ambiente, self.quantidade)

    @property
    def recurso(self):
        return self.__recurso

    @recurso.setter
    def recurso(self, novo_recurso):
        if not isinstance(novo_recurso, sp.Resource):
            raise TypeError("O atributo recurso precisa receber um objeto do tipo simpy.Resource. Tipo do objeto "
                            f"recebido: {type(novo_recurso)}")

        self.__recurso = novo_recurso

    @staticmethod
    def _filtra_outliers(array):
        """
        :param array: numpy.ndarray
        :return: numpy.ndarray
        """
        primeiro_quartil, terceiro_quartil = np.quantile(array, [.25, .75])
        amplitude_interquartil = terceiro_quartil - primeiro_quartil

        limite_inferior_moderado = primeiro_quartil - 1.5 * amplitude_interquartil
        limite_superior_moderado = terceiro_quartil + 1.5 * amplitude_interquartil

        return array[(array > limite_inferior_moderado) & (array < limite_superior_moderado)]
