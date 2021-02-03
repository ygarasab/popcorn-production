import pandas as pd
import simulacao as sim

tempos = pd.read_csv("dados/Mean_Production.csv").to_numpy()

# noinspection SpellCheckingInspection
processo = sim.Processo(tempos)

# to run
# processo.executa()
