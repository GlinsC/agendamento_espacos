from app.compartilhado.dominio.erros import (
    ConflitoDeDadosErro,
    EntidadeNaoEncontradaErro,
)
from app.modulos.espacos.dominio.contratos import EspacoRepositorioContrato
from app.modulos.espacos.dominio.entidades import Espaco
from app.modulos.espacos.interface.esquemas import AtualizarEspaco


class AtualizarEspacoCasoDeUso:
    def __init__(self, repositorio: EspacoRepositorioContrato):
        self.repositorio = repositorio

    def executar(self, id_espaco: int, dados: AtualizarEspaco) -> Espaco:
        espaco = self.repositorio.buscar_por_id(id_espaco)
        
        if not espaco:
            raise EntidadeNaoEncontradaErro(entidade="Espaço", id=id_espaco)

        if dados.nome and dados.nome != espaco.nome:
            if self.repositorio.buscar_por_nome(dados.nome):
                raise ConflitoDeDadosErro("Já existe outro espaço cadastrado com este nome.")
            espaco.nome = dados.nome

        if dados.descricao is not None:
            espaco.descricao = dados.descricao
        if dados.capacidade is not None:
            espaco.capacidade = dados.capacidade
        if dados.bloco is not None:
            espaco.bloco = dados.bloco

        return self.repositorio.atualizar(espaco)