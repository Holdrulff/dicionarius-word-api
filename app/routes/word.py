from fastapi import APIRouter, HTTPException, Query
from services.word_service import WordService

router = APIRouter(tags=["words"])

@router.get("/word")
async def get_word_by_length_router(length: int = Query(5, ge=4, le=8), theme: str = Query(None)):
    try:
        word_service = WordService()
        word = word_service.get_word(length=length, theme=theme)
        if not word:
            raise HTTPException(status_code=404, detail="No word found matching the criteria.")
        return {"word": word}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))