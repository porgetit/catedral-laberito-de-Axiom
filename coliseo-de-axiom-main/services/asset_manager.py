
"""Carga y cacheo de recursos.

Placeholder para Hito 1: sin sprites todavía.
"""
class AssetManager:
    _cache = {}

    @classmethod
    def load(cls, path: str):
        if path not in cls._cache:
            # Aquí se cargaría con pygame.image.load(path)
            cls._cache[path] = None
        return cls._cache[path]
