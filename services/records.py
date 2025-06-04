import json
from datetime import datetime
import os

class RecordsService:
    def __init__(self, records_file="records.json"):
        self.records = {}
        self.records_file = records_file
        self._load_records()

    def _load_records(self):
        """Carga los registros desde el archivo JSON."""
        if os.path.exists(self.records_file):
            try:
                # 'r' para leer en modo texto (JSON es texto)
                with open(self.records_file, 'r', encoding='utf-8') as f:
                    self.records = json.load(f)
            except json.JSONDecodeError:
                print(f"Advertencia: El archivo '{self.records_file}' está corrupto o no es un JSON válido. Empezando con registros vacíos.")
                self.records = {} # Restablecer si el archivo está corrupto
            except IOError:
                print(f"Advertencia: No se pudo leer el archivo '{self.records_file}'. Empezando con registros vacíos.")
                self.records = {}
        else:
            # Si el archivo no existe, simplemente empezamos con registros vacíos.
            # Se creará al guardar el primer registro.
            self.records = {}

    def _save_records(self):
        """Guarda los registros en el archivo JSON."""
        try:
            # 'w' para escribir en modo texto.
            # indent=4 hace que el archivo JSON sea bonito y legible.
            with open(self.records_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, indent=4, ensure_ascii=False)
        except IOError:
            print(f"Error: No se pudo escribir en el archivo '{self.records_file}'.")

    def add_record(self, game_time: float):
        """Agrega un nuevo registro.
        El timestamp es la clave y el puntaje es el valor.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        points = int(game_time)  # Convertir tiempo a puntos
        self.records[timestamp] = points
        self._save_records()

    def get_records(self):
        """Obtiene todos los registros como un diccionario."""
        return self.records

    def get_sorted_records(self, by_score=True, descending=True):
        """
        Obtiene los registros ordenados.
        Por defecto, ordena por puntaje de mayor a menor.
        Devuelve una lista de tuplas (timestamp, score).
        """
        # items() devuelve una vista de los pares (clave, valor) del diccionario
        # lo convertimos a lista para poder ordenarlo
        items = list(self.records.items())

        # La función de ordenamiento (key) dependerá de si ordenamos por fecha (clave) o puntaje (valor)
        if by_score:
            # El índice 1 de la tupla (timestamp, score) es el score
            sort_key_func = lambda item: item[1]
        else:
            # El índice 0 es el timestamp (string), se ordenará alfabéticamente/cronológicamente
            sort_key_func = lambda item: item[0]

        return sorted(items, key=sort_key_func, reverse=descending)