---
name: lgpd-consentimento
description: Implementa consentimento conforme a LGPD - uma opção por finalidade, desmarcada por padrão, com recusa visível, registro com data, hora e versão do texto, revogação tão fácil quanto consentir, verificação do consentimento vigente antes de usar a finalidade e aviso quando a finalidade mudar; inclui banner de cookies no padrão do guia da ANPD e consentimento do responsável para crianças. Use para "tela de consentimento", "banner de cookies", "opt-in", "aceite dos termos", "revogar consentimento", ou quando a auditoria apontar falha em RF-02 a RF-07, RNF-01 ou RF-35.
---

# lgpd-consentimento

Consentimento é a manifestação livre, informada e inequívoca pela qual o titular concorda com o tratamento para uma **finalidade determinada** (art. 5º, XII). Antes de implementar, confirme com o usuário que o consentimento é mesmo a base legal certa: muitos tratamentos se apoiam em outra base (execução de contrato, obrigação legal, tutela da saúde). Pedir consentimento para o que não depende dele confunde o titular e cria um direito de revogação que o sistema não poderá honrar.

Requisitos: RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RNF-01 e, para crianças, RF-35.

## Regras

1. **Uma opção por finalidade** (art. 8º, § 4º: autorizações genéricas são nulas). Nada de "Li e aceito os termos, a política e o recebimento de ofertas" num único checkbox.
2. **Desmarcado por padrão** (RNF-01).
3. **Recusar é possível e visível**, com as consequências explicadas (art. 18, VIII).
4. **Prova** é do controlador (art. 8º, § 2º): registre quem, quando, qual finalidade, qual ação e **qual versão do texto** foi mostrada.
5. **Revogar** a qualquer momento, sem custo, por procedimento facilitado (art. 8º, § 5º).
6. **Depois da revogação, parar**: toda rotina que usa a finalidade consulta o consentimento vigente antes de agir (RF-06).
7. **Mudou a finalidade?** Avise o titular com destaque antes; se a mudança não for compatível, peça novo consentimento (art. 8º, § 6º; art. 9º, § 2º).
8. **Crianças:** quando a base for o consentimento, ele vem de pai, mãe ou responsável legal, com esforço razoável para verificar (art. 14, §§ 1º e 5º).

## Modelo de dados

O esquema completo está em [`assets/consentimento.sql`](assets/consentimento.sql). Ideia central: o consentimento é um **histórico de eventos** (concedeu, revogou), não um booleano que se sobrescreve.

- `finalidade`: código, descrição, base legal, se depende de consentimento.
- `texto_consentimento`: versão do texto por finalidade, com data de vigência.
- `evento_consentimento`: titular, finalidade, versão do texto, ação, data e hora, canal, quem registrou (titular ou responsável).
- *View* `consentimento_vigente`: último evento por titular e finalidade.

## API mínima

| Método | Rota | O que faz |
|---|---|---|
| GET | `/consentimentos` | Finalidades, texto vigente e situação do titular logado. |
| POST | `/consentimentos/{finalidade}` | Registra `concedeu` ou `revogou` com a versão do texto exibida. |
| GET | `/consentimentos/historico` | Histórico do titular (útil para a declaração do art. 19). |

Verificação antes de usar a finalidade:

```ts
export async function temConsentimento(titularId: string, finalidade: string) {
  const r = await db.query(
    `select acao from consentimento_vigente where titular_id = $1 and finalidade = $2`,
    [titularId, finalidade]);
  return r.rows[0]?.acao === "concedeu";
}

// Antes de enviar a newsletter, por exemplo:
if (!(await temConsentimento(t.id, "marketing_email"))) return;
```

## Interface

- Lista de finalidades, cada uma com texto curto, *toggle* desmarcado e link para detalhes.
- Botões "Aceitar" e "Recusar" com o mesmo destaque.
- Tela de preferências acessível a qualquer momento (menu da conta), onde revogar é um clique.
- Linguagem simples (RNF-20).

## Cookies

Siga o **Guia orientativo da ANPD sobre cookies e proteção de dados pessoais** (2022) quando a base for o consentimento:

- cookies não necessários desativados por padrão; nenhum script de analytics ou publicidade carrega antes da escolha;
- primeiro nível do banner com "Aceitar", "Rejeitar" e "Gerenciar", sem dar mais destaque ao aceite;
- segundo nível com categorias (necessários, desempenho, funcionalidade, publicidade) e finalidades descritas de forma simples;
- forma fácil de mudar a escolha depois (link no rodapé).

Registre a escolha de cookies como evento de consentimento, com a versão do banner.

## Saída

Antes de alterar código, mostre ao usuário o plano (tabelas, rotas, telas) e peça aprovação. Depois, atualize a matriz com os requisitos atendidos e a evidência.
