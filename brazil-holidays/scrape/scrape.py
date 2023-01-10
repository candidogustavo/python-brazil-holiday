import requests
import json
from bs4 import BeautifulSoup
#
# For request I need the name upper case and with underscore instead of space
# For the id I need the name upper case and with space and with accent
#
def remove_accents(text):
    text = text.lower()
    accents = {
        'á': 'a',
        'à': 'a',
        'ã': 'a',
        'â': 'a',
        'é': 'e',
        'ê': 'e',
        'í': 'i',
        'ó': 'o',
        'ô': 'o',
        'õ': 'o',
        'ú': 'u',
        'ç': 'c',
    }
    for accent, letter in accents.items():
        text = text.replace(accent, letter)
    return text

city = 'AMÉRICO DE CAMPOS'
cookies = {
    'estado': 'SP',
    'visitas': '1',
    'cidade': remove_accents(city).upper()
}

headers = {'authority': 'www.feriados.com.br','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-language': 'en-US,en;q=0.9','cache-control': 'no-cache','pragma': 'no-cache','sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Linux"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'cross-site','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',}

params = {
    'ano': '2023',
}

endpoint = f"feriados-{cookies['cidade'].lower().replace(' ', '_')}-{cookies['estado'].lower()}.php"
response = requests.get(
    f'https://www.feriados.com.br/{endpoint}',
    params=params,
    cookies=cookies,
    headers=headers,
)

screen = BeautifulSoup(response.text, 'html.parser')

id = f"Feriados { city.upper() } { params['ano'] }"

data_box = screen.find('div', attrs={'id': id})
li_holidays = data_box.find_all('li')

for li in li_holidays:
    date_holiday, reason_holiday = li.find('span').text.split(' - ')    
    print(date_holiday, reason_holiday)

class Holiday:
    def __init__(self, date, reason):
        self.date = date
        self.reason = reason

    def __repr__(self):
        return f"{self.date} - {self.reason}"