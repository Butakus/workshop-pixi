# Solución de problemas

## No se encuentra `pixi` después de instalarlo

El instalador pone `pixi` en `~/.pixi/bin` y añade ese directorio al `PATH`, pero solo lo ven los shells nuevos.
Reinicia la terminal y vuelve a comprobarlo con `pixi --version`.

Si sigue sin aparecer, añádelo tú en `~/.bashrc` o `~/.zshrc`:

```bash
export PATH="$HOME/.pixi/bin:$PATH"
```

En Windows el instalador actualiza el `PATH` del usuario en el registro: cierra Windows Terminal entero (todas las pestañas) y ábrelo de nuevo.

## Tienes ROS instalado en el sistema

Un `source /opt/ros/<distro>/setup.bash` (o el `install/setup.bash` de otro workspace) en tu `~/.bashrc` filtra `ROS_DISTRO`, `AMENT_PREFIX_PATH`, `PYTHONPATH`, `CMAKE_PREFIX_PATH`, `GZ_CONFIG_PATH`... a todos los entornos Pixi, y las dos instalaciones se mezclan.
Síntomas típicos: errores de Python que mencionan `/opt/ros/...`, `ModuleNotFoundError` en `rclpy`, o avisos como `ROS_DISTRO was set to 'rolling' before`.

Busca la línea:

```bash
grep -n "source /opt/ros\|setup.bash" ~/.bashrc
```

Coméntala:

```bash
sed -i 's|^source /opt/ros|# &|' ~/.bashrc
```

y abre una terminal nueva.
Tu ROS del sistema no se toca: descomenta la línea cuando lo necesites.
Si no quieres tocar el `~/.bashrc`, abre una terminal limpia con `env -i HOME=$HOME PATH=$HOME/.pixi/bin:/usr/bin:/bin TERM=$TERM DISPLAY=$DISPLAY WAYLAND_DISPLAY=$WAYLAND_DISPLAY XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR bash --norc`.

## El solver no encuentra un paquete de ROS

Primero comprueba que el canal `robostack-<distro>` está definido, **antes** de `conda-forge`:

```bash
pixi workspace channel add --prepend https://prefix.dev/robostack-lyrical
```

Después comprueba el nombre.
Los paquetes de RoboStack son `ros-<distro>-<nombre>` con guiones: `rclcpp` es `ros-lyrical-rclcpp`.

Si las dos cosas están bien, puede que el paquete no esté construido para tu plataforma.
Búscalo en [prefix.dev](https://prefix.dev/channels/robostack-lyrical) o desde la terminal:

```bash
pixi search -c https://prefix.dev/robostack-lyrical ros-lyrical-rclcpp
```

## `No candidates were found` con un paquete que acabas de publicar

- Si publicaste en un canal local, mira que el workspace consumidor solo declare las plataformas para las que publicaste (`pixi publish --target-platform` para otras).
- Si publicaste en prefix.dev hace un momento, puede que Pixi tenga el índice del canal en caché: `pixi clean cache --repodata -y`.

## Un entorno CUDA no se resuelve

Una build GPU solo se resuelve para una plataforma con versión de CUDA:

```bash
pixi workspace platform add cuda-linux-64=linux-64 --cuda 12
```

Ajusta la versión a lo que dice `nvidia-smi` en la máquina que tiene la GPU.

## Linux: no aparece la ventana de turtlesim

En escritorios modernos (GNOME, KDE...) una interfaz Qt como `turtlesim` se dibuja con Wayland, y el Qt de conda-forge necesita su plugin de Wayland como paquete aparte.
Lo notarás porque `ros2 run turtlesim turtlesim_node` aborta con:

```text
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized.
```

Añade el plugin y dile a Qt que lo use, solo para `linux-64`:

```bash
pixi add --platform linux-64 qt-wayland
pixi workspace activation env set --target linux-64 QT_QPA_PLATFORM=wayland-egl
```

```toml
[target.linux-64.dependencies]
qt-wayland = "*"

[target.linux-64.activation.env]
QT_QPA_PLATFORM = "wayland-egl"
```

## Gazebo no abre o va muy lento

`gz sim` necesita una pila gráfica (OpenGL) funcional. En máquinas virtuales o WSL2 sin GPU, prueba el render por software:

```bash
LIBGL_ALWAYS_SOFTWARE=1 pixi run sim
```

Si tienes ROS o Gazebo instalados en el sistema, comprueba también que no se cuelan sus variables (`GZ_CONFIG_PATH`, `GZ_SIM_RESOURCE_PATH`...): el síntoma es un error como `libgz-sim-gui.so: cannot open shared object file` o `Version mismatch` con rutas de `/opt/ros`. Ver [Tienes ROS instalado en el sistema](#tienes-ros-instalado-en-el-sistema).

## Windows: `Cannot open include file` o `failed to persist temporary file`

Windows limita la mayoría de rutas a 260 caracteres, y un entorno ROS anida mucho.
Mueve el workspace cerca de la raíz (`C:\ws`), o haz que Pixi guarde sus entornos en una ruta corta, una vez para todos los workspaces:

```powershell
pixi config set --global detached-environments 'C:\pix'
```

## Algo va lento

La primera descarga de un entorno ROS son varios GB, y la wifi del taller la comparte toda la sala.
Si nada avanza, cancela y repite el comando: Pixi guarda en caché lo que ya descargó y continúa donde lo dejó.

## Limpiar

```bash
pixi clean          # los entornos de este proyecto (.pixi/)
pixi clean cache    # la caché de paquetes compartida
```

El lockfile puede reconstruir cualquier entorno; lo único que cuesta es volver a descargar.
