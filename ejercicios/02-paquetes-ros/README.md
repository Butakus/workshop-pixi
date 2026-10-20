# Ejercicio 2: construir paquetes ROS con Pixi

> **35 minutos, práctica** · **Trabaja en:** `ejercicios/02-paquetes-ros/` · **Solución:** [`soluciones/02-paquetes-ros/`](../../soluciones/02-paquetes-ros/)
>
> **Objetivo:** pasarle la compilación a Pixi.
> El mismo nodo C++ del Ejercicio 1, más uno en Python, construidos e instalados desde su `package.xml`: sin `colcon build`, sin `source install/setup.bash`, sin directorio `build/`.
> Y al final, publicarlos como paquetes conda e instalarlos desde otro workspace.

En el Ejercicio 1 compilaste el nodo a la manera de ROS: colcon en el workspace, un overlay en `install/` y un `source` antes de cada ejecución.
Pixi puede construir el paquete él mismo y ponerlo en el entorno al lado de `turtlesim`, así que nada de eso hace falta: ni colcon, ni overlay, ni `source`, ni siquiera las herramientas de build en tu entorno.

**Esto sustituye a montarse una buildfarm**: un `pixi.toml` de dos líneas junto al `package.xml` basta para que tu paquete sea un paquete conda que puedes publicar en un canal (local o de prefix.dev) y que cualquiera instala con `pixi add`.

Empieza aquí:

```bash
cd ejercicios/02-paquetes-ros
```

Es donde terminó el Ejercicio 1, recortado a Lyrical: `pixi.toml` compila `src/turtle_dancer/` con colcon y carga el overlay al activar.
El paquete Python `src/turtle_choreographer/` se queda sin compilar hasta el paso 2.6.

Ejecuta primero la manera colcon, para tener el "antes" delante:

```bash
pixi run build      # colcon compila el workspace
ls                  # han aparecido build/ install/ log/ junto a src/
```

---

## 2.1 Activa pixi-build

