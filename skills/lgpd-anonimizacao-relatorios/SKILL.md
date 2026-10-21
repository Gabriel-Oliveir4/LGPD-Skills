---
name: lgpd-anonimizacao-relatorios
description: Gera extrações e relatórios anonimizados com o risco de reidentificação medido, seguindo o esquema da ANPD - identifica identificadores diretos, quase-identificadores e atributo sensível conforme o nicho, compara configurações (sem tratamento, generalização, supressão, k-anonimato, l-diversidade), mede risco médio e máximo, grupos homogêneos e perda de utilidade, e registra técnica e risco por extração. Inclui script em Python sem dependências. Use para "anonimizar dados", "compartilhar base para pesquisa", "relatório sem identificar pacientes", "isso está anonimizado?", "k-anonimato", "dados para BI".
---

# lgpd-anonimizacao-relatorios

Para a LGPD, dado anonimizado não é dado pessoal, **salvo** quando a anonimização pode ser revertida com esforços razoáveis, considerando custo e tempo (art. 12). Por isso "tiramos o nome e o CPF" não basta: a combinação de idade, sexo, bairro e data muitas vezes ainda aponta uma única pessoa. Esta skill trata a anonimização como **risco medido**, não como promessa.

Atende os requisitos RF-24, RNF-07, RF-25, RNF-09 e RNF-08 do catálogo (`lgpd-requisitos`).

## Conceitos (explique ao usuário quando preciso)

- **Identificador direto:** aponta a pessoa sozinho (nome, CPF, e-mail, telefone, prontuário). Sempre sai.
- **Quase-identificador:** sozinho não identifica, mas combinado com outros sim (idade, sexo, bairro, CEP, datas, profissão). A lista típica de cada nicho está em `lgpd-descoberta/references/nichos.md`.
- **Atributo sensível:** o que se quer proteger (diagnóstico, resultado de exame, renda).
- **Grupo:** registros com a mesma combinação de quase-identificadores.
- **k-anonimato:** cada grupo tem pelo menos *k* registros. A letra vem da literatura; não tem significado especial.
- **l-diversidade:** cada grupo tem pelo menos *l* valores distintos do atributo sensível. Sem ela, um grupo em que todos têm o mesmo diagnóstico revela o diagnóstico de qualquer pessoa que se saiba estar ali.
- **Riscos da ANPD (estudo preliminar, 2023):** distinção (isolar um registro), ligação (cruzar com outra base) e inferência (deduzir um atributo).
- **Perfis de atacante (estudo técnico da ANPD, 2023):** **promotor**, que conhece uma pessoa específica e procura o registro dela; **jornalista**, sem alvo, que quer reidentificar qualquer um para mostrar que a base não estava protegida.

## Roteiro

### 1. Finalidade e destinatário
Pergunte: para que serve a extração e quem vai recebê-la (equipe interna de BI, pesquisador, órgão público, publicação aberta). Quanto mais aberto o destino, menor o risco aceitável. A finalidade define o que **não** pode ser generalizado (se o relatório é por região, a região precisa ficar).

### 2. Classificação das colunas
Use `.lgpd/inventario-dados.md` e o nicho. Monte a tabela e confirme com o usuário:

| Coluna | Classe | Tratamento proposto |
|---|---|---|
| nome, cpf | Identificador direto | Remover |
| idade | Quase-identificador | Faixas de 10 anos |
| bairro | Quase-identificador | Agrupar em região |
| data_diag | Quase-identificador | Trimestre |
| resultado | Atributo sensível | Manter; verificar l |

Atenção a texto livre (observações, anotações): remova ou revise, porque costuma conter nomes e detalhes.

### 3. Risco aceitável
O controlador define o limite. A ANPD **não fixa** um valor; no estudo de casos que acompanha o estudo preliminar, usa 0,35 como exemplo. Para dado sensível ou divulgação pública, sugira um limite mais baixo e registre a decisão e quem a tomou em `.lgpd/STATUS.md`. Olhe sempre o **risco máximo** junto com o médio: o médio pode ficar baixo com alguns registros ainda únicos.

