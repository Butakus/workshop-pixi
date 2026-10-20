# Desde que uso Pixi estoy tan Pichi

## Workspaces ROS 2 declarativos y reproducibles con Pixi y RoboStack

Material del taller (~3 horas) sobre entornos reproducibles para ROS 2 con [Pixi](https://pixi.prefix.dev/), [RoboStack](https://robostack.github.io/) y [prefix.dev](https://prefix.dev/).

Autores: Francisco Martín Rico ([fmrico@gmail.com](mailto:fmrico@gmail.com)), Esteve Fernández ([esteve.fernandez@gmail.com](mailto:esteve.fernandez@gmail.com)), Juan Sebastián Cely ([juan.cely@urjc.es](mailto:juan.cely@urjc.es)), Francisco Miguel Moreno ([franciscom.moreno@urjc.es](mailto:franciscom.moreno@urjc.es)).

Pixi es un gestor de paquetes rápido y multiplataforma construido sobre el ecosistema conda.
RoboStack distribuye ROS 2 como paquetes conda.
Juntos permiten declarar todo un entorno ROS (librerías del sistema, paquetes Python y nodos ROS) en un único `pixi.toml`, con un lockfile que garantiza la reproducibilidad.
Al final del taller tu workspace funciona en cualquier máquina con tres comandos: `git clone`, `cd`, `pixi run`.

## Qué hay en este repositorio

```text
slides/        las diapositivas (slides/workshop.pdf; fuente en workshop.src.tex)
ejercicios/    donde trabajas: un directorio por ejercicio, con las instrucciones en su README
soluciones/    los workspaces terminados, con lockfile, probados en CI en Linux, macOS y Windows
referencia/    chuleta de comandos y solución de problemas
```

## Qué vas a hacer

| Duración | Bloque | Formato |
| --- | --- | --- |
| 10 min | Bienvenida y comprobación de la preparación | juntos |
| 10 min | Robótica para todos: por qué ROS necesita algo mejor | hablamos |
| 25 min | Pixi en 25 minutos | hablamos |
| 40 min | [Ejercicio 1: tu primer workspace ROS 2](ejercicios/01-workspace-ros/) | escribís |
| 15 min | Construir paquetes ROS con Pixi | hablamos |
| 35 min | [Ejercicio 2: construir y publicar paquetes ROS](ejercicios/02-paquetes-ros/) | escribís |
| 10 min | Colaboración, CI/CD y Docker | hablamos |
| 20 min | [Ejercicio 3: listo para tu equipo](ejercicios/03-colaboracion/) | escribís |
| 20 min | [Ejercicio 4: compilar un workspace real](ejercicios/04-workspace-real/) | escribís |

- Montar un workspace ROS 2 desde cero con Pixi y RoboStack, y tener dos distros (Lyrical y Jazzy) a la vez.
- Darle a la tortuga un cerebro con PyTorch, y resolver el entorno para una máquina con GPU y para una Jetson desde tu portátil.
- Construir tus propios paquetes ROS con Pixi a partir de su `package.xml`, sin colcon y sin `source`, y publicarlos en un canal (local o de prefix.dev) para instalarlos desde cualquier otro workspace. Sin montar una buildfarm.
- Llevarlo al equipo: un lockfile para Linux, macOS y Windows, CI en dos líneas, una imagen Docker y un entorno empaquetado que se ejecuta sin Pixi.
- Compilar un workspace real de terceros (clonado con `vcs import`, dependencias traducidas desde los `package.xml`, sin `rosdep`) y lanzar un Kobuki en una casa en Gazebo.

Puedes trabajar con el ejemplo de este repositorio o traer tu propio workspace ROS: cada ejercicio explica el paso equivalente.

## Antes del taller (hazlo en casa, no con la wifi del taller)

ROS es grande y la wifi de un taller no. Hacer esto antes te ahorra media hora.

### 1. Instala Pixi

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

En Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

Abre una terminal nueva y comprueba que tienes la 0.77 o posterior con `pixi --version`.

> **Windows y C++:** los ejercicios en C++ necesitan las Visual Studio 2022 Build Tools con la carga de trabajo de C++ y un Windows SDK ([instrucciones de Microsoft](https://learn.microsoft.com/es-es/cpp/build/vscpp-step-0-installation)). Pixi activa esas herramientas, pero no las instala.

### 2. Descarga el material

```bash
git clone <url-de-este-repositorio> workshop-pixi
cd workshop-pixi
```

### 3. Calienta la caché (este es el paso importante)

Los ejercicios usan dos distribuciones de ROS y PyTorch: varios GB. Hazlo la tarde antes.

```bash
pixi install --all --manifest-path soluciones/01-workspace-ros/pixi.toml
pixi install --manifest-path soluciones/02-paquetes-ros/pixi.toml
pixi install --manifest-path soluciones/04-workspace-real/pixi.toml
```

`--all` descarga los entornos de Lyrical y de Jazzy, incluido PyTorch para tu máquina.

### 4. Comprueba que funciona

```bash
pixi run --manifest-path soluciones/01-workspace-ros/pixi.toml sim
```

Debería aparecer una ventana con una tortuga. Ciérrala y prueba la segunda distro:

```bash
pixi run --manifest-path soluciones/01-workspace-ros/pixi.toml -e jazzy sim
```

Si las dos funcionan, estás listo.

### Opcional

- **Docker**, si quieres hacer la parte de Docker del Ejercicio 3 ([descarga](https://docs.docker.com/get-started/get-docker/)).
- **Cuenta gratuita en [prefix.dev](https://prefix.dev/)**, si quieres publicar tus paquetes en un canal en la nube en el Ejercicio 2 (si no, se publica en un canal local).
- **Cuenta de GitHub**, para la CI del Ejercicio 3.
- **Comprobar que Gazebo se ve**, para el Ejercicio 4 (un Kobuki en una casa). `gz sim` necesita OpenGL; en máquinas virtuales o WSL2 sin GPU puede fallar. Pruébalo con la solución, que clona, compila y lanza la simulación:

  ```bash
  pixi run --manifest-path soluciones/04-workspace-real/pixi.toml sim
  ```

  Si no abre o va muy lento, mira [solución de problemas](referencia/problemas.md#gazebo-no-abre-o-va-muy-lento). Si sigue sin ir, ese ejercicio se puede seguir en la pantalla del instructor.

### Lo que no necesitas

- **No necesitas ROS instalado.** Ni `apt`, ni `rosdep`, ni `/opt/ros`.
  Si ya lo tienes, **desactiva el `source /opt/ros/<distro>/setup.bash` de tu `~/.bashrc` durante el taller**: sus variables se cuelan en todas las terminales y mezclan distros con el entorno de Pixi. Ver [solución de problemas](referencia/problemas.md#tienes-ros-instalado-en-el-sistema).
- No necesitas `sudo` ni una máquina virtual.
- No necesitas GPU. Solo el paso opcional 1.9 (ejecutar CUDA de verdad) necesita una GPU NVIDIA.

Si algo falla, mira [solución de problemas](referencia/problemas.md) y, si no, escríbenos con antelación.

## Trabajar en el material

Las tareas del material también son tasks de Pixi (`pixi task list`):

| Comando | Qué hace |
| --- | --- |
| `pixi run slides` | Genera `slides/workshop.tex` desde `workshop.src.tex` y compila `slides/workshop.pdf` (con `tectonic`, sin TeX del sistema) |
| `pixi run lock-soluciones` | Vuelve a resolver todas las soluciones para todas las plataformas |

Edita `slides/workshop.src.tex`, no `workshop.tex`: los listados de ficheros se escriben entre marcadores `%%CODE <lenguaje>` / `%%END` y `slides/generar.py` los colorea con Pygments.

## Agradecimientos y licencia

Este taller adapta el enfoque, la estructura y los ejercicios del taller de prefix.dev en ROSCon 2026, [*Declarative ROS workspaces with Pixi and RoboStack*](https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/) ([repositorio](https://github.com/prefix-dev/roscon-2026-declarative-ros-workspaces-with-pixi)), de Ruben Arts, Wolf Vollprecht y Bas Zalmstra.
Los paquetes `turtle_dancer`, `turtle_choreographer` y `turtle_brain`, el script `check_overlay.py`, los Dockerfile y la CI proceden de ese repositorio, publicado bajo licencia BSD-3-Clause, Copyright (c) 2026, Prefix.dev GmbH: ver [`LICENSE-prefix-dev`](LICENSE-prefix-dev).
