# Catedral Laberinto de Axiom

Un juego de acción y aventura donde exploras una catedral laberíntica llena de enemigos y secretos.

## Estado Actual

El juego está en desarrollo activo. Actualmente implementado:

- ✅ Sistema de movimiento del jugador
- ✅ Generación de mapa básica
- ✅ Sistema de combate básico
- ✅ Diferentes tipos de enemigos
- ✅ Sistema de colisiones
- ⚠️ Sistema de ataques (necesita corrección)

## Requisitos

- Python 3.8 o superior
- Pygame 2.5.2
- PyYAML 6.0.1

## Instalación

1. Clona este repositorio
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Controles

- WASD: Movimiento
- Click Izquierdo: Golpe Ascendente
- Click Derecho: Explosión a Quemarropa
- ESC: Pausar/Reanudar

## Estructura del Proyecto

```
.
├── main.py              # Punto de entrada
├── config.yaml          # Configuración del juego
├── requirements.txt     # Dependencias
├── controllers/         # Controladores
├── models/             # Modelos de datos
├── services/           # Servicios
└── views/              # Vistas
```

## Próximas Mejoras

- [ ] Corregir sistema de ataques
- [ ] Mejorar sistema de colisiones
- [ ] Agregar más tipos de enemigos
- [ ] Implementar sistema de progresión
- [ ] Agregar efectos de sonido y música
