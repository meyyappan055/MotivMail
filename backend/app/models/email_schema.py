from pydantic import BaseModel

class EmailSchema(BaseModel):
    send_mail : str
