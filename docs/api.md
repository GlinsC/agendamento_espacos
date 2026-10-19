# API HTTP

Este documento descreve as rotas atualmente registradas pela aplicação. A documentação interativa gerada pelo FastAPI permanece disponível em `/docs` (Swagger UI) e `/redoc` quando o servidor está em execução.

## Autenticação

As rotas protegidas recebem um token JWT no cabeçalho:

```http
Authorization: Bearer <access_token>
```

O token é obtido em `POST /usuarios/login`, assinado com HS256 e expira após `MINUTOS_EXPIRACAO_TOKEN` (30 minutos por padrão). Os perfis aceitos pela API são `Administrador`, `Coordenador`, `Servidor`, `Monitor` e `Aluno`.

## Rotas

| Método | Caminho | Acesso | Descrição |
|---|---|---|---|
| `GET` | `/` | Público | Verifica se a API está em execução. |
| `POST` | `/usuarios/servidor` | Público | Cadastra um servidor solicitante. |
| `POST` | `/usuarios/interno` | Administrador ou Coordenador | Cadastra usuário interno. |
| `POST` | `/usuarios/login` | Público | Autentica por CPF ou e-mail e retorna JWT. |
| `GET` | `/usuarios/me` | Usuário autenticado | Retorna os dados do usuário do token. |
| `POST` | `/projetos/` | Servidor ou Monitor | Cadastra um projeto com o usuário autenticado como responsável. |
| `GET` | `/projetos/` | Usuário autenticado | Lista todos os projetos e seus participantes. |
| `GET` | `/projetos/{id_projeto}` | Usuário autenticado | Consulta um projeto e seus participantes. |
| `PUT` | `/projetos/{id_projeto}` | Responsável pelo projeto | Atualiza os dados descritivos do próprio projeto. |
| `PATCH` | `/projetos/{id_projeto}/status` | Administrador | Define o estado do projeto como Pendente, Aceito ou Recusado. |
| `DELETE` | `/projetos/{id_projeto}` | Administrador | Exclui o projeto e seus vínculos com participantes. |
| `POST` | `/projetos/{id_projeto}/participantes` | Responsável ou Administrador | Adiciona participante ao projeto. |
| `DELETE` | `/projetos/{id_projeto}/participantes/{id_usuario}` | Responsável ou Administrador | Remove participante do projeto. |

### `GET /`

Retorna uma mensagem de status:

```json
{
  "mensagem": "API do COLAB operando com sucesso!"
}
```

### `POST /usuarios/servidor`

Não exige autenticação. Cria um usuário com perfil `Servidor` e retorna `201 Created`. Para permitir login por CPF, cadastre-o somente com números; a busca no login remove pontos e hífen antes da consulta.

```json
{
  "nome_completo": "Nome do Servidor",
  "cpf": "12345678901",
  "vinculo_institucional": "1234567",
  "email": "servidor@example.com",
  "senha": "senha-com-no-minimo-8"
}
```

Nome precisa ter de 3 a 150 caracteres; CPF, de 11 a 14; vínculo institucional, no mínimo 3. O e-mail deve ser válido e a senha deve conter pelo menos 8 caracteres.

### `POST /usuarios/interno`

Exige token de Administrador ou Coordenador e retorna `201 Created`. O campo `perfil` deve ser um dos valores de perfil listados acima. Para permitir login por CPF, cadastre-o somente com números; a busca no login remove pontos e hífen antes da consulta.

```json
{
  "nome_completo": "Nome do Usuário",
  "cpf": "12345678901",
  "vinculo_institucional": "7654321",
  "email": "usuario@example.com",
  "senha": "senha-com-no-minimo-8",
  "perfil": "Monitor"
}
```

Um Coordenador pode cadastrar perfis não administrativos, mas somente um Administrador pode criar Administradores ou Coordenadores.

Como essa rota exige um perfil privilegiado, o primeiro Administrador precisa ser provisionado por um procedimento externo à API. Não há rota pública de criação inicial de Administrador.

### `POST /usuarios/login`

Não exige autenticação. O valor de `identificacao` pode ser um e-mail ou CPF (com ou sem pontuação).

```json
{
  "identificacao": "servidor@example.com",
  "senha": "senha-com-no-minimo-8"
}
```

Retorna `200 OK`:

```json
{
  "access_token": "<token>",
  "token_type": "bearer",
  "usuario": {
    "id": 1,
    "nome_completo": "Nome do Servidor",
    "cpf": "12345678901",
    "vinculo_institucional": "1234567",
    "email": "servidor@example.com",
    "perfil": "Servidor",
    "ativo": true
  }
}
```

### `GET /usuarios/me`

Exige token válido. Retorna o mesmo objeto `usuario` incluído na resposta do login, sem a senha ou seu hash.

## Projetos

O perfil `Servidor` representa o Professor no fluxo de cadastro de projetos; o perfil `Monitor` também pode criar projetos. O usuário autenticado que cadastra o projeto fica registrado como responsável. Todo usuário autenticado pode consultar e listar projetos; somente o responsável pode editar os dados descritivos. O Administrador pode alterar o estado de avaliação e excluir projetos. O responsável ou um Administrador pode gerenciar os participantes.

O estado inicial é `Pendente`. A avaliação do projeto é independente da aprovação de uma solicitação de uso do laboratório.

### `POST /projetos/`

Exige token de Servidor ou Monitor e retorna `201 Created`.

```json
{
  "descricao": "Projeto de pesquisa em fabricação digital",
  "finalidade": "Pesquisa",
  "quantidade_participantes": 4,
  "documentacao_base": "https://sigaa.example/projeto/123"
}
```

`descricao` e `finalidade` são obrigatórios. `quantidade_participantes` é opcional e não pode ser negativa; `documentacao_base` também é opcional. A resposta inclui o ID do responsável, o estado de avaliação e a lista de participantes.

### `PATCH /projetos/{id_projeto}/status`

Exige token de Administrador. Para aceitar ou recusar o projeto, envie um dos valores definidos:

```json
{
  "status": "Aceito"
}
```

Valores possíveis: `Pendente`, `Aceito` e `Recusado`.

### Gestão de participantes

O responsável pelo projeto ou um Administrador pode adicionar um usuário existente:

```http
POST /projetos/1/participantes
```

```json
{
  "id_usuario": 2,
  "papel_no_projeto": "Pesquisador"
}
```

A remoção é feita por `DELETE /projetos/{id_projeto}/participantes/{id_usuario}`. A API rejeita usuários inexistentes e vínculos duplicados. Cada participante retornado contém `id_usuario`, `nome_completo` e `papel_no_projeto`.

## Erros relevantes

As respostas de erro usam o formato padrão do FastAPI (`detail`):

| Status | Situação |
|---|---|
| `401 Unauthorized` | Credenciais inválidas ou token inválido/expirado. |
| `403 Forbidden` | Perfil sem permissão para a operação; no login, também pode indicar usuário inativo. |
| `409 Conflict` | CPF, e-mail ou vínculo institucional já cadastrado. |
| `422 Unprocessable Entity` | Dados de entrada inválidos ou regra de negócio não atendida. |

## Escopo futuro

As rotas de recursos, horários de funcionamento, solicitações, anexos, agenda e monitoria ainda não estão implementadas. O modelo proposto para esses domínios está descrito em [banco_dados.md](banco_dados.md).
