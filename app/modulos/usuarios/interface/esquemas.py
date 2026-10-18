from pydantic import BaseModel, EmailStr, Field, SecretStr

from app.modulos.usuarios.dominio.entidades import PerfilUsuario


class CriarServidor(BaseModel):
    nome_completo: str = Field(..., min_length=3, max_length=150)
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF apenas números ou formatado")
    vinculo_institucional: str = Field(..., min_length=3, description="Matrícula SIAPE")
    email: EmailStr
    senha: SecretStr = Field(..., min_length=8)

class CriarUsuarioInterno(BaseModel):
    nome_completo: str = Field(..., min_length=3, max_length=150)
    cpf: str = Field(..., min_length=11, max_length=14)
    vinculo_institucional: str = Field(..., min_length=3)
    email: EmailStr
    senha: SecretStr = Field(..., min_length=8)
    perfil: PerfilUsuario = Field(..., description="O perfil do usuário que será criado")

class UsuarioLogin(BaseModel):
    identificacao: str = Field(..., description="Pode ser o CPF (apenas números ou formatado) ou E-mail")
    senha: SecretStr = Field(..., description="Senha em texto puro para validação")


class UsuarioResposta(BaseModel):
    id: int
    nome_completo: str
    cpf: str
    vinculo_institucional: str
    email: EmailStr
    perfil: PerfilUsuario
    ativo: bool

    class Config:
        from_attributes = True


class TokenResposta(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResposta