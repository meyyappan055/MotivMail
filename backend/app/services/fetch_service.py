from models.db_schema import Quotes, Session
import requests
from fastapi import HTTPException

def fetch_quotes_from_external_api():
    session = Session()
    try:
        if session.query(Quotes).count() == 0:
            url = "https://api.quotable.io/quotes?limit=10"
            response = requests.get(url)
            if response.status_code == 200:
                quotes_data = response.json()['results']
                for quote_data in quotes_data:
                    new_quote = Quotes(
                        content=quote_data['content'],
                        author=quote_data.get('author', 'Unknown')
                    )
                    session.add(new_quote)
                session.commit()
                return {"message": "Quotes saved successfully"}
            else:
                return {"message": "Failed to fetch quotes from external API"} 
        else:
            return {"message": "No need to fetch more quotes, existing quotes available"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        session.close()
