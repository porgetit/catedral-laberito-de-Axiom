# 🎮 Coliseo de Axiom

Un roguelike de acción desarrollado en Python usando Pygame, donde te enfrentas a oleadas de enemigos en un coliseo. El proyecto demuestra la implementación de patrones de diseño y arquitectura limpia en el desarrollo de videojuegos.

## 📖 Sobre el Proyecto

Coliseo de Axiom es un proyecto académico desarrollado como parte del curso de programación gráfica en la Universidad Tecnológica de Pereira. El juego implementa conceptos fundamentales de la programación de videojuegos como:

- Arquitectura MVC
- Sistemas de colisiones
- IA básica para enemigos
- Gestión de estados de juego
- Persistencia de datos

## 🛠️ Tecnologías

- Python 3.8+
- Pygame 2.5.0
- PyYAML 6.0
- Numpy 1.26.4

## 📚 Documentación

- [Game Design Document](gdd.md) - Documento detallado de diseño del juego
- [config.yaml](config.yaml) - Configuración del juego

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
├── main.py             # Punto de entrada
├── gdd.md              # Documento de diseño
├── config.yaml         # Configuración
├── controllers/        # Lógica de control
├── models/             # Entidades y datos
├── services/           # Servicios y utilidades
├── views/              # Renderizado
└── assets/             # Recursos multimedia
```
## 👥 Equipo

Desarrollo

- Kevin Esguerra Cardona
  - Arquitectura del juego
  - Sistemas core (combate, enemigos, colisiones)
  - Documentación técnica

Arte y Sonido

- Juan Pablo Sánchez Zapata
  - Diseño visual
  - Efectos de sonido
  - Música

## 📄 Licencia
Este proyecto es parte de un trabajo académico y no está licenciado para uso comercial.

## 🤝 Agradecimientos
Agradecemos a la Universidad EAFIT y al profesor del curso de Desarrollo de Videojuegos por su guía y apoyo durante el desarrollo de este proyecto.
