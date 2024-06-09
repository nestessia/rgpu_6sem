# Лабораторная работа 8
# Создание документация с использованием Sphinx

### Описание
Чтобы создать документацию, неободимо выполнить следующее:

В вашем коде должны быть докстринги с описанием функций:
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)
Установка библиотеки
```
pip install sphinx
```
Инициализация Sphinx
```
sphinx-quickstart
```
Настройка конфигурации Sphinx. Отредактируйте файл conf.py
```
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
```
Использование sphinx-apidoc для генерации файлов .rst
```
sphinx-apidoc -o source ../
```
Создание HTML-документации
```
sphinx-build -b html source build
```
![alt text](image-4.png)

[Ссылка на gh-pages]("https://nestessia.github.io/rgpu_6sem/")
![alt text](image.png)
[Ссылка на ветку]("https://github.com/nestessia/rgpu_6sem/tree/docs")