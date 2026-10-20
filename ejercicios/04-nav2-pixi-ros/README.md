# Ejercicio 4 (opcional): un workspace real, Nav2 con `pixi-ros`

> **Opcional / demo del instructor** · Sin carpeta de solución: el `pixi.toml` lo **genera** `pixi-ros init` a partir de los `package.xml` reales de Nav2, y depende de la versión de Nav2 que clones.
>
> **Objetivo:** migrar un workspace grande que ya existe (más de 80 paquetes C++) sin traducir dependencias a mano, compilarlo y lanzar la simulación con RViz2.

Hasta ahora, paquetes de juguete. ¿Y un workspace real y grande que hoy compilas con `rosdep` y `colcon`?

`rosdep` no sirve dentro de Pixi (llama a `apt`/`pip` del sistema). [`pixi-ros`](https://github.com/ruben-arts/pixi-ros) lee los `package.xml` del workspace y genera el `pixi.toml`, traduciendo cada dependencia a su paquete de RoboStack o conda-forge. Mantiene colcon para compilar, como en el Ejercicio 1; cuando quieras, puedes ir pasando paquetes a `pixi-build-ros` uno a uno como en el Ejercicio 2.

> Nav2 tarda en compilar. En el taller el instructor lanza el build con antelación y enseña el resultado en vivo.

## Comandos, en orden

```bash
# 1. Instalar la herramienta (una vez)
pixi global install pixi-ros

# 2. Crear el workspace y clonar Nav2
mkdir -p nav2_ws/src && cd nav2_ws
git clone -b jazzy https://github.com/ros-navigation/navigation2.git src/navigation2

# 3. Rellenar dependencias automáticamente
pixi-ros init --distro jazzy --platform linux-64

# 4. Ajustar versiones de dependencias
pixi add gcc_linux-64=13.3.0 gxx_linux-64=13.3.0
pixi add libboost=1.88.0 libboost-devel=1.88.0
pixi add ros-jazzy-rviz2

# 5. Instalar y compilar
pixi install
pixi run build

# 6. Verificar
pixi shell
ros2 pkg list | grep nav2
ros2 pkg executables nav2_costmap_2d

# 7. Simulación + RViz2
ros2 launch nav2_bringup tb3_simulation_launch.py
```

En RViz2: **2D Pose Estimate** (localizar el robot) → **Nav2 Goal** (marcar destino) → el robot navega solo.

## Troubleshooting

- **`gz sim` no abre ventana / va muy lento**: necesita una pila gráfica (OpenGL) funcional. En VMs o WSL2 sin passthrough de GPU, prueba:
  ```bash
  LIBGL_ALWAYS_SOFTWARE=1 ros2 launch nav2_bringup tb3_simulation_launch.py
  ```
- **`pixi-ros init` no encuentra alguna dependencia** (aparece como `NOT FOUND` en la tabla de validación): revisa que el nombre del paquete en `package.xml` coincida con el índice de la distro ROS; en último caso se puede añadir un canal extra con `--channel`.
- **`pixi install` falla al leer el `pixi.toml` generado**: en algunas versiones `pixi-ros init` escribe la dependencia fijada de `xtensor` como una clave TOML inválida, `"xtensor ==0.24.7" = "*"`. Cámbiala por `xtensor = "==0.24.7"`.
- **Tienes ROS instalado en el sistema** (`source /opt/ros/...` en tu `~/.bashrc`): sus variables se cuelan en el entorno Pixi y mezclan distros. Ver [Solución de problemas](../../referencia/problemas.md#tienes-ros-instalado-en-el-sistema).
- **El build tarda mucho**: es esperable, Nav2 son más de 80 paquetes C++ — el instructor suele lanzarlo con antelación y mostrar el resultado en vivo.

## Referencia

- Herramienta: <https://github.com/ruben-arts/pixi-ros>
- Repo de Nav2: <https://github.com/ros-navigation/navigation2> (rama `jazzy`)
