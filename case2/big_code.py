# operation_data_shield.py
import re
import base64
import codecs
# Здесь команда размещает все функции


def find_and_validate_credit_cards(text):
    pattern = r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'
    cards = re.findall(pattern, text)
    valid_cards = []
    invalid_cards = []
    for card in cards:
        card = card.replace(" ", "").replace("-", "")
        digits = [int(d) for d in str(card) if d.isdigit()]
        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        if sum(digits) % 10 == 0:
            valid_cards.append(card)
        else:
            invalid_cards.append(card)

    return {
        'valid': valid_cards,
        'invalid': invalid_cards
    }


def find_secrets(text):

    api_pattern = r'\b(?:sk_live|pk_test)_[a-zA-Z0-9]{24,}\b'
    api = re.findall(api_pattern, text)

    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*])[A-Za-z\d!@#$%&*]{12,}$'
    password = re.findall(password_pattern, text)
    return {
        'api': api,
        'password': password
    }


def find_system_info(text):

    ip_pattern = r'\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b'
    ips = re.findall(ip_pattern, text)

    basic_file_extensions = [
        "txt", "md", "rtf", "csv", "log",
        "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
        "jpg", "jpeg", "png", "gif", "bmp", "svg", "webp",
        "mp3", "wav", "ogg", "flac", "aac",
        "mp4", "avi", "mkv", "mov", "wmv", "webm",
        "zip", "rar", "7z", "tar", "gz",
        "exe", "msi", "bat", "sh", "dll",
        "html", "css", "js", "json", "xml",
        "py", "java", "c", "cpp", "php", "go", "ts"
    ]

    string = ""
    for ext in range(len(basic_file_extensions)):
        string = string + basic_file_extensions[ext]
        if ext != len(basic_file_extensions)-1:
            string += "|"

    files_pattern = rf'\b[a-zA-Z0-9_\-]+\.(?:{string})\b'
    files = re.findall(files_pattern, text, re.IGNORECASE)

    emails_pattern = r'\b(?:[a-zA-Z0-9_\-]\.*)+\@(?:[a-z]+\.*)+[a-z]{2,}\b'

    emails = re.findall(emails_pattern, text)

    return {
        "ips": ips,
        "files": files,
        "emails": emails
    }


def decode_messages(text):
    decode_base64 = []
    b64_candidates = re.findall(r'\b[A-Za-z0-9+/]{8,}={0,2}', text)
    for cand1 in b64_candidates:
        try:
            decoded1 = base64.b64decode(cand1).decode('utf-8')
            if len(cand1) % 4 != 0:
                continue
            if all(ord(c) < 128 for c in decoded1):  # проверка на читаемость
                decode_base64.append(decoded1)
        except:
            continue

    decode_hex = []
    hex_candidates1 = re.findall(r'\b0x[0-9A-Fa-f]{1,}\b', text)
    for cand2 in hex_candidates1:
        try:
            hex_clean = cand2[2:]
            if len(hex_clean) % 2 != 0:
                continue
            decoded2 = bytes.fromhex(hex_clean).decode('utf-8')
            if all(ord(c) < 128 for c in decoded2):
                decode_hex.append(decoded2)
        except:
            continue
    hex_candidates2 = re.findall(r'(?:\\x[0-9A-Fa-f]{2})+', text)
    for cand22 in hex_candidates2:
        try:
            hex_values = re.findall(r'\\x([0-9A-Fa-f]{2})', cand22)
            hex_string = ''.join(hex_values)
            decoded22 = bytes.fromhex(hex_string).decode('utf-8')
            if all(ord(c) < 128 for c in decoded22):
                decode_hex.append(decoded22)
        except:
            continue

    decod_rot13 = []
    rot13_candidates = re.findall(r'\b[A-Za-z]+\b', text)
    for cand3 in rot13_candidates:
        try:
            decoded3 = codecs.decode(cand3, 'rot_13')
            decod_rot13.append(decoded3)
        except:
            continue

    return {
        "base 64": decode_base64,
        "hex": decode_hex,
        "rot13": decod_rot13
    }


def analyze_logs(log_text):
    sql_injections = []
    xss_attempts = []
    suspicious_user_agents = []
    failed_logins = []

    log_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+-\s+(\S+)\s+\[([^\]]+)\]\s+"(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)\s+([^\s]+)\s+HTTP/[\d\.]+"\s+(\d+)\s+(\d+|-)\s+"([^"]*)"\s+"([^"]*)"'
    logs = re.findall(log_pattern, log_text)
    sql_pattern = r"(?i)(UNION\s+SELECT|DROP\s+TABLE|INSERT\s+INTO|DELETE\s+FROM|UPDATE\s+\w+\s+SET|OR\s+\S+\s*=|AND\s+\S+\s*=|1\s*=\s*1|'\s*=\s*'|--|#|/\*)"
    xss_pattern = r"(?i)(<script|javascript:|onerror\s*=|onload\s*=|onclick\s*=|alert\s*\(|<iframe|<svg)"
    ua_pattern = r"(?i)(sqlmap|nikto|nmap|curl|wget|python|scanner)"
    login_pattern = r"(?i)/(login|admin|wp-login|signin|auth|administrator|panel|dashboard)"
    for injections in logs:
        try:
            url = injections[4]
            if re.search(sql_pattern, url):
                inj = ''.join(injections)
                sql_injections.append(inj)
        except:
            continue
    for attempts in logs:
        try:
            url = attempts[4]
            if re.search(xss_pattern, url):
                att = ''.join(attempts)
                xss_attempts.append(att)
        except:
            continue

    for log in logs:
        try:
            user_agent = log[8]
            if re.search(ua_pattern, user_agent):
                suspicious_user_agents.append(user_agent)
        except:
            continue
    for failed in logs:
        try:
            url = failed[4]
            status = failed[5]
            if re.search(login_pattern, url) and status in ['401', '403', '429', '404', '405', '503']:
                failed_logins.append(failed)
        except:
            continue

    return {
        'sql_injections': sql_injections,
        'xss_attempts': xss_attempts,
        'suspicious_user_agents': suspicious_user_agents,
        'failed_logins': failed_logins
    }


def normalize_and_validate(messy_data):
    phones_pattern = r'(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
    valid_phones = re.findall(phones_pattern, messy_data)
    invalid_phones = []

    # дата через точки
    dates_pattern1 = r'(?:\d{1,2}\.){2}\d{1,4}'

    # дата через тире
    dates_pattern2 = r'\d{1,4}-\d{1,2}-\d{1,2}'

    # дата через слэши
    dates_pattern3 = r'\d{1,2}/\d{1,2}/\d{1,4}'

    dates = re.findall(
        f'{dates_pattern1}|{dates_pattern2}|{dates_pattern3}',
        messy_data
    )

    valid_dates = []
    invalid_dates = []

    for date in dates:
        try:
            if '.' in date:
                d, m, y = date.split('.')
            elif '-' in date:
                y, m, d = date.split('-')
            elif '/' in date:
                d, m, y = date.split('/')
            else:
                invalid_dates.append(date)
                continue

            d, m, y = int(d), int(m), int(y)

            if 1 <= d <= 31 and 1 <= m <= 12 and 1900 <= y <= 2100:
                valid_dates.append(f"{y:04d}-{m:02d}-{d:02d}")
            else:
                invalid_dates.append(date)
        except:
            invalid_dates.append(date)

    inn_pattern = r'\b\d{10}\b|\b\d{12}\b'
    # юр лицо - 10 сим, физ лицо - 12 сим
    inns = re.findall(inn_pattern, messy_data)

    valid_inn = []
    invalid_inn = []

    for inn in inns:
        inn = str(inn)
        length = len(inn)
        if length == 10:
            # Валидация для 10 цифр (ЮЛ)
            weights = [2, 4, 10, 3, 5, 9, 4, 6, 8, 0]
            check_sum = sum(int(inn[i]) * weights[i] for i in range(10))
            if (check_sum % 11) % 10 == int(inn[9]):
                valid_inn.append(inn)
            else:
                invalid_inn.append(inn)
        elif length == 12:
            # Валидация для 12 цифр (ФЛ)
            weights1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0, 0]
            weights2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0]

            check1 = sum(int(inn[i]) * weights1[i] for i in range(12))
            check2 = sum(int(inn[i]) * weights2[i] for i in range(12))

            if (check1 % 11) % 10 == int(inn[10]) and (check2 % 11) % 10 == int(inn[11]):
                valid_inn.append(inn)
            else:
                invalid_inn.append(inn)
        else:
            invalid_inn.append(inn)

    cards_result = find_and_validate_credit_cards(messy_data)

    return {
        'phones': {'valid': valid_phones, 'invalid': invalid_phones},
        'dates': {'normalized': valid_dates, 'invalid': invalid_dates},
        'inn': {'valid': valid_inn, 'invalid': invalid_inn},
        'cards': cards_result
    }


