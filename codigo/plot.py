import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import ticker as tkr
from simulacao.entidades.subentidade import SubEntidade

df = pd.read_csv('dados/Mean_Production.csv')

for coluna in df.columns:
    dados_filtrados = SubEntidade._filtra_outliers(df.loc[:, coluna])
    print(dados_filtrados)
    figura, eixo = plt.subplots(1, 1)
    # eixo.hist(dados_filtrados, edgecolor='black', linewidth=1.2, bins=4)
    sns.distplot(dados_filtrados, bins=4, kde=False)
    eixo.set_xlabel("")
    eixo.set_ylabel("")
    eixo.set_ylim(0, 5)
    eixo.yaxis.set_major_formatter(tkr.FormatStrFormatter('%d'))
    eixo.yaxis.set_major_locator(tkr.MaxNLocator(integer=True))
    figura.savefig(f"{coluna}.pdf")



