# Registro das operações de tratamento (art. 37)

> Uma linha por operação (processo) de tratamento. Mantenha atualizado; versione no Git.

- **Organização:** [razão social, CNPJ] — **Papel:** controladora | operadora
- **Encarregado:** [nome, contato]
- **Data da última revisão:** [data]

| # | Processo | Finalidade | Base legal | Categorias de titulares | Categorias de dados | Dados sensíveis? | Origem dos dados | Compartilhado com | Transferência internacional | Prazo de retenção | Medidas de segurança | Sistemas/tabelas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [Agendamento] | [Marcar consultas] | [Execução de contrato] | [Pacientes] | [Cadastrais, contato] | Não | [Titular] | [—] | [Não] | [ ] | [Acesso por perfil, TLS] | [`agenda`, `titular`] |
| 2 | [Atendimento] | [Registro clínico] | [Tutela da saúde, art. 11, II, f] | [Pacientes] | [Saúde] | Sim | [Profissional] | [Laboratório X] | [Não] | [ ] | [Pseudonimização, RLS, trilha] | [`ficha_clinica`] |

## Pendências

- [A PREENCHER: prazos de retenção decididos pela organização]
