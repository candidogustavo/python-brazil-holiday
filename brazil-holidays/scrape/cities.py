import requests
import json
from bs4 import BeautifulSoup
ESTADOS = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),    
)
visits = 0
cookies = {
    'estado': 'SP',
    'visitas': str(visits),
    'cidade': 'SANTA_RITA_DOESTE',
}

def create_state(code, name, cities):
    return """
from .state_base import StateBase


class {code}(StateBase):
    code = '{code}'
    name = '{name}'
    cities = {cities}
    """.format(code=code.upper(), name=name, cities=str(cities))

def create_file(code, name, cities):
    with open(f'../states/{code}.py', 'w') as f:
        f.write(create_state(code, name, cities))

# for state in ESTADOS:
#     visits += 1
#     cookies.update({'visitas': str(visits)})
#     print(cookies)
    

YEAR = '2023'
headers = {
    'authority': 'www.feriados.com.br',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',    
    'origin': 'https://www.feriados.com.br',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

for state in ESTADOS:
    code, name = state
    data = {
        'estado': code,
    }
    response = requests.post('https://www.feriados.com.br/cidades.php', headers=headers, data=data)
    soup = BeautifulSoup(response.text, 'html.parser')
    cities = soup.find_all('option')
    cities = [city.text for city in cities if city.text != 'Escolha uma Cidade']
    create_file(code, name, cities)
    

    
# data = {
#     'estado': 'SP',
# }

# response = requests.post('https://www.feriados.com.br/cidades.php', headers=headers, data=data)
# print(response.text)

# def create_state(code, name, cities):
#     return """
#     from .state_base import StateBase


#     class {code}(StateBase):
#         code = {code}
#         name = {name}
#         cities = {cities}
#     """.format(code.upper(), name, cities)
