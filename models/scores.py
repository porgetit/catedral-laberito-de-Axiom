class ScoresModel:
    def __init__(self, records_service):
        self.records_service = records_service
        self.title = "Mejores Puntuaciones"
        
    def get_sorted_scores(self):
        """Obtiene los puntajes ordenados de mayor a menor."""
        records = self.records_service.get_records()
        # Ordenar por puntaje (segundo elemento de cada tupla) de mayor a menor
        sorted_scores = sorted(
            [(date, score) for date, score in records.items()],
            key=lambda x: x[1], 
            reverse=True
        )
        return sorted_scores[:10]  # Retornar solo los 10 mejores