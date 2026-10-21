# Referência normativa

Base normativa usada pelo lgpd-kit. **Conferida em outubro de 2026.** A LGPD e as resoluções da ANPD mudam com frequência; antes de citar qualquer ponto em um documento oficial, confira a versão vigente nas fontes indicadas no fim.

## LGPD — Lei nº 13.709/2018

Texto compilado com as alterações até a **Lei nº 15.352/2026**, que transformou a ANPD na **Agência Nacional de Proteção de Dados**, autarquia de natureza especial (a sigla foi mantida).

| Tema | Artigos | O que importa para o software |
|---|---|---|
| Definições | 5º | Dado pessoal (I), dado sensível (II), dado anonimizado (III), titular (V), controlador (VI), operador (VII), encarregado (VIII), tratamento (X), anonimização (XI), consentimento (XII). |
| Princípios | 6º | Finalidade, adequação, necessidade, livre acesso, qualidade, transparência, segurança, prevenção, não discriminação, responsabilização e prestação de contas. |
| Bases legais | 7º | Hipóteses que autorizam o tratamento de dado pessoal. |
| Consentimento | 8º | Por escrito ou outro meio que demonstre a vontade; ônus da prova do controlador; finalidades determinadas; revogação a qualquer momento; aviso em caso de mudança de finalidade. |
| Transparência | 9º | O que o titular tem direito de saber sobre o tratamento. |
| Dado sensível | 11 | Bases legais restritas; inclui tratamento que **revele** dado sensível (§ 1º); vedação de compartilhar dado de saúde para vantagem econômica (§ 4º). |
| Anonimização | 12 | Dado anonimizado não é dado pessoal, salvo se reversível com esforços razoáveis; custo e tempo como critério (§ 1º). |
| Estudos e pseudonimização | 13 | Pseudonimização definida no § 4º: informação adicional mantida separadamente, em ambiente controlado e seguro. |
| Crianças e adolescentes | 14 | Melhor interesse; consentimento de pai, mãe ou responsável para crianças; informação simples e acessível. |
| Término do tratamento | 15 e 16 | Quando o tratamento termina e quando os dados podem ser conservados. |
| Direitos do titular | 18 a 22 | Confirmação, acesso, correção, anonimização/bloqueio/eliminação, portabilidade, informação sobre compartilhamento e revogação; formas e prazos da resposta (art. 19). |
| Registro das operações | 37 | Controlador e operador mantêm registro das operações de tratamento. |
| Relatório de impacto | 38 | RIPD, quando exigido pela ANPD. |
| Operador | 39 | Trata conforme as instruções do controlador. |
| Encarregado | 41 | Indicação e divulgação do encarregado. |
| Segurança | 46 a 49 | Medidas de segurança desde a concepção (art. 46, § 2º); dever após o término (47); comunicação de incidente (48); sistemas estruturados para segurança (49). |
| Boas práticas | 50 | Programa de governança em privacidade. |
| Sanções | 52 | Da advertência à multa de até 2% do faturamento, limitada a R$ 50 milhões por infração. |
| Competências da ANPD | 55-J | Inclui zelar pelo tratamento simples e acessível dos dados de idosos (XIX). |

## Resoluções do Conselho Diretor da ANPD

Situação conforme a página oficial de regulamentações da ANPD.

