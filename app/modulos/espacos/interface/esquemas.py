from pydantic import BaseModel, ConfigDict, Field


class CriarEspaco(BaseModel):
    nome: str = Field(..., min_length=3, description="Nome da sala ou laboratório (ex: COLAB Maker)")
    descricao: str | None = Field(None, description="Descrição dos equipamentos ou finalidade do espaço")
    capacidade: str | None = Field(None, description="Capacidade máxima de pessoas (ex: 20 pessoas)")
    bloco: str | None = Field(None, description="Localização física no campus (ex: Bloco de Informática)")
    disponibilidade: bool = Field(True, description="Indica se o espaço está ativo para uso")

class AtualizarEspaco(BaseModel):
    nome: str | None = Field(None, min_length=3, description="Novo nome da sala")
    descricao: str | None = Field(None, description="Nova descrição")
    capacidade: str | None = Field(None, description="Nova capacidade")
    bloco: str | None = Field(None, description="Novo bloco")

class EspacoResposta(BaseModel):
    id: int
    nome: str
    descricao: str | None
    capacidade: str | None
    bloco: str | None
    disponibilidade: bool

    model_config = ConfigDict(from_attributes=True)