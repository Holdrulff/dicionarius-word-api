from fastapi import FastAPI
from routes.word import router as word_router
from routes.meaning import router as meaning_router

app = FastAPI()

app.include_router(word_router)
app.include_router(meaning_router)