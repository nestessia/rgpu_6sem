import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn import tree
from sklearn import model_selection 
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold

# Чтение данных
voice_data = pd.read_csv('./data/voice_gender.csv')
print(voice_data.head())

# Проверка на наличие пропусков
print(f"Количество пропущенных: {voice_data.isnull().sum().sum()}")

# Факторы и целевой признак
features = voice_data.drop('label', axis=1).columns
X, y = voice_data[features], voice_data['label']

# Разбиение на тренировочную и тестовую выборки
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
print('Тренировочная выборка:', X_train.shape)
print('Тестовая выборка:', X_test.shape)

# Создаём и обучаем модель DecisionTreeClassifier с глубиной 1
model_depth1 = tree.DecisionTreeClassifier(criterion='entropy', max_depth=1, random_state=42)
model_depth1.fit(X_train, y_train)

# Визуализируем модель
fig, ax = plt.subplots(figsize=(25, 15))
tree.plot_tree(model_depth1, feature_names=X.columns, class_names=["0 - male", "1 - female"], filled=True, ax=ax)
plt.show()

# Предсказание на тестовой выборке и оценка точности
y_pred_depth1 = model_depth1.predict(X_test)
accuracy_depth1 = accuracy_score(y_test, y_pred_depth1)
print("Точность модели с глубиной 1:", round(accuracy_depth1, 3))

# Создаём и обучаем модель DecisionTreeClassifier с глубиной 2
model_depth2 = tree.DecisionTreeClassifier(criterion='entropy', max_depth=2, random_state=42)
model_depth2.fit(X_train, y_train)

# Визуализируем модель
fig, ax = plt.subplots(figsize=(25, 15))
tree.plot_tree(model_depth2, feature_names=X.columns, class_names=["0 - male", "1 - female"], filled=True, ax=ax)
plt.show()

# Предсказание на тестовой выборке и оценка точности
y_pred_depth2 = model_depth2.predict(X_test)
accuracy_depth2 = accuracy_score(y_test, y_pred_depth2)
print("Точность модели с глубиной 2:", round(accuracy_depth2, 3))

# Создаём и обучаем свободную модель DecisionTreeClassifier
model_unrestricted = tree.DecisionTreeClassifier(criterion='entropy', random_state=0)
model_unrestricted.fit(X_train, y_train)

# Исследование параметров модели
depth = model_unrestricted.get_depth()
n_leaves = model_unrestricted.get_n_leaves()
print(f'Глубина дерева: {depth}')
print(f'Количество листьев: {n_leaves}')

# Визуализируем модель
fig, ax = plt.subplots(figsize=(25, 15))
tree.plot_tree(model_unrestricted, feature_names=X.columns, class_names=["0 - male", "1 - female"], filled=True, ax=ax)
plt.show()

# Предсказание на тестовой и тренировочной выборках и оценка точности
y_pred_unrestricted_test = model_unrestricted.predict(X_test)
y_pred_unrestricted_train = model_unrestricted.predict(X_train)
accuracy_unrestricted_test = accuracy_score(y_test, y_pred_unrestricted_test)
accuracy_unrestricted_train = accuracy_score(y_train, y_pred_unrestricted_train)
print("Точность свободной модели на тестовой выборке:", round(accuracy_unrestricted_test, 3))
print("Точность свободной модели на тренировочной выборке:", round(accuracy_unrestricted_train, 3))

# Поиск оптимальных гиперпараметров с помощью GridSearchCV
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [4, 5, 6, 7, 8, 9, 10],
    'min_samples_split': [3, 4, 5, 10]
}
cv = StratifiedKFold(n_splits=5)
grid_search = GridSearchCV(estimator=tree.DecisionTreeClassifier(), param_grid=param_grid, cv=cv, scoring='accuracy')
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
best_score = grid_search.best_score_
print("Лучшие параметры:", best_params)
print("Лучшая оценка модели:", best_score)

# Создаём и обучаем оптимальную модель DecisionTreeClassifier
model_best = tree.DecisionTreeClassifier(criterion='entropy', max_depth=best_params['max_depth'], min_samples_split=best_params['min_samples_split'])
model_best.fit(X_train, y_train)

# Визуализируем модель
fig, ax = plt.subplots(figsize=(25, 15))
tree.plot_tree(model_best, feature_names=X.columns, class_names=["0 - male", "1 - female"], filled=True, ax=ax)
plt.show()

# Предсказание на тестовой и тренировочной выборках и оценка точности
y_pred_best_test = model_best.predict(X_test)
y_pred_best_train = model_best.predict(X_train)
accuracy_best_test = accuracy_score(y_test, y_pred_best_test)
accuracy_best_train = accuracy_score(y_train, y_pred_best_train)
print("Точность оптимальной модели на тестовой выборке:", round(accuracy_best_test, 3))
print("Точность оптимальной модели на тренировочной выборке:", round(accuracy_best_train, 3))

# Важность факторов
feature_importances = model_best.feature_importances_
fig, ax = plt.subplots(figsize=(25, 10))
sns.barplot(x=features, y=feature_importances, ax=ax, palette="viridis")
ax.set_title('Важность факторов', fontsize=20)
ax.set_xlabel('Факторы', fontsize=18)
ax.set_ylabel('Важность', fontsize=18)
plt.xticks(rotation=45, ha='right', fontsize=14)
plt.yticks(fontsize=14)
plt.show()
