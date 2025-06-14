# loader.py – ładowanie danych z API NBP do bazy danych SQLite (ExchangeRate)
from datetime import datetime, timedelta
from utils.config import read_config
from utils.web import fetch_exchange_rates_for_date
from utils.db import get_engine, create_tables, get_session, ExchangeRate

# Wczytaj konfigurację z config.yaml
config = read_config()

# Ustawienia z configa
start_date = config["start_date"]
end_date = config["end_date"]
table_type = config.get("table", "A")  # domyślnie tabela A

# Przygotowanie bazy danych
engine = get_engine()
create_tables(engine)
session = get_session(engine)

# Główna pętla: dzień po dniu
current_date = start_date
while current_date <= end_date:
    print(f"📥 Pobieranie danych dla {current_date}...")

    # Pobierz wszystkie kursy dla danej daty i typu tabeli
    rates = fetch_exchange_rates_for_date(current_date, table_type)

    if rates:
        for rate in rates:
            # Sprawdź, czy rekord już istnieje w bazie
            exists = session.query(ExchangeRate).filter_by(
                date=current_date, code=rate["code"]).first()

            if not exists:
                new_entry = ExchangeRate(date=current_date,
                                         currency=rate["currency"],
                                         code=rate["code"],
                                         rate=rate["mid"])
                session.add(new_entry)

        session.commit()
    else:
        print(f"⚠️ Brak danych lub błąd dla {current_date}")

    current_date += timedelta(days=1)

print("✅ Zakończono ładowanie danych.")

print("\n📄 Przykładowe dane z bazy:")
for row in session.query(ExchangeRate).limit(10):
    print(row.date, row.code, row.currency, row.rate)
