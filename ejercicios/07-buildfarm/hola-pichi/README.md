# Fase A — Construir el paquete con rattler-build

Corresponde a la Fase A del ejercicio del bloque 7 "Tu propia Buildfarm basada en RoboStack" (ver slides).

## Cómo usar esta carpeta

`solucion/` contiene el estado final esperado: `pixi.toml` con `rattler-build`/`rattler-index` como dependencias, la receta `recipe/recipe.yaml`, y el paquete Python mínimo en `src/`.

```bash
cd solucion
pixi run rattler-build build --recipe ./recipe/recipe.yaml -c conda-forge
ls output/noarch/*.conda
pixi run rattler-index fs ./output --force
```

Checkpoint: debe existir `output/noarch/hola-pichi-1.0.0-*.conda`.

## Siguiente paso

Publicar en un canal de prueba de prefix.dev (Fase B) — ver `../consumidor-pixi/` y `../consumidor-ros2/` para las fases C y D (instalar y consumir el paquete ya publicado).
