from fastapi import FastAPI
from routes.word import router as word_router

app = FastAPI()

app.include_router(word_router)