## Blog Application

## Setup python version

To install and manage Python versions using pyenv, you can follow these steps:

### Install pyenv:

```shell
curl https://pyenv.run | bash

```

Follow the instructions provided to add pyenv to your shell's configuration.

### Install the required Python version:

```shell
pyenv install 3.9.1

```

### Set the local version for your project:

```shell
pyenv local 3.9.1

```

### Create virtual environment for python

```shell

python3.12.2 -m venv env

```

### Activate environment

```shell
source venv/bin/activate

```

### Activate environment for windows

```shell
source venv\Scripts\activate

```

### Install packages for fastapi

```shell
pip install -r requirements. txt

```

## Migrations

### Create migration

```shell
cd alembic
alembic revision --autogenerate -m "Initial migration"

```

### Run migration up

```shell
alembic upgrade head

```

### Run migration down

```shell
alembic downgrade -1

```

### Start app

```shell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

```
