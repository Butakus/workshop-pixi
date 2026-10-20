# Ejercicios

Trabaja en estos directorios.
Cada uno tiene su propio workspace de partida, así que puedes empezar en cualquiera.
Las instrucciones paso a paso están en el `README.md` de cada carpeta, con las soluciones plegadas: inténtalo primero, ábrelas si te atascas.

| Directorio | Empiezas con | Terminas con |
| --- | --- | --- |
| [`01-workspace-ros/`](01-workspace-ros/) | Un workspace vacío con nodos C++ y PyTorch ya escritos | ROS 2 funcionando, tu nodo compilado con colcon, dos distros (Lyrical y Jazzy) a la vez, y un nodo PyTorch resuelto para una GPU y una Jetson |
| [`02-paquetes-ros/`](02-paquetes-ros/) | Ese workspace, recortado a Lyrical, con colcon compilando | Pixi construyendo el paquete C++ y uno Python desde su `package.xml`, publicados como paquetes conda e instalados desde otro workspace |
| [`03-colaboracion/`](03-colaboracion/) | Un workspace multiplataforma con los nodos `talker`/`listener` ya construidos | CI en verde, una imagen Docker y un entorno empaquetado que se ejecuta sin Pixi |
| [`04-workspace-real/`](04-workspace-real/) | Nada: clonas dos repositorios de terceros | Un workspace real compilado con colcon dentro de Pixi, sin `rosdep`, y un Kobuki en una casa en Gazebo movido con el teclado |

Las versiones terminadas están en [`../soluciones/`](../soluciones/).
Mirar está permitido, pero escribe tú los comandos: ahí está el aprendizaje.

Si tienes tu propio workspace ROS, cada ejercicio termina con una nota "Con tu propio workspace" que explica el paso equivalente. Hacerlo sobre tu código es lo más útil, y preferimos ayudarte con eso.

Referencia: [chuleta de comandos](../referencia/chuleta.md) · [solución de problemas](../referencia/problemas.md).
