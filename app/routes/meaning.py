from fastapi import APIRouter, Query, HTTPException
from services.word_service import WordService

router = APIRouter(tags=["meanings"])

@router.get("/meanings")
async def get_word_meanings_router(word: str = Query(..., min_length=1)):
    try:
        word_service = WordService()
        meanings = word_service.get_meanings(word=word)
        if not meanings:
            raise HTTPException(status_code=404, detail="No meanings found for the given word.")
        return {"word": word, "meanings": meanings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))