from services.records import RecordsService

class ScoresModel:
    def __init__(self, records_service: RecordsService):
        self.records_service = records_service
        self.title = "Mejores Puntuaciones"
        self.cached_scores = None

    def get_top_scores(self, count: int = 10, force_refresh: bool = True):
        """
        Obtiene los 'count' mejores puntajes ordenados de mayor a menor.
        
        Args:
            count: Número de puntajes a retornar
            force_refresh: Si es True, fuerza una recarga desde el archivo
        
        Returns:
            Lista de tuplas (timestamp, score)
        """
        if force_refresh or self.cached_scores is None:
            # Recargar registros del archivo
            self.records_service._load_records()
            all_sorted_scores = self.records_service.get_sorted_records()
            self.cached_scores = all_sorted_scores[:count]
            
        return self.cached_scores