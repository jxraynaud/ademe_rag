from pydantic import BaseModel

class CarbEquiv(BaseModel):
    name: str
    description: str
    unit: str
    quantity: float
