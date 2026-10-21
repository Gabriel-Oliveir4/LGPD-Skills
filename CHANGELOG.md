# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Versionamento semântico.

## [0.2.0] — 2026-10-21

### Adicionado
- Auditoria por camada: `lgpd-banco-de-dados`, `lgpd-backend`, `lgpd-frontend`, `lgpd-infra`.
- `lgpd-organizacional`: questionário sobre encarregado, pequeno porte, documentação, operadores, transferência internacional, governança e incidentes.
- `lgpd-documentos`: modelos de aviso de privacidade, registro das operações, RIPD, teste de legítimo interesse, termo de consentimento e cláusulas com operador.
- `lgpd-consentimento`: regras, API mínima, cookies conforme o guia da ANPD e esquema SQL com histórico imutável.
- `lgpd-direitos-titular`: fluxo, modelo de dados, exportação, eliminação e controle de prazos.
- `lgpd-trilha-auditoria`: trilha somente de inclusão, encadeada por hash, com função de verificação.
- `lgpd-pseudonimizacao`: modelo com HMAC, armadilhas de ligação, exemplos em TypeScript, Python e SQL, e script `estimar_reversao.py`.
- `lgpd-anonimizacao-relatorios`: método com risco medido e scripts `anonimizar.py` (medir, aplicar, comparar C0–C4) e `gerar_exemplo.py`.
- `lgpd-incidentes`: roteiro de urgência, prazos, modelos de registro e de comunicação aos titulares.

## [0.1.0] — 2026-10-21

### Adicionado
- `lgpd-auditoria`: maestro com entrevista inicial, cinco caminhos (verificação rápida, auditoria completa, documentos, ferramentas, incidente), roteamento entre skills e modelos de `STATUS.md` e `plano-acao.md`.
- `lgpd-descoberta`: detecção de camadas, identificação de nicho (oito nichos) e script `inventario.py` para Prisma, SQL, Django e TypeORM.
- `lgpd-requisitos`: catálogo de 55 requisitos em 11 famílias com artigo de origem, camadas e o que verificar; 9 obrigações organizacionais; referência normativa com LGPD e resoluções da ANPD (conferida em outubro de 2026).
- Manifesto de plugin para o Claude Code.
