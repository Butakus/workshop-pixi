# Chuleta de comandos

Cada comando enlaza a su página en la [documentación de Pixi](https://pixi.prefix.dev/latest/).

## Workspace

| Comando | Qué hace |
| --- | --- |
| [`pixi init`](https://pixi.prefix.dev/latest/reference/cli/pixi/init/) | Crea un `pixi.toml` en el directorio actual |
| [`pixi workspace channel add <canal>`](https://pixi.prefix.dev/latest/reference/cli/pixi/workspace/channel/add/) | Añade un canal (`--prepend` para darle prioridad) |
| [`pixi workspace platform add <plataforma>`](https://pixi.prefix.dev/latest/reference/cli/pixi/workspace/platform/add/) | Añade una plataforma (`nombre=linux-64 --cuda 12` para una con GPU) |
| [`pixi workspace activation scripts add <script>`](https://pixi.prefix.dev/latest/reference/cli/pixi/workspace/activation/) | Carga un script al activar el entorno |
| [`pixi add <paquete>`](https://pixi.prefix.dev/latest/reference/cli/pixi/add/) | Añade una dependencia y actualiza el lockfile |
| [`pixi add --pypi <paquete>`](https://pixi.prefix.dev/latest/concepts/conda_pypi/) | Añade una dependencia de PyPI |
| [`pixi add --path <dir> <nombre>`](https://pixi.prefix.dev/latest/build/getting_started/) | Añade un paquete local que construye Pixi |
| [`pixi remove <paquete>`](https://pixi.prefix.dev/latest/reference/cli/pixi/remove/) | Quita una dependencia |
| [`pixi task add <nombre> "<cmd>"`](https://pixi.prefix.dev/latest/reference/cli/pixi/task/add/) | Añade una task (`--depends-on otra`) |

## Ejecutar

| Comando | Qué hace |
| --- | --- |
| [`pixi run <task>`](https://pixi.prefix.dev/latest/reference/cli/pixi/run/) | Ejecuta una task de `[tasks]` |
| [`pixi run <comando>`](https://pixi.prefix.dev/latest/reference/cli/pixi/run/) | Ejecuta cualquier comando dentro del entorno |
| [`pixi run -e <entorno> <task>`](https://pixi.prefix.dev/latest/workspace/multi_environment/) | Ejecuta en un entorno concreto |
| [`pixi shell`](https://pixi.prefix.dev/latest/reference/cli/pixi/shell/) | Abre un shell con el entorno activado (`exit` para salir) |
| [`pixi task list`](https://pixi.prefix.dev/latest/reference/cli/pixi/task/list/) | Lista las tasks disponibles |

## Entornos y lockfile

| Comando | Qué hace |
| --- | --- |
| [`pixi install`](https://pixi.prefix.dev/latest/reference/cli/pixi/install/) | Instala el entorno desde el lockfile (`--locked` falla si no está al día) |
| [`pixi lock`](https://pixi.prefix.dev/latest/reference/cli/pixi/lock/) | Actualiza el lockfile sin instalar |
| [`pixi lock --check`](https://pixi.prefix.dev/latest/reference/cli/pixi/lock/) | Falla si el lockfile no está al día. Para la CI |
| [`pixi update <paquete>`](https://pixi.prefix.dev/latest/reference/cli/pixi/update/) | Actualiza un paquete a la versión más nueva permitida |
| [`pixi list`](https://pixi.prefix.dev/latest/reference/cli/pixi/list/) | Muestra lo instalado |
| [`pixi tree <paquete>`](https://pixi.prefix.dev/latest/reference/cli/pixi/tree/) | Muestra por qué está un paquete en el entorno |
| [`pixi clean`](https://pixi.prefix.dev/latest/reference/cli/pixi/clean/) | Borra `.pixi/` |

## Inspeccionar

| Comando | Qué hace |
| --- | --- |
| [`pixi info`](https://pixi.prefix.dev/latest/reference/cli/pixi/info/) | Versiones, cachés y los paquetes virtuales de tu máquina (`__cuda`, `__glibc`...) |
| [`pixi search <paquete>`](https://pixi.prefix.dev/latest/reference/cli/pixi/search/) | Busca en los canales configurados |
| [`pixi list --platform <plataforma>`](https://pixi.prefix.dev/latest/workspace/multi_platform_configuration/) | Qué se instalaría en otra plataforma |

## Construir y publicar

| Comando | Qué hace |
| --- | --- |
| [`pixi workspace preview add pixi-build`](https://pixi.prefix.dev/latest/reference/pixi_manifest/#preview-features) | Activa la construcción de paquetes |
| [`pixi build`](https://pixi.prefix.dev/latest/build/getting_started/) | Construye el `[package]` de este directorio en un `.conda` |
| [`pixi publish --target-channel <canal>`](https://pixi.prefix.dev/latest/reference/cli/pixi/publish/) | Construye y sube los paquetes con `publish = true` (carpeta local o `https://prefix.dev/<canal>`) |
| [`pixi auth login prefix.dev`](https://pixi.prefix.dev/latest/reference/cli/pixi/auth/login/) | Inicia sesión para publicar (`--token pfx_...`) |

El backend que convierte un `package.xml` en un paquete conda es [`pixi-build-ros`](https://pixi.prefix.dev/latest/build/backends/pixi-build-ros/).

## Herramientas globales

| Comando | Qué hace |
| --- | --- |
| [`pixi global install <herramienta>`](https://pixi.prefix.dev/latest/global_tools/introduction/) | Instala una CLI aislada, fuera de cualquier workspace (`gh`, `pixi-ros`, `pixi-pack`...) |
| `pixi-ros init --distro <distro>` | Genera un `pixi.toml` a partir de los `package.xml` de un workspace existente |
| `pixi-pack` / `pixi-unpack` | Empaqueta un entorno en un `.tar` y lo instala sin Pixi ni red |

## Canales de RoboStack

| Distribución | Repositorio | Canal |
| --- | --- | --- |
| Rolling | [ros-rolling](https://github.com/robostack/ros-rolling) | [robostack-rolling](https://prefix.dev/channels/robostack-rolling) |
| Lyrical | [ros-lyrical](https://github.com/robostack/ros-lyrical) | [robostack-lyrical](https://prefix.dev/channels/robostack-lyrical) |
| Kilted | [ros-kilted](https://github.com/robostack/ros-kilted) | [robostack-kilted](https://prefix.dev/channels/robostack-kilted) |
| Jazzy (LTS) | [ros-jazzy](https://github.com/robostack/ros-jazzy) | [robostack-jazzy](https://prefix.dev/channels/robostack-jazzy) |
| Humble (LTS) | [ros-humble](https://github.com/robostack/ros-humble) | [robostack-humble](https://prefix.dev/channels/robostack-humble) |
| Noetic (ROS 1) | [ros-noetic](https://github.com/robostack/ros-noetic) | [robostack-noetic](https://prefix.dev/channels/robostack-noetic) |

## Para leer más

| Tema | Página |
| --- | --- |
| Todos los campos de `pixi.toml` | [Referencia del manifiesto](https://pixi.prefix.dev/latest/reference/pixi_manifest/) |
| Features, entornos y solve groups | [Multi entorno](https://pixi.prefix.dev/latest/workspace/multi_environment/) |
| Dependencias, inputs y outputs de tasks | [Tasks avanzadas](https://pixi.prefix.dev/latest/workspace/advanced_tasks/) |
| Construir tus paquetes ROS | [Build a ROS package](https://pixi.prefix.dev/latest/build/ros/) |
| Pixi para robótica de principio a fin | [Robotics](https://pixi.prefix.dev/latest/robotics/) y el [tutorial de ROS 2](https://pixi.prefix.dev/latest/tutorials/ros2/) |
| El taller original de prefix.dev (ROSCon 2026, en inglés) | [Declarative ROS workspaces with Pixi](https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/) |
