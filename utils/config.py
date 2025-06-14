# wczytanie pliku konfiguracyjnego YAML

import yaml


def read_config(file_path="config.yaml"):
  with open(file_path, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
  return config
