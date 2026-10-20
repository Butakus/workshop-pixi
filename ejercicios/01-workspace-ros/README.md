# Ejercicio 1: tu primer workspace ROS 2

> **40 minutos, práctica** · **Trabaja en:** `ejercicios/01-workspace-ros/` · **Solución:** [`soluciones/01-workspace-ros/`](../../soluciones/01-workspace-ros/)
>
> **Objetivo:** un `pixi.toml` y un `pixi.lock` que te den turtlesim funcionando, un nodo propio compilado con colcon, el mismo workspace con dos distribuciones de ROS, y un nodo con PyTorch resuelto para una máquina con GPU y para una Jetson, todo desde tu portátil.

Este ejercicio es una serie de pasos cortos.
Cada uno dice qué hacer, y los comandos están plegados en una solución debajo.
Inténtalo primero por tu cuenta (la [chuleta](../../referencia/chuleta.md) ayuda con los nombres de los comandos) y abre la solución si te atascas.

Empieza en este directorio:

```bash
cd ejercicios/01-workspace-ros
```

Ya hay dos paquetes ROS escritos en `src/`: `turtle_dancer` (C++) y `turtle_brain` (Python + PyTorch).
**No hay `pixi.toml` a propósito**: crearlo es el primer paso.

---

## 1.1 Inicializa un workspace

1. Crea un manifiesto de Pixi en este directorio con la CLI de Pixi.
2. Abre `pixi.toml` y mira con qué plataformas y canales empieza un workspace nuevo.

<details>
<summary>Solución</summary>

```bash
pixi init
```

El `pixi.toml` resultante (el autor y la plataforma se leen de tu máquina):

```toml
[workspace]
authors = ["Jane Doe <jane.doe@example.com>"]
channels = ["conda-forge"]
name = "01-workspace-ros"
platforms = ["linux-64"]
version = "0.1.0"

[tasks]

[dependencies]
```

</details>

## 1.2 Instala ROS 2

Los paquetes de ROS viven en un canal de RoboStack, no en `conda-forge`.
Un canal es como una fuente de `apt`, pero escrita en tu manifiesto.

1. Añade el canal `https://prefix.dev/robostack-lyrical` con **más prioridad** que `conda-forge`.
   Pista: `pixi workspace channel add --help`.
2. Añade `ros-lyrical-ros-base` y `ros-lyrical-turtlesim` como dependencias.
3. Mira qué se ha instalado realmente en el entorno.
4. Demuestra que ROS funciona listando sus topics.
   Pista: cualquier comando se ejecuta dentro del entorno con `pixi run <comando>`, o abre un shell dentro con `pixi shell`.

<details>
<summary>Solución</summary>

```bash
# 1
pixi workspace channel add --prepend https://prefix.dev/robostack-lyrical
# 2
pixi add ros-lyrical-ros-base ros-lyrical-turtlesim
# 3
pixi list
# 4
pixi run ros2 topic list
# o desde un shell dentro del entorno:
pixi shell
ros2 topic list
exit
```

Ha aparecido un `pixi.lock` junto al manifiesto.
Registra cada paquete que resolvió el paso 2, y `pixi run` instala a partir de él antes de ejecutar nada.

```toml
[workspace]
channels = ["https://prefix.dev/robostack-lyrical", "conda-forge"]
# ...

[dependencies]
ros-lyrical-ros-base = ">=0.13.0,<0.14"
ros-lyrical-turtlesim = ">=1.10.9,<2"
```

</details>

## 1.3 Convierte los comandos en tasks

Los comandos que repites reciben un nombre en el manifiesto, para que tus compañeros los ejecuten sin saberse el conjuro completo.

1. Añade una task `sim` que ejecute `ros2 run turtlesim turtlesim_node`.
2. Añade una task `teleop` para `ros2 run turtlesim turtle_teleop_key`, y otra `topics` para `ros2 topic list`.
3. Abre dos terminales y mueve la tortuga: el simulador en una, la teleoperación en la otra.

<details>
<summary>Solución</summary>

```bash
# 1
pixi task add sim "ros2 run turtlesim turtlesim_node"
# 2
pixi task add teleop "ros2 run turtlesim turtle_teleop_key"
pixi task add topics "ros2 topic list"
# 3: en dos terminales
pixi run sim        # aparece una tortuga
pixi run teleop     # haz clic en esta terminal y usa las flechas
```

