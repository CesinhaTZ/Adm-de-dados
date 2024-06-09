# Adm-de-dados💻
projeto sobre admnistração de dados ministrado por Henrique Poyatos.


## Projeto: Consulta de Dados de Asteroides com API da NASA 🌕

Este projeto é um script Python que consulta a API de Near Earth Objects (NEO) da NASA para obter informações sobre asteroides que passarão próximos à Terra em um intervalo de datas especificado pelo usuário. O script coleta informações detalhadas sobre os asteroides, incluindo nome, velocidade relativa e diâmetro estimado. Os dados são organizados em um DataFrame do pandas e podem ser exportados para um arquivo CSV.

### Funcionalidades

Consulta a API de NEO da NASA para obter dados de asteroides.
Permite especificar um intervalo de datas para a consulta.
Divide o intervalo de datas em partes menores de até 7 dias para evitar sobrecarga da API.
Organiza os dados em um DataFrame do pandas.
Exporta os dados coletados para um arquivo CSV.
Compatível com Power BI para análise e visualização dos dados.

### Requisitos
Python 3.7 ou superior
Bibliotecas Python: requests, pandas, datetime

###PASSOS PARA INSTALAÇÃO

#### 1 INSTALAÇÃO DO REPOSITORIO

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

#### 2 INSTALAÇÃO DE DEPENDENCIAS

pip install requests pandas

### SEU USO

#### EXECUÇÃO STANDLONE

Substitua a chave da API no script:

Obtenha uma chave da API da NASA em API NASA.
Substitua 'uTfP3czlwNl3ajaAj7AUjLL3CQP396MVjvJGjlKz' pela sua chave de API

Execute o script:

"python app.py"

#### 4 Digite as datas de início e fim quando solicitado:

As datas devem estar no formato YYYY-MM-DD.
Integração com Power BI
Defina os parâmetros no Power BI:

#### 5 Crie parâmetros chamados START_DATE e END_DATE no Power BI.
 


#### 6 Substitua as linhas onde start_date_str e end_date_str são definidos para usar os parâmetros do Power BI:
python
Copiar código
start_date_str = str(START_DATE)
end_date_str = str(END_DATE)
Configure o script no Power BI:

#### 7
Vá para Home > Obter dados > Mais....
Selecione Outro > Script Python.
Cole o script no editor de scripts Python do Power BI.
Instale os pacotes necessários no ambiente Python do Power BI:


#### 8 

para ser executado no  power bi basta verificar a pasta que ele está conectado o python e fazer uma copa do seu caminho de exemplo abaixo "C:\Users\meu usuario\AppData\Local\Programs\Python/python312"
feito isso basta entra no CMD como administrador e digitar cd "C:\Users\meu usuario\AppData\Local\Programs\Python/python312" feito isso você vai instalar os frameworks que (panda e um erro que vimos mas que deixamos aa soluçao logo abaixo a instalação do request também caso peça.)


##### .\python.exe -m pip install pandas 

logo em seguida


##### .\python.exe -m pip install requests 

feito isso sucesso as dependencias ja etão instaladas na sua maquina.

e poderá entra no power bi e começar a fazer o layout para funcionamento da api a api tem uma pequena mudança de execução ao entrar no power bi porem o codigo segue tambem abaixo para maior coompreensão

entrar em contato.

##codigo fonte para o power bi

### 4

import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_asteroid_data(start_date, end_date, api_key):
    """
    Busca dados de asteroides da API da NASA para um intervalo de datas.
    """
    url = "https://api.nasa.gov/neo/rest/v1/feed"
    parameters = {
        "start_date": start_date,
        "end_date": end_date,
        "api_key": api_key
    }
    # Usado um try-except
    try:
        response = requests.get(url, params=parameters)
        response.raise_for_status()  # Lança uma exceção se a resposta não for bem-sucedida
        data = response.json()

        asteroid_list = []
        for date in data["near_earth_objects"]:
            for asteroid in data["near_earth_objects"][date]:
                asteroid_info = {
                    "date": date,
                    "name": asteroid["name"],
                    "speed_kph": asteroid["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"],
                    "diameter_m": asteroid["estimated_diameter"]["meters"]["estimated_diameter_max"]
                }
                asteroid_list.append(asteroid_info)

        return pd.DataFrame(asteroid_list)

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None
    except KeyError as e:
        print(f"Erro ao processar dados: {e}")
        return None
def main():
    # chave da api
    api_key = 'uTfP3czlwNl3ajaAj7AUjLL3CQP396MVjvJGjlKz'

    # Obtenção das datas do Power BI
    start_date_str = START_DATE
    end_date_str = END_DATE

    # Conversão das datas para objetos datetime
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        print("Formato de data inválido nos parâmetros do Power BI. Use o formato YYYY-MM-DD.")
        return

    # Verificação das datas (correção da indentação)
    if not (start_date and end_date): # <-- Removi a indentação extra nesta linha
        print("Datas de início e fim são obrigatórias.")
        return

    # Verificação se a data final é posterior à data inicial
    if start_date > end_date:
        print("A data final deve ser posterior à data inicial.")
        return

    # ... (resto do código para dividir o intervalo de datas e fazer as requisições) 

if __name__ == "__main__":
    main()
