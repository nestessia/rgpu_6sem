# Автор: Anastasia Kryuchkova

from flask import Flask
from utils import factorial1, factorial2, load, save

app = Flask(__name__)
app.config['CACHE_LOADED'] = False

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/about")
def author():
    return "<p>Anastasia Kryuchkova</p>"

@app.route("/calc/<string:func>/<int:number>")
def calculate(func, number):
    if number < 0:
        return "Факториал не определен для отрицательных чисел", 400
    if func == 'f1':
        res = str(factorial1(number))
        return f'factorial of {number} = {res}'
    elif func == 'f2':
        res = str(factorial2(number))
        return f'factorial of {number} = {res}'
    else:
        return "Неверное имя функции", 400

@app.route("/load_from_cache")
def load_from_cache():
    app.config['CACHE_LOADED'] = True
    cache = load('cache.json')
    factorial1.cache = cache
    factorial2.cache = cache
    return f'Загружен кэш: {cache}'

@app.route("/save_to_cache")
def save_to_cache():
    if not app.config['CACHE_LOADED']:
        load_from_cache()
    cache = {**factorial1.cache, **factorial2.cache}
    save('cache.json', cache)
    return f'Saved cache: {cache}'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
