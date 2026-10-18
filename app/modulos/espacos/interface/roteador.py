from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.modulos.espacos.casos_uso.atualizar_espaco import AtualizarEspacoCasoDeUso
from app.modulos.espacos.casos_uso.cadastrar_espaco import CadastrarEspacoCasoDeUso
from app.modulos.espacos.casos_uso.desativar_espaco import DesativarEspacoCasoDeUso
from app.modulos.espacos.casos_uso.gerenciar_vinculos import GerenciarVinculosCasoDeUso
from app.modulos.espacos.casos_uso.listar_espacos import ListarEspacosCasoDeUso
from app.modulos.espacos.casos_uso.reativar_espaco import ReativarEspacoCasoDeUso
from app.modulos.espacos.interface.dependencias import (
    pegar_caso_de_uso_atualizar_espaco,
    pegar_caso_de_uso_cadastrar_espaco,
    pegar_caso_de_uso_desativar_espaco,
    pegar_caso_de_uso_gerenciar_vinculos,
    pegar_caso_de_uso_listar_espacos,
    pegar_caso_de_uso_reativar_espaco,
)
from app.modulos.espacos.interface.esquemas import (
    AtualizarEspaco,
    CriarEspaco,
    EspacoResposta,
)
from app.modulos.usuarios.dominio.entidades import PerfilUsuario, Usuario
from app.modulos.usuarios.interface.seguranca_http import (
    VerificarPerfil,
    obter_usuario_atual,
)

roteador = APIRouter(prefix="/espacos", tags=["Infraestrutura e Espaços"])

apenas_admin = VerificarPerfil([PerfilUsuario.ADMINISTRADOR])
admin_ou_coordenador = VerificarPerfil(
    [PerfilUsuario.ADMINISTRADOR, PerfilUsuario.COORDENADOR]
)


@roteador.post(
    "/",
    response_model=EspacoResposta,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo espaço físico/sala (Somente Admin)",
)
def cadastrar_espaco(
    dados: CriarEspaco,
    usuario_logado: Annotated[Usuario, Depends(apenas_admin)],
    caso_de_uso: Annotated[
        CadastrarEspacoCasoDeUso, Depends(pegar_caso_de_uso_cadastrar_espaco)
    ],
):
    return caso_de_uso.executar(dados)


@roteador.get(
    "/",
    response_model=list[EspacoResposta],
    status_code=status.HTTP_200_OK,
    summary="Listar todos os espaços do laboratório (Disponível para todos os perfis)",
)
def listar_espacos(
    usuario_logado: Annotated[Usuario, Depends(obter_usuario_atual)],
    caso_de_uso: Annotated[
        ListarEspacosCasoDeUso, Depends(pegar_caso_de_uso_listar_espacos)
    ],
):
    return caso_de_uso.executar(usuario_logado)


@roteador.delete(
    "/{id_espaco}",
    response_model=EspacoResposta,
    status_code=status.HTTP_200_OK,
    summary="Desativar/Indisponibilizar um espaço (Somente Admin)",
)
def desativar_espaco(
    id_espaco: int,
    usuario_logado: Annotated[Usuario, Depends(apenas_admin)],
    caso_de_uso: Annotated[
        DesativarEspacoCasoDeUso, Depends(pegar_caso_de_uso_desativar_espaco)
    ],
):
    return caso_de_uso.executar(id_espaco)


@roteador.put(
    "/{id_espaco}",
    response_model=EspacoResposta,
    status_code=status.HTTP_200_OK,
    summary="Atualizar dados de um espaço (Admin e Coordenador)",
)
def atualizar_espaco(
    id_espaco: int,
    dados: AtualizarEspaco,
    usuario_logado: Annotated[Usuario, Depends(admin_ou_coordenador)],
    caso_de_uso: Annotated[
        AtualizarEspacoCasoDeUso, Depends(pegar_caso_de_uso_atualizar_espaco)
    ],
):
    return caso_de_uso.executar(id_espaco, dados)


@roteador.patch(
    "/{id_espaco}/reativar",
    response_model=EspacoResposta,
    status_code=status.HTTP_200_OK,
    summary="Reativar um espaço indisponível (Somente Admin)",
)
def reativar_espaco(
    id_espaco: int,
    usuario_logado: Annotated[Usuario, Depends(apenas_admin)],
    caso_de_uso: Annotated[
        ReativarEspacoCasoDeUso, Depends(pegar_caso_de_uso_reativar_espaco)
    ],
):
    return caso_de_uso.executar(id_espaco)


@roteador.post(
    "/{id_espaco}/usuarios/{id_usuario}",
    status_code=status.HTTP_201_CREATED,
    summary="Vincular Coordenador/Monitor ao Espaço"
)
def vincular_usuario_espaco(
    id_espaco: int,
    id_usuario: int,
    usuario_logado: Annotated[Usuario, Depends(admin_ou_coordenador)],
    caso_de_uso: Annotated[GerenciarVinculosCasoDeUso, Depends(pegar_caso_de_uso_gerenciar_vinculos)]
):
    return caso_de_uso.vincular(id_espaco, id_usuario)


@roteador.delete(
    "/{id_espaco}/usuarios/{id_usuario}",
    status_code=status.HTTP_200_OK,
    summary="Remover vínculo de Coordenador/Monitor com o Espaço"
)
def desvincular_usuario_espaco(
    id_espaco: int,
    id_usuario: int,
    usuario_logado: Annotated[Usuario, Depends(admin_ou_coordenador)],
    caso_de_uso: Annotated[GerenciarVinculosCasoDeUso, Depends(pegar_caso_de_uso_gerenciar_vinculos)]
):
    return caso_de_uso.desvincular(id_espaco, id_usuario)