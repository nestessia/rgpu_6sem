import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.api import SimpleExpSmoothing, seasonal_decompose
from statsmodels.tsa.ar_model import AutoReg
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("./data/tovar_moving.csv", index_col=['date'], parse_dates=['date'], dayfirst=True)


decomposition = seasonal_decompose(df, model='additive')
decomposition.plot()
plt.savefig('seasonal_decomposition.png')
plt.close()

# Разделение на обучающую и тестовую выборки
test_df = df.iloc[-1]
train_df = df.iloc[:-1]


alpha = 0.7
ses = SimpleExpSmoothing(train_df)
model = ses.fit(smoothing_level=alpha, optimized=False)
exp_pred = model.forecast(1)

# Сравнение последних значений
print(f'Реальное последнее значение: {round(test_df.values[0], 3)}')
print(f'Прелсказанное последнее значение: {round(exp_pred.values[0], 3)}')

# Проверка на стационарность
test = sm.tsa.adfuller(train_df)
print ('adf: ', test[0] )
print ('p-value: ', test[1])
print('Critical values: ', test[4])
if test[0] > test[4]['5%']: 
    print ('есть единичные корни, ряд не стационарен')
else:
    print ('единичных корней нет, ряд стационарен')


# Графики автокорреляции и частичной автокорреляции
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
sm.graphics.tsa.plot_acf(train_df.values.squeeze(), lags=25, ax=ax1, color='green')
sm.graphics.tsa.plot_pacf(train_df, lags=25, ax=ax2, color='orange')
plt.savefig('autocorrelation.png') 
plt.close()

# Модель авторегрессии
ar_model = AutoReg(train_df, lags=2).fit()
print(ar_model.summary())

# Предсказание с помощью модели AR
ar_pred = ar_model.predict(start=len(train_df), end=(len(train_df)), dynamic=False)
print(f'Предсказанное последнее значение ряда с помощью модели AR: {round(ar_pred.values[0], 3)}')
