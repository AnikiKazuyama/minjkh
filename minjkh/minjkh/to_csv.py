import pandas as pd

with open('E:\\projects\\work\\base-parser\\minjkh\\minjkh\\results\\minjkh\\minjkh_0.json') as f_input:
    df = pd.read_json(f_input)
    df.rename(columns={
        'company_description': "Описание",
        'company_name': "Название УК(ТСЖ)",
        'company_city': "Город",
        'company_adress': "Адрес",
        'company_phone': "Телефон",
        'company_manager': "Управляющий",
        'dispetcher_phone': "Телефон диспетчерской",
        'inn': "ИНН",
        'ogrn': "ОГРН",
        'email': "Почта",
        'region_name': "Регион",
        'region_fond': "Жилой фонд",
    }, inplace=True)
    df.to_csv('jk.csv', encoding='utf-8', index=False)
