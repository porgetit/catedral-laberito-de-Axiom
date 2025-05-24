# 🎮 Coliseo de Axiom

Un roguelike de combate cuerpo a cuerpo con vista superior, donde te enfrentas a oleadas de enemigos en un coliseo gótico-futurista. Sobrevive el mayor tiempo posible mientras derrotas enemigos y mejoras tus habilidades.

## 📖 Historia

Un estudiante universitario cae rendido de cansancio mientras desarrolla un videojuego para su proyecto final. Al despertar, se encuentra en un extraño coliseo rodeado de niebla, con una espada en sus manos. Una voz misteriosa le informa que debe sobrevivir a las oleadas de enemigos y derrotar al Custodio para ser liberado.

## 🎯 Características Implementadas

### Sistema de Combate
- ✅ Sistema de movimiento fluido con controles WASD o flechas
- ✅ Dos tipos de ataques:
  - Golpe liviano (K/X): Ataque rápido de corto alcance
  - Golpe pesado (L/C): Ataque potente que consume MP
- ✅ Sistema de daño crítico con multiplicador
- ✅ Sistema de knockback para los enemigos
- ✅ Regeneración automática de HP y MP

### Sistema de Enemigos
- ✅ Múltiples tipos de enemigos: (Pendiente de ajustar en diseño)
  - Reclutas: Enemigos básicos con movimiento y ataques lentos
  - Soldados: Más rápidos que los reclutas, ataques más coordinados
  - Caballeros: Resistentes, ataques potentes pero predecibles
  - Campeones: Rápidos y fuertes, combinan ataques y defensas
  - Custodio: Jefe final con patrones de ataque complejos
- ✅ Sistema de oleadas progresivas
- ✅ IA básica de persecución y ataque

### Sistema de Juego
- ✅ Generación de mapa procedural
- ✅ Sistema de colisiones con el entorno
- ✅ Panel de información con estadísticas
- ✅ Sistema de rondas y progresión
- ✅ Pantalla de muerte con estadísticas
- ✅ Sistema de pausa

## 🎮 Controles

| Tecla | Función |
|-------|---------|
| W/↑ | Movimiento hacia arriba |
| A/← | Movimiento hacia la izquierda |
| S/↓ | Movimiento hacia abajo |
| D/→ | Movimiento hacia la derecha |
| K/X | Golpe liviano |
| L/C | Golpe pesado |
| ESC | Pausar/Reanudar |
| R | Reiniciar (después de morir) |

## 🛠️ Requisitos Técnicos

- Python 3.8 o superior
- Pygame 2.5.2
- PyYAML 6.0.1

## 📥 Instalación

1. Clona este repositorio
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🚀 Ejecución

```bash
python main.py
```

## 📁 Estructura del Proyecto

```
.
├── main.py              # Punto de entrada
├── config.yaml          # Configuración del juego
├── requirements.txt     # Dependencias
├── controllers/         # Controladores de la lógica
├── models/             # Modelos de datos y entidades
├── services/           # Servicios y utilidades
├── views/              # Vistas y renderizado
├── assets/             # Recursos gráficos y de audio
└── tests/              # Pruebas unitarias
```

## 🐛 Bugs Conocidos

1. Sistema de Enemigos:
   - El contador de enemigos eliminados no refleja el total de la partida
   - Algunos enemigos pueden quedarse atascados en las paredes

## 📋 Próximas Mejoras

### Prioridad Alta
- [ ] Implementar sistema de progresión de personaje
- [ ] Mejorar la IA de los enemigos
- [ ] Agregar efectos visuales para los ataques

### Prioridad Media
- [ ] Implementar sistema de sonido y música
- [ ] Mejorar la generación del mapa
- [ ] Implementar sistema de power-ups (Tentativo)

### Prioridad Baja
- [ ] Agregar más efectos visuales
- [ ] Mejorar la interfaz de usuario

## 👥 Créditos

- **Desarrollo y Diseño**: Kevin Esguerra Cardona
- **Arte y Animaciones**: Juan Pablo Sánchez Zapata
- **Sonido y Música**: Juan Pablo Sánchez Zapata 