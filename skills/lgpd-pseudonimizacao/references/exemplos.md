# Exemplos de pseudonimização

Adapte nomes de tabelas e colunas ao projeto. Os exemplos usam dados fictícios.

## TypeScript (Node.js)

```ts
// lib/pseudonimo.ts
import { createHmac, randomBytes, timingSafeEqual } from "node:crypto";

const CHAVE = process.env.PSEUDONIMO_CHAVE; // 32+ bytes em base64, vindo do cofre de segredos
if (!CHAVE) throw new Error("PSEUDONIMO_CHAVE não configurada");
const chave = Buffer.from(CHAVE, "base64");

/** Referência aleatória do titular, gravada só na base de identificação. */
export function novaReferencia(): string {
  return randomBytes(16).toString("hex");
}

/** Pseudônimo usado na base de dados sensíveis. Sem a chave, não é recalculável. */
export function pseudonimo(referencia: string): string {
  return createHmac("sha256", chave).update(referencia).digest("hex");
}

export function mesmoPseudonimo(a: string, b: string): boolean {
  const x = Buffer.from(a, "hex"), y = Buffer.from(b, "hex");
  return x.length === y.length && timingSafeEqual(x, y);
}
```

Uso ao cadastrar:

```ts
const ref = novaReferencia();
await dbIdentificacao.titular.create({ data: { nome, cpf, ref } });
await dbSensivel.registro.create({
  data: { pseudonimo: pseudonimo(ref), diagnostico, data: hoje() /* sem hora */ },
});
```

Gerar a chave: `node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"`.

## Python

```python
import hmac, hashlib, os, secrets, base64

_CHAVE = base64.b64decode(os.environ["PSEUDONIMO_CHAVE"])

def nova_referencia() -> str:
    return secrets.token_hex(16)

def pseudonimo(referencia: str) -> str:
    return hmac.new(_CHAVE, referencia.encode(), hashlib.sha256).hexdigest()
```

## PostgreSQL — esquemas, papéis e RLS

```sql
-- Dois esquemas (ou dois bancos) e dois papéis
create schema identificacao;
create schema sensivel;

create role app_recepcao  nologin;   -- lê identificação
create role app_clinico   nologin;   -- lê sensível (e identificação, para a ficha)
create role app_relatorio nologin;   -- lê só sensível, para relatórios anonimizados

create table identificacao.titular (
  id   uuid primary key default gen_random_uuid(),   -- v4
  ref  text not null unique,                          -- referência aleatória
  nome text not null,
  cpf  text not null unique
);

create table sensivel.registro (
  id          uuid primary key default gen_random_uuid(),  -- outro v4, sem relação com titular.id
  pseudonimo  text not null,
  diagnostico text not null,
  data        date not null                                 -- só a data
);
create index on sensivel.registro (pseudonimo);

revoke all on schema identificacao, sensivel from public;
grant usage on schema identificacao to app_recepcao, app_clinico;
grant select, insert, update on identificacao.titular to app_recepcao;
grant select on identificacao.titular to app_clinico;
grant usage on schema sensivel to app_clinico, app_relatorio;
grant select, insert, update on sensivel.registro to app_clinico;
grant select on sensivel.registro to app_relatorio;
```

Com Supabase, aplique RLS nas tabelas expostas pela API e nunca use a `service_role` key no cliente:

```sql
alter table sensivel.registro enable row level security;
create policy clinico_le on sensivel.registro
  for select using (auth.jwt() ->> 'papel' = 'profissional');
```

## Verificação rápida

```bash
# Nenhum hash simples de CPF/e-mail como pseudônimo
grep -rnE "(sha256|md5|sha1).*\b(cpf|email|telefone)\b" --include=*.{ts,js,py,sql} .
# Nenhuma chave de pseudônimo no repositório
git grep -nE "PSEUDONIMO_CHAVE\s*=\s*\S+" -- ':!*.example'
```
