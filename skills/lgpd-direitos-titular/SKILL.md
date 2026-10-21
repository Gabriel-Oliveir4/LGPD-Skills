---
name: lgpd-direitos-titular
description: Implementa o atendimento aos direitos do titular da LGPD (arts. 18 a 22) - canal de requisições, verificação de identidade, confirmação e acesso simplificado imediato, declaração completa em até 15 dias, correção, anonimização, bloqueio, eliminação, portabilidade em formato estruturado, informação sobre compartilhamentos, revogação, revisão de decisão automatizada, aviso aos destinatários e registro de cada pedido e resposta. Use para "portal do titular", "pedido de exclusão de dados", "exportar meus dados", "DSAR", "direito de acesso", ou quando a auditoria apontar falha em RF-15 a RF-22, RNF-04 ou RNF-05.
---

# lgpd-direitos-titular

Requisitos: RF-15 a RF-22, RNF-04 e RNF-05. O atendimento é gratuito (art. 18, § 5º) e os dados gerados pelo exercício de direitos não podem ser usados contra o titular (art. 21).

## Direitos e como o sistema atende

| Direito (art. 18) | Resposta do sistema | Prazo ou regra |
|---|---|---|
| I — confirmação da existência de tratamento | Sim/não e resumo | Formato simplificado: imediato (art. 19, I) |
| II — acesso aos dados | Dados do titular em tela ou arquivo | Simplificado imediato; declaração completa com origem, critérios e finalidade em até **15 dias** (art. 19, II) |
| III — correção | Edição com registro do valor anterior | Avisar destinatários (art. 18, § 6º) |
| IV — anonimização, bloqueio ou eliminação de dados desnecessários, excessivos ou tratados em desconformidade | Rotina por titular | Avisar destinatários |
| V — portabilidade | Exportação estruturada (JSON, CSV) | Conforme regulamentação da ANPD; não inclui dados já anonimizados (art. 18, § 7º) |
| VI — eliminação dos dados tratados com consentimento | Rotina por titular | Exceto hipóteses de conservação do art. 16 |
| VII — informação sobre compartilhamento | Lista de entidades que receberam os dados | Vem do registro de compartilhamentos |
| VIII — informação sobre a possibilidade de não consentir | Texto na tela de consentimento | Ver `lgpd-consentimento` |
| IX — revogação do consentimento | Ver `lgpd-consentimento` | A qualquer momento |
| Art. 20 — revisão de decisão automatizada | Pedido de revisão e informação sobre os critérios | Respeitado o segredo comercial e industrial |

Quando não for possível atender de imediato, o controlador responde informando que não é agente de tratamento (indicando, se possível, quem é) ou as razões de fato ou de direito que impedem a adoção imediata (art. 18, § 4º). Registre a justificativa (RF-22).

A ANPD tem a regulamentação dos direitos dos titulares na agenda regulatória. Confira se já foi publicada e se mudou prazos ou formatos antes de fechar a implementação.

## Fluxo

1. **Recebimento (RF-15):** tela no app, formulário público ou e-mail do encarregado. Aceite pedido de representante legal.
2. **Identidade:** confirme que quem pede é o titular, sem pedir mais dados do que o necessário (login já autenticado, código por e-mail ou telefone já cadastrados). Nunca entregue dados a quem só informou um CPF.
3. **Registro (RF-22):** grave o pedido com tipo, data, prazo e status.
4. **Execução:** rotina específica por tipo de pedido.
5. **Resposta:** registre o que foi respondido, quando e, se for o caso, a justificativa.
6. **Destinatários (RF-21):** depois de correção, eliminação, anonimização ou bloqueio, avise quem recebeu os dados.

## Modelo de dados

```sql
create table requisicao_titular (
  id             uuid primary key default gen_random_uuid(),
  titular_id     uuid not null,
  representante  text,                                  -- nome e vínculo, se houver
  tipo           text not null check (tipo in (
                   'confirmacao','acesso','declaracao_completa','correcao','anonimizacao',
                   'bloqueio','eliminacao','portabilidade','compartilhamentos',
                   'revogacao','revisao_decisao_automatizada')),
  detalhes       text,
  recebida_em    timestamptz not null default now(),
  prazo          timestamptz,                           -- ex.: recebida_em + 15 dias (declaração)
  status         text not null default 'aberta'
                   check (status in ('aberta','em_andamento','atendida','negada','parcial')),
  resposta       text,
  justificativa  text,                                  -- art. 18, § 4º
  respondida_em  timestamptz
);

create table compartilhamento (
  id            uuid primary key default gen_random_uuid(),
  titular_id    uuid not null,
  destinatario  text not null,                          -- operador ou terceiro
  finalidade    text not null,
  dados         text not null,                          -- categorias enviadas
  enviado_em    timestamptz not null default now()
);
```

## Exportação (RF-16, RF-20, RNF-05)

Monte a exportação a partir do inventário (`.lgpd/inventario-dados.md`): para cada tabela com dado pessoal, a consulta que traz os registros do titular. Se alguma tabela não tiver caminho até o titular, isso é falha de RNF-05.

```ts
export async function exportarDados(titularId: string) {
  return {
    geradoEm: new Date().toISOString(),
    titular: await db.titular.findUnique({ where: { id: titularId },
      select: { nome: true, email: true, telefone: true, criadoEm: true } }),
    consentimentos: await historicoConsentimento(titularId),
    compartilhamentos: await db.compartilhamento.findMany({ where: { titularId } }),
    // ...demais tabelas do inventário
  };
}
```

## Eliminação (RF-18, RF-27, RF-28)

- Verifique antes se há hipótese de conservação (art. 16): obrigação legal ou regulatória (por exemplo, prazos de guarda de prontuário ou fiscais), estudo por órgão de pesquisa, transferência a terceiro, uso exclusivo do controlador com dados anonimizados.
- Quando houver obrigação de guardar, **bloqueie** em vez de eliminar e explique ao titular.
- Elimine também de caches, índices de busca e serviços terceiros; para backups, registre quando a cópia expira.
- Registre cada eliminação (RF-28), sem guardar o dado eliminado.

## Prazos (RNF-04)

Crie um *job* diário que liste pedidos perto do prazo e avise o encarregado. Mostre no painel interno: abertas, vencendo em 3 dias, vencidas.

## Saída

Apresente o plano (tabelas, rotas, telas, *jobs*) e peça aprovação antes de alterar código. Atualize a matriz com os requisitos atendidos.
