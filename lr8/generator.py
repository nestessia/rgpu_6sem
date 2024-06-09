import random
import string

def generate_password(length=12, include_uppercase=True, include_numbers=True, include_special_chars=True):
    """
    Генерирует безопасный пароль с включением различных символов и гарантией их наличия.

    :param length: Длина пароля. По умолчанию 12.
    :param include_uppercase: Включать ли заглавные буквы. По умолчанию True.
    :param include_numbers: Включать ли цифры. По умолчанию True.
    :param include_special_chars: Включать ли специальные символы. По умолчанию True.
    :return: Сгенерированный пароль.
    """
    if length < 4 and (include_uppercase or include_numbers or include_special_chars):
        raise ValueError("Length should be at least 4 to include all selected character types.")

    # Обязательные символы
    password_chars = []
    
    if include_uppercase:
        password_chars.append(random.choice(string.ascii_uppercase))
    if include_numbers:
        password_chars.append(random.choice(string.digits))
    if include_special_chars:
        password_chars.append(random.choice(string.punctuation))
    
    # Основные символы
    all_chars = string.ascii_lowercase
    if include_uppercase:
        all_chars += string.ascii_uppercase
    if include_numbers:
        all_chars += string.digits
    if include_special_chars:
        all_chars += string.punctuation
    
    while len(password_chars) < length:
        next_char = random.choice(all_chars)
        # Убедимся, что нет двух одинаковых символов подряд
        if not password_chars or password_chars[-1] != next_char:
            password_chars.append(next_char)
    
    # Перемешаем символы для лучшей безопасности
    random.shuffle(password_chars)
    
    password = ''.join(password_chars)
    return password
