from app.compartilhado.dominio.erros import EntidadeNaoEncontradaErro
from app.modulos.espacos.dominio.contratos import EspacoRepositorioContrato
from app.modulos.espacos.dominio.entidades import Espaco


class DesativarEspacoCasoDeUso:
    def __init__(self, repositorio: EspacoRepositorioContrato):
        self.repositorio = repositorio

    def executar(self, id_espaco: int) -> Espaco:
        espaco = self.repositorio.buscar_por_id(id_espaco)
        
        if not espaco:
            raise EntidadeNaoEncontradaErro(entidade="Espaço", id=id_espaco)
        
        espaco.disponibilidade = False
        return self.repositorio.atualizar(espaco)