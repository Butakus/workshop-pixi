# Fase D — Integrarlo en un workspace ROS 2

Corresponde a la Fase D (cierre) del ejercicio del bloque 7 "Tu propia Buildfarm basada en RoboStack" (ver slides). Mezcla el paquete propio `hola-pichi` (publicado en la Fase B) con ROS 2 oficial de RoboStack, en el mismo entorno.

Sustituye `workshop-pichi-<nombre>` en `solucion/pixi.toml` por tu canal real:

```bash
cd solucion
mkdir -p src
pixi install
pixi shell
hola-pichi
```

Este es el mismo patrón que usa la buildfarm real de IntelligentRoboticsLabs (`ros-rolling`/`ros-jazzy`): canal propio primero en `channels`, luego `robostack-<distro>`, luego `conda-forge`.