```toml
[tasks]
sim = "ros2 run turtlesim turtlesim_node"
teleop = "ros2 run turtlesim turtle_teleop_key"
topics = "ros2 topic list"
```

> **¿No aparece la ventana en Linux?** Mira [Solución de problemas](../../referencia/problemas.md#linux-no-aparece-la-ventana-de-turtlesim) (Wayland / `qt-wayland`).

</details>

## 1.4 Compila tu propio nodo con colcon

`src/turtle_dancer/` es un paquete ROS 2 en C++ pequeño, ya escrito.
Para compilarlo hacen falta herramientas y las librerías de ROS que incluye, y vienen de los mismos canales que todo lo demás.

1. Añade `ros-dev-tools`: un único paquete que trae colcon, CMake y los compiladores.
   Las librerías de ROS que usa el nodo ya están: `ros-lyrical-ros-base` las incluye.
2. Compila el workspace con colcon.
3. Intenta ejecutar el nodo con `ros2 run turtle_dancer dance` y lee el error.
4. Arréglalo: haz que Pixi cargue el overlay de colcon (`install/`) cada vez que se activa el entorno.
   Pista: busca [`activation`](https://pixi.prefix.dev/latest/reference/pixi_manifest/#the-activation-table) en la documentación de Pixi, y ojo: el nombre del script cambia según la plataforma.
5. Añade una task `build`, y una task `dance` que dependa de ella.
6. Ejecuta el simulador en una terminal y tu nodo en otra.

<details>
<summary>Solución</summary>

```bash
# 1
pixi add ros-dev-tools
# 2
pixi run colcon build
# 3
pixi run ros2 run turtle_dancer dance
# Package 'turtle_dancer' not found
```

El error es el esperado.
colcon compiló el nodo en `install/`, y `ros2` solo lo encuentra cuando ese overlay está cargado.
Puedes hacer `source` a mano en cada terminal, o dejar que lo haga Pixi con un script de activación.

```bash
# 4, Linux y macOS
pixi workspace activation scripts add --target unix install/setup.sh
# 4, Windows
pixi workspace activation scripts add --target win-64 install/setup.bat
```

El script solo existe tras el primer `colcon build`, así que Pixi avisa hasta entonces.

```bash
# 5
pixi task add build "colcon build"
pixi task add dance "ros2 run turtle_dancer dance" --depends-on build
# 6: en dos terminales
pixi run sim
pixi run dance    # la tortuga empieza a bailar
```

```toml
[tasks]
sim = "ros2 run turtlesim turtlesim_node"
teleop = "ros2 run turtlesim turtle_teleop_key"
topics = "ros2 topic list"
build = "colcon build"
dance = { cmd = "ros2 run turtle_dancer dance", depends-on = ["build"] }

[dependencies]
ros-lyrical-ros-base = ">=0.13.0,<0.14"
ros-lyrical-turtlesim = ">=1.10.9,<2"
ros-dev-tools = ">=1.0.2,<2"

[target.unix.activation]
scripts = ["install/setup.sh"]
```

colcon ha dejado `build/`, `install/` y `log/`, exactamente como fuera de Pixi.
Fíjate en que **no hemos necesitado** `setuptools<=58.2.0` ni `empy==3.3.4`: `ros-dev-tools` trae versiones compatibles.

</details>

## 1.5 Dos distros de ROS, un workspace

Una segunda distribución de ROS es un segundo **entorno** en el mismo manifiesto.
Las herramientas y las tasks se comparten, pero los paquetes compilados pertenecen a la distro que los compiló: cada entorno tiene sus propios directorios de colcon y activa solo su overlay.

1. Mueve el canal de Lyrical y los paquetes `ros-lyrical-*` a `[environments.default]`.
2. Pon la activación dentro del entorno por defecto, apuntando a `install/default/local_setup.sh`.
3. Añade un entorno `jazzy` con su propio canal (`https://prefix.dev/robostack-jazzy`), sus paquetes `ros-jazzy-*` y su activación en `install/jazzy/`.
4. Cambia la task `build` para que colcon use `build/<entorno>`, `install/<entorno>` y `log/<entorno>`.
   Pixi define `$PIXI_ENVIRONMENT_NAME` en su shell de tasks multiplataforma.
5. Desde una terminal normal (fuera de `pixi shell`), compila una vez en cada entorno.
6. Ejecuta turtlesim y `dance` en cada distribución. Para cada simulador antes de lanzar el siguiente.

<details>
<summary>Solución</summary>

Deja solo `conda-forge` en los canales del workspace, y mueve las dependencias de ROS y la activación a cada entorno:

```toml
[environments.default]
channels = ["https://prefix.dev/robostack-lyrical", "conda-forge"]

[environments.default.dependencies]
ros-lyrical-ros-base = ">=0.13"
ros-lyrical-turtlesim = ">=1.10"

[environments.default.target.unix.activation]
scripts = ["install/default/local_setup.sh"]

[environments.default.target.win-64.activation]
scripts = ["install/default/local_setup.bat"]

[environments.jazzy]
channels = ["https://prefix.dev/robostack-jazzy", "conda-forge"]

[environments.jazzy.dependencies]
ros-jazzy-ros-base = "*"
ros-jazzy-turtlesim = "*"

[environments.jazzy.target.unix.activation]
scripts = ["install/jazzy/local_setup.sh"]

[environments.jazzy.target.win-64.activation]
scripts = ["install/jazzy/local_setup.bat"]
```

Sustituye la task `build` por:

```toml
[tasks.build]
cmd = "colcon --log-base log/$PIXI_ENVIRONMENT_NAME build --base-paths src --build-base build/$PIXI_ENVIRONMENT_NAME --install-base install/$PIXI_ENVIRONMENT_NAME"
```

Usamos `local_setup` y no `setup`: Pixi ya aporta el underlay de ROS correcto, y el `setup` de colcon volvería a cargar los underlays grabados al compilar, que pueden ser de la otra distro.

```bash
# 5
pixi run -e default build
pixi run -e jazzy build
# 6: para cada simulador con Ctrl+C antes del siguiente
pixi run -e default sim
pixi run -e jazzy sim
```

Todo lo que está a nivel de workspace pertenece a la *feature* por defecto, y todos los entornos la incluyen.
Por eso `sim`, `dance` y `build` se comparten, mientras que las rutas de build y la activación eligen la distro correcta.

</details>

## 1.6 Dale a la tortuga un cerebro con PyTorch

`src/turtle_brain/` es un paquete `ament_python` ya escrito.
Mueve la tortuga con un cálculo pequeño en PyTorch, en la GPU si hay una y en la CPU si no.

1. Añade `pytorch` como dependencia.
2. Añade una task `brain` que ejecute `ros2 run turtle_brain brain` y dependa de `build`.
3. Ejecuta `pixi run build` una vez, para que exista el overlay antes de activarlo.
4. Ejecuta el simulador y el cerebro, en dos terminales.

<details>
<summary>Solución</summary>

```bash
# 1
pixi add pytorch
# 2
pixi task add brain "ros2 run turtle_brain brain" --depends-on build
# 3
pixi run build
# 4: en dos terminales
pixi run sim
pixi run brain    # la tortuga se mueve y el nodo dice "thinking on: cpu"
```

En un portátil sin GPU NVIDIA el nodo corre en la CPU. Lo siguiente es darle una GPU.

</details>

## 1.7 Apunta a una GPU, y a todas las plataformas

Una build de PyTorch con GPU solo se resuelve para una plataforma que tenga CUDA.
Le dices a Pixi que una plataforma tiene GPU dándole una versión de CUDA: el *paquete virtual* `__cuda`.

1. Añade una plataforma CUDA llamada `cuda-linux-64`, sobre `linux-64`, con CUDA 12.
   Dale prioridad sobre `linux-64` normal, para que una máquina con GPU compatible elija la build CUDA.
2. Añade también las plataformas normales: `linux-64`, `osx-arm64`, `win-64`.
3. Haz que PyTorch use la build GPU donde haya CUDA y la de CPU en el resto.
   Pista: una condición `when` en la dependencia.
4. Mira qué obtendría cada plataforma, todo desde tu máquina.

<details>
<summary>Solución</summary>

```bash
# 1
pixi workspace platform add cuda-linux-64=linux-64 --cuda 12
# 2
pixi workspace platform add linux-64 osx-arm64 win-64
pixi workspace platform move cuda-linux-64 --to-top
```

```toml
[dependencies]
# 3: build GPU donde haya CUDA, build CPU en el resto.
pytorch-gpu = { version = ">=2.5", when = "__cuda" }
pytorch = ">=2.5"
```

```bash
# 4
pixi list --platform win-64          # tu compañera con Windows: build CPU
pixi list --platform cuda-linux-64   # la máquina con GPU: build CUDA
```

Resolver no es instalar: esto funciona desde cualquier portátil de la sala, incluso los Mac.

</details>

## 1.8 Apunta a una Jetson

Una Jetson es `linux-aarch64` con CUDA.
Es solo otra plataforma, así que se añade igual, con su versión de CUDA.

1. Añade una plataforma `jetson` sobre `linux-aarch64` con CUDA 13.
2. Resuelve el entorno del robot desde tu portátil.

<details>
<summary>Solución</summary>

```bash
# 1
pixi workspace platform add jetson=linux-aarch64 --cuda 13
# 2
pixi list --platform jetson
```

Damos por hecho JetPack 7.2 o posterior, que trae CUDA 13.
Con un JetPack anterior la versión cambia (JetPack 6 trae CUDA 12.6): ajusta `cuda` a lo que tenga tu robot.

Eso es un entorno CUDA completo para una máquina que no tienes delante.
Resuelves en el portátil e instalas en la Jetson.

</details>

## 1.9 (Opcional) Ejecútalo en una GPU de verdad

> **Necesita una GPU NVIDIA** con un driver compatible (en Linux), o la Jetson del paso 1.8.
> Declarar CUDA permite a Pixi *resolver* un entorno; no le da una GPU a tu portátil. Una GPU de Apple no ejecuta CUDA.

`src/turtle_brain/turtle_brain/check_cuda.py` hace una operación con tensores directamente en CUDA, sin nodos ni ventanas, así que funciona por SSH.
Falla si CUDA no está disponible, en vez de usar la CPU en silencio.

1. Comprueba que `nvidia-smi` ve la GPU.
2. Añade una task `cuda-check` que ejecute `python src/turtle_brain/turtle_brain/check_cuda.py`.
3. Ejecútala en la plataforma `cuda-linux-64` (en la Jetson, `jetson`).
4. Ejecuta el cerebro en la misma plataforma. Páralo con Ctrl+C cuando diga `thinking on: cuda`.

<details>
<summary>Solución</summary>

```bash
nvidia-smi
pixi task add cuda-check "python src/turtle_brain/turtle_brain/check_cuda.py"
pixi run --platform cuda-linux-64 cuda-check     # ... GPU result: 8.0
pixi run --platform cuda-linux-64 build
pixi run --platform cuda-linux-64 brain
```

</details>

El `pixi.toml` completo está en [`soluciones/01-workspace-ros/pixi.toml`](../../soluciones/01-workspace-ros/pixi.toml).

---

## Comprueba tu trabajo

```bash
pixi run topics              # ROS está vivo
pixi run dance               # tu nodo mueve la tortuga
pixi run brain               # un nodo con PyTorch mueve la tortuga
pixi run -e jazzy dance      # ...y el mismo workspace con otra distro
pixi list --platform jetson  # un entorno para Jetson, resuelto desde tu portátil
```

## Si te sobra tiempo

- Añade un visor con `pixi add ros-lyrical-rviz2` y ejecuta `pixi run rviz2`.
- Borra la carpeta `.pixi/`, ejecuta `pixi install` y mira cómo el entorno se reconstruye desde el lockfile.
- Usa `pixi tree ros-lyrical-rclcpp` para ver por qué está cada paquete en el entorno.

> **Con tu propio workspace:** son los mismos pasos.
> `pixi init` en el repo, añade el canal `robostack-<tu-distro>`, añade los paquetes `ros-<tu-distro>-*` de los que dependes, y haz funcionar `colcon build` dentro del entorno como en el paso 1.4.
> Para no traducir los `package.xml` a mano, [`pixi-ros`](https://github.com/ruben-arts/pixi-ros) los lee y genera el `pixi.toml`: `pixi global install pixi-ros` y `pixi-ros init --distro <tu-distro>` en la raíz del workspace.

---

Siguiente: [Ejercicio 2: construir paquetes ROS con Pixi](../02-paquetes-ros/).
