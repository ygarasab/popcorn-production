import enum as e
import simpy as sp
import sys


# noinspection SpellCheckingInspection
class Entidade:
    def __init__(self, ambiente: sp.Environment, estados: e.EnumMeta, verboso):
        self.ambiente, self.estados, self.verboso = ambiente, estados, verboso
        self.estado_atual = list(estados)[0]

    @property
    def ambiente(self):
        return self.__ambiente

    @ambiente.setter
    def ambiente(self, novo_ambiente):
        if not isinstance(novo_ambiente, sp.Environment):
            raise TypeError("O atributo ambiente precisa receber uma instância de simpy.Environment.")

        self.__ambiente = novo_ambiente

    @property
    def estados(self):
        return self.__estados

    @estados.setter
    def estados(self, novo_estados):
        if not isinstance(novo_estados, e.EnumMeta):
            raise TypeError("O atributo estados precisa receber um enum.")

        self.__estados = novo_estados

        self._imprime(f"Estado atual: {self.estados}.")

    @property
    def verboso(self):
        return self.__verboso

    @verboso.setter
    def verboso(self, novo_verboso):
        if not isinstance(novo_verboso, bool):
            raise TypeError("O atributo verboso precisa receber um objeto do tipo bool.")

        self.__verboso = novo_verboso

    @property
    def estado_atual(self):
        return self.__estado_atual

    @estado_atual.setter
    def estado_atual(self, novo_estado):
        if isinstance(novo_estado, int):
            if novo_estado < 0 or novo_estado >= len(self.estados):
                raise ValueError(f"O atributo estado_atual precisa receber um valor entre 0 e {len(self.estados)}."
                                 f"Valor recebido: {novo_estado}")

            self.__estado_atual = list(self.estados)[novo_estado]
        elif isinstance(novo_estado, str):
            try:
                self.__estado_atual = self.estados[novo_estado]
            except KeyError:
                raise ValueError(f"O atributo estado_atual precisa receber um estado válido. Estado recebido: "
                                 f"{novo_estado}.")
        elif isinstance(novo_estado, self.estados):
            if novo_estado not in self.estados:
                raise ValueError(f"O atributo estado_atual precisa receber um objeto enum válido. Objeto recebido: "
                                 f"{novo_estado}.")

            self.__estado_atual = novo_estado
        else:
            raise TypeError(f"O atributo estado_atual precisa receber um objeto do tipo int ou str. Tipo recebido: "
                            f"{type(novo_estado)}.")

    def _imprime(self, conteudo):
        print(f"[Tempo: {self.ambiente.now}] [{self.__class__.__name__}] {conteudo}", file=sys.stdout)
