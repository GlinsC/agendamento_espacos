from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.compartilhado.infra.banco_dados import Base

espaco_usuario_tabela = Table(
    "espaco_usuario",
    Base.metadata,
    Column("id_espaco", Integer, ForeignKey("espaco.id", ondelete="CASCADE"), primary_key=True),
    Column("id_usuario", Integer, ForeignKey("usuario.id", ondelete="CASCADE"), primary_key=True)
)

class EspacoModelo(Base):
    __tablename__ = "espaco"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), unique=True, nullable=False)
    descricao = Column(String(255), nullable=True)
    capacidade = Column(String(50), nullable=True)
    bloco = Column(String(50), nullable=True)
    disponibilidade = Column(Boolean, default=True, nullable=False)

    usuarios_vinculados = relationship("UsuarioModelo", secondary=espaco_usuario_tabela, backref="espacos_vinculados")