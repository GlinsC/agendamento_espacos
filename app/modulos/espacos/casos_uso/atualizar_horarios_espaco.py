from app.compartilhado.dominio.erros import EntidadeNaoEncontradaErro
from app.modulos.espacos.dominio.contratos import (
    EspacoRepositorioContrato,
    RegrasHorarioRepositorioContrato,
)
from app.modulos.espacos.dominio.entidades import (
    EspacoHorarioFuncionamento,
)
from app.modulos.espacos.interface.esquemas import AtualizarHorario


class AtualizarHorariosEspacoCasoDeUso:
    def __init__(
        self, 
        repo_espaco: EspacoRepositorioContrato, 
        repo_horario: RegrasHorarioRepositorioContrato
    ):
        self.repo_espaco = repo_espaco
        self.repo_horario = repo_horario

    def executar(self, id_espaco: int, dados: AtualizarHorario) -> EspacoHorarioFuncionamento:
        espaco = self.repo_espaco.buscar_por_id(id_espaco)
        if not espaco:
            raise EntidadeNaoEncontradaErro(entidade="Espaço", id=id_espaco)

        horario_atualizado = EspacoHorarioFuncionamento(
            dia_semana=dados.dia_semana,
            hora_abertura=dados.hora_abertura,
            hora_fechamento=dados.hora_fechamento,
            ativo=dados.ativo,
            id_espaco=id_espaco
        )
        
        return self.repo_horario.atualizar_horario(horario_atualizado)