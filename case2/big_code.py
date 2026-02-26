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

    password_pattern = r''
    return api

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
        string  = string + basic_file_extensions[ext]
        if ext != len(basic_file_extensions)-1:
            string += "|"

    files_pattern = rf'\b[a-zA-Z0-9_\-]+\.(?:{string})\b'
    files = re.findall(files_pattern, text, re.IGNORECASE)


    emails_pattern = r'\b(?:[a-zA-Z0-9_\-]\.*)+\@(?:[a-z]+\.*)+[a-z]{2,}\b'

    emails = re.findall(emails_pattern, text)

    return {"ips": ips,
            "files": files,
            "emails": emails
           }

def decode_messages(text):
    return ''

def analyze_logs(log_text):
    return log_text

def normalize_and_validate(messy_data):
    return messy_data

def generate_comprehensive_report(main_text, log_text, messy_data):
    """ Генерирует полный отчет о расследовании """
    report = { 'financial_data': find_and_validate_credit_cards(main_text),
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
    sections = [ ("ФИНАНСОВЫЕ ДАННЫЕ", report['financial_data']),
                 ("СЕКРЕТНЫЕ КЛЮЧИ", report['secrets']),
                 ("СИСТЕМНАЯ ИНФОРМАЦИЯ", report['system_info']),
                 ("РАСШИФРОВАННЫЕ СООБЩЕНИЯ", report['encoded_messages']),
                 ("УГРОЗЫ БЕЗОПАСНОСТИ", report['security_threats']),
                 ("НОРМАЛИЗОВАННЫЕ ДАННЫЕ", report['normalized_data']) ]
    for title, data in sections:
        print(f"\n{title}:")
        print("-" * 30)
        print(data)
        # Детальный вывод данных...

if __name__ == "__main__":
    # Чтение файлов с данными
    with open('case2/data_leak_sample.txt', 'r', encoding='utf-8') as f:
        main_text = f.read()
        
    with open('case2/web_server_logs.txt', 'r', encoding='utf-8') as f:
        log_text = f.read()
    with open('case2/messy_data.txt', 'r', encoding='utf-8') as f:
        messy_data = f.read()
        # Запуск расследования
    report = generate_comprehensive_report(main_text, log_text, messy_data)
    print_report(report)