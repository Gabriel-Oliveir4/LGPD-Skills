---
name: lgpd-requisitos
description: Catálogo de 55 requisitos de software derivados da LGPD (Lei 13.709/2018), com artigo de origem, camada (banco, back-end, front-end, infra) e o que verificar no código, mais 9 obrigações organizacionais e a referência normativa (LGPD e resoluções da ANPD). Use para checar um projeto contra a LGPD requisito por requisito, montar a matriz de rastreabilidade artigo → requisito → código, ou responder "que requisitos de software a LGPD exige?". Também é a base consultada pelas outras skills do lgpd-kit.
---

# Requisitos de software da LGPD

Esta skill é o **catálogo central** do lgpd-kit. Ela traduz a LGPD em requisitos de software verificáveis e diz onde procurar cada um no projeto. As skills de camada (banco, back-end, front-end, infra) consultam este catálogo, e o resultado final da auditoria é a **matriz de rastreabilidade**.

## Arquivos de referência

| Arquivo | Conteúdo | Quando ler |
|---|---|---|
| [`references/catalogo-requisitos.md`](references/catalogo-requisitos.md) | 55 requisitos em 11 famílias: texto, artigo, tipo, camadas e o que verificar. | Sempre que for verificar requisitos. |
| [`references/obrigacoes-organizacionais.md`](references/obrigacoes-organizacionais.md) | 9 obrigações que dependem da organização e o recurso do sistema que apoia cada uma. | Na parte organizacional da auditoria. |
| [`references/referencia-normativa.md`](references/referencia-normativa.md) | Artigos-chave da LGPD, resoluções da ANPD vigentes e normas setoriais a sinalizar. | Ao citar uma norma ou explicar a origem de um requisito. |

## Como usar

1. **Filtre pelo contexto.** Leia `.lgpd/descoberta.md`, se existir, para saber as camadas presentes, o nicho e se há dado sensível ou de crianças. Requisitos de tratamento que o projeto não faz recebem ➖ *Não se aplica*, sempre com a justificativa.
2. **Adapte ao nicho.** Os requisitos usam saúde como exemplo de dado sensível. Troque pelo dado sensível do nicho (biometria, origem racial, convicção religiosa, vida sexual etc.), mantendo o artigo de origem.
3. **Procure evidência, não intenção.** Para cada requisito, siga a coluna "O que verificar" e registre arquivo e linha. Se a regra só existe na interface, o status é 🟡 *Parcial*: a verificação precisa estar no servidor ou no banco.
4. **Registre na matriz.** Escreva em `.lgpd/matriz-rastreabilidade.md` no formato abaixo.
5. **Separe o que é organizacional.** As obrigações do arquivo de obrigações recebem 🏢 e vão para a parte organizacional do relatório.

## Formato da matriz de rastreabilidade

```markdown
| ID | Requisito (resumo) | Origem | Camada | Status | Evidência | Ação recomendada |
|---|---|---|---|---|---|---|
| RF-04 | Registrar consentimento com versão do texto | Art. 8º, § 2º | BE, BD | 🟡 Parcial | prisma/schema.prisma:42 (falta versão do texto) | Adicionar coluna `versao_texto` e gravá-la no aceite |
```

Ao final, inclua um resumo por família e por camada (quantos ✅, 🟡, ❌, ➖, 🏢).

## Regras

- **Não invente artigos.** Use apenas as origens do catálogo e da referência normativa. Se um ponto não estiver coberto, diga que não está e sugira consulta ao texto oficial.
- **Requisitos com asterisco (\*)** são decisões de projeto. Aceite uma solução diferente quando ela atender ao mesmo objetivo, desde que a justificativa fique registrada.
- **Não afirme conformidade jurídica.** A matriz mostra se o software atende aos requisitos; a conformidade com a LGPD depende também da organização. Sempre que o usuário perguntar "estamos em conformidade?", lembre que a avaliação jurídica cabe ao encarregado ou a um advogado.
- **Datas da norma.** A referência normativa foi conferida em outubro de 2026. Se o usuário citar uma norma mais recente, peça a fonte e não a contradiga sem verificar.
