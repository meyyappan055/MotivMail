from fastapi import APIRouter, HTTPException
from models.db_schema import Quotes, Session, User, SentQuote
from services.email_service import send_email as send_email_service
from services.fetch_service import fetch_quotes_from_external_api
from sqlalchemy.sql.expression import func
import logging
from models.email_schema import EmailSchema

router = APIRouter()
logger = logging.getLogger(__name__)

async def send_email_task(email: str):
    session = Session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            user = User(email=email, name="Unknown")
            session.add(user)
            session.commit()
            session.refresh(user)

        random_quote = (
            session.query(Quotes)
            .filter(~Quotes.sent_quotes.any(SentQuote.user_id == user.id))
            .order_by(func.random())
            .first()
        )

        if not random_quote:
            random_quote = fetch_quotes_from_external_api()

        context = {
            "title": "Daily Motivation",
            "message": random_quote.content,
            "author": random_quote.author
        }

        await send_email_service(email, "Daily Motivation", context)
        sent_quote = SentQuote(user_id=user.id, quote_id=random_quote.id)
        session.add(sent_quote)
        session.commit()

        return {"message": "Email sent successfully!"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error sending email in email.py: {e}")

    finally:
        session.close()

async def send_email_to_all_users():
    session = Session()
    try:
        users = session.query(User).all()
        for user in users:
            logger.info(f"Sending email to user: {user.email}")
            await send_email_task(user.email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cannot send mail to all the users: {e}")
    finally:
        session.close()

@router.post("/send-email")
async def send_email_endpoint(email: EmailSchema):
    return await send_email_task(email.send_mail)
