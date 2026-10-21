---
name: lgpd-organizacional
description: Avalia as obrigações da LGPD que dependem da organização e não do código - encarregado (Res. CD/ANPD nº 18/2024), enquadramento como agente de pequeno porte (Res. nº 2/2022), registro das operações, RIPD, contratos com operadores, transferência internacional (Res. nº 19/2024 e nº 32/2026), programa de governança, registro de incidentes e canal do titular. Faz um questionário curto, pede evidências e marca cada item como dependente da organização na matriz. Use para "governança LGPD", "preciso de DPO?", "somos pequeno porte?", "contrato com fornecedor", ou quando o maestro lgpd-auditoria chamar a etapa organizacional.
---

# lgpd-organizacional

Esta etapa não lê código: conversa com o usuário e pede evidências (um link, um documento, um contrato). Use [`lgpd-requisitos/references/obrigacoes-organizacionais.md`](../lgpd-requisitos/references/obrigacoes-organizacionais.md) como base e registre cada item com 🏢 na matriz, indicando se a evidência foi apresentada.

Não é aconselhamento jurídico: aponte lacunas e o que a norma pede; a decisão é da organização.

## Questionário

Faça em blocos de até quatro perguntas, usando a ferramenta de múltipla escolha quando houver.

### Bloco 1 — Enquadramento
1. Papel: controladora, operadora ou as duas? (já pode estar em `.lgpd/descoberta.md`)
2. Porte: microempresa, empresa de pequeno porte, startup ou pessoa natural com fins econômicos? Se sim, verifique se **não** há tratamento de alto risco (larga escala ou que afete significativamente os titulares, combinado com dado sensível, dados de crianças, adolescentes ou idosos, decisões automatizadas ou tecnologias emergentes). Só sem alto risco valem as flexibilizações da Res. CD/ANPD nº 2/2022.

### Bloco 2 — Encarregado (OBR-01; Res. CD/ANPD nº 18/2024)
3. Há encarregado indicado por ato formal? Interno ou externo?
4. Nome e contato estão divulgados em local de fácil acesso (site, app)?
5. O canal funciona? (peça para testar: um e-mail enviado é respondido?)
6. O encarregado acumula função que gere conflito de interesse (por exemplo, quem decide sobre o tratamento)?

Pequeno porte sem alto risco pode ser dispensado de indicar encarregado, mas precisa manter canal de comunicação com o titular.

### Bloco 3 — Documentação (OBR-02)
7. Existe registro das operações de tratamento (art. 37)? Quando foi atualizado?
8. Existe RIPD para os tratamentos de maior risco (art. 38)?
9. Os avisos de privacidade correspondem ao que o sistema faz?

Para gerar ou revisar, use `lgpd-documentos`.

### Bloco 4 — Terceiros (OBR-04)
10. Para cada operador encontrado por `lgpd-backend` e `lgpd-infra` (nuvem, e-mail, pagamentos, analytics, IA): há contrato com cláusulas de proteção de dados?
11. Algum deles trata dados fora do Brasil? Qual mecanismo de transferência internacional é usado (cláusulas-padrão da ANPD, cláusulas específicas, normas corporativas globais ou decisão de adequação, como a da União Europeia pela Res. nº 32/2026)?

### Bloco 5 — Governança e incidentes (OBR-03, OBR-05)
12. Há política interna de proteção de dados, treinamento das pessoas que acessam dados e revisão periódica (art. 50)?
13. Há plano de resposta a incidentes e registro de **todos** os incidentes, guardado por no mínimo 5 anos (Res. nº 15/2024)?
14. Quem decide sobre comunicar um incidente?

### Bloco 6 — Titulares (OBR-06, OBR-07, OBR-08, OBR-09)
15. As requisições dos titulares são atendidas sem custo e dentro dos prazos?
16. Dados de saúde são compartilhados com alguém para obter vantagem econômica (art. 11, § 4º)?
17. Há uso dos dados para decisões que possam discriminar (art. 6º, IX)?

## Saída

- Linhas `OBR-01` a `OBR-09` e os pontos das resoluções na matriz, com status 🏢 e a evidência apresentada (ou "não apresentada").
- Pendências no `plano-acao.md`, com prioridade: falta de canal do titular e de plano de incidentes são **altas**; contratos e documentação, **médias**.
- Se o usuário perguntar sobre multas: as sanções estão no art. 52 (de advertência a multa de até 2% do faturamento, limitada a R$ 50 milhões por infração) e a dosimetria na Res. CD/ANPD nº 4/2023, que considera, entre outros fatores, a adoção de boas práticas e a correção da infração. Não estime valores.
