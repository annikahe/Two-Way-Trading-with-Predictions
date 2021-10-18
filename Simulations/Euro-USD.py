import algorithms as alg
import offline as off
import numpy as np

import pandas as pd
from decimal import *


exchange_rates_all = pd.read_csv(r'../Data/euro-daily-hist_1999_2021.csv')

exchange_rates_orig = pd.to_numeric(exchange_rates_all['[US dollar ]'], errors='coerce').dropna().values.tolist()

exchange_rates = exchange_rates_orig / np.min(exchange_rates_orig)

print(exchange_rates)
print(np.max(exchange_rates))
print(np.min(exchange_rates))
print(off.get_opt_off_return(exchange_rates))