from app.compartilhado.dominio.erros import (
    ConflitoDeDadosErro,
    EntidadeNaoEncontradaErro,
)
from app.modulos.espacos.dominio.contratos import EspacoRepositorioContrato
from app.modulos.espacos.dominio.entidades import Espaco


class ReativarEspacoCasoDeUso:
    def __init__(self, repositorio: EspacoRepositorioContrato):
        self.repositorio = repositorio

    def executar(self, id_espaco: int) -> Espaco:
        espaco = self.repositorio.buscar_por_id(id_espaco)
        
        if not espaco:
            raise EntidadeNaoEncontradaErro(entidade="Espaço", id=id_espaco)

        if espaco.disponibilidade:
            raise ConflitoDeDadosErro("O espaço já está ativo e disponível para uso.")
        
        espaco.disponibilidade = True
        return self.repositorio.atualizar(espaco)