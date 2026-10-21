---
name: lgpd-documentos
description: Gera e revisa documentos de adequação à LGPD a partir do que foi encontrado no projeto - aviso (política) de privacidade com os itens do art. 9º, registro das operações de tratamento (art. 37), relatório de impacto à proteção de dados (RIPD, art. 38), teste de legítimo interesse, termo de consentimento, cláusulas para contrato com operador e texto de banner de cookies. Usa o inventário e a descoberta como fonte, marca o que precisa ser preenchido pela organização e nunca publica sem revisão. Use para "política de privacidade", "termos de uso", "ROPA", "registro de tratamento", "RIPD", "DPIA", "LIA", "contrato com fornecedor".
---

# lgpd-documentos

Os documentos saem dos fatos levantados (`.lgpd/descoberta.md`, `.lgpd/inventario-dados.md`, matriz). Onde o código não responde (contato do encarregado, prazos de guarda decididos, contratos), deixe o campo marcado como **[A PREENCHER: …]** e liste essas pendências no fim. Um documento que descreve tratamento que o sistema não faz, ou omite o que ele faz, é pior do que nenhum.

Grave em `.lgpd/documentos/`. **Pare antes de publicar ou assinar:** todo documento passa pela revisão do encarregado e do jurídico.

## Qual documento

| Documento | Quando | Base | Modelo |
|---|---|---|---|
| Aviso de privacidade | Sempre que houver titular usando o sistema | Art. 9º; art. 41, § 1º | [`aviso-privacidade.md`](assets/modelos/aviso-privacidade.md) |
| Registro das operações | Sempre (controlador e operador) | Art. 37 | [`registro-operacoes.md`](assets/modelos/registro-operacoes.md) |
| RIPD | Quando exigido pela ANPD; recomendado para dado sensível em escala ou tecnologia nova | Arts. 5º, XVII; 38; 10, § 3º | [`ripd.md`](assets/modelos/ripd.md) |
| Teste de legítimo interesse | Quando a base legal for o legítimo interesse | Arts. 7º, IX; 10 | [`legitimo-interesse.md`](assets/modelos/legitimo-interesse.md) |
| Termo de consentimento | Quando a base for o consentimento | Art. 8º | [`termo-consentimento.md`](assets/modelos/termo-consentimento.md) |
| Cláusulas com operador | Para cada fornecedor que trata dados em nome da organização | Arts. 39; 42; 46 | [`clausulas-operador.md`](assets/modelos/clausulas-operador.md) |

O texto do banner de cookies está na skill `lgpd-consentimento`.

## Como preencher

1. **Liste as finalidades** a partir do código (rotas, *jobs*, integrações). Para cada uma: dados usados, base legal, prazo, compartilhamentos.
2. **Confirme a base legal com o usuário.** O kit sugere, a organização decide. Para dado sensível, só as bases do art. 11.
3. **Compartilhamentos:** use a lista de terceiros que `lgpd-backend` e `lgpd-infra` encontraram. Inclua país quando houver transferência internacional.
4. **Linguagem:** o aviso de privacidade é para o titular, em linguagem simples (RNF-20). O registro e o RIPD são para a organização e a ANPD, e podem ser técnicos.
5. **Pequeno porte:** se a organização se enquadrar na Res. CD/ANPD nº 2/2022, o registro pode ser simplificado. A ANPD disponibilizou um modelo de registro simplificado em 2023, com contato da entidade, categorias de titulares, tipos de dados, compartilhamentos, medidas de segurança, tempo de armazenamento, processo, finalidade e base legal.
6. **Coerência:** o que o aviso promete precisa existir no sistema. Se o aviso diz que o titular pode exportar os dados, a rota de exportação precisa existir (RF-20). Aponte as divergências.

## Revisão de documento existente

Compare o documento com o que o sistema faz. Para cada divergência, registre: trecho do documento, o que o código mostra (arquivo e linha) e sugestão de correção. Verifique também os itens obrigatórios do art. 9º e o contato do encarregado.

## Fontes

- Lei nº 13.709/2018 (texto compilado no Planalto).
- ANPD. Guia orientativo de hipóteses legais: legítimo interesse (2024).
- ANPD. Guia orientativo sobre cookies e proteção de dados pessoais (2022).
- ANPD. Modelo de registro simplificado para agentes de tratamento de pequeno porte (2023).
