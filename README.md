# Dicionarius API

A lightweight FastAPI service that serves random Portuguese words for my homie’s Wordle/Termo-style web app, **Dicionarius** (built by GitHub user **buemura**). This API exists so the frontend can fetch fresh words by length on demand.

## What It Does
- Returns a random word based on length (4–8 letters)
- Simple HTTP interface designed for frontend consumption
- Dictionary files live in `dict/`

## Endpoint
`GET /word`

Query params:
- `length` (int, required): 4–8
- `theme` (string, optional): reserved for future filtering

Example:
```
GET /word?length=5
```

Response:
```json
{ "word": "..." }
```

## Local Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker
```bash
docker-compose up --build
```

API will be at `http://localhost:8000`.

## Notes
- Word lists are stored in `dict/palavras_*.txt`
- If no word matches, the API responds with 404

## Credits
- Frontend (Dicionarius): **buemura**
- API: **bruno**
