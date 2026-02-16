from fastapi import APIRouter, HTTPException, Query
from services.word_service import WordService

router = APIRouter(tags=["words"])

@router.get("/word")
async def get_word_by_length_router(
    length: int = Query(5),
    lang: str = Query("en-us"),
):
    try:
        word_service = WordService()
        entry = word_service.get_word(length=length, lang=lang)
        if not entry:
            raise HTTPException(status_code=404, detail="No word found matching the criteria.")
        return entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
