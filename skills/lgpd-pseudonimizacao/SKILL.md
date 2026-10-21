---
name: lgpd-pseudonimizacao
description: Implementa a separação entre dados de identificação e dados sensíveis ligados por pseudônimo, como define o art. 13, § 4º da LGPD - pseudônimo com HMAC ou token aleatório, chave ou tabela de correspondência fora do banco, sem IDs sequenciais nem timestamps que liguem as partes, credenciais de banco distintas. Inclui script que mostra a reversão de hash de CPF sem chave. Use para "pseudonimizar", "separar dados sensíveis", "hash de CPF é seguro?", "tokenizar", ou quando a auditoria apontar falha em RF-23, RNF-06, RNF-10, RNF-11 ou RNF-12.
---

# lgpd-pseudonimizacao

Pseudonimização é o tratamento pelo qual o dado perde a possibilidade de associação direta a uma pessoa, **senão pelo uso de informação adicional mantida separadamente** em ambiente controlado e seguro (art. 13, § 4º). Dado pseudonimizado **continua sendo dado pessoal**; o ganho é que um vazamento de uma das partes, sozinha, não expõe quem é quem.

Requisitos atendidos: RF-23, RNF-06, RNF-10, RNF-11 e RNF-12.

## Modelo

```
 base de identificação            base de dados sensíveis
 ┌──────────────────────┐         ┌──────────────────────────┐
 │ titular              │         │ registro_sensivel        │
 │  id (uuid v4)        │         │  id (uuid v4, outro)     │
 │  nome, cpf, contato  │         │  pseudonimo  ◄───┐       │
 │  ref_aleatoria ──────┼──┐      │  diagnostico      │       │
 └──────────────────────┘  │      │  data (sem hora)  │       │
                           │      └───────────────────┼───────┘
                           └──► HMAC(chave, ref) ─────┘
                                 chave no cofre de segredos
```

- A ligação é `pseudonimo = HMAC-SHA256(chave, ref_aleatoria)`. Sem a chave, não se calcula o pseudônimo a partir da identificação.
- Use uma **referência aleatória** do titular como entrada, não o CPF: assim, nem quem tem a chave e uma lista de CPFs consegue ligar sem acesso à base de identificação.
- Alternativa: **token aleatório** + tabela de correspondência guardada fora das bases da aplicação.

## Opções comparadas

| Método | Revertível por quem tem só a base sensível? | Observação |
|---|---|---|
| `sha256(cpf)` sem chave | **Sim** | Cerca de 10⁹ CPFs possíveis: percorrer todos leva minutos num computador comum e segundos numa GPU. |
| `sha256(cpf + sal fixo no código)` | Sim, se o código vazar | O sal no repositório é público para quem tem o código. |
| HMAC com chave fora do banco | Não, sem a chave | Recomendado. Proteja e controle o acesso à chave. |
| Token aleatório + tabela de correspondência | Não, sem a tabela | A tabela precisa ficar fora das bases da aplicação. |
| Criptografia reversível (AES) do CPF | Não, sem a chave | Útil quando é preciso recuperar o CPF; trate a chave como a do HMAC. |

Mostre ao usuário com números: `python3 scripts/estimar_reversao.py --demo 20`.

## Armadilhas de ligação (RNF-11)

- **ID sequencial compartilhado:** se o paciente 1532 e o registro 1532 nasceram juntos, a ordem liga as tabelas. Use UUID v4 ou token aleatório, diferentes em cada lado.
- **UUID v1 e v7** carregam data e hora de criação. Evite no lado sensível.
- **Timestamps coincidentes:** gravar identificação e dado sensível no mesmo milissegundo permite ligá-los. Guarde só a data, ou arredonde, quando a hora exata não for necessária.
- **Ordem física e logs:** inserções em lote na mesma ordem e logs que registram as duas inserções juntas também ligam.

## Acesso (RNF-06, RNF-12)

- Chave do HMAC em cofre de segredos (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, Vault) ou, no mínimo, variável de ambiente do servidor, **nunca** no banco nem no repositório.
- Papéis de banco distintos: o serviço que lê o dado sensível não lê a identificação, e vice-versa. Só o serviço que precisa juntar (por exemplo, a tela do profissional) tem acesso às duas partes e à chave.
- Registre na trilha cada vez que a ligação for feita.

## Implementação

Exemplos prontos em [`references/exemplos.md`](references/exemplos.md): TypeScript (Node), Python e SQL (PostgreSQL com RLS e papéis).

## Rotação de chave

Trocar a chave muda todos os pseudônimos. Planeje: gere a nova chave, recalcule os pseudônimos em lote dentro de uma transação, troque a chave em uso e descarte a antiga. Registre a rotação.

## Pausas

Mudar o esquema em produção exige migração de dados. Apresente o plano (tabelas novas, script de migração, rollback) e peça aprovação antes de executar.
