# Dokumentacja techniczna projektu – Kursy Walut 2.0

## Cel projektu

Celem projektu było stworzenie aplikacji webowej typu PWA umożliwiającej przegląd kursów walut, ich filtrowanie oraz eksport. Aplikacja została rozbudowana o system rejestracji i logowania użytkowników, możliwość oznaczania ulubionych walut oraz działanie w trybie mobilnym.

## Zrealizowane funkcjonalności

- Logowanie i rejestracja użytkownika (Flask-Login + haszowanie haseł)
- Formularz wyboru waluty i zakresu dat
- Interaktywny wykres kursu wybranej waluty (Chart.js)
- Eksport danych do plików CSV i Excel
- Dodawanie/usuwanie ulubionych walut (przyciski gwiazdek, AJAX)
- Osobny widok dla ulubionych walut
- Responsywny interfejs z trybem ciemnym/jasnym
- Aplikacja w trybie PWA (manifest, favicon, instalacja na urządzeniu)

## Technologie i biblioteki

- Python 3.11
- Flask
- SQLite (SQLAlchemy)
- Flask-Login
- Bootstrap 5
- Chart.js
- Openpyxl
- HTML, CSS, JavaScript
- PWA (manifest.json + statyczne zasoby)

## Struktura projektu

```
kurs-walut-20/
├── main.py               # Uruchamianie aplikacji
├── viewer.py             # Trasy Flask i logika użytkownika
├── utils/
│   └── db.py             # Modele i połączenie z bazą SQLite
├── templates/
│   ├── rates.html        # Widok główny z wykresem i tabelą
│   ├── favorites.html    # Widok zarządzania ulubionymi
│   ├── login.html        # Formularz logowania
│   └── register.html     # Formularz rejestracji
├── static/
│   ├── css/
│   │   └── dark.css      # Styl trybu ciemnego
│   └── pwa/
│       ├── manifest.json # Konfiguracja aplikacji PWA
│       └── icon-192.png  # Ikona aplikacji
└── data.sqlite           # Lokalna baza danych
```

## Użytkownicy i bezpieczeństwo

- Użytkownik może samodzielnie się zarejestrować i zalogować
- Hasła są haszowane
- Dostęp do filtrowania i ulubionych tylko po zalogowaniu

## Źródło danych

Dane kursów walut są pobierane z API Narodowego Banku Polskiego:

```
https://api.nbp.pl/api/exchangerates/rates/A/{kod_waluty}/{data_od}/{data_do}/?format=json
```

## Eksport danych

- Do CSV: `/export`
- Do Excel: `/export_xlsx`
- Dane są filtrowane według wybranych dat i waluty

## Ulubione waluty

- Użytkownik może oznaczyć walutę jako ulubioną klikając gwiazdkę
- Obsługa odbywa się w tle przy pomocy AJAX
- Dostępny jest filtr „tylko ulubione” oraz osobny widok zarządzania

## Tryb PWA i mobilny

- `manifest.json` definiuje nazwę, ikony i kolory aplikacji
- Projekt działa na urządzeniach mobilnych i można go zainstalować
- Responsywny układ Bootstrap zapewnia dopasowanie do rozmiaru ekranu

## Spełnienie wymagań projektowych

Projekt realizuje oba wymagane zadania:

1. **Aplikacja PWA**:
   - Zawiera `manifest.json`, favicon i responsywny układ
   - Może zostać zainstalowana na telefonie
   - Obsługuje interfejs mobilny (dostosowanie rozmiaru i stylu)

2. **Aplikacja hybrydowa z autoryzacją i eksportem danych**:
   - Umożliwia rejestrację/logowanie użytkowników
   - Korzysta z lokalnej bazy SQLite
   - Eksportuje dane do plików
   - Wspiera logikę filtrowania danych i personalizacji

## Link do aplikacji

Projekt działa w przeglądarce, dostępny publicznie:

https://kursy-walut-2-0.onrender.com
https://replit.com/@AleksandraZbier/kurs-walut-20

