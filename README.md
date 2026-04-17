## One of (and main) module of **EGE CARDS** app

It just gives a ```number``` of random cards from database


## Setting up (after pulling)

- ```cd ./accent_cards_API_module```
- ```pip install uv```
- ```uv sync```


### Activate your venv
If you're on Windows:
```.venv\Scripts\activate.ps1```

If you're on Linux:
```.venv/Scripts/activate```

- ```pre-commit install --hook-type pre-commit --hook-type pre-push```
- ```pre-commit run --all-files```
- ```pre-commit run --hook-stage push --all-files```

## Launching

```python main.py``` will launch uvicorn dev server.
For production please change main.py
