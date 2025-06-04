# Coliseo de Axiom - Game Design Document

## 🎮 Descripción General
Coliseo de Axiom es un juego de acción roguelike con vista superior donde el jugador debe enfrentarse a oleadas de enemigos en un coliseo. El objetivo es sobrevivir la mayor cantidad de tiempo posible mientras se eliminan enemigos y se acumulan puntos.

## 📖 Historia

En el reino de Axiom, una antigua civilización que dominó las artes arcanas y la tecnología, existía un legendario coliseo donde los más valientes guerreros se enfrentaban a desafíos sobrenaturales. Este coliseo, conocido como "El Coliseo de Axiom", era más que un simple lugar de combate; era un portal entre dimensiones, un lugar donde la realidad se doblegaba y las leyes de la física se alteraban.

Hace siglos, durante el apogeo de Axiom, los sabios del reino descubrieron que el coliseo era en realidad una prisión dimensional, diseñada para contener a seres de otras realidades que amenazaban con invadir su mundo. Los combates que allí se realizaban no eran meros espectáculos, sino rituales necesarios para mantener el equilibrio dimensional.

Sin embargo, en su ambición por dominar estas fuerzas, los sabios de Axiom cometieron un error fatal. Intentaron controlar la energía del coliseo, lo que provocó una catástrofe dimensional. El reino entero fue consumido por un vórtice de energía arcana, y el coliseo quedó sellado en una dimensión intermedia, donde el tiempo y el espacio se distorsionan.

Ahora, siglos después, tú, un guerrero elegido por los últimos vestigios de la conciencia colectiva de Axiom, has sido convocado para enfrentar el desafío definitivo. Tu misión es adentrarte en el Coliseo de Axiom y enfrentarte a las criaturas que han logrado escapar de sus celdas dimensionales. Cada ronda que superes te acercará más a la verdad sobre lo que realmente sucedió con Axiom y, quizás, a la posibilidad de restaurar el equilibrio dimensional.

Los enemigos que enfrentarás no son meras criaturas, sino manifestaciones de las diferentes facetas de la energía arcana que se descontroló durante la catástrofe. Cada nivel de enemigo representa una frecuencia diferente de esta energía, desde las más básicas (rojo semi-oscuro) hasta las más poderosas y corruptas (magenta semi-oscuro).

Tu viaje a través del coliseo no es solo una prueba de habilidad, sino una odisea para descubrir la verdad sobre el destino de Axiom y, posiblemente, encontrar una manera de restaurar el equilibrio entre las dimensiones. ¿Podrás sobrevivir a los desafíos del coliseo y desvelar los secretos que se ocultan en sus profundidades?

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
| 2 | 120 | 4 | 10 | Verde |  
| 3 | 140 | 3 | 15 | Azul |
| 4 | 160 | 2 | 20 | Amarillo |
| 5 | 200 | 1 | 50 | Magenta |

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

### Sprites del Jugador
- Sprites obtenidos de itch.io bajo licencia libre
- Animaciones completas para:
  - Movimiento en 4 direcciones para el PJ y 8 direcciones para el enemigo debido a que el enemigo persigue al jugador principal.
  - Ataque básico
  - Ataque pesado
  - Muerte
- Tamaño base: 32x32 píxeles
- Estilo pixel art consistente con la temática del juego

### Sprites de Enemigos
- Sprites obtenidos de itch.io bajo licencia libre
- 5 variantes de color según nivel:
  - Nivel 1: Rojo semi-oscuro
  - Nivel 2: Verde semi-oscuro
  - Nivel 3: Azul semi-oscuro
  - Nivel 4: Amarillo semi-oscuro
  - Nivel 5: Magenta semi-oscuro
- Animaciones para:
  - Movimiento
  - Ataque
  - Muerte
- Tamaño base: 32x32 píxeles (escalado a 90% para mejor rendimiento)

## 🔊 Audio

### Música
- Música generada con IA a través de Mureka.ai
- Tema principal: Atmosférico y misterioso
- Tema de combate: Intenso y dinámico
- Transiciones suaves entre estados

### Efectos de Sonido
- Efectos obtenidos de Sound Library (YouTube Licencia Libre)
- Implementados para:
  - Ataques del jugador
  - Impactos
  - Muerte de enemigos
  - Victoria/Derrota
- Sistema de audio dinámico que se adapta a la intensidad del combate

### Intención Sonora
El diseño de audio busca crear una atmósfera de misterio y suspenso, reforzando la tensión durante el combate y creando momentos de anticipación entre rondas. La música y los efectos trabajan en conjunto para mantener al jugador inmerso en la experiencia del coliseo.

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
