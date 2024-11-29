import pandas as pd
import random

# Словари для генерации случайных данных
first_names = ['Иван', 'Сергей', 'Петр', 'Илья', 'Михаил', 'Олег', 'Николай', 'Владимир', 'Александр', 'Евгений']
middle_names = ['Иванович', 'Сергеевич', 'Петрович', 'Ильич', 'Михайлович', 'Олегович', 'Николаевич', 'Владимирович', 'Александрович', 'Евгеньевич']
last_names = ['Иванов', 'Сергеев', 'Петров', 'Ильин', 'Михайлов', 'Олегов', 'Николаев', 'Владимиров', 'Александров', 'Евгеньев']
cities = ['Москва', 'Санкт-Петербург', 'Екатеринбург', 'Новосибирск', 'Казань', 'Челябинск', 'Омск', 'Ростов-на-Дону', 'Уфа', 'Пермь']
regions = ['Московская область', 'Ленинградская область', 'Свердловская область', 'Новосибирская область', 'Татарстан', 'Челябинская область', 'Омская область', 'Ростовская область', 'Башкортостан', 'Пермский край']
countries = ['Россия', 'Беларусь', 'Украина', 'Казахстан', 'Таджикистан', 'Кыргызстан', 'Узбекистан', 'Азербайджан', 'Армения', 'Грузия']
marital_statuses = ['Женат', 'Незамужняя', 'Замужем', 'Вице-адмирал', 'Без семьи']
genders = ['Мужской', 'Женский']
mil_statuses = ['Военнослужащий', 'Нет']
zagran_statuses = ['Загран', 'Нет']
vip_statuses = ['VIP', 'Нет']
contact_vc = ['ВКонтакте', 'Телеграм', 'Нет']
contact_tg = ['Телеграм', 'ВКонтакте', 'Нет']
contact_other = ['Нет', 'ВКонтакте', 'Телеграм']
addr_cities = ['Москва', 'Санкт-Петербург', 'Екатеринбург', 'Новосибирск', 'Казань', 'Челябинск', 'Омск', 'Ростов-на-Дону', 'Уфа', 'Пермь']
addr_regions = ['Московская область', 'Ленинградская область', 'Свердловская область', 'Новосибирская область', 'Татарстан', 'Челябинская область', 'Омская область', 'Ростовская область', 'Башкортостан', 'Пермский край']
addr_countries = ['Россия', 'Беларусь', 'Украина', 'Казахстан', 'Таджикистан', 'Кыргызстан', 'Узбекистан', 'Азербайджан', 'Армения', 'Грузия']
source_cds = ['Сайт', 'Социальные сети', 'Другое']

# Генерация случайных данных
data = {
    'client_id': range(1, 51),
    'client_first_name': [random.choice(first_names) for _ in range(50)],
    'client_middle_name': [random.choice(middle_names) for _ in range(50)],
    'client_last_name': [random.choice(last_names) for _ in range(50)],
    'client_fio_full': [f'{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}' for _ in range(50)],
    'client_bday': [f'1990-01-{random.randint(1, 31)}' for _ in range(50)],
    'client_bplace': [random.choice(cities) for _ in range(50)],
    'client_cityzen': [random.choice(cities) for _ in range(50)],
    'client_resident_cd': [random.choice(addr_regions) for _ in range(50)],
    'client_gender': [random.choice(genders) for _ in range(50)],
    'client_marital_cd': [random.choice(marital_statuses) for _ in range(50)],
    'client_graduate': [random.choice(addr_cities) for _ in range(50)],
    'client_child_cnt': [random.randint(0, 5) for _ in range(50)],
    'client_mil_cd': [random.choice(mil_statuses) for _ in range(50)],
    'client_zagran_cd': [random.choice(zagran_statuses) for _ in range(50)],
    'client_inn': [f'123456789012' for _ in range(50)],
    'client_snils': [f'123456789012' for _ in range(50)],
    'client_vip_cd': [random.choice(vip_statuses) for _ in range(50)],
    'contact_vc': [random.choice(contact_vc) for _ in range(50)],
    'contact_tg': [random.choice(contact_tg) for _ in range(50)],
    'contact_other': [random.choice(contact_other) for _ in range(50)],
    'contact_email': [f'{random.choice(first_names)}{random.choice(last_names)}@gmail.com' for _ in range(50)],
    'contact_phone': [f'+7{random.randint(1000000000, 9999999999)}' for _ in range(50)],
    'addr_region': [random.choice(addr_regions) for _ in range(50)],
    'addr_country': [random.choice(addr_countries) for _ in range(50)],
    'addr_zip': [f'{random.randint(100000, 999999)}' for _ in range(50)],
    'addr_street': [random.choice(addr_cities) for _ in range(50)],
    'addr_house': [random.randint(1, 100) for _ in range(50)],
    'addr_body': [random.choice(addr_cities) for _ in range(50)],
    'addr_flat': [random.randint(1, 100) for _ in range(50)],
    'addr_area': [random.choice(addr_cities) for _ in range(50)],
    'addr_loc': [random.choice(addr_cities) for _ in range(50)],
    'addr_city': [random.choice(addr_cities) for _ in range(50)],
    'addr_reg_dt': [f'2022-01-{random.randint(1, 31)}' for _ in range(50)],
    'addr_str': [f'{random.choice(addr_regions)} {random.choice(addr_cities)}' for _ in range(50)],
    'fin_rating': [random.randint(1, 100) for _ in range(50)],
    'fin_loan_limit': [random.randint(100000, 1000000) for _ in range(50)],
    'fin_loan_value': [random.randint(10000, 100000) for _ in range(50)],
    'fin_loan_debt': [random.randint(1000, 10000) for _ in range(50)],
    'fin_loan_percent': [random.randint(1, 100) for _ in range(50)],
    'fin_loan_begin_dt': [f'2022-01-{random.randint(1, 31)}' for _ in range(50)],
    'fin_loan_end_dt': [f'2022-01-{random.randint(1, 31)}' for _ in range(50)],
    'tream_favorite_show': [random.randint(1, 100) for _ in range(50)],
    'tream_duration': [random.randint(1, 100) for _ in range(50)],
    'create_date': [f'2022-01-{random.randint(1, 31)}' for _ in range(50)],
    'update_date': [f'2022-01-{random.randint(1, 31)}' for _ in range(50)],
    'ource_cd': [random.choice(source_cds) for _ in range(50)]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Сохранение DataFrame в CSV-файл
df.to_csv('clients.csv', index=False)