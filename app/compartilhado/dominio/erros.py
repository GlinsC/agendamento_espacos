from fastapi import HTTPException, status


class ColabErro(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class EntidadeNaoEncontradaErro(ColabErro):
    def __init__(self, entidade: str, id: int | str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entidade} com ID {id} não encontrado(a).",
        )


class ConflitoDeDadosErro(ColabErro):
    def __init__(self, detalhe: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detalhe)


class RegraDeNegocioErro(ColabErro):
    def __init__(self, detalhe: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=detalhe
        )


class AcessoNegadoErro(ColabErro):
    def __init__(
        self, detalhe: str = "Você não tem permissão para realizar esta ação."
    ):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detalhe)


class CredenciaisInvalidasErro(ColabErro):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas."
        )
