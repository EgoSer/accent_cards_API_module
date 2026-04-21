## Contributing / forking project

[![Python](https://raw.githubusercontent.com/EgoSer/ege-cards-API/refs/heads/main/img/python_badge.svg?sanitize=True)](https://github.com/EgoSer/ege-cards-API/main)

[![Linter](https://raw.githubusercontent.com/EgoSer/ege-cards-API/refs/heads/main/img/linter_badge.svg?sanitize=True)](https://github.com/EgoSer/ege-cards-API/main)
[![Stack](https://raw.githubusercontent.com/EgoSer/ege-cards-API/refs/heads/main/img/stack_badge.svg?sanitize=True)](https://github.com/EgoSer/ege-cards-API/main)

This project has a modular structure.

You can modify or add a new type of cards using ```base``` module and ```shared``` logic. More on that in [Adding new functionality](https://github.com/EgoSer/ege-cards-API/blob/main/CONTRIBUTING.md#adding-new-functionality).

This project uses Github Actions workflow to run tests from ```test``` folder

## Setting up dev environment

### Download project and all dependencies

```bash
git clone https://github.com/EgoSer/ege-cards-API
cd ege-cards-API
pip install uv
uv sync
```


### Activate your venv
If you're on Windows:
```.venv\Scripts\activate.ps1```

If you're on Linux:
```source .venv/Scripts/activate```

### Setup ruff

```bash
pre-commit install --hook-type pre-commit
pre-commit run --all-files
```

### Launch all required services
- ```docker compose up -d --wait```

### Setup database
- ```alembic upgrade head```

## Launching dev server

```python main.py``` will launch uvicorn dev server

## Adding new functionality

### 1. Copy existing module
The first step to creating a new module is to build upon the old one! Seriously, modules have A LOT of metadata used by app, so consider copying existing module!

### 2. Define your ORM models
The reason behind this is **ALEMBIC**, so define your models, inheriting from ```Base``` class, (import from ```src.core.sql``` module)

### 3. Register your ORM
Navigate to **migration/env.py** file, find line that says **YOUR MODULES GO HERE** and add line importing all models from your ```YOUR_MODULE/models.py``` file
```python
############################# YOUR MODULES GO HERE #############################


from src.modules.YOUR_MODULE.models import *


################################################################################
```

### 4. Update Alembic
- ```alembic revision --autogenerate -m "Your meaningful commit message"```
- ```alembic upgrade head```

### 5. Update meta.py
In every module there's a ```meta.py``` file that contains information about module name, version and prefix. Make sure to update this information!
```python
module_name = "Accent cards" # The name of your module
version = "0.1a" # Actual version of your module
prefix = "/cards/accent" # prefix is used by fastapi Router class to define how to access your module
module_tags = ["accent"]
```

### 6. Define logic!
Now you're free to define whatever logic!


---

### P.S Please consider covering your logic with tests ^_^
