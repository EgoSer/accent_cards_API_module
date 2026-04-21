
## **EGE CARDS** app backend
[![Tests](https://github.com/EgoSer/ege-cards-API/actions/workflows/tests.yml/badge.svg)](https://github.com/EgoSer/ege-cards-API/actions/workflows/tests.yml)

[![image](https://raw.githubusercontent.com/EgoSer/ege-cards-API/refs/heads/main/img/version_badge.svg?sanitize=True)](https://github.com/EgoSer/ege-cards-API/main)
[![image](https://raw.githubusercontent.com/EgoSer/ege-cards-API/refs/heads/main/img/license_badge.svg?sanitize=True)](https://github.com/EgoSer/ege-cards-API/blob/main/LICENSE)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

---

API. Gives a ```number``` of random cards from database

---

The project has a modular structure. You can easily modify or add a new type of cards using ```base``` module and ```shared``` logic. More on that in ```Adding new functionality```


## Setting up dev environment

### Download project and all dependencies

- ```git clone https://github.com/EgoSer/ege-cards-API```
- ```cd ege-cards-API```
- ```pip install uv```
- ```uv sync```


### Activate your venv
If you're on Windows:
```.venv\Scripts\activate.ps1```

If you're on Linux:
```source .venv/Scripts/activate```

### Setup ruff

- ```pre-commit install --hook-type pre-commit```
- ```pre-commit run --all-files```

### Launch all required services
- ```docker compose up -d --wait```

### Setup database
- ```alembic upgrade head```

## Launching

```python main.py``` will launch uvicorn dev server.
For production please change main.py

## Adding new functionality

### 1. Copy existing module
The first step to creating a new module is to build upon the old one! Seriously, modules have A LOT of metadata used by app, so consider copying existing module!

### 2. Define your ORM models
The reason behind this is **ALEMBIC**, so define your models, inheriting from Base, imported from ```src.core.sql``` module

### 3. Register your ORM
Navigate to file **migration/env.py**, find line that says **YOUR MODULES GO HERE** and add line importing all models from your ```YOUR_MODULE/models.py``` file (e.g ```from src.modules.YOUR_MODULE.models import *```)

### 4. Update Alembic
- ```alembic revision --autogenerate -m "Your meaningful commit message"```
- ```alembic upgrade head```

### 5. Update meta.py
In every module there's a ```meta.py``` file that contains information about module name, version and prefix. Make sure to update this information!

### 6. Define logic!
Now you're free to define whatever logic!


---

### P.S Please consider cover your logic with tests (This repo has github actions set up and uses pytest)
