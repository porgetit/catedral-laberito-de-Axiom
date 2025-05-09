
"""Entidad base: sólo lógica, sin dependencias gráficas.
"""
from dataclasses import dataclass

@dataclass
class Entity:
    x: float
    y: float
    def pos(self):
        return self.x, self.y
