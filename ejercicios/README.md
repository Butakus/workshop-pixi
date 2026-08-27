# Ejercicios del taller

Material de apoyo para los bloques prácticos del taller (ver las slides en [`../slides/workshop.pdf`](../slides/workshop.pdf)). No cubre el bloque 3 (instalación y uso básico de Pixi) porque sus ejercicios son autocontenidos y muy cortos — se construyen en vivo sin necesitar plantilla.

Cada carpeta numerada corresponde a un ejercicio y sigue el mismo patrón:

- `README.md`: qué ejercicio es y cómo usar la carpeta.
- `solucion/` (cuando aplica): el estado final esperado tras completar el ejercicio, por si os atascáis y queréis seguir el ritmo del resto del grupo, o simplemente comparar.

| Carpeta | Ejercicio |
|---|---|
| `05-ros2-robostack/02-mi-paquete/` | Entorno ROS 2 + paquete propio con colcon |
| `05-ros2-robostack/04-nav2-pixi-ros/` | Nav2 completo con `pixi-ros`, simulación y navegación |
| `07-buildfarm/hola-pichi/` | Fase A: construir un paquete con rattler-build |
| `07-buildfarm/consumidor-pixi/` | Fase C: instalar desde un `pixi.toml` propio |
| `07-buildfarm/consumidor-ros2/` | Fase D: integrarlo en un workspace ROS 2 |

La Fase B (publicar en prefix.dev) no tiene carpeta propia: es solo el comando `rattler-build upload prefix` con vuestra API key, documentado en el README de `hola-pichi/` y explicado en las slides.
