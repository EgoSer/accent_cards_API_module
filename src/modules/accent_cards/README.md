## How to use: Accent cards

[Home](https://github.com/EgoSer/ege-cards-API/blob/main/README.md)

### Review

Accent cards is a module which returns an "accent card", which consists of two main fields:

- ```word```: a string in utf-8 encoding, containing only cyrillic letters
- ```accent```: a 4-byte integer

### Endpoints

Module contains 2 endpoints:

```/``` - Root endpoint

It gives meta information about module, e.g.

request: ```http://your.domain.backend.org/cards/accent```

response:

```json
{
    "module": "Accent cards",
    "description": "Returns requested amount of accent cards (or less if database have not enough)",
    "version": "0.2.1-alpha"
}
```

---

```/get_cards``` - working endpoint. Gives ```number``` of cards or less if requested amount is greater than number of cards in the database

#### E.G

request: ```http://your.domain.backend.org/cards/accent/get_cards?amount=3```

response:

```json
{
    "cards": [
        {
            "word": "туфля",
            "accent": 1,
            "id": "15515d0b-6177-4e05-92a8-32c987656094"
        },
        {
            "word": "торты",
            "accent": 1,
            "id": "96e8a9a1-4fb7-4178-b346-210196dfe0f4"
        },
        {
            "word": "привет",
            "accent": 4,
            "id": "ef97e914-5568-41d7-a2db-1d320e47c8db"
        }
    ]
}
```

## Cards purpose

It is one of EGE tasks. It requires a student to put right acent to a right letter in a word.
This module works with database to provide tasks to a frontend application
