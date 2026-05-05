from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated, List

NotaDecimal = Annotated[
    Decimal,
    Field(
        max_digits=3,
        decimal_places=2,
        ge=0,
        le=5
    )
]

class NotaBase(BaseModel):
    valor: NotaDecimal
    
class NotaUpdateList(BaseModel):
    notas: List[NotaBase]
    
class NotaRead(BaseModel):
    id: int
    valor: NotaDecimal
    
    model_config= {
        "from_attributes": True
    }