### 4. Medir e comparar

```bash
python3 scripts/anonimizar.py medir dados.csv --qi idade,sexo,bairro,data_diag --sensivel resultado

python3 scripts/anonimizar.py comparar dados.csv \
  --qi idade,sexo,bairro,data_diag --sensivel resultado --remover nome,cpf \
  --faixa idade=10 --data data_diag=trimestre --mapa bairro=regioes.csv \
  --k 2,5,10 --l 2 --estatistica bairro --risco-aceitavel 0.2
```

| Config. | Tratamento |
|---|---|
| C0 | Sem tratamento |
| C1 | Generalização |
| C2 | Supressão dos registros únicos |
| C3 | Generalização + supressão dos grupos com menos de k |
| C4 | C3 + supressão dos grupos com menos de l valores sensíveis |

Outras regras: `--truncar cep=5` mantém os 5 primeiros dígitos; `--data coluna=mes|trimestre|semestre|ano`.

Sem dados reais à mão? `python3 scripts/gerar_exemplo.py --n 2000 --semente 1` cria uma base fictícia de clínica. Para comparar métodos com rigor, gere várias versões (sementes diferentes) e reporte média e desvio padrão.

### 5. Escolher
Entre as configurações com risco abaixo do aceitável **e** sem grupos homogêneos, escolha a de **menor perda de utilidade** (menos suprimidos, menor distorção). Mostre ao usuário a tabela e, se ajudar, um gráfico de risco × utilidade (cada configuração é um ponto; mapa R-U de Duncan, Keller e Stokes, 2001).

### 6. Aplicar e registrar

```bash
python3 scripts/anonimizar.py aplicar dados.csv --qi ... --sensivel resultado --remover nome,cpf \
  --faixa idade=10 --data data_diag=trimestre --mapa bairro=regioes.csv --k 5 --l 2
```

Saída em `.lgpd/anonimizacao/`: o CSV anonimizado e o relatório com técnica, parâmetros e risco medido (RF-25). Peça aprovação antes de liberar a extração.

### 7. Implementar no sistema (quando o usuário quiser)
Leve a mesma lógica para o código: rotina que gera o relatório, mede k, l e risco antes de liberar, bloqueia quando o limite não é atendido e grava o registro da extração (técnica, parâmetros, risco, data, finalidade, destinatário). Exemplo de tabela:

```sql
create table extracao_anonimizada (
  id uuid primary key default gen_random_uuid(),
  finalidade text not null,
  destinatario text not null,
  tecnica jsonb not null,          -- regras de generalização, k, l
  risco_medio numeric not null,
  risco_maximo numeric not null,
  suprimidos_pct numeric not null,
  risco_aceitavel numeric not null,
  aprovado_por text not null,
  criado_em timestamptz not null default now()
);
```

## Limites que o usuário precisa saber

- A medição cobre os quase-identificadores informados. Se o atacante souber outra coisa, o risco muda.
- Agregados pequenos também identificam: uma célula com contagem 1 ou 2 num relatório já é um grupo pequeno. Suprima ou agrupe células abaixo de k.
- Anonimizar não é para sempre: novas bases públicas podem permitir ligações que antes não eram possíveis. Reavalie quando o contexto mudar.
- Pseudonimizar (trocar nome por código) **não** é anonimizar: o dado continua pessoal. Para isso, use `lgpd-pseudonimizacao`.

## Referências

- ANPD. Estudo técnico sobre anonimização de dados na LGPD (2023).
- ANPD. Estudo preliminar sobre anonimização e pseudonimização para proteção de dados (2023).
- Grupo de Trabalho do Artigo 29. Parecer 05/2014 sobre técnicas de anonimização (WP216).
- Duncan, Keller-McNulty e Stokes. Disclosure risk vs. data utility: the R-U confidentiality map. NISS, Technical Report 121 (2001).
