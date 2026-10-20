# Ejercicio 3: listo para tu equipo

> **25 minutos, práctica** · **Trabaja en:** `ejercicios/03-colaboracion/` · **Solución:** [`soluciones/03-colaboracion/`](../../soluciones/03-colaboracion/)
>
> **Objetivo:** llevar el workspace a tu equipo: una CI en verde, una imagen Docker y un archivo que se desempaqueta y se ejecuta sin Pixi.

Probar el workspace en CI o desplegar la aplicación con Docker es el siguiente paso natural.
Vas a configurar GitHub Actions, construir una imagen Docker y luego empaquetar el entorno para una máquina sin Docker.

Empieza aquí:

```bash
cd ejercicios/03-colaboracion
```

Es un workspace nuevo con paquetes ROS 2 ya construidos de RoboStack, no los paquetes locales del Ejercicio 2.
Las tasks `talker` y `listener` ejecutan los nodos de `demo_nodes_cpp`.
En este ejercicio no compilas nada.

---

## 3.1 Prepara GitHub

La CI se ejecuta en GitHub, así que tu workspace tiene que ser un repositorio allí.
La [CLI de GitHub](https://cli.github.com) lo hace desde la terminal, y se instala como cualquier otra herramienta.

1. Instala la CLI de GitHub, si no la tienes.
   Pista: Pixi también instala herramientas fuera de tu workspace, con `pixi global install <herramienta>`.
2. Inicia sesión con tu cuenta de GitHub.
3. Resuelve este workspace para generar su `pixi.lock`.
4. Crea un repositorio Git en la rama `main`, haz commit del workspace **incluyendo `pixi.lock`**, y súbelo a GitHub.

<details>
<summary>Solución</summary>

```bash
# 1
pixi global install gh
# 2
gh auth login
# 3
pixi lock
# 4: desde una copia de esta carpeta fuera del repo del taller
git init -b main
git add .
git commit -m "Workspace ROS 2 con Pixi"
gh repo create ros-demo-team --source=. --push --public
```

Para no anidar un repositorio dentro del del taller, copia antes la carpeta fuera: `cp -r ejercicios/03-colaboracion ~/ros-demo-team && cd ~/ros-demo-team`.

</details>

## 3.2 Añade CI

El workflow de abajo hace checkout de tu repositorio y se para ahí.
Lo tuyo es la parte de Pixi, con la acción [`prefix-dev/setup-pixi`](https://pixi.prefix.dev/latest/integration/ci/github_actions/).
La task `test` del workspace ejecuta `ros2 pkg executables demo_nodes_cpp`: comprueba que ROS encuentra el paquete instalado y lista sus ejecutables.

1. Crea `.github/workflows/ci.yml` en tu repositorio, a partir de este esqueleto:

   ```yaml
   name: CI

   on:
     push:
       branches: [main]
     pull_request:

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v7
         # Te toca: instalar Pixi y ejecutar los tests.
   ```

2. Añade la instalación de Pixi con `locked: true`: instalar desde el lockfile del commit, y fallar si falta o no está al día.
3. Ejecuta tu task `test` en la CI.
4. Commit, push, y mira cómo se pone en verde la pestaña Actions.

<details>
<summary>Solución</summary>

Ver [`soluciones/03-colaboracion/ci-template.yml`](../../soluciones/03-colaboracion/ci-template.yml):

```yaml
      - uses: actions/checkout@v7
      - uses: prefix-dev/setup-pixi@v0.10.2
        with:
          locked: true
      - run: pixi run test
```

`locked: true` hace que setup-pixi ejecute `pixi install --locked`, que falla si `pixi.lock` falta o ya no coincide con el manifiesto.
Las mismas tasks que usas en local son el script de la CI: no hay un segundo conjunto de instrucciones de instalación en YAML que pueda desincronizarse.
La caché de setup-pixi usa como clave el hash de `pixi.lock`.

```bash
git add .github/workflows/ci.yml
git commit -m "Añade CI"
git push
```

</details>

## 3.3 Despliega una imagen Docker

Una imagen de despliegue no debería contener un gestor de paquetes, y no debería poder desviarse de lo que probó el equipo.
El [patrón de la documentación de Pixi](https://pixi.prefix.dev/latest/deployment/container/) consigue las dos cosas con un build multi-etapa: la etapa de build tiene Pixi e instala desde el lockfile; la etapa final solo recibe el entorno terminado más un script de activación generado por `pixi shell-hook`.

Completa las tres líneas `FIXME` de `Dockerfile`:

1. Sustituye el primer `RUN pixi FIXME` por una instalación *locked* del entorno por defecto.
   Debe fallar, en vez de volver a resolver, si `pixi.lock` falta o no está al día.
2. Sustituye el segundo `RUN pixi FIXME` por un shell-hook de activación para Bash escrito en `/shell-hook.sh`.
   Añade `exec "$@"` al final del script para que ejecute el comando del contenedor tras activar.
3. Completa `COPY --from=build FIXME` para copiar `/app/.pixi/envs/default` desde la etapa de build a la misma ruta absoluta.
4. Lee tu fichero terminado: ¿dónde se impone el lockfile, y dónde se ejecuta Pixi por última vez?
5. Construye la imagen.
6. Ejecútala, párala con Ctrl+C y mira cuánto pesa.

<details>
<summary>Solución</summary>

Compara tus tres líneas con [`soluciones/03-colaboracion/Dockerfile`](../../soluciones/03-colaboracion/Dockerfile):

```dockerfile
RUN pixi install --locked

RUN pixi shell-hook -s bash > /shell-hook.sh \
    && echo 'exec "$@"' >> /shell-hook.sh

COPY --from=build /app/.pixi/envs/default /app/.pixi/envs/default
```

El lockfile se impone con `pixi install --locked`, la misma negativa que usa la CI.
Pixi aparece por última vez en la línea `pixi shell-hook`: escribe la activación como un script de shell normal, y la etapa final solo copia ese script y el entorno instalado.

```bash
# 5
docker build -t ros-demo-team:latest .
# 6
docker run --rm ros-demo-team:latest     # Publishing: 'Hello World: N'
docker images ros-demo-team
```

Para GPU, la imagen base tiene variantes CUDA (`ghcr.io/prefix-dev/pixi:noble-cuda-13.0.0`), y los rebuilds van mucho más rápido conservando la caché de paquetes: `RUN --mount=type=cache,target=/root/.cache/rattler pixi install --locked`.

</details>

## 3.4 Empaqueta el entorno

Desplegar en robots es a veces otro problema: 4G poco fiable, sin acceso a internet, sin Docker.
[`pixi-pack`](https://pixi.prefix.dev/latest/deployment/pixi_pack/) mete un entorno en `environment.tar`, y `pixi-unpack` lo instala sin solver ni conexión.
En este ejercicio empaquetas para tu propia máquina y usas un directorio aparte como "máquina destino".

1. Instala `pixi-pack` y `pixi-unpack` como herramientas globales.
2. Comprueba que el lockfile del workspace está al día.
3. Empaqueta el entorno **default** para tu plataforma actual.
4. Añade `environment.tar` y `unpacked/` al `.gitignore` de tu repositorio.

<details>
<summary>Solución</summary>

Desde `ejercicios/03-colaboracion/`, fuera de un `pixi shell`:

```bash
pixi global install pixi-pack pixi-unpack
pixi lock --check
pixi-pack --environment default pixi.toml
```

`pixi-pack` descarga los paquetes binarios del lockfile, incluido `demo_nodes_cpp`, y los mete en el archivo.

> **Empaqueta para la máquina donde vas a ejecutar.** El destino debe coincidir en SO y arquitectura.
> Como aquí todo son paquetes ya construidos, puedes empaquetar para otra plataforma declarada (`--platform linux-aarch64`, por ejemplo para una Raspberry Pi o una Jetson) solo descargando sus paquetes, incluso desde un Mac.

</details>

## 3.5 Desempaqueta y ejecuta sin Pixi

El destino necesita el archivo y el binario `pixi-unpack`; no tu código, ni el manifiesto, ni el lockfile.

1. Crea un directorio vacío `unpacked/` y copia solo `environment.tar` dentro.
2. Entra en él, desempaqueta y activa el entorno.
3. Comprueba que `ros2` encuentra los ejecutables de `demo_nodes_cpp`.
4. Ejecuta el talker directamente con `ros2 run`, sin `pixi run`. Páralo con Ctrl+C.

<details>
<summary>Solución</summary>

En una terminal nueva, fuera de `pixi shell`:

```bash
mkdir unpacked
cp environment.tar unpacked/
cd unpacked
pixi-unpack environment.tar
source activate.sh
ros2 pkg executables demo_nodes_cpp
ros2 run demo_nodes_cpp talker
```

En Windows, desde **Command Prompt** (`cmd.exe`): `pixi-unpack --shell cmd environment.tar` y `call activate.bat`.

`pixi-unpack` crea `env/` y un script de activación para tu shell.
Ningún proceso de Pixi interviene en los comandos `ros2`.
Cierra esta terminal al terminar para que el entorno desempaquetado no se cuele en otros comandos.

</details>

---

## Si te sobra tiempo

- Añade una barrera barata: un primer job que ejecute `pixi lock --check` y falle cuando alguien edite `pixi.toml` sin volver a resolver el lockfile. Rómpelo a propósito para verlo funcionar.
- Amplía el workflow a una matriz de Linux, macOS y Windows, como [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) de este repositorio.
- Mira qué se instalaría en una Jetson con la solución: `pixi run --manifest-path ../../soluciones/03-colaboracion/pixi.toml robot-list`.
- Deja que la CI actualice el lockfile por ti: [actualizar lockfiles con GitHub Actions](https://pixi.prefix.dev/latest/integration/ci/updates_github_actions/).
- Prueba `pixi-pack --environment default --create-executable pixi.toml`: un único fichero autoextraíble que lleva el desempaquetador dentro.
- Publica en la CI: añade un job que haga `pixi publish --target-channel https://prefix.dev/<tu-canal>` con los paquetes del Ejercicio 2 en cada tag. Ya tienes tu buildfarm.

---

Eso es todo el taller. Si quieres seguir con un workspace grande de verdad, ve al [Ejercicio 4 (opcional): Nav2 con `pixi-ros`](../04-nav2-pixi-ros/).
