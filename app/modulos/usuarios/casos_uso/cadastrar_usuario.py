from app.compartilhado.dominio.erros import AcessoNegadoErro, ConflitoDeDadosErro
from app.modulos.usuarios.dominio.contratos import (
    CodificadorSenhaContrato,
    UsuarioRepositorioContrato,
)
from app.modulos.usuarios.dominio.entidades import PerfilUsuario, Usuario
from app.modulos.usuarios.interface.esquemas import CriarServidor, CriarUsuarioInterno


class CadastrarUsuarioCasoDeUso:
    def __init__(
        self,
        repositorio: UsuarioRepositorioContrato,
        codificador: CodificadorSenhaContrato,
    ):
        self.repositorio = repositorio
        self.codificador = codificador

    def servidor(self, dados: CriarServidor) -> Usuario:
        self._verificar_conflitos(dados)
        return self.repositorio.salvar(self._criar_usuario(dados))

    def interno(self, dados: CriarUsuarioInterno, usuario_logado: Usuario) -> Usuario:
        self._pode_criar_usuario(usuario_logado, dados.perfil)
        self._verificar_conflitos(dados)
        return self.repositorio.salvar(self._criar_usuario(dados))

    def _verificar_conflitos(self, dados: CriarServidor | CriarUsuarioInterno):
        if self.repositorio.buscar_por_cpf(dados.cpf):
            raise ConflitoDeDadosErro("Já existe um usuário cadastrado com este CPF.")

        if self.repositorio.buscar_por_email(dados.email):
            raise ConflitoDeDadosErro(
                "Já existe um usuário cadastrado com este e-mail."
            )

        if self.repositorio.buscar_por_vinculo(dados.vinculo_institucional):
            raise ConflitoDeDadosErro(
                "Já existe um usuário cadastrado com este vínculo institucional."
            )

    def _pode_criar_usuario(
        self, usuario_logado: Usuario, perfil_novo_usuario: PerfilUsuario
    ) -> None:
        if (
            perfil_novo_usuario in [PerfilUsuario.ADMINISTRADOR, PerfilUsuario.COORDENADOR]
            and usuario_logado.perfil != PerfilUsuario.ADMINISTRADOR
        ):
            raise AcessoNegadoErro(
                "Apenas administradores podem criar coordenadores ou novos administradores."
            )

    def _criar_usuario(self, dados: CriarServidor | CriarUsuarioInterno) -> Usuario:
        senha_codificada = self.codificador.codificar_senha(
            dados.senha.get_secret_value()
        )
        return Usuario(
            nome_completo=dados.nome_completo,
            cpf=dados.cpf,
            vinculo_institucional=dados.vinculo_institucional,
            email=dados.email,
            senha_codificada=senha_codificada,
            perfil=dados.perfil
            if isinstance(dados, CriarUsuarioInterno)
            else PerfilUsuario.SERVIDOR,
            ativo=True,
        )
