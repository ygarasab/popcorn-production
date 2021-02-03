import numpy as np

from .entidade import Entidade


# noinspection SpellCheckingInspection
class SubEntidade(Entidade):
    def __init__(self, entidade, estados, verboso):
        """

        :param entidade: simpy.Environment
        :param estados: enum.Enum
        :param verboso: bool
        """
        super().__init__(entidade.ambiente, estados, verboso)

        self.__entidade = entidade

    @property
    def entidade(self):
        return self.__entidade

    @staticmethod
    def _filtra_outliers(array):
        """
        :param array: ndarray
        :return:
        """
        primeiro_quartil, terceiro_quartil = np.quantile(array, [.25, .75])
        amplitude_interquartil = terceiro_quartil - primeiro_quartil

        limite_inferior_moderado = primeiro_quartil - 1.5 * amplitude_interquartil
        limite_superior_moderado = terceiro_quartil + 1.5 * amplitude_interquartil

        return array[(array > limite_inferior_moderado) & (array < limite_superior_moderado)]
