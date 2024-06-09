import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_asteroid_data(start_date, end_date, api_key):
  url = "https://api.nasa.gov/neo/rest/v1/feed"
  parameters = {
    "start_date": start_date,
    "end_date": end_date,
    "api_key": api_key
  }
  response = requests.get(url, params=parameters)

  if response.status_code == 200:
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
  else:
    print("Falha na solicitação:", response.status_code)
    print("Resposta da solicitação:", response.text)
    return None

def main():
  # minha chave para api da nasa
  api_key = 'uTfP3czlwNl3ajaAj7AUjLL3CQP396MVjvJGjlKz'

  # Solicitar ao usuário as datas de início e fim
  start_date = input("Digite a data de início (formato YYYY-MM-DD): ")
  end_date = input("Digite a data de fim (formato YYYY-MM-DD): ")

  # Verificar se as datas estão no formato correto
  if not (start_date and end_date):
    print("Datas de início e fim são obrigatórias.")
    return
  
  try:
    pd.to_datetime(start_date)
    pd.to_datetime(end_date)
  except ValueError:
    print("Formato de data inválido. Use o formato YYYY-MM-DD.")
    return

  # Dividir o intervalo de datas em partes menores de até 7 dias
  date_ranges = []
  current_date = datetime.strptime(start_date, "%Y-%m-%d")
  end_date = datetime.strptime(end_date, "%Y-%m-%d")
  while current_date <= end_date:
    chunk_end_date = min(current_date + timedelta(days=6), end_date)
    date_ranges.append((current_date.strftime("%Y-%m-%d"), chunk_end_date.strftime("%Y-%m-%d")))
    current_date = chunk_end_date + timedelta(days=1)

  # Fazer solicitações para cada parte do intervalo de datas especificado
  asteroid_data_combined = pd.DataFrame()  # DataFrame vazio para armazenar os resultados
  for date_range in date_ranges:
    asteroid_data = fetch_asteroid_data(date_range[0], date_range[1], api_key)
    if asteroid_data is not None:
      asteroid_data_combined = pd.concat([asteroid_data_combined, asteroid_data], ignore_index=True)

  # Verificar os dados
  if not asteroid_data_combined.empty:
    print(asteroid_data_combined.head())  # Exibir as primeiras linhas do DataFrame
    # Salvar o DataFrame em CSV (se houver dados)
    asteroid_data_combined.to_csv('asteroid_data.csv', index=False)
  else:
    print("Não foi possível obter dados de asteroides para o intervalo de datas especificado.")

if __name__ == "__main__":
  main()
