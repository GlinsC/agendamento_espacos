from datetime import datetime  # noqa: F401

from pydantic import BaseModel, ConfigDict


class EntidadeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int | None = None
