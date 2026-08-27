# Entorno ROS 2 + paquete propio con colcon

Corresponde a los ejercicios del bloque "Uso básico de RoboStack para compilar un workspace ROS 2" (ver slides).

## Cómo usar esta carpeta

- Sigue los pasos de las slides construyendo tú mismo el `pixi.toml` y el paquete `mi_paquete` con `ros2 pkg create`.
- Si te atascas o quieres comparar, `solucion/` tiene el estado final esperado: `pixi.toml` con dependencias + `[activation]` + `[tasks]`, y el paquete `src/mi_paquete/` completo (el que generaría `ros2 pkg create --build-type ament_python --node-name talker_custom mi_paquete`, con el nodo publicador ya relleno).

## Para probar la solución directamente

```bash
cd solucion
pixi install
pixi run run_talker
```

## Nota

No se incluye `pixi.lock` en esta plantilla — en un proyecto real lo commitearíais también (es el punto central de todo el taller: reproducibilidad), pero aquí se genera de nuevo en cada máquina al ejecutar `pixi install`.
