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

## Erros relevantes

As respostas de erro usam o formato padrão do FastAPI (`detail`):

| Status | Situação |
|---|---|
| `401 Unauthorized` | Credenciais inválidas ou token inválido/expirado. |
| `403 Forbidden` | Perfil sem permissão para a operação; no login, também pode indicar usuário inativo. |
| `409 Conflict` | CPF, e-mail ou vínculo institucional já cadastrado. |
| `422 Unprocessable Entity` | Dados de entrada inválidos ou regra de negócio não atendida. |

## Escopo atual

As rotas de projetos, espaços, recursos, solicitações, anexos, agenda e monitoria ainda não estão implementadas. O modelo proposto para esses domínios está descrito em [banco_dados.md](banco_dados.md).
