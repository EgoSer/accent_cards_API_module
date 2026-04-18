## Backend part of **EGE CARDS** app

API. Gives a ```number``` of random cards from database

---

The project has a modular structure. You can easily modify or add a new type of cards using ```base``` module and ```shared``` logic. More on that in ```Adding new functionality```


## Setting up (after pulling)

- ```cd ./accent_cards_API_module```
- ```pip install uv```
- ```uv sync```


### Activate your venv
If you're on Windows:
```.venv\Scripts\activate.ps1```

If you're on Linux:
```source .venv/Scripts/activate```

- ```pre-commit install --hook-type pre-commit```
- ```pre-commit run --all-files```

## Launching

```python main.py``` will launch uvicorn dev server.
For production please change main.py

## Adding new functionality

This block is still under construction
