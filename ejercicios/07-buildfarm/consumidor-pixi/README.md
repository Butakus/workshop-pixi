# Fase C — Instalar desde un pixi.toml propio

Corresponde a la Fase C del ejercicio del bloque 7 "Tu propia Buildfarm basada en RoboStack" (ver slides).

Sustituye `workshop-pichi-<nombre>` en `solucion/pixi.toml` por el nombre real de tu canal en prefix.dev (creado en la Fase B) antes de probarlo:

```bash
cd solucion
pixi install
pixi run hola-pichi
```

Si no aparece el paquete recién subido (`No candidates found`):

```bash
pixi clean cache --repodata -y
```
