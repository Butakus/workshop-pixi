# Una imagen de ejecución construida a partir del mismo lockfile con el que
# desarrolla el equipo.
#
#     docker build -t ros-demo-team:latest .
#     docker run --rm ros-demo-team:latest
#
# La etapa de build tiene Pixi; la final no. Solo lleva el entorno resuelto,
# así que nada de la imagen puede desviarse de pixi.lock.

FROM ghcr.io/prefix-dev/pixi:0.80.0-noble AS build

WORKDIR /app
COPY pixi.toml pixi.lock ./

RUN pixi install --locked

# Guardamos la activación en un script, para que la etapa final no necesite Pixi.
RUN pixi shell-hook -s bash > /shell-hook.sh \
    && echo 'exec "$@"' >> /shell-hook.sh

FROM ubuntu:26.04 AS runtime

COPY --from=build /app/.pixi/envs/default /app/.pixi/envs/default
COPY --from=build /shell-hook.sh /shell-hook.sh

WORKDIR /app
ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]
CMD ["ros2", "run", "demo_nodes_cpp", "talker"]
