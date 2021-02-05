import numpy as np
import pandas as pd
import simulacao as sim
import seaborn as sns

from matplotlib import pyplot as plt

tempos_coletados = pd.read_csv("dados/Mean_Production.csv").to_numpy()

# noinspection SpellCheckingInspection
# processo = sim.Processo(tempos_coletados, aquecedor_sempre_ligado=True, panela_sempre_cheia=False)

# to run
# processo.executa()


# noinspection SpellCheckingInspection
def executa_processo(tempos, limite_de_tempo, execucoes):
    figura, eixo = plt.subplots(1, 1)
    tempos_de_producao = {}

    for estado_do_aquecedor in [False, True]:
        for estado_da_panela in [False, True]:
            if estado_do_aquecedor is False:
                categoria = "Controle" if estado_da_panela is False else "Panela sempre cheia"
            else:
                categoria = "Aquecedor sempre ligado" if estado_da_panela is False else "Ambas as otimizações"

            print(categoria)

            vetores = []

            for _ in range(execucoes):
                processo = sim.Processo(
                    tempos,
                    aquecedor_sempre_ligado=estado_do_aquecedor,
                    panela_sempre_cheia=estado_da_panela,
                    verboso=False
                )

                vetores.append(processo.executa(limite_de_tempo) / 60)

            numero_maximo_de_porcoes = max([vetor.size for vetor in vetores])

            for v in range(len(vetores)):
                while vetores[v].size < numero_maximo_de_porcoes:
                    ultimo_valor = vetores[v][-1]
                    vetores[v] = np.append(vetores[v], ultimo_valor)

            for v in range(len(vetores)):
                vetores[v] = pd.DataFrame(np.concatenate(
                    (
                        np.full((numero_maximo_de_porcoes, 1), categoria),
                        np.full((numero_maximo_de_porcoes, 1), v),
                        np.arange(1, numero_maximo_de_porcoes + 1).reshape(-1, 1),
                        vetores[v].reshape(-1, 1)
                    ), axis=1
                ), columns=["Categoria", "Execução", "Porções produzidas", "Minutos decorridos"])

            tempos_de_producao[categoria] = pd.concat(vetores, axis=0)

    tempos_de_producao = pd.concat(tempos_de_producao.values(), axis=0)

    # tempos_de_producao.drop(
    #     tempos_de_producao.loc[tempos_de_producao.loc[:, "Minutos decorridos"] == "nan"].index, inplace=True
    # )

    for coluna in ["Execução", "Porções produzidas", "Minutos decorridos"]:
        tempos_de_producao.loc[:, coluna] = pd.to_numeric(tempos_de_producao.loc[:, coluna])

    sns.lineplot(data=tempos_de_producao, x="Porções produzidas", y="Minutos decorridos", hue="Categoria")

    return figura, tempos_de_producao
