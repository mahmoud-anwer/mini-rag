from pydantic import BaseModel


class RetrievedDocument(BaseModel):
    text: str
    score: float
