-- Trilha de auditoria somente de inclusão, encadeada por hash (PostgreSQL 13+).
-- Requisitos: RF-31, RNF-18, RNF-19, RF-32, RF-33.

create extension if not exists pgcrypto;

create table trilha (
  seq         bigint generated always as identity primary key,  -- ordem da cadeia (só na trilha)
  quando      timestamptz not null default now(),
  autor       text not null,
  papel       text not null,
  operacao    text not null check (operacao in
                ('leitura','criacao','alteracao','eliminacao','exportacao','compartilhamento')),
  recurso     text not null,
  registro    text,
  titular     text,              -- pseudônimo; nunca nome, CPF ou dado sensível (RNF-18)
  finalidade  text not null,
  origem      text,
  hash_ant    text not null,
  hash        text not null
);
create index on trilha (autor, quando);
create index on trilha (titular, quando);

-- Calcula o encadeamento na inclusão.
create or replace function trilha_encadear() returns trigger language plpgsql as $$
declare ant text;
begin
  perform pg_advisory_xact_lock(hashtext('trilha'));      -- uma inclusão por vez na cadeia
  select hash into ant from trilha order by seq desc limit 1;
  new.hash_ant := coalesce(ant, repeat('0', 64));
  new.hash := encode(digest(
      new.hash_ant || '|' || to_char(new.quando at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US') || '|' || new.autor || '|' || new.papel || '|' ||
      new.operacao || '|' || new.recurso || '|' || coalesce(new.registro, '') || '|' ||
      coalesce(new.titular, '') || '|' || new.finalidade || '|' || coalesce(new.origem, ''),
      'sha256'), 'hex');
  return new;
end $$;

create trigger trilha_encadear before insert on trilha
  for each row execute function trilha_encadear();

-- Bloqueia alteração e exclusão (RNF-19).
create or replace function trilha_imutavel() returns trigger language plpgsql as $$
begin
  raise exception 'trilha de auditoria é somente de inclusão';
end $$;

create trigger trilha_imutavel before update or delete on trilha
  for each row execute function trilha_imutavel();
create trigger trilha_sem_truncate before truncate on trilha
  for each statement execute function trilha_imutavel();

-- Verificação: devolve as linhas em que a cadeia quebra.
create or replace function trilha_verificar()
returns table (seq bigint, problema text) language sql as $$
  with t as (
    select *, lag(hash) over (order by seq) as hash_anterior_real from trilha
  )
  select seq, case
    when hash_ant <> coalesce(hash_anterior_real, repeat('0', 64)) then 'hash_ant não confere'
    else 'conteúdo alterado' end
  from t
  where hash_ant <> coalesce(hash_anterior_real, repeat('0', 64))
     or hash <> encode(digest(
          hash_ant || '|' || to_char(quando at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US') || '|' || autor || '|' || papel || '|' ||
          operacao || '|' || recurso || '|' || coalesce(registro, '') || '|' ||
          coalesce(titular, '') || '|' || finalidade || '|' || coalesce(origem, ''),
          'sha256'), 'hex');
$$;

-- Papel da aplicação: só inclui e consulta.
-- create role app_trilha nologin;
-- grant insert, select on trilha to app_trilha;
-- revoke update, delete, truncate on trilha from app_trilha;
