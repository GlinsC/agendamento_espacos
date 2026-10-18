from app.compartilhado.dominio.erros import ConflitoDeDadosErro
from app.modulos.espacos.dominio.contratos import (
    EspacoRepositorioContrato,
)
from app.modulos.espacos.dominio.entidades import Espaco
from app.modulos.espacos.interface.esquemas import CriarEspaco


class CadastrarEspacoCasoDeUso:
    def __init__(self, repositorio: EspacoRepositorioContrato):
        self.repositorio = repositorio

    def executar(self, dados: CriarEspaco) -> Espaco:
        if self.repositorio.buscar_por_nome(dados.nome):
            raise ConflitoDeDadosErro("Já existe um espaço cadastrado com este nome.")

        novo_espaco = Espaco(
            nome=dados.nome,
            descricao=dados.descricao,
            capacidade=dados.capacidade,
            bloco=dados.bloco,
            disponibilidade=dados.disponibilidade
        )

        espaco_salvo = self.repositorio.salvar(novo_espaco)
        return espaco_salvo