# Nichos

Tabela usada pela descoberta para **identificar o nicho** do sistema e ajustar o resto da auditoria. O nicho é um palpite inicial: sempre confirme com o usuário. Um sistema pode ter mais de um nicho (por exemplo, uma clínica que também vende produtos).

Os sinais são palavras procuradas em nomes de tabelas, colunas, rotas e telas, em português e em inglês.

## Saúde

- **Sinais:** paciente, patient, prontuario, medical_record, consulta, appointment, exame, exam, diagnostico, diagnosis, cid, receita, prescription, medicamento, medication, alergia, convenio, plano_saude, laudo, triagem, vacina.
- **Dados sensíveis prováveis:** diagnóstico, resultados de exames, medicamentos, histórico clínico, saúde mental, gestação, dados genéticos.
- **Quase-identificadores típicos:** idade ou data de nascimento, sexo, bairro ou CEP, data do atendimento, unidade de atendimento, profissão.
- **Bases legais típicas:** tutela da saúde (art. 11, II, f) para o atendimento; consentimento para finalidades opcionais, como lembretes e marketing.
- **Atenção:** inferência pelo setor, especialidade ou medicamento (art. 11, § 1º); vedação de compartilhar dado de saúde para vantagem econômica (art. 11, § 4º); dados de crianças em pediatria.
- **Normas a sinalizar:** prontuário eletrônico, sigilo de condições específicas, conselhos profissionais.

## Financeiro

- **Sinais:** conta, account, saldo, balance, transacao, transaction, cartao, card, pix, boleto, emprestimo, loan, credito, score, renda, income, investimento, fatura, invoice.
- **Dados sensíveis prováveis:** em regra, dado financeiro **não** é sensível pelo art. 11, mas é de alto risco em incidentes (Res. CD/ANPD nº 15/2024). Biometria usada em autenticação é sensível.
- **Quase-identificadores típicos:** faixa de renda, cidade, idade, profissão, datas de transação.
- **Bases legais típicas:** execução de contrato, cumprimento de obrigação legal, proteção do crédito, legítimo interesse (com avaliação).
- **Atenção:** decisões automatizadas de crédito (direito de revisão, art. 20); dados de autenticação.
- **Normas a sinalizar:** sigilo bancário; normas do Banco Central e do CMN.

## Varejo e comércio eletrônico

- **Sinais:** pedido, order, produto, product, carrinho, cart, cliente, customer, entrega, shipping, endereco, address, cupom, coupon, pagamento, payment, avaliacao, review.
- **Dados sensíveis prováveis:** em geral nenhum; atenção a produtos que revelam condição (farmácia, artigos religiosos, produtos íntimos) — o histórico de compra pode **revelar** dado sensível (art. 11, § 1º).
- **Quase-identificadores típicos:** CEP, cidade, idade, sexo, histórico de compras.
- **Bases legais típicas:** execução de contrato para a venda; consentimento ou legítimo interesse para marketing.
- **Atenção:** cookies e rastreamento; perfis de consumo; compartilhamento com meios de pagamento e transportadoras (operadores).
- **Normas a sinalizar:** Código de Defesa do Consumidor.

## Educação

- **Sinais:** aluno, student, matricula, enrollment, turma, class, nota, grade, frequencia, attendance, responsavel, guardian, escola, school, boletim, disciplina.
- **Dados sensíveis prováveis:** necessidades especiais e laudos, saúde, religião em escolas confessionais.
- **Quase-identificadores típicos:** idade, turma, escola, bairro, ano de ingresso.
- **Bases legais típicas:** execução de contrato, obrigação legal; consentimento do responsável para crianças (art. 14, § 1º).
- **Atenção:** **crianças e adolescentes** são a regra, não a exceção: melhor interesse, informação acessível e consentimento do responsável (art. 14).
- **Normas a sinalizar:** ECA; ECA Digital.

## Recursos humanos

- **Sinais:** funcionario, employee, colaborador, salario, salary, folha, payroll, ponto, timesheet, ferias, admissao, demissao, atestado, beneficio, dependente.
- **Dados sensíveis prováveis:** atestados e saúde ocupacional, filiação sindical, origem racial ou étnica (censos de diversidade), biometria do ponto.
- **Quase-identificadores típicos:** cargo, setor, data de admissão, faixa salarial, idade.
- **Bases legais típicas:** execução de contrato de trabalho, obrigação legal.
- **Atenção:** relatórios por setor pequeno podem identificar a pessoa; dados de dependentes, inclusive crianças.
- **Normas a sinalizar:** legislação trabalhista e previdenciária (prazos de guarda).

## Marketing e CRM

- **Sinais:** lead, campanha, campaign, newsletter, segmento, segment, interesse, tracking, utm, pixel, opt_in, opt_out, perfil, persona.
- **Dados sensíveis prováveis:** perfis que inferem saúde, religião, orientação sexual ou opinião política a partir de comportamento.
- **Quase-identificadores típicos:** cidade, idade, interesses, dispositivo.
- **Bases legais típicas:** consentimento; legítimo interesse com avaliação documentada.
- **Atenção:** consentimento por finalidade, revogação, cookies e compartilhamento com terceiros.

## Mobilidade, entregas e localização

- **Sinais:** localizacao, location, latitude, longitude, geo, rota, route, corrida, ride, motorista, driver, entrega, checkin.
- **Dados sensíveis prováveis:** geolocalização em si não é sensível pelo art. 11, mas pode **revelar** visitas a hospitais, templos e sindicatos.
- **Quase-identificadores típicos:** origem e destino frequentes (casa, trabalho), horários.
- **Atenção:** trajetos identificam pessoas mesmo sem nome; generalizar coordenadas e horários em relatórios.

## Poder público

- **Sinais:** cidadao, citizen, protocolo, processo, beneficio_social, nis, servidor_publico, secretaria, orgao.
- **Atenção:** regras próprias para o poder público (arts. 23 a 32 da LGPD); a base costuma ser a execução de políticas públicas ou a obrigação legal. Avise que o lgpd-kit foi pensado para controladores privados e que a análise do poder público exige cuidado adicional.

## Quando nenhum nicho se encaixa

Classifique como **geral**, faça o inventário de dados normalmente e pergunte ao usuário qual é a atividade do sistema.
