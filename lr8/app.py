from flask import Flask, request, jsonify, render_template
from generator import generate_password

app = Flask(__name__)


@app.route('/')
def index():
    """
    Дефотный роут
    Возвращает сгенерированный шаблон index.html
    """
    return render_template('index.html')

@app.route('/api/generate_password', methods=['GET', 'POST'])
def api_generate_password():
    """
    Роут для генерации пароля.
    Возвращает 
        json: сгенерированный пароль.
    """
    if request.method == 'POST':
        data = request.get_json()
        length = data.get('length', 18)
        include_uppercase = data.get('include_uppercase', True)
        include_numbers = data.get('include_numbers', True)
        include_special_chars = data.get('include_special_chars', True)
    else:
        length = int(request.args.get('length', 12))
        include_uppercase = request.args.get('include_uppercase', 'true').lower() == 'true'
        include_numbers = request.args.get('include_numbers', 'true').lower() == 'true'
        include_special_chars = request.args.get('include_special_chars', 'true').lower() == 'true'

    password = generate_password(length, include_uppercase, include_numbers, include_special_chars)
    return jsonify(password=password)

@app.errorhandler(404)
def page_not_found(e):
    """
    Обработчик ошибки 404
    Возвращает 
        json: описание ошибки 404.
    """
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    """
    Обработчик ошибки 500
    Возвращает 
        json: описание ошибки 500.
    """
    return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)