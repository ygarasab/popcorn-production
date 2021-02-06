import pandas as pd
from datetime import datetime
import numpy as np

''' Loading the database '''
df = pd.read_csv('dados/Production.csv')
df = df.drop(['EmergencyStop'], axis=1)

df_n_lines = df.shape[0]
df_n_columns = df.shape[1]
df_columns = df.columns

''' Converting Milliseconds Unix Timestamp to Datetime Timestamp '''
for index in range(df_n_lines):
    unix_ts = df.at[index, 'Timestamp']
    df.at[index, 'Timestamp'] = datetime.fromtimestamp(unix_ts/1000)

''' Collecting Times '''
# 1 - Tempo de enchimento da panela (CupState: 0 -> 1)
# 2 - Tempo entre momento que o processo iniciou e o aquecedor ligou (HeaterOn: 0 -> 1)
# 3 - Tempo do momento que o aquecedor ligou, até começar a encher o copo de pipoca (CurrentWeight: 0.5 -> 1)
# 4 - Tempo entre o momento que o copo começa a encher de pipoca até o momento que começa a despejar (CupState: 1 -> 2)
# 5 - Tempo de despejo de pipoca (CupState: 2 -> 0)

df_aux = df.iloc[:7596]
dfaux_n_lines = df_aux.shape[0]

processes_periods = [990, 1962, 2992, 3857, 4812, 5806, 6704, 7596]
times = {
    time: [] for time in [
        'Enchimento da panela', 'Ligação do aquecedor', 'Aquecimento da panela', 'Enchimento do copo', 'Despejo do copo'
    ]
}
mean = []

for period in processes_periods[:-1]:
    
    index = processes_periods.index(period)+1
    df = df_aux.iloc[period:processes_periods[index]]

    # 1 - Tempo de enchimento da panela
    time = df.query('CupState == 0')['Timestamp'].values
    time = time[-1] - time[0]
    times['Enchimento da panela'].append(float('{}.{}'.format(time.seconds, time.microseconds)))
    
    # 2 - Tempo entre momento que o processo iniciou e o aquecedor ligou
    time = df.query('HeaterOn == 0')['Timestamp'].values[0]
    time_aux = df.query('HeaterOn == 1')['Timestamp'].values[0]
    time = time_aux - time
    times['Ligação do aquecedor'].append(float('{}.{}'.format(time.seconds, time.microseconds)))
    
    # 3 - Tempo do momento que o aquecedor ligou, até começar a encher o copo de pipoca 
    time = df.query('HeaterOn == 1')['Timestamp'].values[0]
    time_aux = df.query('HeaterOn == 1').query('CurrentWeight > 1')['Timestamp'].values[0]
    time = time_aux - time
    times['Aquecimento da panela'].append(float('{}.{}'.format(time.seconds, time.microseconds)))
    
    # 4 - Tempo entre o momento que o copo começa a encher de pipoca até o momento que começa a despejar (CupState: 1 -> 2)
    time = df.query('HeaterOn == 1').query('CurrentWeight > 1')['Timestamp'].values[0]
    time_aux = df.query('CupState == 2')['Timestamp'].values[0]
    time = time_aux - time
    times['Enchimento do copo'].append(float('{}.{}'.format(time.seconds, time.microseconds)))
    
    # 5 - Tempo de despejo de pipoca
    time = df.query('CupState == 2')['Timestamp'].values[0]
    time_aux = df.iloc[-1]['Timestamp']
    time = time_aux - time
    times['Despejo do copo'].append(float('{}.{}'.format(time.seconds, time.microseconds)))


''' Converting Dict to DataFrame '''
# Analisar e remover outliers
df_executions = pd.DataFrame(times)
df_executions.to_csv('dados/Mean_Production.csv', index=False)
''' Calculating mean and std '''
for label in times.keys():
    print('{}======================'.format(label))
    print('Media: {}'.format(np.mean(df_executions[label])))
    print('Desvio Padrão: {}'.format(np.std(df_executions[label])))
    print()
