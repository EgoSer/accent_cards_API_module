
## **EGE CARDS** app backend
[![Tests](https://github.com/EgoSer/ege-cards-API/actions/workflows/tests.yml/badge.svg)](https://github.com/EgoSer/ege-cards-API/actions/workflows/tests.yml)

[![Version](https://raw.githubusercontent.com/EgoSer/ege-cards-API/refs/heads/main/img/version_badge.svg?sanitize=True)](https://github.com/EgoSer/ege-cards-API/blob/main)
[![License](https://raw.githubusercontent.com/EgoSer/ege-cards-API/refs/heads/main/img/license_badge.svg?sanitize=True)](https://github.com/EgoSer/ege-cards-API/blob/main/LICENSE)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

---

RESTful API. Gives a requested number of random cards from database

---

## How to build this app (update when branch "release" is present: links for cloning and docker-compose.yml):

### 1. Clone repo and locate into the folder
```shell
git clone https://github.com/EgoSer/ege-cards-API.git
cd ./ege-cards-API
```

### 2. [Install docker](https://docs.docker.com/engine/install/)

### 3. Build docker image
```shell
docker build . -t ege-cards-api:latest
```

### 4. Run built image and all required services
```shell
docker compose up -d --wait
```

## How to use:

Check out usage guides / manuals written for each module individually!

- [Accent cards module](https://github.com/EgoSer/ege-cards-API/blob/main/src/modules/accent_cards/README.md)

## How to fork / contribute

[Read more on how to extend / modify functionality here](https://github.com/EgoSer/ege-cards-API/blob/main/CONTRIBUTING.md)