def generate_comprehensive_report(main_text, log_text, messy_data):
    """ Генерирует полный отчет о расследовании """
    report = {'financial_data': find_and_validate_credit_cards(main_text),
              'secrets': find_secrets(main_text),
              'system_info': find_system_info(main_text),
              'encoded_messages': decode_messages(main_text),
              'security_threats': analyze_logs(log_text),
              'normalized_data': normalize_and_validate(messy_data)
              }
    return report


def print_report(report):
    """Красиво выводит отчет"""
    print("=" * 50)
    print("ОТЧЕТ ОПЕРАЦИИ 'DATA SHIELD'")
    print("=" * 50)
    # Вывод результатов каждой роли
    sections = [("ФИНАНСОВЫЕ ДАННЫЕ", report['financial_data']),
                ("СЕКРЕТНЫЕ КЛЮЧИ", report['secrets']),
                ("СИСТЕМНАЯ ИНФОРМАЦИЯ", report['system_info']),
                ("РАСШИФРОВАННЫЕ СООБЩЕНИЯ", report['encoded_messages']),
                ("УГРОЗЫ БЕЗОПАСНОСТИ", report['security_threats']),
                ("НОРМАЛИЗОВАННЫЕ ДАННЫЕ", report['normalized_data'])]
    for title, data in sections:
        with open("artifacts.txt", 'a', encoding='utf-8') as f:
            f.write(f'{title}\n')
            f.write(f'{"-" * 30}\n')
            f.write(f"{data}\n")

        print(f"\n{title}:")
        print("-" * 30)
        print(data)
        # Детальный вывод данных...


if __name__ == "__main__":
    # Чтение файлов с данными
    with open('data_leak_sample.txt', 'r', encoding='utf-8') as f:
        main_text = f.read()
    with open('web_server_logs.txt', 'r', encoding='utf-8') as f:
        log_text = f.read()
    with open('messy_data.txt', 'r', encoding='utf-8') as f:
        messy_data = f.read()
        # Запуск расследования
    report = generate_comprehensive_report(main_text, log_text, messy_data)
    print_report(report)
