import numpy as np


# noinspection SpellCheckingInspection
def verifica_numpy_ndarray(**kwargs):
    for nome, array in kwargs.items():
        if not isinstance(array, np.ndarray):
            raise TypeError(f"O atributo {nome} precisa receber um objeto do tipo numpy.ndarray.")
        elif array.ndim != 1:
            raise ValueError(f"O atributo {nome} precisa receber um numpy.ndarray com ndim = 1.")
        elif array[array < 0].size > 0:
            raise ValueError(f"Os valores do atributo {nome} precisam ser todos positivos.")
