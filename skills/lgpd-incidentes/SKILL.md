---
name: lgpd-incidentes
description: Roteiro de resposta a incidente de segurança com dados pessoais conforme o art. 48 da LGPD e a Resolução CD/ANPD nº 15/2024 - contenção, preservação de evidências, levantamento de dados e titulares afetados pela trilha de auditoria, avaliação de risco ou dano relevante, prazos de 3 dias úteis para ANPD e titulares, rascunhos de comunicação e registro do incidente por no mínimo 5 anos. Use quando o usuário disser "vazou", "fomos invadidos", "acesso indevido", "incidente", "ransomware", "dados expostos", "comunicar a ANPD", mesmo sem citar a LGPD.
---

# lgpd-incidentes

**Comece pela urgência.** Pergunte só o essencial e siga. O prazo de comunicação conta a partir do conhecimento de que o incidente afetou dados pessoais.

Este roteiro organiza o trabalho técnico e prepara rascunhos. A decisão de comunicar, o texto final e o envio são do controlador, com o encarregado e o jurídico. **Nunca envie comunicação à ANPD ou aos titulares em nome do usuário.**

## 1. Primeiras perguntas (no máximo cinco)

1. O que aconteceu e como foi descoberto? (data e hora do conhecimento)
2. O incidente ainda está em andamento?
3. Quais sistemas, bases ou contas estão envolvidos?
4. A organização é controladora ou operadora desses dados? (o operador avisa o controlador, que comunica)
5. O encarregado e o jurídico já sabem?

## 2. Conter e preservar (primeiras horas)

- Interrompa o acesso: revogue credenciais e *tokens* envolvidos, troque segredos expostos, feche o recurso público (bucket, porta, link).
- **Preserve evidências antes de limpar:** cópia dos logs, da trilha, das configurações e dos artefatos envolvidos, com data e hora. Não apague nada que mostre o que ocorreu.
- Registre cada ação tomada, com horário e responsável, desde já.

## 3. Levantar o que foi afetado

Use a trilha de auditoria (RF-33) e os logs:

```sql
-- O que a conta comprometida acessou no período
select recurso, operacao, count(*) as operacoes, count(distinct titular) as titulares
from trilha
where autor = :conta and quando between :inicio and :fim
group by recurso, operacao;
```

Responda, com números: quais **categorias de dados** (cadastrais, de autenticação, financeiros, sensíveis), **quantos titulares**, se há **crianças, adolescentes ou idosos**, e se os dados estavam **cifrados ou pseudonimizados** (e se a chave também foi exposta). Use o inventário (`.lgpd/inventario-dados.md`) para traduzir tabelas em categorias.

Se não houver trilha, diga isso claramente: a ausência dificulta o levantamento e deve entrar no plano de ação.

## 4. Avaliar se a comunicação é obrigatória

Pela Res. CD/ANPD nº 15/2024, o incidente deve ser comunicado quando puder acarretar risco ou dano relevante aos titulares: quando puder **afetar significativamente** interesses e direitos fundamentais **e** envolver, por exemplo, dados sensíveis; de crianças, adolescentes ou idosos; financeiros; de autenticação; protegidos por sigilo; ou em larga escala. Monte a avaliação com os fatos levantados e entregue ao encarregado. Na dúvida, recomende consultar o jurídico, não decida pelo usuário.

## 5. Prazos

| O quê | Prazo | Observação |
|---|---|---|
| Comunicação à ANPD | **3 dias úteis** | Contados do conhecimento de que o incidente afetou dados pessoais. |
| Comunicação aos titulares | **3 dias úteis** | Linguagem simples; individual quando possível. |
| Complementação à ANPD | até **20 dias úteis** | Informações que não estavam disponíveis na primeira comunicação. |
| Agente de pequeno porte | prazos em dobro | Se a organização se enquadrar na Res. CD/ANPD nº 2/2022. |
| Registro do incidente | **mínimo 5 anos** | Vale para todos os incidentes, comunicados ou não. |

Calcule as datas-limite em dias úteis e mostre ao usuário. Confira o texto vigente da resolução antes de fechar as datas.

## 6. Rascunhos

Prepare, para revisão humana, em `.lgpd/incidentes/AAAA-MM-DD-<apelido>/`:

- `registro.md` — modelo em [`assets/registro-incidente.md`](assets/registro-incidente.md);
- `comunicacao-anpd.md` — com o conteúdo mínimo do art. 48, § 1º: natureza dos dados afetados; informações sobre os titulares envolvidos; medidas técnicas e de segurança utilizadas; riscos relacionados; motivos da demora, se a comunicação não foi imediata; medidas adotadas para reverter ou mitigar os efeitos. A ANPD recebe a comunicação pelo canal oficial indicado no seu site;
- `comunicacao-titulares.md` — modelo em [`assets/comunicacao-titulares.md`](assets/comunicacao-titulares.md).

**Pare aqui** e peça que o encarregado e o jurídico revisem antes de qualquer envio.

## 7. Depois

- Corrija a causa e registre no `plano-acao.md`.
- Atualize o registro com a conclusão.
- Se a auditoria nunca foi feita, recomende a auditoria completa com `lgpd-auditoria`.
