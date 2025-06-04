from services.records import RecordsService

class ScoresModel:
    def __init__(self, records_service: RecordsService):
        self.records_service = records_service
        self.title = "Mejores Puntuaciones"

    def get_top_scores(self, count: int = 10):
        """
        Obtiene los 'count' mejores puntajes ordenados de mayor a menor.
        Devuelve una lista de tuplas (timestamp, score).
        """
        all_sorted_scores = self.records_service.get_sorted_records()

        # Retornar solo los 'count' mejores
        return all_sorted_scores[:count]