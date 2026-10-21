---
name: lgpd-descoberta
description: Primeira etapa de uma auditoria LGPD — identifica a stack e as camadas do projeto (banco, back-end, front-end, infra), descobre o nicho do sistema (saúde, financeiro, varejo, educação, RH, marketing, mobilidade, poder público) e faz o inventário inicial de dados pessoais, sensíveis e quase-identificadores. Use quando o usuário pedir "mapear dados pessoais", "inventário de dados", "que dados pessoais temos", "data mapping", ou como primeira etapa chamada pelo lgpd-auditoria.
---

# Descoberta: stack, nicho e inventário de dados

A descoberta prepara o terreno para o resto da auditoria. Ela responde a três perguntas: **que camadas o projeto tem**, **de que nicho ele é** e **que dados pessoais ele trata**. As respostas definem quais requisitos importam, quais dados sensíveis são prováveis e quais quase-identificadores entram na anonimização.

## Passo a passo

### 1. Rode o inventário automático

```bash
python3 <pasta-desta-skill>/scripts/inventario.py <raiz-do-projeto> --saida .lgpd/inventario-dados.md
```

O script varre definições de dados em **Prisma, SQL (inclusive migrations do Supabase), Django e TypeORM**, classifica cada campo pelo nome e sugere o nicho e as camadas. Ele usa só a biblioteca padrão do Python.

Se o projeto usa outro formato (Mongoose, Sequelize, Drizzle, JSON Schema, NoSQL sem esquema), o script não vai achar os campos. Nesse caso, leia os modelos manualmente e preencha o inventário no mesmo formato.

### 2. Revise a classificação

A classificação por nome erra. Revise com atenção:

- **Falsos negativos:** campos genéricos que guardam dado sensível, como `observacoes`, `notas`, `metadata`, `payload` ou colunas JSON. Abra amostras do código que grava nesses campos.
- **Falsos positivos:** campos como `nome_produto` que não são dado pessoal.
- **Inferência (art. 11, § 1º):** campos que não são sensíveis sozinhos, mas revelam um dado sensível, como setor de atendimento, especialidade, medicamento ou categoria de compra.
- **Dados fora do banco:** logs, filas, *buckets* de arquivos, analytics, ferramentas de terceiros (e-mail, CRM, monitoramento).

### 3. Mapeie as camadas

Confirme o que o script detectou e complete:

| Camada | O que procurar |
|---|---|
| Banco de dados | Esquema, migrations, políticas de acesso (RLS), *views*, *backups*, réplicas. |
| Back-end | Rotas e *endpoints*, autenticação e papéis, rotinas agendadas, integrações, logs. |
| Front-end | Formulários de coleta, telas que exibem dado pessoal, aviso de privacidade, consentimento, cookies, armazenamento no navegador. |
| Infra | Hospedagem e região dos servidores, segredos e chaves, TLS, *backups*, CI/CD, monitoramento. |

### 4. Identifique e confirme o nicho

Use a sugestão do script e a tabela de [`references/nichos.md`](references/nichos.md). **Pergunte ao usuário** antes de seguir, por exemplo:

> Pelo banco de dados, o sistema parece ser da área de **saúde** (tabelas de pacientes, exames e consultas). Confere? Há também dados de crianças ou adolescentes?

O nicho confirmado define:
- os **dados sensíveis prováveis** a procurar;
- as **bases legais típicas**;
- os **quase-identificadores** que a anonimização vai tratar;
- as **normas setoriais** a sinalizar (sem auditá-las);
- se há **crianças e adolescentes** (art. 14).

### 5. Registre o resultado

Grave dois arquivos em `.lgpd/`:

- `.lgpd/inventario-dados.md` — gerado pelo script e revisado.
- `.lgpd/descoberta.md` — no formato abaixo.

```markdown
# Descoberta

- **Data:** AAAA-MM-DD
- **Nicho:** saúde (confirmado pelo usuário)
- **Normas setoriais a sinalizar:** prontuário eletrônico; sigilo de condições específicas
- **Crianças e adolescentes:** sim (pediatria)
- **Papel da organização:** controladora
- **Camadas:** banco (PostgreSQL/Supabase), back-end (Next.js API), front-end (Next.js), infra (Vercel + Supabase)

## Dados sensíveis encontrados
- `Exame.diagnostico`, `Exame.resultadoExame`, `Exame.medicamento`

## Quase-identificadores principais
- `Paciente.dataNascimento`, `Paciente.sexo`, `Paciente.bairro`, data do atendimento

## Dados fora do banco
- Logs da aplicação (Vercel), e-mails transacionais (serviço X)

## Alertas
- Identificação e dado sensível na mesma tabela `consulta`
```

## Regras

- **Nunca copie dados reais** para o relatório. Registre nomes de tabelas e campos, não valores.
- Se precisar olhar dados para classificar um campo, peça autorização e use amostras mínimas.
- O nicho é um palpite até o usuário confirmar.
- Se o projeto for do **poder público**, avise que as regras dos arts. 23 a 32 da LGPD se aplicam e que o lgpd-kit foi pensado para controladores privados.
