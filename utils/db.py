from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os
from flask_login import UserMixin

# Bazowa klasa ORM
Base = declarative_base()


# Model tabeli kursów walut
class ExchangeRate(Base):
  """
    Model tabeli exchange_rates przechowującej kursy walut z API NBP.
    """
  __tablename__ = "exchange_rates"

  id = Column(Integer, primary_key=True)
  date = Column(Date, nullable=False)  # Data kursu
  currency = Column(String, nullable=False)  # Nazwa waluty
  code = Column(String(3), nullable=False)  # Kod waluty
  rate = Column(Float, nullable=False)  # Średni kurs


# Model użytkownika
class User(Base, UserMixin):
  """
    Model tabeli users przechowującej dane logowania użytkownika.
    """
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  username = Column(String(50), unique=True,
                    nullable=False)  # Unikalna nazwa użytkownika
  password_hash = Column(String(128), nullable=False)  # Hasło w postaci hasha

  favorites = relationship(
      "Favorite", back_populates="user")  # Relacja do ulubionych walut


# Model ulubionych walut przypisanych do użytkownika
class Favorite(Base):
  """
    Model tabeli favorites przechowującej ulubione waluty użytkownika.
    """
  __tablename__ = "favorites"

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey("users.id"),
                   nullable=False)  # ID użytkownika
  currency_code = Column(String(3), nullable=False)  # Kod waluty

  user = relationship("User", back_populates="favorites")


# Funkcja do tworzenia połączenia z bazą danych
def get_engine(db_path="data.sqlite"):
  """
    Tworzy silnik bazy danych SQLite.

    Argumenty:
    - db_path: ścieżka do pliku bazy danych (domyślnie "data.sqlite")

    Zwraca:
    - engine: obiekt silnika SQLAlchemy
    """
  db_path = os.path.abspath(db_path)
  return create_engine(f"sqlite:///{db_path}", echo=False)


# Funkcja tworząca wszystkie tabele na podstawie modeli
def create_tables(engine):
  """
    Tworzy wszystkie tabele w bazie danych na podstawie modeli.
    """
  Base.metadata.create_all(engine)


# Funkcja do uzyskania sesji do pracy z bazą danych
def get_session(engine):
  """
    Zwraca sesję połączenia z bazą danych.

    Argument:
    - engine: silnik bazy danych

    Zwraca:
    - session: obiekt sesji ORM
    """
  Session = sessionmaker(bind=engine)
  return Session()
