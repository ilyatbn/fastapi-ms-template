
## Python API service quickstart
This is my implementation of FastAPI, coupled with SQLAlchemy and PostgreSQL or SQLite as a backend.
There are many different examples of this found around the web. This version has some neat tricks that I couldn't find in other code, and some modifications to existing code I found and liked.

**Features are added here based on my personal needs while I work on other services which are based on this template. As long as they are generic and can help ease setup pains, they will be added here.**
### Features
- FastAPI with a semi-modular BaseRouter class which is hopefully quite easy to use.
- SQLAlchemy with PostgreSQL/SQLite support. Currently manual database and table creation methods are provided. Alembic migration support is on the roadmap.


### Prerequisites and Installation
1. Install docker and docker-compose (v2.x)

    See https://docs.docker.com/engine/install/ubuntu/

2. Run make to build, then enter the shell to create the database and tables.
    ```
    make
    make start
    make shell
    ```

3. Inside the IPython shell, run the following to initialize the database and templates:
    ```
    from db.helpers import first_run
    await first_run()
    ```
---
* **Note:** Don't forget to modify the Dockerfile, and docker-compose.yml and rename image tags.
