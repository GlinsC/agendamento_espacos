from datetime import time

from app.compartilhado.dominio.erros import ConflitoDeDadosErro
from app.modulos.espacos.dominio.contratos import (
    EspacoRepositorioContrato,
    RegrasHorarioRepositorioContrato,
)
from app.modulos.espacos.dominio.entidades import Espaco, EspacoHorarioFuncionamento
from app.modulos.espacos.interface.esquemas import CriarEspaco


class CadastrarEspacoCasoDeUso:
    def __init__(
        self,
        repositorio: EspacoRepositorioContrato,
        repo_horario: RegrasHorarioRepositorioContrato,
    ):
        self.repositorio = repositorio
        self.repo_horario = repo_horario

    def executar(self, dados: CriarEspaco) -> Espaco:
        with self.repositorio.transacao():
            if self.repositorio.buscar_por_nome(dados.nome):
                raise ConflitoDeDadosErro("Já existe um espaço cadastrado com este nome.")

            novo_espaco = Espaco(
                nome=dados.nome,
                descricao=dados.descricao,
                capacidade=dados.capacidade,
                bloco=dados.bloco,
                disponibilidade=dados.disponibilidade
            )

            espaco_salvo = self.repositorio.salvar(novo_espaco)
            if espaco_salvo.id is None:
                raise RuntimeError("Não foi possível obter o ID do espaço cadastrado.")

            self._definir_horario_padrao(espaco_salvo.id)
        return espaco_salvo

    def _definir_horario_padrao(self, id_espaco: int) -> None:
        for dia in range(7):
            dia_util = 1 <= dia <= 5

            horario_padrao = EspacoHorarioFuncionamento(
                dia_semana=dia,
                hora_abertura=time(8, 0),
                hora_fechamento=time(18, 0),
                ativo=dia_util,
                id_espaco=id_espaco
            )

            self.repo_horario.definir_horario(horario_padrao)