| Resolução | Tema | Pontos de atenção para o software e para a organização |
|---|---|---|
| nº 1/2021 | Fiscalização e processo administrativo sancionador | Prazos de defesa e recurso; poderes de acesso da ANPD a documentos e sistemas. |
| nº 2/2022 (alterada pela nº 15/2024) | Agentes de tratamento de pequeno porte | Flexibilizações (registro simplificado, dispensa de encarregado com canal mantido, prazos em dobro) **não valem** para quem faz tratamento de alto risco: em larga escala ou que afete significativamente os titulares, combinado com dado sensível, dado de crianças, adolescentes ou idosos, decisões automatizadas ou tecnologias emergentes. |
| nº 4/2023 | Dosimetria e aplicação de sanções | Critérios de cálculo das multas; atenuantes para quem corrige a infração e mantém programa de governança. |
| nº 15/2024 | Comunicação de incidente de segurança | Comunicar à ANPD e aos titulares em **3 dias úteis** a partir do conhecimento de que o incidente afetou dados pessoais (prazo em dobro para pequeno porte); complementação em até 20 dias úteis; registro de todos os incidentes por **no mínimo 5 anos**. Comunicação obrigatória quando o incidente pode afetar significativamente os titulares **e** envolve, por exemplo, dado sensível, de crianças, adolescentes ou idosos, financeiro, de autenticação, protegido por sigilo ou em larga escala. |
| nº 18/2024 | Atuação do encarregado | Identidade e contato divulgados em local de fácil acesso; canal que funcione de fato; acúmulo de funções sem conflito de interesse; encarregado externo permitido. |
| nº 19/2024 | Transferência internacional de dados | Mecanismos válidos: cláusulas-padrão contratuais (modelo da ANPD, sem alterações substanciais), cláusulas específicas, normas corporativas globais e decisões de adequação. |
| nº 32/2026 | Adequação da União Europeia | Transferências para a União Europeia passam a contar com decisão de adequação. |
| nº 23/2024 (alterada pela nº 31/2025) | Agenda regulatória 2025–2026 | Temas em regulamentação, como anonimização e pseudonimização, direitos dos titulares e dados de saúde. Acompanhe: podem gerar novas regras. |

> Os números de artigo das resoluções **não** foram incluídos de propósito. Ao citar um dispositivo específico de uma resolução, confira o texto oficial.

## Documentos orientativos e estudos da ANPD

Não obrigam, mas servem de referência técnica:

- **Guia orientativo de segurança da informação para agentes de tratamento de pequeno porte** (2021).
- **Estudo técnico sobre anonimização de dados na LGPD** (2023) e **Estudo preliminar sobre anonimização e pseudonimização** (2023, submetido a consulta à sociedade). Base do método de anonimização do lgpd-kit: riscos de distinção, ligação e inferência; perfis de atacante promotor e jornalista; risco aceitável × risco medido.

## Normas setoriais — apenas sinalizar

O lgpd-kit **não audita** normas setoriais. Quando a descoberta identificar o nicho, avise o usuário de que podem existir regras próprias e recomende consulta especializada. Exemplos, a confirmar caso a caso:

| Nicho | Normas que costumam se aplicar |
|---|---|
| Saúde | Lei nº 13.787/2018 (prontuário eletrônico); Lei nº 14.289/2022 (sigilo de pessoas com HIV, hepatites crônicas, hanseníase e tuberculose); resoluções dos conselhos profissionais. |
| Financeiro | Lei Complementar nº 105/2001 (sigilo bancário); normas do Banco Central e do Conselho Monetário Nacional sobre segurança cibernética. |
| Educação e público infantojuvenil | Estatuto da Criança e do Adolescente (Lei nº 8.069/1990); Lei nº 15.211/2025 (ECA Digital). |
| Varejo e serviços ao consumidor | Código de Defesa do Consumidor (Lei nº 8.078/1990). |
| Plataformas e aplicações de internet | Marco Civil da Internet (Lei nº 12.965/2014), inclusive guarda de registros de acesso. |
| Recursos humanos | Consolidação das Leis do Trabalho e normas previdenciárias (prazos de guarda de documentos). |

## Fontes oficiais

- LGPD (texto compilado): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
- Regulamentações da ANPD: https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd
- Consulta sobre anonimização e pseudonimização (estudos): https://www.gov.br/participamaisbrasil/consulta-a-sociedade-estudo-preliminar-anonimizacao-e-pseudonimizacao-para-protecao-de-dados
