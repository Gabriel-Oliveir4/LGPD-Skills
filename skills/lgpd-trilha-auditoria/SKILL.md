---
name: lgpd-trilha-auditoria
description: Implementa trilha de auditoria para a LGPD - registro de cada operação de tratamento com autor, data e hora, operação, registro afetado e finalidade; titular identificado por pseudônimo, sem nome nem dado sensível; proteção contra alteração e exclusão com tabela somente de inclusão e encadeamento por hash; relatório das operações para prestação de contas; e consulta por conta ou período para levantar afetados em incidente. Use para "log de auditoria", "registro de acessos", "quem acessou o dado", "trilha imutável", ou quando a auditoria apontar falha em RF-31, RNF-18, RNF-19, RF-32 ou RF-33.
---

# lgpd-trilha-auditoria

A LGPD exige que controlador e operador mantenham registro das operações de tratamento (art. 37) e possam demonstrar a adoção de medidas eficazes (art. 6º, X). Na prática, a trilha responde três perguntas: **quem fez o quê com qual dado, quando e para quê**; **a trilha foi adulterada?**; e, num incidente, **o que essa conta acessou?**

Requisitos: RF-31, RNF-18, RNF-19, RF-32 e RF-33.

## O que registrar (RF-31)

| Campo | Exemplo |
|---|---|
| autor | ID do usuário e papel (`u_8f2…`, `profissional`) |
| quando | `2026-10-21T14:03:11Z` |
| operação | `leitura`, `criacao`, `alteracao`, `eliminacao`, `exportacao`, `compartilhamento` |
| recurso | tabela ou entidade (`ficha_clinica`) |
| registro | ID do registro afetado |
| titular | **pseudônimo**, nunca nome ou CPF (RNF-18) |
| finalidade | código da finalidade (`atendimento`) |
| origem | IP ou dispositivo, quando necessário |

**Não** registre o conteúdo do dado (o diagnóstico, o valor anterior de um campo sensível). Se precisar do valor anterior para correções (RF-14), guarde-o na tabela de histórico do próprio dado, com o mesmo controle de acesso, e não na trilha.

## Proteção (RNF-19)

Três camadas, da mais simples à mais forte:

1. **Somente inclusão:** trigger que bloqueia `UPDATE` e `DELETE`; papel da aplicação só com `INSERT`.
2. **Encadeamento por hash:** cada linha guarda o hash da anterior. Alterar ou apagar uma linha quebra a cadeia, e a verificação mostra onde.
3. **Cópia externa:** envio periódico para armazenamento de objetos com bloqueio de alteração (por exemplo, S3 Object Lock) ou outro serviço só de inclusão.

O esquema com trigger, encadeamento e função de verificação está em [`assets/trilha.sql`](assets/trilha.sql).

## Onde registrar no código

Um único ponto de passagem evita esquecimentos: *middleware* da API, *hook* do ORM (Prisma `$extends`, TypeORM *subscribers*, *signals* do Django) ou camada de serviço. Leituras também contam: abrir uma ficha é operação de tratamento.

```ts
// exemplo com Prisma: registra leituras e escritas de modelos com dado pessoal
const MODELOS = new Set(["FichaClinica", "Titular"]);
export const comTrilha = (ctx: { usuario: string; papel: string; finalidade: string }) =>
  prisma.$extends({
    query: {
      $allModels: {
        async $allOperations({ model, operation, args, query }) {
          const r = await query(args);
          if (MODELOS.has(model)) {
            await registrarTrilha({ ...ctx, recurso: model, operacao: operation,
              registro: (r as any)?.id ?? null, titular: (r as any)?.pseudonimo ?? null });
          }
          return r;
        },
      },
    },
  });
```

## Consultas

- **Prestação de contas (RF-32):** operações por período, por finalidade, por papel.
- **Incidente (RF-33):** tudo o que uma conta acessou num intervalo; titulares afetados (pseudônimos distintos), recursos e quantidade.

```sql
select recurso, operacao, count(*) as operacoes, count(distinct titular) as titulares
from trilha
where autor = $1 and quando between $2 and $3
group by recurso, operacao;
```

## Prazo de guarda

A LGPD não fixa prazo para a trilha. Defina com o encarregado, registre a decisão e considere: prazo de prescrição de eventuais responsabilidades, o registro de incidentes por no mínimo 5 anos (Res. CD/ANPD nº 15/2024) e, para provedores de aplicação de internet, a guarda de registros de acesso por 6 meses (Marco Civil, art. 15). Trilhas grandes podem ser particionadas por mês e arquivadas em armazenamento mais barato, mantendo a verificação da cadeia.

## Saída

Mostre o plano e peça aprovação antes de criar tabelas ou *middlewares*. Atualize a matriz.
