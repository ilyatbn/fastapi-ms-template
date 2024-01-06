
## Python API service quickstart
There's probably a bunch of these to be found online. This is my implementation of FastAPI, coupled with SQLAlchemy and PostgreSQL or SQLite as a backend.

### Features
- FastAPI.
- SQLAlchemy with PostgreSQL/SQLite.


### Prerequisites and Installation
1. Install docker and docker-compose (v2.x)

    See https://docs.docker.com/engine/install/ubuntu/

2. Run make to build, then enter the shell to create the database and tables.
    ```
    make
    make start
    make shell
    ```

3. Inside the IPython shell, run the following:
    ```
    from core.db_helpers import first_run
    await first_run()
    ```
---
* **Note:** Don't forget to modify the Dockerfile, and docker-compose.yml and rename image tags.
