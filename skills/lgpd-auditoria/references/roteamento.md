# Roteamento entre skills

Sequência de skills de cada caminho e o que fazer se uma delas ainda não estiver instalada.

## Skills do lgpd-kit

| Skill | Papel | Situação |
|---|---|---|
| `lgpd-auditoria` | Maestro: entrevista, caminho e estado | ✅ disponível |
| `lgpd-descoberta` | Stack, camadas, nicho e inventário de dados | ✅ disponível |
| `lgpd-requisitos` | Catálogo de requisitos, obrigações e referência normativa | ✅ disponível |
| `lgpd-banco-de-dados` | Auditoria da camada de banco | 🚧 planejada |
| `lgpd-backend` | Auditoria da camada de back-end | 🚧 planejada |
| `lgpd-frontend` | Auditoria da camada de front-end | 🚧 planejada |
| `lgpd-infra` | Auditoria da infraestrutura | 🚧 planejada |
| `lgpd-organizacional` | Obrigações da organização | 🚧 planejada |
| `lgpd-documentos` | Política de privacidade, registro das operações, RIPD, termos, contratos | 🚧 planejada |
| `lgpd-consentimento` | Código de consentimento com versão do texto | 🚧 planejada |
| `lgpd-direitos-titular` | Código para pedidos do titular e prazos | 🚧 planejada |
| `lgpd-trilha-auditoria` | Código de trilha encadeada, sem dado pessoal em claro | 🚧 planejada |
| `lgpd-pseudonimizacao` | Separação dos dados, HMAC, sem metadados de ligação | 🚧 planejada |
| `lgpd-anonimizacao-relatorios` | Relatórios anonimizados com medição de risco e utilidade | 🚧 planejada |
| `lgpd-incidentes` | Levantamento de afetados e comunicação no prazo | 🚧 planejada |

## Sequência por caminho

### Verificação rápida
1. `lgpd-descoberta`
2. `lgpd-requisitos` — só os requisitos críticos listados no maestro
3. Semáforo por camada em `.lgpd/STATUS.md`

### Auditoria completa
1. `lgpd-descoberta`
2. `lgpd-banco-de-dados`
3. `lgpd-backend`
4. `lgpd-frontend`
5. `lgpd-infra`
6. `lgpd-organizacional`
7. Matriz de rastreabilidade e plano de ação (`lgpd-requisitos`)

### Documentos
1. `lgpd-descoberta` (pode ser resumida: nicho, papel e dados tratados)
2. `lgpd-documentos`
3. Pausa para revisão humana antes de publicar ou assinar

### Ferramentas
1. `lgpd-descoberta` (resumida: stack e nicho)
2. Skill da ferramenta escolhida
3. Pausa antes de cada alteração de código

### Incidente agora
1. `lgpd-incidentes`
2. Consulta à trilha (RF-33) para levantar dados e titulares afetados
3. Registro do incidente em `.lgpd/incidentes/` (guardar por no mínimo 5 anos)

## Se a skill ainda não estiver instalada

Enquanto as skills planejadas não existirem, siga esta orientação mínima e registre no STATUS que a etapa foi feita sem a skill específica.

- **Camadas (banco, back-end, front-end, infra):** use o catálogo de `lgpd-requisitos`, filtrando pela coluna "Camadas", e verifique cada requisito pela coluna "O que verificar".
- **Organizacional:** use `lgpd-requisitos/references/obrigacoes-organizacionais.md`.
- **Documentos:** liste os documentos necessários e o conteúdo mínimo exigido pela lei (por exemplo, os itens do art. 9º para o aviso de privacidade), sem redigir a versão final.
- **Incidente:** oriente o usuário a acionar o encarregado e o jurídico imediatamente, levante os dados e titulares afetados pela trilha de auditoria e lembre o prazo de 3 dias úteis da Res. CD/ANPD nº 15/2024.
