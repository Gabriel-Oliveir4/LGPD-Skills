-- Consentimento por finalidade, com histórico e versão do texto (PostgreSQL).
-- Requisitos: RF-02, RF-04, RF-05, RF-06, RF-08, RF-35.

create table finalidade (
  codigo                 text primary key,             -- ex.: 'marketing_email'
  descricao              text not null,
  base_legal             text not null,                -- ex.: 'consentimento (art. 7º, I)'
  depende_consentimento  boolean not null,
  trata_dado_sensivel    boolean not null default false,
  prazo_retencao         interval,                     -- RF-26 (ou evento de término em texto)
  criada_em              timestamptz not null default now()
);

create table texto_consentimento (
  id             uuid primary key default gen_random_uuid(),
  finalidade     text not null references finalidade(codigo),
  versao         int  not null,
  texto          text not null,
  vigente_desde  timestamptz not null default now(),
  unique (finalidade, versao)
);

create table evento_consentimento (
  id               uuid primary key default gen_random_uuid(),
  titular_id       uuid not null,                       -- ou pseudônimo, conforme o projeto
  finalidade       text not null references finalidade(codigo),
  texto_id         uuid not null references texto_consentimento(id),
  acao             text not null check (acao in ('concedeu', 'revogou')),
  registrado_por   text not null check (registrado_por in ('titular', 'responsavel_legal')),
  responsavel_id   uuid,                                -- RF-35: preenchido quando é criança
  canal            text not null,                       -- 'app', 'site', 'presencial'...
  ocorrido_em      timestamptz not null default now()
);
create index on evento_consentimento (titular_id, finalidade, ocorrido_em desc);

-- Eventos não são alterados nem apagados: o histórico é a prova (art. 8º, § 2º).
create or replace function bloquear_alteracao() returns trigger language plpgsql as $$
begin
  raise exception 'evento_consentimento é somente de inclusão';
end $$;
create trigger evento_consentimento_imutavel
  before update or delete on evento_consentimento
  for each row execute function bloquear_alteracao();

-- Situação atual por titular e finalidade.
create view consentimento_vigente as
select distinct on (titular_id, finalidade)
       titular_id, finalidade, acao, texto_id, ocorrido_em
from evento_consentimento
order by titular_id, finalidade, ocorrido_em desc;

-- RF-09: finalidade com dado sensível só com base legal do art. 11.
-- Ajuste a lista às bases usadas no projeto.
alter table finalidade add constraint base_legal_sensivel check (
  not trata_dado_sensivel or base_legal ilike any (array[
    '%art. 11, I%', '%art. 11, II%'
  ])
);
