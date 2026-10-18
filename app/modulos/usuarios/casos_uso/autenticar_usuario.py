from app.compartilhado.dominio.erros import AcessoNegadoErro, CredenciaisInvalidasErro
from app.modulos.usuarios.dominio.contratos import (
    CodificadorSenhaContrato,
    TokenContrato,
    UsuarioRepositorioContrato,
)
from app.modulos.usuarios.dominio.entidades import Usuario
from app.modulos.usuarios.interface.esquemas import TokenResposta, UsuarioLogin


class AutenticarUsuarioCasoDeUso:
    def __init__(
        self,
        repositorio: UsuarioRepositorioContrato,
        codificador: CodificadorSenhaContrato,
        token_servico: TokenContrato,
    ):
        self.repositorio = repositorio
        self.codificador = codificador
        self.token_servico = token_servico

    def executar(self, dados: UsuarioLogin) -> TokenResposta:
        usuario = self._pegar_usuario_por_identificacao(dados.identificacao)
        self._validar_usuario(usuario, dados.senha.get_secret_value())

        token_jwt = self.token_servico.criar_token_acesso(id_usuario=usuario.id)

        return TokenResposta(access_token=token_jwt, usuario=usuario)
    

    def _pegar_usuario_por_identificacao(self, identificacao: str) -> Usuario | None:
        if "@" in identificacao:
            return self.repositorio.buscar_por_email(identificacao)

        cpf_limpo = identificacao.replace(".", "").replace("-", "")
        return self.repositorio.buscar_por_cpf(cpf_limpo)
    

    def _validar_usuario(self, usuario: Usuario | None, senha: str):
        if not usuario or not self.codificador.verificar_senha(
            senha=senha,
            senha_codificada=usuario.senha_codificada,
        ):
            raise CredenciaisInvalidasErro()

        if not usuario.ativo:
            raise AcessoNegadoErro("Usuário inativo. Procure a coordenação do COLAB.")
