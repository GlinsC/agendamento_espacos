from pydantic import BaseModel, ConfigDict


class Espaco(BaseModel):
    id: int | None = None
    nome: str
    descricao: str | None = None
    capacidade: str | None = None
    bloco: str | None = None
    disponibilidade: bool = True
    
    model_config = ConfigDict(from_attributes=True)