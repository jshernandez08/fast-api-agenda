from datetime import datetime
from pydantic import BaseModel


class InitModel(BaseModel):
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()