# lgpd-kit

> Skills para assistentes de código que ajudam a adequar sistemas à **LGPD (Lei nº 13.709/2018)** e às **resoluções da ANPD** — da descoberta dos dados pessoais à matriz de rastreabilidade artigo → requisito → código, com um módulo próprio de **anonimização com medição de risco**.

[![Licença: MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-yellow.svg)](./LICENSE)
[![LGPD](https://img.shields.io/badge/LGPD-Lei%2013.709%2F2018-blue)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm)
![Status](https://img.shields.io/badge/status-em%20constru%C3%A7%C3%A3o-orange)

---

## O que é

O lgpd-kit é um conjunto de **Agent Skills**: pacotes de instruções que o assistente de código (como o Claude Code) carrega quando o assunto é LGPD. Ele trabalha no seu repositório, procura evidências no código e grava os resultados em uma pasta `.lgpd/`, versionada junto com o projeto.

O que diferencia o kit:

- **Começa perguntando.** Uma entrevista inicial define se você quer uma verificação rápida, uma auditoria completa, documentos, código pronto ou ajuda com um incidente.
- **Entende o nicho.** A descoberta identifica pelo banco de dados se o sistema é de saúde, financeiro, varejo, educação, RH, marketing ou mobilidade, e ajusta a auditoria a isso.
- **Audita por camada.** Banco de dados, back-end, front-end e infraestrutura, cada um com seus requisitos.
- **Rastreia até a lei.** Um catálogo de 55 requisitos de software, construído em um TCC ([veja a origem](#origem-um-tcc-sobre-lgpd-e-anonimização)) e com cada requisito ligado ao artigo da LGPD que o originou, resulta numa matriz requisito → artigo → arquivo e linha → status.
- **Trata a anonimização como risco medido.** Em vez de "removemos o nome", o kit compara métodos e mede o risco de reidentificação e a perda de utilidade, seguindo o esquema proposto pela ANPD.

## Skills

| Skill | O que faz | Situação |
|---|---|---|
| `lgpd-auditoria` | Maestro: entrevista, escolhe o caminho, coordena as outras skills e mantém o estado em `.lgpd/STATUS.md`. | ✅ |
| `lgpd-descoberta` | Detecta stack e camadas, identifica o nicho e gera o inventário de dados pessoais (com script). | ✅ |
| `lgpd-requisitos` | Catálogo de 55 requisitos, 9 obrigações organizacionais e referência normativa. | ✅ |
| `lgpd-banco-de-dados` | Auditoria da camada de banco. | 🚧 |
| `lgpd-backend` | Auditoria da camada de back-end. | 🚧 |
| `lgpd-frontend` | Auditoria da camada de front-end. | 🚧 |
| `lgpd-infra` | Auditoria da infraestrutura. | 🚧 |
| `lgpd-organizacional` | Obrigações da organização (encarregado, contratos, governança). | 🚧 |
| `lgpd-documentos` | Política de privacidade, registro das operações, RIPD, termos e contratos. | 🚧 |
| `lgpd-consentimento` | Código de consentimento por finalidade, com versão do texto. | 🚧 |
| `lgpd-direitos-titular` | Código para os pedidos do titular, com controle de prazos. | 🚧 |
| `lgpd-trilha-auditoria` | Trilha encadeada e à prova de alteração, sem dado pessoal em claro. | 🚧 |
| `lgpd-pseudonimizacao` | Separação de dados, pseudônimo com HMAC, sem metadados de ligação. | 🚧 |
| `lgpd-anonimizacao-relatorios` | Relatórios anonimizados com medição de risco (k, l, risco médio e máximo) e utilidade. | 🚧 |
| `lgpd-incidentes` | Levantamento de afetados e comunicação no prazo da Res. CD/ANPD nº 15/2024. | 🚧 |

✅ disponível · 🚧 planejada

## Instalação

### Claude Code

```text
/plugin marketplace add SEU_USUARIO/lgpd-kit
/plugin install lgpd-kit@lgpd-kit
```

### Manual

Funciona com qualquer agente que leia skills de `~/.claude/skills/` ou `.claude/skills/`:

```bash
git clone https://github.com/SEU_USUARIO/lgpd-kit.git
cp -r lgpd-kit/skills/lgpd-* ~/.claude/skills/        # para todos os projetos
# ou: cp -r lgpd-kit/skills/lgpd-* .claude/skills/   # só para o projeto atual
```

O script de inventário precisa apenas de **Python 3.9+**, sem dependências.

## Como usar

Peça ao assistente, em linguagem natural:

- "Audite a LGPD deste projeto."
- "Que dados pessoais esse sistema guarda?"
- "Faz uma verificação rápida de privacidade."
- "Preciso de uma política de privacidade para esse app."
- "Tivemos um vazamento, o que eu faço?"

O maestro faz a entrevista inicial e segue daí. Também dá para chamar uma skill diretamente, por exemplo: "use a skill lgpd-descoberta".

## O que fica em `.lgpd/`

```
.lgpd/
├── STATUS.md                  # onde a adequação está e próximos passos
├── descoberta.md              # nicho, camadas, papel da organização
├── inventario-dados.md        # dados pessoais por tabela e campo
├── matriz-rastreabilidade.md  # requisito → artigo → código → status
├── plano-acao.md              # correções priorizadas
├── documentos/                # política, registro das operações, RIPD...
└── incidentes/                # registro de incidentes (mínimo 5 anos)
```

Adicione `.lgpd/` ao Git: o histórico mostra a evolução da adequação. Nunca grave dados reais de titulares nessa pasta.

## Cobertura normativa

- **LGPD** (Lei nº 13.709/2018), com as alterações até a Lei nº 15.352/2026.
- **Resoluções do Conselho Diretor da ANPD:** nº 1/2021 (fiscalização), nº 2/2022 (pequeno porte), nº 4/2023 (dosimetria), nº 15/2024 (incidentes), nº 18/2024 (encarregado), nº 19/2024 (transferência internacional), nº 32/2026 (adequação da União Europeia) e a agenda regulatória vigente.
- **Estudos da ANPD sobre anonimização e pseudonimização** (2023), como referência técnica.
- **Normas setoriais** (saúde, financeiro, educação, consumo, internet, trabalho) são **apenas sinalizadas**, não auditadas.

Detalhes em [`skills/lgpd-requisitos/references/referencia-normativa.md`](skills/lgpd-requisitos/references/referencia-normativa.md). Base conferida em outubro de 2026.

## Aviso

**Este projeto não é aconselhamento jurídico.** O kit verifica requisitos de software e ajuda a organizar documentos, mas a conformidade com a LGPD depende também de decisões e processos da organização. Decisões sobre comunicação de incidentes, bases legais, contratos e respostas à ANPD devem envolver o encarregado e um advogado especializado.

## Origem: um TCC sobre LGPD e anonimização

A ideia do lgpd-kit partiu do meu TCC em Tecnologia em Sistemas para Internet, na UFSM. Eu queria entender como transformar o que a LGPD exige, que está escrito em linguagem jurídica, em requisitos que possam ser implementados e testados no código.

Para isso, fui lendo a lei artigo por artigo e separando o que se aplica ao sistema. Cheguei a 55 requisitos (35 funcionais e 20 não funcionais), divididos em 11 famílias, e cada um aponta para o artigo de onde saiu. O que não depende do software, como nomear o encarregado ou fazer o relatório de impacto, deixei separado em 9 obrigações da organização. Depois apliquei tudo a um cenário de clínica médica, com dados fictícios.

A outra parte do TCC é sobre anonimização. Nela comparo métodos de anonimização e pseudonimização para ver qual deixa menor risco de alguém descobrir a quem pertence o dado, sem prejudicar muito a utilidade dele. Para medir esse risco, sigo o esquema que a ANPD propõe.

Enquanto fazia o TCC, pensei que isso poderia ajudar quem desenvolve sistemas no dia a dia, em vez de ficar só no papel. Então trouxe para cá:

- o **catálogo de requisitos** e as **obrigações da organização** (`lgpd-requisitos`), adaptados para qualquer nicho;
- o modelo da **matriz** que liga artigo → requisito → código;
- o **método de anonimização com medição de risco**, que vai virar a skill `lgpd-anonimizacao-relatorios`.

> OLIVEIRA, Gabriel Jaime de. *Transformação de Exigências da LGPD em Requisitos de Software para a Proteção de Dados Pessoais Sensíveis*. Trabalho de Conclusão de Curso (Tecnologia em Sistemas para Internet) — Universidade Federal de Santa Maria, Santa Maria, 2026. Em andamento.

A organização em skills foi inspirada no projeto [lgpd-skills](https://github.com/goul4rt/lgpd-skills), de goul4rt. O conteúdo do lgpd-kit é próprio.

## Contribuindo

Contribuições são bem-vindas, principalmente correções normativas, novos nichos e suporte a outros formatos de esquema no script de inventário. Veja [CONTRIBUTING.md](./CONTRIBUTING.md).

## Licença

[MIT](./LICENSE)
