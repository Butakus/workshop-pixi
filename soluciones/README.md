# Soluciones

La versión terminada de cada ejercicio.
Cada una es un workspace de Pixi independiente con su `pixi.lock`, y la CI de este repositorio las instala y prueba en Linux, macOS y Windows.

| Directorio | Muestra |
| --- | --- |
| `01-workspace-ros/` | Lyrical y Jazzy, un nodo C++ compilado con colcon, un cerebro PyTorch, plataformas CPU/CUDA/Jetson y una operación CUDA real |
| `02-paquetes-ros/` | El mismo paquete C++ y uno Python, construidos con `pixi-build-ros`: sin colcon, sin `source`, y recompilando cuando cambia un fuente. `consumidor/` instala los paquetes publicados desde un canal |
| `03-colaboracion/` | Nodos de demo ya construidos, plataformas con nombre `jetson` y `workstation-gpu` resueltas desde un portátil, comprobación del lockfile, Docker y un workspace para empaquetar |

Ejecútalas desde la raíz del repositorio:

```bash
pixi run --manifest-path soluciones/01-workspace-ros/pixi.toml sim
pixi run --manifest-path soluciones/01-workspace-ros/pixi.toml -e jazzy sim   # la misma task, otra distro
```

O desde dentro del directorio:

```bash
cd soluciones/01-workspace-ros
pixi run sim
```

El Ejercicio 1 guarda la salida de colcon en `build/<entorno>`, `install/<entorno>` y `log/<entorno>`.
Compila una vez en cada entorno antes de lanzar nodos:

```bash
pixi run -e default build
pixi run -e default test-overlay
pixi run -e jazzy build
pixi run -e jazzy test-overlay
```

Para probar CUDA hace falta una GPU NVIDIA con un driver compatible.
Desde `soluciones/01-workspace-ros/` en una máquina Linux con GPU:

```bash
pixi run --platform cuda-linux-64 cuda-check    # GPU result: 8.0
pixi run --platform cuda-linux-64 build
pixi run --platform cuda-linux-64 brain
```

Para el consumidor del Ejercicio 2, publica antes los paquetes en el canal local:

```bash
cd soluciones/02-paquetes-ros
pixi publish --target-channel output
cd consumidor
pixi run dance
```

El consumidor no lleva `pixi.lock` versionado: apunta a un canal local con rutas absolutas de tu máquina.

Volver a resolver todas las soluciones tras cambiar un manifiesto:

```bash
pixi run lock-soluciones
```
