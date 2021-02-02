import pandas as pd
import simpy as sp
import simulacao as sim

tempos = pd.read_csv("dados/Mean_Production.csv").to_numpy()

# noinspection SpellCheckingInspection
ambiente = sp.Environment()
# noinspection SpellCheckingInspection
processo = sim.Processo(ambiente, tempos)

# to run
# processo.executa()
