# bda-dashboard

> Se necesita <https://docs.docker.com/get-docker/>.

Antes de correrlo hay que ejecutar:

```sh
git submodule init && git submodule update --remote
```

Y descargar el archivo `steam_db.sql` y colocarlo en `data/`, de <https://drive.usercontent.google.com/download?id=1kR9uIj7tv9BY2RxThL3KElbpb3vQ9Oxg&export=download&authuser=1>

Una vez hecho esto, para lanzar la base de datos, la pagina web y phpMyAdmin:

```sh
docker compose up --build
```

Para lanzar los contendores y lanzarlos otra vez cada que se modifica algún archivo:
```sh
docker compose watch
```

Ya lanzado se puede acceder al proyecto en <http://localhost:8000> (ó <http://127.0.0.1:8000>) y a phpMyAdmin en <http://localhost:8080> (ó <http://127.0.0.1:8080>).

Usuarios disponibles para acceder en phpMyAdmin son:

| Usuario | Contraseña |
|---------|------------|
| root    | root       |
| dbuser  | dbuser     |