Construir paquetes desde el código es una funcionalidad en [preview](https://pixi.prefix.dev/latest/reference/pixi_manifest/#preview-features), así que el workspace tiene que activarla.
También necesita un [backend de build](https://pixi.prefix.dev/latest/build/backends/), la pieza que entiende el sistema de build.
Para ROS es [`pixi-build-ros`](https://pixi.prefix.dev/latest/build/backends/pixi-build-ros/), y como todos los paquetes del workspace usan el mismo, se declara una vez, en [`[workspace.dependencies]`](https://pixi.prefix.dev/latest/build/workspace_dependencies/).

1. Activa la preview `pixi-build` en la tabla `[workspace]`.
2. Añade `pixi-build-ros = ">=0.7.5"` a `[workspace.dependencies]`.

<details>
<summary>Solución</summary>

```bash
pixi workspace preview add pixi-build
pixi workspace dependencies add "pixi-build-ros >=0.7.5"
```

```toml
[workspace]
# ...
preview = ["pixi-build"]

[workspace.dependencies]
pixi-build-ros = ">=0.7.5"
```

`[workspace.dependencies]` es un *pool* de versiones compartidas, no una lista de instalación: nada entra en el entorno por estar ahí.
Los paquetes cogen entradas del pool (siguiente paso), y actualizar el backend más adelante es cambiar una línea.

</details>

## 2.2 Dale un manifiesto al paquete

Hasta ahora todos tus `pixi.toml` tenían una tabla `[workspace]`.
Hay una segunda tabla principal, que describe **un paquete**:

| Rol | Marcado por | Describe | En este ejercicio |
| --- | --- | --- | --- |
| **Workspace** | `[workspace]` | tu entorno: canales, plataformas, dependencias, tasks | `pixi.toml` |
| **Paquete** | `[package]` | cómo se construye un paquete | `src/turtle_dancer/pixi.toml` |

Un workspace es lo que ejecutas con `pixi run`.
Un paquete es lo que Pixi convierte en un paquete conda, a través del backend.
`pixi-build-ros` lee el `package.xml` (nombre, versión, dependencias y tipo de build), traduce las dependencias a sus nombres de RoboStack, y ejecuta el build `ament_cmake` o `ament_python` que ya tienes.
Así que el manifiesto del paquete tiene muy poco que decir.

1. Crea `src/turtle_dancer/pixi.toml` indicando `pixi-build-ros` como backend, con la versión del pool del workspace.
   Pista: `workspace = true`.
2. Abre `package.xml` y `CMakeLists.txt`.
   ¿Qué líneas necesita el backend, y cuál hace que `ros2 run` encuentre el ejecutable?
   No cambies nada.

<details>
<summary>Solución</summary>

```toml
# src/turtle_dancer/pixi.toml
[package.build.backend]
name = "pixi-build-ros"
workspace = true
```

Dos líneas: qué backend, y "la versión está en el pool del workspace".
La distro de ROS sale del canal `robostack-lyrical` del workspace, y todo lo demás del `package.xml`.

Del `package.xml` el backend toma `<name>`, `<version>`, `<depend>` y `<build_type>`.
Del `CMakeLists.txt` la línea importante es `install(TARGETS dance DESTINATION lib/${PROJECT_NAME})`: `ros2 run` busca en `lib/<paquete>/`, y ahí instala el backend lo que instale tu CMake.
Ambos ficheros son los que usaba colcon hace un minuto, sin cambios.

</details>

## 2.3 Depende de tu propio paquete

Un workspace depende de un paquete local como de cualquier otro, solo que la especificación es un `path` al directorio del paquete.
El nombre de la dependencia es el del `package.xml` con el prefijo de la distro y guiones: `ros-lyrical-turtle-dancer`, el nombre que le daría RoboStack si lo publicara.

1. Añade `ros-lyrical-turtle-dancer` como dependencia de tipo `path` sobre `src/turtle_dancer`.
2. Instala, y mira lo que pasa.
3. Busca tu paquete en `pixi list`.

<details>
<summary>Solución</summary>

```bash
# 1
pixi add --path src/turtle_dancer ros-lyrical-turtle-dancer
# 2
pixi install
# 3
pixi list turtle
```

```toml
[dependencies]
ros-lyrical-turtle-dancer = { path = "src/turtle_dancer" }
ros-lyrical-ros-base = ">=0.13"
ros-lyrical-turtlesim = ">=1.10"
ros-dev-tools = ">=1.0"
```

La primera instalación descarga el backend y un entorno de build (CMake, compiladores, las librerías de ROS del `package.xml`) en `.pixi/`, compila el nodo e instala el resultado en el entorno **como un paquete conda**.
Las siguientes son incrementales.

```console
$ pixi list turtle
ros-lyrical-turtle-dancer                                       conda  src/turtle_dancer
ros-lyrical-turtlesim   1.10.9   ...                            conda  https://prefix.dev/robostack-lyrical
```

Donde los demás paquetes muestran un canal, el tuyo muestra la ruta desde la que se construyó.

</details>

## 2.4 Borra la maquinaria de colcon

Ahora mismo el nodo está dos veces en el entorno: una en el `install/` de colcon y otra construido por Pixi.
Todo lo que necesitaba colcon puede irse.

1. Quita el `depends-on` de `dance` y las dos tablas de `activation`; después quita la task `build` y la dependencia `ros-dev-tools`.
2. Borra `build/`, `install/` y `log/`.
3. Ejecuta el nodo, con el simulador en otra terminal.

<details>
<summary>Solución</summary>

```bash
# 1: en el editor, quita `depends-on` de dance y las tablas [target.*.activation]
pixi task remove build
pixi remove ros-dev-tools
# 2
rm -rf build install log
# 3: en dos terminales
pixi run sim
pixi run dance
```

```toml
[workspace]
name = "02-paquetes-ros"
channels = ["https://prefix.dev/robostack-lyrical", "conda-forge"]
platforms = ["linux-64", { platform = "osx-arm64", macos = "14.0" }, "win-64"]
version = "0.1.0"
preview = ["pixi-build"]

[workspace.dependencies]
pixi-build-ros = ">=0.7.5"

[dependencies]
ros-lyrical-turtle-dancer = { path = "src/turtle_dancer" }
ros-lyrical-ros-base = ">=0.13"
ros-lyrical-turtlesim = ">=1.10"

[tasks]
sim = "ros2 run turtlesim turtlesim_node"
teleop = "ros2 run turtlesim turtle_teleop_key"
topics = "ros2 topic list"
dance = "ros2 run turtle_dancer dance"
```

`pixi run ros2 run turtle_dancer dance` también funciona, desde una terminal nueva, sin `source` de nada.
El nodo es ahora un paquete más del entorno, igual que `turtlesim`.

</details>

## 2.5 Vive en el bucle editar-ejecutar

En el Ejercicio 1, cambiar el nodo era editar, `pixi run build`, ejecutar, con el `source` escondido en un script de activación.
Mira qué es ahora.

1. Abre `src/turtle_dancer/src/dance.cpp` y cambia la velocidad angular por defecto de `0.8` a `3.0`.
2. Ejecuta otra vez el nodo, con el simulador abierto.

<details>
<summary>Solución</summary>

```cpp
angular_speed_ = declare_parameter("angular_speed", 3.0);
```

```bash
pixi run dance      # sale la salida del build y la tortuga gira en círculos cerrados
```

`pixi run` comprueba las entradas de cada dependencia de código fuente antes de ejecutar nada: `package.xml`, `CMakeLists.txt`, los fuentes.
Una ha cambiado, así que el paquete se reconstruye y reinstala primero.

> **Qué cuenta como entrada:** el backend vigila fuentes C/C++, `package.xml`, `CMakeLists.txt`, `setup.py`, launch files, mensajes y alguno más.
> Para cualquier otra cosa, `extra-input-globs` en `[package.build.config]` del manifiesto del paquete.

</details>

## 2.6 Añade el paquete Python

`src/turtle_choreographer/` es un segundo nodo, esta vez en Python: un paquete `ament_python` ya escrito.
Recibe el mismo tratamiento: un manifiesto de paquete, una dependencia `path` y una task.

1. Crea `src/turtle_choreographer/pixi.toml`: las mismas dos líneas que el de C++.
2. Añade `ros-lyrical-turtle-choreographer` como dependencia `path`.
3. Añade una task `choreograph` que ejecute `ros2 run turtle_choreographer choreograph`.
4. Ejecútala, con el simulador abierto.

<details>
<summary>Solución</summary>

```toml
# src/turtle_choreographer/pixi.toml
[package.build.backend]
name = "pixi-build-ros"
workspace = true
```

```bash
pixi add --path src/turtle_choreographer ros-lyrical-turtle-choreographer
pixi task add choreograph "ros2 run turtle_choreographer choreograph"
pixi run choreograph     # la tortuga dibuja un ocho
```

Un workspace, dos lenguajes, un lockfile.

> **`setup.cfg` es lo que hace que `ros2 run` encuentre un nodo Python**: `install_scripts=$base/lib/turtle_choreographer` pone el ejecutable en `lib/<paquete>/`, donde mira `ros2 run`, en vez de en `bin/`.
> `ros2 pkg create --build-type ament_python` te genera este fichero.

</details>

## 2.7 Publica los paquetes

Hasta ahora los paquetes son dependencias de código fuente: cualquier workspace que los quiera necesita el árbol de fuentes.
Publicar convierte el resultado del build en paquetes `.conda` normales, en un **canal**.
Empezamos con un canal local (una carpeta) para ver exactamente qué se subiría.

Pixi solo publica los paquetes que lo piden explícitamente, para no publicar por accidente todo lo que encuentra en un workspace.

1. Añade `publish = true` a la tabla `[package]` de los dos manifiestos de paquete.
2. Publica los paquetes del workspace en un canal local, `output`.
3. Mira los paquetes que ha escrito Pixi.

<details>
<summary>Solución</summary>

```toml
# src/turtle_dancer/pixi.toml (y lo mismo en src/turtle_choreographer/pixi.toml)
[package]
publish = true

[package.build.backend]
name = "pixi-build-ros"
workspace = true
```

```bash
# 2
pixi publish --target-channel output
# 3
find output -name "*.conda"
```

```text
output/<plataforma>/ros-lyrical-turtle-choreographer-0.1.0-<build>.conda
output/<plataforma>/ros-lyrical-turtle-dancer-0.1.0-<build>.conda
```

`output/` es un canal conda de verdad, con su `repodata.json`.

</details>

### Publicar en prefix.dev

El mismo comando publica en un canal de [prefix.dev](https://prefix.dev). Necesitas una cuenta (gratuita) y crear un canal en la web:

```bash
pixi auth login prefix.dev          # o con una API key: --token pfx_...
pixi publish --target-channel https://prefix.dev/<tu-canal>
```

Eso es todo lo que antes requería una receta `rattler-build`, `rattler-index` y `rattler-build upload`.
Para varias plataformas, publica desde cada una (o desde la CI, con una matriz) con `--target-platform`.

## 2.8 Instala tus paquetes desde otro workspace

Un paquete publicado se consume como cualquier paquete de RoboStack: pones su canal en la lista y lo añades por nombre.

1. Crea un workspace nuevo `consumidor/` dentro de este directorio, con los canales `../output`, `https://prefix.dev/robostack-lyrical` y `conda-forge`, **en ese orden**.
2. Añade `ros-lyrical-turtle-dancer` y `ros-lyrical-turtlesim`, sin `path`.
3. Comprueba de dónde viene cada paquete y ejecuta el nodo.

<details>
<summary>Solución</summary>

```bash
pixi init consumidor -c ../output -c https://prefix.dev/robostack-lyrical -c conda-forge
cd consumidor
pixi add ros-lyrical-turtle-dancer ros-lyrical-turtlesim
pixi list turtle
pixi run ros2 run turtle_dancer dance
```

```console
$ pixi list turtle
ros-lyrical-turtle-dancer   0.1.0   hb0f4dca_0   61.54 KiB  conda  file:///.../02-paquetes-ros/output
ros-lyrical-turtlesim       1.10.9  hb0f4dca_28   1.98 KiB  conda  https://prefix.dev/robostack-lyrical
```

Aquí no hay código fuente ni compilador: se instala el binario ya construido, al lado de ROS 2 oficial de RoboStack.
Con prefix.dev sería exactamente igual, cambiando `../output` por `https://prefix.dev/<tu-canal>`.

`pixi init` solo declara tu plataforma, que es justo para la que has publicado.
Si añades otra plataforma sin publicar para ella, el solver dirá `No candidates were found for ros-lyrical-turtle-dancer`.

El orden de los canales importa: tu canal, después RoboStack, después conda-forge.

Si no aparece un paquete recién publicado en prefix.dev: `pixi clean cache --repodata -y`.

</details>

La solución completa está en [`soluciones/02-paquetes-ros/`](../../soluciones/02-paquetes-ros/) (el consumidor en `soluciones/02-paquetes-ros/consumidor/`).

---

## Comprueba tu trabajo

```bash
pixi run dance          # nodo C++, sin source
pixi run choreograph    # nodo Python
pixi run executables    # ros2 ve los dos nodos, igual que tras un colcon build
ls                      # src/, pixi.toml, consumidor/ y output/; nada de build/ install/ log/
```

`executables` es una task más que puedes añadir: `ros2 pkg executables turtle_dancer && ros2 pkg executables turtle_choreographer`.

## Si te sobra tiempo

- Compara con lo que tenías al principio: `git diff --stat ejercicios/02-paquetes-ros/pixi.toml`.
- Adelgaza el workspace: cambia `ros-lyrical-ros-base` por `ros-lyrical-ros2run`.
  Todo lo que necesitan los nodos llega ahora por su `package.xml`, así que `pixi list` se acorta mucho.
- Añade un tercer paquete con un `.msg` propio y úsalo desde los dos nodos. La generación de interfaces funciona con este backend.
- Construye para dos distros, como en el paso 1.5: deja solo `conda-forge` en el workspace y crea `[environments.default]` (canal `robostack-lyrical`, `ros-lyrical-turtle-dancer = { path = "src/turtle_dancer" }`, `ros-lyrical-ros-base`) y `[environments.jazzy]` (canal `robostack-jazzy`, `ros-jazzy-turtle-dancer = { path = "src/turtle_dancer" }`, `ros-jazzy-ros-base`).
  El mismo `package.xml` se construye para las dos distros: `pixi run -e jazzy dance`.
- ¿Tienes una receta `recipe.yaml` de `rattler-build` que quieras conservar? Usa el backend `pixi-build-rattler-build` con `[package.build.config] recipe = "recipe.yaml"` y publícala igual con `pixi publish`.

> **Con tu propio workspace:** elige un paquete hoja (que no dependa de tus otros paquetes).
> Pon el `pixi.toml` de dos líneas del paso 2.2 junto a su `package.xml`, añade la dependencia `path` y `pixi install`.
> Lo normal es que falle la primera vez: casi siempre es una dependencia del `package.xml` que no está en RoboStack con ese nombre (se arregla con `extra-package-mappings` en la configuración del backend) o que no está empaquetada.
> Estos son los diez minutos del taller que más queremos pasar contigo: levanta la mano.

---

Siguiente: [Ejercicio 3: listo para tu equipo](../03-colaboracion/).
