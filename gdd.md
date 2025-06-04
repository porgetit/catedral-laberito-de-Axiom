# Coliseo de Axiom - Game Design Document

## 🎮 Descripción General
Coliseo de Axiom es un juego de acción roguelike con vista superior donde el jugador debe enfrentarse a oleadas de enemigos en un coliseo. El objetivo es sobrevivir la mayor cantidad de tiempo posible mientras se eliminan enemigos y se acumulan puntos.

## 📖 Historia
[PLACEHOLDER PARA HISTORIA]

## 🎯 Gameplay

### Sistema de Puntuación
- Los puntos se calculan en base al tiempo de supervivencia (1 punto por segundo)
- El récord de puntos se guarda automáticamente al morir o ganar
- Se mantiene un historial de las mejores puntuaciones con fecha y hora

### Mecánicas Principales

#### Movimiento
- Controles WASD o flechas direccionales para movimiento fluido en 8 direcciones
- Colisiones con paredes y bordes del mapa
- Velocidad base de movimiento: 4.9 unidades/segundo

#### Sistema de Combate
- **Ataque Básico (K/X)**
  - Daño base: 20
  - Alcance: 3 unidades
  - Tiempo de cast: 1 segundo
  - Cooldown: 1 segundo
  - Sin costo de MP

- **Ataque Pesado (L/C)**
  - Daño base: 60
  - Alcance: 4 unidades
  - Tiempo de cast: 2 segundos 
  - Cooldown: 2.5 segundos
  - Costo: 5 MP

#### Estadísticas del Jugador
- HP: 100 (regeneración de 0.5% por segundo)
- MP: 100 (regeneración de 0.5% por segundo)
- Probabilidad crítica: 25%
- Multiplicador crítico: x5
- Tiempo para iniciar regeneración: 1 segundo

### Sistema de Enemigos

#### Tipos de Enemigos
Implementados 5 niveles de enemigos con diferentes estadísticas:

| Nivel | HP | Velocidad | Daño | Color |
|-------|-----|-----------|-------|--------|
| 1 | 100 | 5 | 5 | Rojo |
| 2 | 120 | 4 | 10 | Naranja |  
| 3 | 140 | 3 | 15 | Rojo Oscuro |
| 4 | 160 | 2 | 20 | Azul |
| 5 | 200 | 1 | 50 | Morado |

#### Comportamiento de Enemigos
- Persiguen al jugador activamente
- Atacan al estar en rango
- Reciben knockback al ser golpeados
- Sistema de fricción en el knockback (0.9)
- Duración del knockback: 0.5 segundos

### Sistema de Rondas
- 10 rondas totales
- Cantidad de enemigos por ronda: 2^ronda - 1
- Victoria al completar todas las rondas
- Los enemigos se distribuyen por nivel según la fórmula: enemigos_nivel = floor(total_enemigos / nivel)

### Sistema de Knockback
- Fuerza de knockback básico: 8 unidades
- Fuerza de knockback pesado: 12 unidades
- Sistema de fricción progresiva
- Cálculo de dirección basado en el punto de impacto

## 🎨 Arte y Visuales
[PLACEHOLDER PARA ARTE]

## 🔊 Audio
[PLACEHOLDER PARA AUDIO]

## 🖥️ Interfaz

### HUD En Juego
- Panel lateral izquierdo con:
  - Puntuación actual
  - Ronda actual
  - Enemigos restantes
  - HP actual
  - MP actual
  - Lista de ataques disponibles
  - Controles de movimiento

### Menús
- **Menú Principal**
  - Jugar
  - Puntajes
  - Créditos
  - Salir

- **Menú de Pausa**
  - Continuar
  - Salir al Menú

- **Pantalla de Muerte/Victoria**
  - Puntuación final
  - Botón Reiniciar
  - Botón Menú Principal

## 🛠️ Aspectos Técnicos

### Motor y Tecnologías
- Pygame 2.5.0
- Python 3.8+
- PyYAML 6.0
- Numpy 1.26.4

### Arquitectura
- Patrón MVC (Model-View-Controller)
- Sistema modular con:
  - Controllers: Lógica de juego
  - Models: Entidades y datos
  - Views: Renderizado
  - Services: Gestión de recursos

### Sistemas Core
- Sistema de colisiones basado en hitboxes
- Sistema de guardado de récords en JSON
- Configuración centralizada en YAML
- Debug mode para hitboxes (configurable)

## ⚙️ Configuración

### Ventana
- Resolución: 1280x720
- FPS: 60

### Área de Juego
- Ancho: 800px
- Alto: 600px
- Panel info: 360px ancho

### Mapa
- Dimensiones: 64x64 tiles
- Tamaño tile: 10px