---
name: lgpd-banco-de-dados
description: Audita a camada de banco de dados de um projeto quanto à LGPD - separação entre identificação e dado sensível, pseudônimo, metadados de ligação, criptografia em repouso, papéis de acesso, retenção, eliminação, backups e dados reais fora de produção. Gera evidência com arquivo e linha para a matriz de rastreabilidade. Use em auditorias de esquema (Prisma, SQL, migrations, ORMs), quando o usuário perguntar "meu banco está de acordo com a LGPD?" ou quando o maestro lgpd-auditoria chamar a etapa de banco.
---

# lgpd-banco-de-dados

Audita o esquema e a configuração do banco. Parte do inventário gerado por `lgpd-descoberta` (`.lgpd/inventario-dados.md`); se ele não existir, rode a descoberta antes.

## Entradas

- `.lgpd/inventario-dados.md` e `.lgpd/descoberta.md` (nicho, dados sensíveis, quase-identificadores).
- Esquema: `schema.prisma`, `migrations/`, `*.sql`, `models.py`, `*.entity.ts`, políticas RLS, seeds e fixtures.
- Catálogo: `lgpd-requisitos/references/catalogo-requisitos.md`, filtrando a coluna "Camadas" por **BD**.

## Roteiro

Verifique na ordem abaixo. Para cada item, registre o status (✅ 🟡 ❌ ➖) com arquivo e linha.

### 1. Onde está o dado sensível
- O dado sensível (art. 5º, II) está na mesma tabela que nome, CPF ou e-mail? Se sim, **RF-23 ❌**.
- Campos de texto livre (`observacao`, `anotacao`, `descricao`, `motivo`) podem conter dado sensível sem que o nome do campo diga. Pergunte ao usuário ou olhe exemplos nos seeds fictícios.
- Tabelas que **revelam** dado sensível indiretamente (art. 11, § 1º): agenda por especialidade, compra de medicamento, filiação a sindicato, doação a partido.

### 2. Pseudônimo e ligação (RF-23, RNF-06, RNF-10, RNF-11, RNF-12)
- Como as tabelas de identificação e de dado sensível se ligam? Chave estrangeira direta para `paciente.id` derrota a separação.
- O pseudônimo é `sha256(cpf)` ou `md5(email)` sem chave? **RNF-10 ❌**: o espaço de CPFs (cerca de 10⁹ combinações de base) é percorrido em pouco tempo.
- ID sequencial (`serial`, `autoincrement()`, `IDENTITY`) compartilhado entre as tabelas? **RNF-11 ❌**: a ordem dos registros liga as duas.
- `created_at` gravado no mesmo instante nas duas tabelas? **RNF-11 🟡**: o horário liga os registros. UUID v1 e v7 carregam data e hora; prefira v4 ou token aleatório.
- A chave do HMAC ou a tabela de correspondência está no mesmo banco? **RNF-06 ❌**.
- As duas partes são lidas pelo mesmo usuário de banco? **RNF-12 ❌**.

Para corrigir, use `lgpd-pseudonimizacao`.

### 3. Acesso (RF-11, RF-29, RNF-16)
- Há RLS, *views* restritas ou papéis (`GRANT`) que limitem o dado sensível aos perfis autorizados?
- A aplicação usa um superusuário (`postgres`, `root`, `service_role`) para tudo? Registre como 🟡 e explique o risco.
- No Supabase, a `service_role` key aparece em código de front-end? **❌ grave**.

### 4. Criptografia (RNF-15)
- Criptografia em repouso do disco ou do serviço gerenciado (verifique com o usuário ou na configuração da nuvem).
- Campos especialmente sensíveis cifrados na aplicação ou com `pgcrypto`, com a chave fora do banco.
- Senhas: hash lento (bcrypt, scrypt, Argon2). Senha em texto puro ou com `md5`/`sha1` é ❌ grave.

### 5. Localização por titular (RNF-05)
- Toda tabela com dado pessoal tem caminho até o titular (chave ou pseudônimo)? Sem isso, não há como atender acesso, portabilidade ou eliminação.

### 6. Ciclo de vida (RF-26, RF-27, RF-28, RF-04, RF-22)
- Existe campo ou tabela de prazo de retenção por finalidade?
- Exclusão lógica (`deleted_at`) sem eliminação definitiva depois de um prazo não é eliminação. Registre 🟡.
- Tabelas de consentimento (RF-04) e de requisições do titular (RF-22) existem?
- Há registro das eliminações (RF-28)?

### 7. Backups e cópias (RNF-13)
- Backups cifrados, com acesso restrito e prazo de guarda definido.
- *Dumps* (`*.sql`, `*.dump`, `*.bak`) dentro do repositório: ❌ grave.

### 8. Dados reais fora de produção
- Seeds, fixtures e bancos de homologação com dados reais de titulares. Procure CPFs válidos, e-mails de domínios reais e nomes completos em `seed*`, `fixtures/`, `__tests__/`. Nunca copie os valores para o relatório: informe só arquivo, linha e tipo de dado.

### 9. Trilha (RF-31, RNF-18, RNF-19)
- A tabela de auditoria existe, guarda o titular por pseudônimo e está protegida contra `UPDATE` e `DELETE` (trigger, permissão ou armazenamento só de inclusão)?

## Buscas úteis

```bash
grep -rniE "autoincrement|serial|identity|uuid_generate_v1|uuidv7" --include=*.prisma --include=*.sql .
grep -rniE "sha256|md5|sha1|createHash|digest\(" --include=*.{ts,js,py,sql} .
grep -rniE "row level security|create policy|grant |revoke " --include=*.sql .
grep -rniE "deleted_at|soft.?delete|paranoid" .
find . -name "*.sql" -o -name "*.dump" -o -name "*.bak" | grep -v node_modules
```

## Saída

Acrescente as linhas da camada **BD** em `.lgpd/matriz-rastreabilidade.md`:

| ID | Requisito | Origem | Camada | Status | Evidência | Ação recomendada |
|---|---|---|---|---|---|---|

Atualize o semáforo da camada em `.lgpd/STATUS.md`. Pare e peça aprovação antes de criar ou alterar qualquer migration.
