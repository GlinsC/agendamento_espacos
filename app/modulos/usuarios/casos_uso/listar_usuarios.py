from app.modulos.usuarios.dominio.contratos import UsuarioRepositorioContrato
from app.modulos.usuarios.dominio.entidades import PerfilUsuario, Usuario


class ListarUsuariosCasoDeUso:
    def __init__(self, repositorio: UsuarioRepositorioContrato):
        self.repositorio = repositorio

    def executar(self, perfil: PerfilUsuario | None = None, ativo: bool | None = None) -> list[Usuario]:
        return self.repositorio.listar(perfil=perfil, ativo=ativo)