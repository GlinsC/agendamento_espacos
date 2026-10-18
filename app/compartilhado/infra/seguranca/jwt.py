from datetime import UTC, datetime, timedelta

import jwt

from app.compartilhado.infra.config import config
from app.modulos.usuarios.dominio.contratos import TokenContrato


class JWT(TokenContrato):
    def criar_token_acesso(self, id_usuario: int) -> str:
        agora = datetime.now(UTC)

        payload = {
            "sub": str(id_usuario),
            "iat": agora,
            "exp": agora + timedelta(minutes=config.minutos_expiracao_token),
        }

        return jwt.encode(
            payload,
            config.chave_secreta,
            algorithm="HS256",
        )