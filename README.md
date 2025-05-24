# Coliseo de Axiom

Un juego de acción y supervivencia donde te enfrentas a oleadas de enemigos en un coliseo laberíntico. Sobrevive el mayor tiempo posible mientras derrotas enemigos y mejoras tus habilidades.

## Características Implementadas

### Sistema de Combate
- ✅ Sistema de movimiento fluido con controles WASD
- ✅ Dos tipos de ataques:
  - Golpe Ascendente (K): Ataque rápido de corto alcance
  - Explosión a Quemarropa (L): Ataque potente que consume MP
- ✅ Sistema de daño crítico con multiplicador
- ✅ Sistema de knockback para los enemigos
- ✅ Regeneración automática de HP y MP

### Sistema de Enemigos
- ✅ Múltiples tipos de enemigos:
  - Básicos: Enemigos estándar
  - Rápidos: Mayor velocidad de movimiento
  - Pesados: Mayor resistencia
  - A distancia: Atacan desde lejos
  - Jefes: Enemigos más poderosos
- ✅ Sistema de oleadas progresivas
- ✅ IA básica de persecución y ataque

### Sistema de Juego
- ✅ Generación de mapa procedural
- ✅ Sistema de colisiones con el entorno
- ✅ Panel de información con estadísticas
- ✅ Sistema de rondas y progresión
- ✅ Pantalla de muerte con estadísticas
- ✅ Sistema de pausa

## Requisitos Técnicos

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
- K: Golpe Ascendente
- L: Explosión a Quemarropa
- ESC: Pausar/Reanudar
- R: Reiniciar (después de morir)

## Estructura del Proyecto

```
.
├── main.py              # Punto de entrada
├── config.yaml          # Configuración del juego
├── requirements.txt     # Dependencias
├── controllers/         # Controladores de la lógica
├── models/             # Modelos de datos y entidades
├── services/           # Servicios y utilidades
└── views/              # Vistas y renderizado
```

## Bugs Conocidos

1. Sistema de Ataques:
   - La dirección del ataque no apunta correctamente hacia el cursor
   - El knockback no se aplica en la dirección correcta
   - Los rangos de los ataques no funcionan como se espera

2. Sistema de Enemigos:
   - El contador de enemigos eliminados no refleja el total de la partida
   - Algunos enemigos pueden quedarse atascados en las paredes

## Próximas Mejoras

### Prioridad Alta
- [ ] Corregir sistema de ataques y knockback
- [ ] Implementar sistema de progresión de personaje
- [ ] Mejorar la IA de los enemigos
- [ ] Agregar efectos visuales para los ataques

### Prioridad Media
- [ ] Implementar sistema de sonido y música
- [ ] Agregar más tipos de enemigos
- [ ] Mejorar la generación del mapa
- [ ] Implementar sistema de power-ups

### Prioridad Baja
- [ ] Agregar sistema de logros
- [ ] Implementar modo cooperativo
- [ ] Agregar más efectos visuales
- [ ] Mejorar la interfaz de usuario
