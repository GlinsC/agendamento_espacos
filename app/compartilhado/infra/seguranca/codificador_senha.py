from pwdlib import PasswordHash

from app.modulos.usuarios.dominio.contratos import CodificadorSenhaContrato


class CodificadorSenha(CodificadorSenhaContrato):
    def __init__(self):
        self._codificador = PasswordHash.recommended()

    def codificar_senha(self, senha: str) -> str:
        return self._codificador.hash(senha)

    def verificar_senha(
        self,
        senha: str,
        senha_codificada: str,
    ) -> bool:
        return self._codificador.verify(senha, senha_codificada)