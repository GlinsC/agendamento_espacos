from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.compartilhado.infra.banco_dados import Base, motor
from app.modulos.espacos.infra.modelos import EspacoModelo, espaco_usuario_tabela
from app.modulos.usuarios.infra.modelos import UsuarioModelo


@asynccontextmanager
async def ciclo_de_vida_app(_: FastAPI) -> AsyncGenerator[None, None]:
    Base.metadata.create_all(
        bind=motor, tables=[UsuarioModelo.__table__, EspacoModelo.__table__, espaco_usuario_tabela]
    )
    yield
