import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from simulacao.entidades import SubEntidade

df = pd.read_csv('dados/Mean_Production.csv')
dados = np.array([[0.0 for i in range(7)]for i in range(5)])
dados[0] = df['Enchimento da panela'].to_numpy()
dados[1] = df['Ligação do aquecedor'].to_numpy()
dados[2] = df['Aquecimento da panela'].to_numpy()
dados[3] = df['Enchimento do copo'].to_numpy()
dados[4] = df['Despejo do copo'].to_numpy()

for value in range(len(dados)):
    dados_filtrados = SubEntidade._filtra_outliers(dados[value])
    print(dados_filtrados)
    figura, eixo = plt.subplots(1, 1)
    plt.hist(dados_filtrados, edgecolor='black', linewidth=1.2, bins=4)
    plt.ylabel('Número de amostras')
    plt.xlabel('Tempo de duração')
    figura.savefig("%d.pdf" %value)



