from app.modulos.espacos.casos_uso.atualizar_espaco import AtualizarEspacoCasoDeUso
from app.modulos.espacos.casos_uso.cadastrar_espaco import CadastrarEspacoCasoDeUso
from app.modulos.espacos.casos_uso.desativar_espaco import DesativarEspacoCasoDeUso
from app.modulos.espacos.casos_uso.gerenciar_vinculos import GerenciarVinculosCasoDeUso
from app.modulos.espacos.casos_uso.listar_espacos import ListarEspacosCasoDeUso
from app.modulos.espacos.casos_uso.reativar_espaco import ReativarEspacoCasoDeUso
from app.modulos.espacos.infra.repositorios import EspacoRepositorio
from app.modulos.usuarios.infra.repositorios import UsuarioRepositorio
from app.modulos.usuarios.interface.dependencias import SessaoBD


def pegar_caso_de_uso_cadastrar_espaco(db: SessaoBD) -> CadastrarEspacoCasoDeUso:
    repositorio = EspacoRepositorio(db)
    return CadastrarEspacoCasoDeUso(repositorio)

def pegar_caso_de_uso_listar_espacos(db: SessaoBD) -> ListarEspacosCasoDeUso:
    return ListarEspacosCasoDeUso(EspacoRepositorio(db))

def pegar_caso_de_uso_desativar_espaco(db: SessaoBD) -> DesativarEspacoCasoDeUso:
    return DesativarEspacoCasoDeUso(EspacoRepositorio(db))

def pegar_caso_de_uso_atualizar_espaco(db: SessaoBD) -> AtualizarEspacoCasoDeUso:
    return AtualizarEspacoCasoDeUso(EspacoRepositorio(db))

def pegar_caso_de_uso_reativar_espaco(db: SessaoBD) -> ReativarEspacoCasoDeUso:
    return ReativarEspacoCasoDeUso(EspacoRepositorio(db))

def pegar_caso_de_uso_gerenciar_vinculos(db: SessaoBD) -> GerenciarVinculosCasoDeUso:
    repo_espaco = EspacoRepositorio(db)
    repo_usuario = UsuarioRepositorio(db)
    return GerenciarVinculosCasoDeUso(repo_espaco, repo_usuario)