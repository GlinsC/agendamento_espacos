from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modulos.espacos.dominio.contratos import (
    EspacoRepositorioContrato,
)
from app.modulos.espacos.dominio.entidades import Espaco
from app.modulos.espacos.infra.modelos import EspacoModelo, espaco_usuario_tabela


class EspacoRepositorio(EspacoRepositorioContrato):
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_nome(self, nome: str) -> Espaco | None:
        modelo = self.db.query(EspacoModelo).filter(EspacoModelo.nome == nome).first()
        if not modelo:
            return None
        return Espaco.model_validate(modelo)

    def buscar_todos_ativos(self) -> list[Espaco]:
        modelos = self.db.query(EspacoModelo).filter(EspacoModelo.disponibilidade == True).all()
        return [Espaco.model_validate(modelo) for modelo in modelos]

    def buscar_por_vinculo_usuario(self, id_usuario: int) -> list[Espaco]:
        modelos = (
            self.db.query(EspacoModelo)
            .join(espaco_usuario_tabela)
            .filter(espaco_usuario_tabela.c.id_usuario == id_usuario)
            .all()
        )
        return [Espaco.model_validate(modelo) for modelo in modelos]

    def buscar_por_id(self, id_espaco: int) -> Espaco | None:
        modelo = self.db.query(EspacoModelo).filter(EspacoModelo.id == id_espaco).first()
        if not modelo:
            return None
        return Espaco.model_validate(modelo)

    def buscar_todos(self) -> list[Espaco]:
        modelos = self.db.query(EspacoModelo).all()
        return [Espaco.model_validate(modelo) for modelo in modelos]

    def salvar(self, espaco: Espaco) -> Espaco:
        modelo = EspacoModelo(
            nome=espaco.nome,
            descricao=espaco.descricao,
            capacidade=espaco.capacidade,
            bloco=espaco.bloco,
            disponibilidade=espaco.disponibilidade,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return Espaco.model_validate(modelo)

    def atualizar(self, espaco: Espaco) -> Espaco:
        modelo = self.db.query(EspacoModelo).filter(EspacoModelo.id == espaco.id).first()
        if modelo:
            modelo.nome = espaco.nome
            modelo.descricao = espaco.descricao
            modelo.capacidade = espaco.capacidade
            modelo.bloco = espaco.bloco
            modelo.disponibilidade = espaco.disponibilidade
            
            self.db.commit()
            self.db.refresh(modelo)
            return Espaco.model_validate(modelo)
        raise ValueError("Espaço não encontrado no banco de dados.")

    def verificar_vinculo(self, id_espaco: int, id_usuario: int) -> bool:
        consulta = select(espaco_usuario_tabela).where(
            espaco_usuario_tabela.c.id_espaco == id_espaco,
            espaco_usuario_tabela.c.id_usuario == id_usuario
        )
        resultado = self.db.execute(consulta).first()
        return resultado is not None

    def adicionar_vinculo(self, id_espaco: int, id_usuario: int) -> None:
        comando = espaco_usuario_tabela.insert().values(id_espaco=id_espaco, id_usuario=id_usuario)
        self.db.execute(comando)
        self.db.commit()

    def remover_vinculo(self, id_espaco: int, id_usuario: int) -> None:
        comando = espaco_usuario_tabela.delete().where(
            espaco_usuario_tabela.c.id_espaco == id_espaco,
            espaco_usuario_tabela.c.id_usuario == id_usuario
        )
        self.db.execute(comando)
        self.db.commit()