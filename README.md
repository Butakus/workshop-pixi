# Desde que uso Pixi estoy tan Pichi

## Entornos reproducibles para ROS 2 con Pixi, RoboStack y Prefix.dev

Material del workshop (~4 horas) sobre gestión de entornos reproducibles para ROS 2 con [Pixi](https://pixi.sh/), [RoboStack](https://robostack.github.io/) y [Prefix.dev](https://prefix.dev/).

Autores: Francisco Martín Rico, Esteve Fernández.

## Contenido de este repositorio

- **[`slides/workshop.pdf`](slides/workshop.pdf)** — las diapositivas del taller.
- **[`ejercicios/`](ejercicios/)** — plantillas de partida y soluciones de referencia para los bloques prácticos, por si os atascáis en algún ejercicio durante el taller. Ver [`ejercicios/README.md`](ejercicios/README.md).

## Estructura del taller

1. Introducción: ¿por qué ROS 2 necesita algo mejor?
2. ¿Qué es Pixi?
3. Instalación y uso básico de Pixi (práctica)
4. ¿Qué es RoboStack?
5. Uso básico de RoboStack para compilar un workspace ROS 2 (práctica)
6. Infraestructura de RoboStack
7. Tu propia Buildfarm basada en RoboStack (práctica)

## Antes del taller (leer con antelación)

Para aprovechar el tiempo práctico, por favor completa esto **antes** de venir:

- [ ] **Sistema operativo**: Linux (nativo o WSL2) o macOS. Windows nativo funciona con Pixi, pero RoboStack tiene más fricción — si usas Windows, instala [WSL2](https://learn.microsoft.com/es-es/windows/wsl/install) con Ubuntu.
- [ ] **Conexión a internet**: se van a descargar varios cientos de MB de paquetes conda (sobre todo `ros-jazzy-desktop` en el bloque 5 y Nav2 en el 5.4). Si puedes, hazlo desde una red rápida antes del día del taller.
- [ ] **`curl` instalado** (viene por defecto en la mayoría de distros Linux y en macOS).
- [ ] **Cuenta gratuita en [prefix.dev](https://prefix.dev/)** creada de antemano — la necesitarás en el bloque 7 para generar una API key y publicar un paquete propio. El plan free incluye 1 canal privado y 3 GB de almacenamiento público.
- [ ] **Instalar Pixi** (el bloque 3 lo instala en vivo, pero así no dependemos todos a la vez de la misma red el día del taller):
  ```bash
  curl -fsSL https://pixi.sh/install.sh | sh
  ```
  Verifica con `pixi --version`.
- [ ] **Comprobar que Gazebo Sim renderiza correctamente** (solo relevante para el ejercicio 5.4, simulación + RViz2 con Nav2). `gz sim` necesita una pila gráfica (OpenGL) funcional; en máquinas virtuales o WSL2 sin passthrough de GPU puede fallar o ir muy lento. Pruébalo con un mundo de ejemplo estándar:
  ```bash
  mkdir -p /tmp/test-gz && cd /tmp/test-gz
  pixi init . -c robostack-jazzy -c conda-forge
  pixi add ros-jazzy-ros-gz-sim
  pixi run gz sim shapes.sdf -v 4
  ```
  Debería abrirse una ventana con varias figuras geométricas simples. Si falla o va muy lento, prueba forzando render por software: `LIBGL_ALWAYS_SOFTWARE=1 pixi run gz sim shapes.sdf -v 4`. Si sigue sin ir, no pasa nada — ese paso concreto se puede seguir como demo proyectada por el instructor.

Si algo de esto falla, mejor descubrirlo ahora que en mitad del taller — escríbenos con antelación.
