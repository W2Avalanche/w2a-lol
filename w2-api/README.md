# W2-API

API definition for W2 Project. Designed to Handle CRUD operations and Game manual updates.

## Requirements

Install the python requirements by PIP.

```bash
python -m pip install -r requirements.txt
```

Also, `w2project` package is required. Please, check more information on [W2Package](https://github.com/W2Avalanche/W2Package) repository.

A Postgres Instance is also required. It could be deployed as docker container by using [PG15 image](https://hub.docker.com/_/postgres).

## Usage

Configure the `configuration.json` by defining the propper database data connection. You can create a new secret key by running

```bash
openssl rand -hex 32
```

Configure `.json`:

```json
{
    "db_host": "localhost",
    "db_port": "15432",
    "db_name": "postgres",
    "db_user": "postgres",
    "db_password": "postgres",
    "auth_secret": "8674582f0f57eed7351bef7927d8a8aa84099fc2122aae2c421a0551c0627e8c"
}
```

Run the Uvicorn server by using the uvicorn command

```bash
uvicorn src.main:app --reload
```
