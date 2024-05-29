import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import metrics
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import seaborn as sns

data = pd.read_csv('./data/insurance.csv')
data.head()
print(data.shape)
print(data.isnull().sum())
data['smoker'] = data['smoker'].apply(lambda x: 0 if x == 'no' else 1)
data['sex'] = data['sex'].apply(lambda x: 0 if x == 'female' else 1) 
data = pd.get_dummies(data)
data.head()
features = data.drop('charges', axis=1).columns
X, y = data[features], data['charges']




# Разбиение на тренировочную и тестовую выборки с помощью train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)
print('Train shape: {}'.format(X_train.shape))
print('Test shape: {}'.format(X_test.shape))


linear_reg_model = linear_model.LinearRegression()
linear_reg_model
linear_reg_model.fit(X_train, y_train)
intercept = linear_reg_model.intercept_
y_train_pred = linear_reg_model.predict(X_train)
y_test_pred = linear_reg_model.predict(X_test)

# Подсчет метрик R^2, MAE, MAPE
print('Train R^2: {:.3f}'.format(metrics.r2_score(y_train, y_train_pred)))
print('Train MAE: {:.3f}'.format(metrics.mean_absolute_error(y_train, y_train_pred)))
print('Train MAPE: {:.3f}'.format(metrics.mean_absolute_percentage_error(y_train, y_train_pred)*100))
print('\n')
print('Test R^2: {:.3f}'.format(metrics.r2_score(y_test, y_test_pred)))
print('Test MAE: {:.3f}'.format(metrics.mean_absolute_error(y_test, y_test_pred)))
print('Test MAPE: {:.3f}'.format(metrics.mean_absolute_percentage_error(y_test, y_test_pred)*100))
print("Значение свободного члена (intercept) обученной модели:", round(intercept, 2))





# Визуализируем ошибки
fig, ax = plt.subplots(figsize=(12, 6))
y_train_errors = y_train - y_train_pred
y_test_errors = y_test - y_test_pred
predict_df = pd.DataFrame(
    {'Train errors': y_train_errors, 
     'Test errors': y_test_errors
    }
)
sns.boxplot(data=predict_df, ax=ax)
ax.set_xlabel('Model errors')
ax.set_ylabel('Linear regression model')
fig.show()



# Создаем объект для min-max нормализации
scaler = preprocessing.MinMaxScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Создаем объект для генерации полиномиальных признаков степени 2
poly = preprocessing.PolynomialFeatures(degree=2, include_bias=False)
# Вычисляем параметры генерации - результирующее количество признак
poly.fit(X_train_scaled)
#Производим преобразование для каждой из выборок
X_train_scaled_poly = poly.transform(X_train_scaled)
X_test_scaled_poly = poly.transform(X_test_scaled)
print('Train shape: {}'.format(X_train_scaled_poly.shape))
print('Test shape: {}'.format(X_test_scaled_poly.shape))








# создаем логарифмированный целевой признак цены
y_train_log = np.log(y_train)
# Инициализируем объект класса линейная регрессия с L2-регуляризацией (Ridge)
ridge_linear_reg_poly = linear_model.Ridge()
# Обучаем модель предсказывать логарифм целевого признака
ridge_linear_reg_poly.fit(X_train_scaled_poly, y_train_log)

# Делаем предсказание для каждой из выборок
# Берем обратную функцию - экспоненту, тк обучали на логарифме
y_train_pred = np.exp(ridge_linear_reg_poly.predict(X_train_scaled_poly))
y_test_pred = np.exp(ridge_linear_reg_poly.predict(X_test_scaled_poly))
# Подсчет метрик R^2, MAE, MAPE
print('Train R^2: {:.3f}'.format(metrics.r2_score(y_train, y_train_pred)))
print('Train MAE: {:.3f}'.format(metrics.mean_absolute_error(y_train, y_train_pred)))
print('Train MAPE: {:.3f}'.format(metrics.mean_absolute_percentage_error(y_train, y_train_pred)*100))
print('\n')
print('Test R^2: {:.3f}'.format(metrics.r2_score(y_test, y_test_pred)))
print('Test MAE: {:.3f}'.format(metrics.mean_absolute_error(y_test, y_test_pred)))
print('Test MAPE: {:.3f}'.format(metrics.mean_absolute_percentage_error(y_test, y_test_pred)*100))
print("Значение свободного члена (intercept) обученной модели:", round(intercept, 2))





print("Коэффициенты модели:")
coefficients = ridge_linear_reg_poly.coef_
for i, coef in enumerate(coefficients):
    print(f"Коэффициент для признака x^{i}: {coef}")




# Линейная регрессия с L1 регуляризацией (Lasso)
lasso_lr_poly = linear_model.Lasso(max_iter=2000)
# Обучаем модель предсказывать логарифм целевого признака
lasso_lr_poly.fit(X_train_scaled_poly, y_train_log)

# Делаем предсказание для каждой из выборок
# Если обучили на логарифме, то от результата необходимо взять обратную функцию - экспоненту
y_train_pred = np.exp(lasso_lr_poly.predict(X_train_scaled_poly))
y_test_pred = np.exp(lasso_lr_poly.predict(X_test_scaled_poly))
# Подсчет метрик R^2, MAE, MAPE
print('Train R^2: {:.3f}'.format(metrics.r2_score(y_train, y_train_pred)))
print('Train MAE: {:.3f}'.format(metrics.mean_absolute_error(y_train, y_train_pred)))
print('Train MAPE: {:.3f}'.format(metrics.mean_absolute_percentage_error(y_train, y_train_pred)*100))
print('\n')
print('Test R^2: {:.3f}'.format(metrics.r2_score(y_test, y_test_pred)))
print('Test MAE: {:.3f}'.format(metrics.mean_absolute_error(y_test, y_test_pred)))
print('Test MAPE: {:.3f}'.format(metrics.mean_absolute_percentage_error(y_test, y_test_pred)*100))
print("Значение свободного члена (intercept) обученной модели:", round(intercept, 2))