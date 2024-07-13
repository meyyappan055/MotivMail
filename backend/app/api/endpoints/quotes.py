from fastapi import APIRouter, HTTPException
from services.fetch_service import fetch_quotes_from_external_api  

router = APIRouter()

@router.get("/random")
async def random_quote():
    try:
        result = fetch_quotes_from_external_api()
        return result  
    except HTTPException as e:
        raise e

