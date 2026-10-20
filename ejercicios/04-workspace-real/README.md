# Ejercicio 4: compilar un workspace real

> **20 minutos, práctica** · **Trabaja en:** `ejercicios/04-workspace-real/` · **Solución:** [`soluciones/04-workspace-real/`](../../soluciones/04-workspace-real/)
>
> **Objetivo:** clonar repositorios de terceros, averiguar sus dependencias, compilarlos con colcon dentro de Pixi y lanzar un Kobuki en una casa en Gazebo, moviéndolo con el teclado.

Hasta ahora los paquetes venían escritos para el taller.
En la vida real tienes un `src/` con repositorios de otros, cada uno con sus `package.xml`, y la receta de siempre es `rosdep install` + `colcon build` + `source`.
Aquí haces lo mismo, pero sin `rosdep`, sin `apt` y sin `sudo`: las dependencias acaban escritas en tu `pixi.toml` y fijadas en el lockfile.

Vas a usar dos repositorios:

- [`EasyNavigation/easynav_playgrounds`](https://github.com/EasyNavigation/easynav_playgrounds/tree/pichi-workshop), rama `pichi-workshop`: el modelo del Kobuki (`easynav_playground_kobuki_description`) y la simulación en Gazebo de una casa (`easynav_playground_kobuki_worlds`).
- [`ros2/teleop_twist_keyboard`](https://github.com/ros2/teleop_twist_keyboard), rama `rolling`: el nodo de teleoperación con el teclado.

Empieza aquí:

```bash
cd ejercicios/04-workspace-real
```

> **Gazebo necesita OpenGL.** Si estás en una máquina virtual o en WSL2 sin GPU y la ventana no abre o va muy lenta, mira [Solución de problemas](../../referencia/problemas.md#gazebo-no-abre-o-va-muy-lento).

---

## 4.1 Crea el workspace con ROS y las herramientas

1. Crea un workspace de Pixi en este directorio con los canales `https://prefix.dev/robostack-lyrical` y `conda-forge`.
2. Añade `ros-lyrical-ros-base` y `ros-dev-tools` (que trae colcon y también `vcstool`).

<details>
<summary>Solución</summary>

```bash
pixi init -c https://prefix.dev/robostack-lyrical -c conda-forge
pixi add ros-lyrical-ros-base ros-dev-tools
```

</details>

## 4.2 Clona los repositorios con un fichero `.repos`

En ROS, la lista de repositorios de un workspace se suele guardar en un fichero `.repos`, y [`vcstool`](https://github.com/dirk-thomas/vcstool) los clona todos de una vez.
Así el workspace entero (repositorios + entorno) queda descrito en ficheros que van a git.

1. Crea `workspace.repos` con los dos repositorios y sus ramas.
2. Clónalos en `src/` con `vcs import`.
3. Conviértelo en una task `importar`.

<details>
<summary>Solución</summary>

```yaml
# workspace.repos
repositories:
  easynav_playgrounds:
    type: git
    url: https://github.com/EasyNavigation/easynav_playgrounds.git
    version: pichi-workshop
  teleop_twist_keyboard:
    type: git
    url: https://github.com/ros2/teleop_twist_keyboard.git
    version: rolling
```

```bash
pixi task add importar "mkdir -p src && vcs import --input workspace.repos src"
pixi run importar
ls src     # easynav_playgrounds  teleop_twist_keyboard
```

`mkdir -p` funciona también en Windows: el shell de las tasks de Pixi lo trae integrado.

</details>

## 4.3 Averigua las dependencias (lo que haría `rosdep`)

`rosdep` no sirve dentro de Pixi: llama a `apt` o `pip` del sistema.
Lo que hace es leer los `package.xml` y traducir cada dependencia a un paquete del sistema.
Aquí la traducción es directa: `ros_gz_sim` en un `package.xml` es `ros-lyrical-ros-gz-sim` en RoboStack.

1. Mira los `package.xml` de los tres paquetes y apunta sus dependencias que no estén ya en el workspace.
   Pista: `grep -h "depend>" src/*/package.xml src/*/*/*/package.xml`.
2. Añádelas con `pixi add`, con el prefijo `ros-lyrical-` y guiones en vez de guiones bajos.
   Las que vienen en `ros-lyrical-ros-base` (`rclpy`, `geometry_msgs`, `launch`, `launch_ros`...) no hacen falta.

<details>
<summary>Solución</summary>

`easynav_playground_kobuki_worlds` pide `gz_sim_vendor`, `ros_gz_sim`, `ros_gz_bridge`, `robot_state_publisher`, `xacro` y `launch_yaml`, además de `easynav_playground_kobuki_description`, que está en el propio workspace.
`teleop_twist_keyboard` solo pide `rclpy`, `geometry_msgs` y `rcl_interfaces`, que ya están.

```bash
pixi add ros-lyrical-gz-sim-vendor ros-lyrical-ros-gz-sim ros-lyrical-ros-gz-bridge \
  ros-lyrical-xacro ros-lyrical-robot-state-publisher ros-lyrical-launch-yaml
```

Esa línea es tu `rosdep install`, pero escrita en el `pixi.toml` y fijada en el `pixi.lock`: tu compañero obtiene exactamente las mismas versiones.

> Para workspaces grandes, [`pixi-ros`](https://github.com/ruben-arts/pixi-ros) hace esta traducción por ti: `pixi global install pixi-ros` y `pixi-ros init --distro lyrical`.

</details>

## 4.4 Compila y lanza la simulación

Igual que en el paso 1.4 del Ejercicio 1.

1. Añade una task `build` que ejecute `colcon build` y dependa de `importar`.
2. Carga el overlay al activar el entorno (`install/setup.sh`, o `install/setup.bat` en Windows).
3. Compila.
4. Añade una task `sim` que lance `ros2 launch easynav_playground_kobuki_worlds gazebo_sim.launch.yaml` y dependa de `build`, y ejecútala.

<details>
<summary>Solución</summary>

```bash
pixi task add build "colcon build" --depends-on importar
pixi workspace activation scripts add --target unix install/setup.sh
pixi workspace activation scripts add --target win-64 install/setup.bat
pixi run build
pixi task add sim "ros2 launch easynav_playground_kobuki_worlds gazebo_sim.launch.yaml" --depends-on build
pixi run sim
```

Se abre Gazebo con la casa y el Kobuki en el salón.
Los tres paquetes compilan en un par de segundos: solo instalan ficheros (URDF, mundo, launchers) o son Python.
Si ves un `SetuptoolsDeprecationWarning` al compilar `teleop_twist_keyboard`, es solo un aviso.

</details>

## 4.5 Mueve el Kobuki

`teleop_twist_keyboard` publica `geometry_msgs/msg/Twist` en `/cmd_vel`, que es justo lo que el puente ROS–Gazebo de la simulación le pasa al robot.

1. Añade una task `teleop` que ejecute `ros2 run teleop_twist_keyboard teleop_twist_keyboard`.
2. Con la simulación abierta, ejecútala en otra terminal y pasea el Kobuki por la casa.
3. En una tercera terminal, mira lo que publica el robot.

<details>
<summary>Solución</summary>

```bash
pixi task add teleop "ros2 run teleop_twist_keyboard teleop_twist_keyboard"
pixi run teleop          # i: avanzar, j/l: girar, k: parar
```

```bash
pixi run ros2 topic list            # /cmd_vel /odom /scan_raw /tf /clock ...
pixi run ros2 topic echo /odom --field pose.pose.position
```

</details>

El `pixi.toml` completo está en [`soluciones/04-workspace-real/pixi.toml`](../../soluciones/04-workspace-real/pixi.toml).
Desde la solución, todo el flujo es `pixi run sim`: clona, compila y lanza.

---

## Comprueba tu trabajo

```bash
pixi run sim                                       # Gazebo con el Kobuki en la casa
pixi run teleop                                    # en otra terminal: el Kobuki se mueve
pixi run ros2 pkg executables teleop_twist_keyboard
```

Borra `src/`, `build/`, `install/` y `log/` y vuelve a hacer `pixi run sim`: el workspace entero se reconstruye desde `workspace.repos`, `pixi.toml` y `pixi.lock`.

## Si te sobra tiempo

- `teleop_twist_keyboard` también existe ya construido en RoboStack: cambia el repositorio por `pixi add ros-lyrical-teleop-twist-keyboard`. Mezclar paquetes binarios y paquetes compilados desde fuente es lo normal.
- Constrúyelo como en el Ejercicio 2, sin colcon: los dos paquetes del Kobuki ya traen su `pixi.toml` para `pixi-build-ros`.
  Activa `pixi-build`, añade `pixi-build-ros` a `[workspace.dependencies]` y usa dependencias `path` sobre `src/easynav_playgrounds/playground_kobuki/easynav_playground_kobuki_description` y `..._worlds`.
  Fíjate en que entonces **no hace falta** añadir a mano las dependencias de Gazebo del paso 4.3: el backend las lee del `package.xml`.
- Lanza dos Kobukis: `ros2 launch easynav_playground_kobuki_worlds multirobot_gazebo_sim.launch.yaml`, y mueve cada uno con `pixi run teleop --ros-args -r cmd_vel:=/r1/cmd_vel`.
- Añade una plataforma más con `pixi workspace platform add` y comprueba con `pixi lock` que el mismo workspace se resuelve también para la máquina de tu compañero.

> **Con tu propio workspace:** son exactamente estos pasos.
> Un `.repos` con tus repositorios (o los que ya tengas en `src/`), las dependencias de sus `package.xml` traducidas a `ros-<distro>-*` (o generadas con `pixi-ros`), `colcon build` y la activación.
> Después puedes ir pasando paquetes a `pixi-build-ros` uno a uno, como en el Ejercicio 2.
