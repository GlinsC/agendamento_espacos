from app.modulos.espacos.dominio.contratos import EspacoRepositorioContrato
from app.modulos.espacos.dominio.entidades import Espaco
from app.modulos.usuarios.dominio.entidades import PerfilUsuario, Usuario


class ListarEspacosCasoDeUso:
    def __init__(self, repositorio: EspacoRepositorioContrato):
        self.repositorio = repositorio

    def executar(self, usuario_logado: Usuario) -> list[Espaco]:
        if usuario_logado.perfil == PerfilUsuario.ADMINISTRADOR:
            return self.repositorio.buscar_todos()
            
        if usuario_logado.perfil == PerfilUsuario.SERVIDOR:
            return self.repositorio.buscar_todos_ativos()
            
        if usuario_logado.perfil in [PerfilUsuario.COORDENADOR, PerfilUsuario.MONITOR]:
            return self.repositorio.buscar_por_vinculo_usuario(usuario_logado.id)
            
        return []