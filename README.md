# bda-dashboard

> Se necesita <https://docs.docker.com/get-docker/>.

Antes de correrlo hay que ejecutar:

```sh
git submodule init && git submodule update --remote
```

Para lanzar un contenedor con la base de datos y otro con la página web:

```sh
docker compose up --build
```

Para lanzar los contendores y lanzarlos otra vez cada que se modifica algún archivo:
```sh
docker compose watch
```
