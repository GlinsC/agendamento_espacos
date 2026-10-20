from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.compartilhado.dominio.erros import RegraDeNegocioErro


class Espaco(BaseModel):
    id: int | None = None
    nome: str
    descricao: str | None = None
    capacidade: int | None = None
    bloco: str | None = None
    disponibilidade: bool = True

    model_config = ConfigDict(from_attributes=True)


class EspacoHorarioFuncionamento(BaseModel):
    id: int | None = None
    dia_semana: int = Field(
        ..., ge=0, le=6, description="0=Domingo, 1=Segunda, ..., 6=Sábado"
    )
    hora_abertura: time
    hora_fechamento: time
    ativo: bool = True
    id_espaco: int

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validar_regras_horario(self):
        if self.hora_fechamento <= self.hora_abertura:
            raise RegraDeNegocioErro(
                f"Horário inválido para o dia {self.dia_semana}: "
                f"O fechamento ({self.hora_fechamento}) deve ser posterior à abertura ({self.hora_abertura})."
            )
        return self


class EspacoPausaFuncionamento(BaseModel):
    id: int | None = None
    data_inicio: date
    data_fim: date
    motivo: str
    id_espaco: int
    
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def validar_datas(self):
        if self.data_fim < self.data_inicio:
            raise RegraDeNegocioErro("A data final do bloqueio não pode ser anterior à data inicial.")
        return self
