# pobieranie danych z API NBP

import requests
from datetime import datetime
from utils.config import read_config


def fetch_exchange_rates_for_date(date, table="A"):
  """
    Pobiera dane o kursach walut z API NBP dla podanej daty i tabeli.

    Argumenty:
    - date: obiekt datetime.date (np. datetime(2025, 1, 1).date())
    - table: typ tabeli NBP (domyślnie 'A')

    Zwraca:
    - lista słowników z kursami walut lub None, jeśli nie udało się pobrać danych
    """
  url = f"https://api.nbp.pl/api/exchangerates/tables/{table}/{date.strftime('%Y-%m-%d')}?format=json"

  try:
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      return data[0]["rates"]
    else:
      print(f"Błąd pobierania danych ({response.status_code}) dla {date}")
      return None
  except Exception as e:
    print(f"Błąd połączenia: {e}")
    return None
