"""Servicio para manejar los registros de partidas."""
import pickle
from datetime import datetime
import os

class RecordsService:
    def __init__(self):
        self.records = {}
        self.records_file = "records.bin"
        self._load_records()
    
    def _load_records(self):
        """Carga los registros desde el archivo binario."""
        if os.path.exists(self.records_file):
            try:
                with open(self.records_file, 'rb') as f:
                    self.records = pickle.load(f)
            except:
                self.records = {}
    
    def _save_records(self):
        """Guarda los registros en el archivo binario."""
        with open(self.records_file, 'wb') as f:
            pickle.dump(self.records, f)
    
    def add_record(self, game_time: float, enemies_killed: int):
        """Agrega un nuevo registro."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.records[timestamp] = (game_time, enemies_killed)
        self._save_records()
    
    def get_records(self):
        """Obtiene todos los registros."""
        return self.records 