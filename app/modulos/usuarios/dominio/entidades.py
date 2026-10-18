from enum import Enum

from pydantic import EmailStr, Field

from app.compartilhado.dominio.entidade_base import EntidadeBase


class PerfilUsuario(str, Enum):
    ADMINISTRADOR = "Administrador"
    COORDENADOR = "Coordenador"
    SERVIDOR = "Servidor"
    MONITOR = "Monitor"
    ALUNO = "Aluno"

class Usuario(EntidadeBase):
    nome_completo: str = Field(..., min_length=3, max_length=150)
    cpf: str = Field(..., min_length=11, max_length=14)
    vinculo_institucional: str = Field(..., min_length=3, description="Matrícula acadêmica")
    email: EmailStr
    senha_codificada: str
    perfil: PerfilUsuario
    ativo: bool = True