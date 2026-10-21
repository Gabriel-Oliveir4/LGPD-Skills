# Catálogo de requisitos

Catálogo de requisitos de software derivados da LGPD (Lei nº 13.709/2018), organizado em famílias. Cada requisito tem o artigo de origem, o tipo (F = funcional, NF = não funcional), as camadas onde normalmente é implementado e o que procurar no projeto para verificá-lo.

- **Camadas:** BD = banco de dados; BE = back-end; FE = front-end; INF = infraestrutura.
- **Asterisco (\*):** decisão de projeto que vai além do texto da lei para atender a uma exigência geral. Pode ser substituída por outra solução equivalente, desde que a justificativa fique registrada.
- Os requisitos foram escritos para um sistema genérico com dados sensíveis. Onde o texto cita saúde, troque pelo dado sensível do nicho identificado na descoberta.

## Como registrar o status

| Status | Quando usar |
|---|---|
| ✅ Atendido | Há evidência no código ou na configuração (indique arquivo e linha). |
| 🟡 Parcial | Existe, mas incompleto ou só na interface. |
| ❌ Ausente | Não há implementação. |
| ➖ Não se aplica | O tratamento correspondente não existe no projeto (justifique). |
| 🏢 Depende da organização | O software apoia, mas o cumprimento é organizacional. |

## Transparência e consentimento

| ID | Requisito | Origem (LGPD) | Tipo | Camadas | O que verificar |
|---|---|---|---|---|---|
| RF-01 | O sistema deve disponibilizar ao titular um aviso de privacidade com finalidade, forma e duração do tratamento, identificação e contato do controlador, contato do encarregado, compartilhamentos, responsabilidades e direitos. | Arts. 9º, I a VII; 41, § 1º | F | FE | Página ou tela de aviso de privacidade acessível sem login, com todos os itens do art. 9º e o contato do encarregado. |
| RF-02 | O sistema deve solicitar o consentimento separadamente para cada finalidade que dependa dele. | Arts. 8º, § 4º; 11, I | F | FE, BE | Uma opção de consentimento por finalidade; nada de aceite único que cubra várias finalidades. |
| RF-03 | O sistema deve oferecer a opção de recusar o consentimento, informando as consequências da recusa. | Art. 18, VIII | F | FE | Botão de recusa visível e texto que explique o que muda se o titular recusar. |
| RF-04 | O sistema deve registrar cada consentimento com data, hora, finalidade e versão do texto apresentado. | Art. 8º, § 2º | F | BE, BD | Tabela de consentimentos com titular, finalidade, data/hora, ação (concedeu/revogou) e versão do texto. |
| RF-05 | O sistema deve permitir ao titular revogar o consentimento a qualquer momento, sem custo. | Arts. 8º, § 5º; 18, IX | F | FE, BE | Caminho no app para revogar, tão simples quanto o de consentir; endpoint de revogação. |
| RF-06 | O sistema deve interromper o tratamento baseado em consentimento após a revogação. | Arts. 8º, § 5º; 15, III | F | BE | Rotinas que usam a finalidade (envio de e-mail, analytics etc.) consultam o consentimento vigente antes de agir. |
| RF-07 | O sistema deve avisar o titular, com destaque, antes de alterar a finalidade de um tratamento. | Arts. 8º, § 6º; 9º, § 2º | F | FE, BE | Fluxo de aviso ao titular quando a finalidade muda, antes da mudança valer. |
| RNF-01* | As opções de consentimento devem ser apresentadas desmarcadas. | Art. 5º, XII | NF | FE | Checkboxes e toggles de consentimento iniciam desmarcados no código da interface. |

## Base legal do tratamento

| ID | Requisito | Origem (LGPD) | Tipo | Camadas | O que verificar |
|---|---|---|---|---|---|
| RF-08 | O sistema deve associar uma base legal a cada finalidade de tratamento cadastrada. | Arts. 7º; 11 | F | BD, BE | Cadastro de finalidades com campo de base legal obrigatório. |
| RF-09 | O sistema deve impedir que uma finalidade que trate dado sensível seja associada a base legal não prevista no art. 11. | Art. 11 | F | BD, BE | Validação (no banco ou no servidor) que recusa base legal fora do art. 11 para finalidade com dado sensível. |
| RF-10 | O sistema deve registrar, para cada tratamento de dado sensível sem consentimento, a hipótese do art. 11, II utilizada. | Arts. 11, II; 37 | F | BD, BE | Registro da hipótese do art. 11, II usada quando o dado sensível é tratado sem consentimento. |
| RF-11* | O sistema deve restringir o acesso aos dados sensíveis aos perfis cuja função exige esse acesso, como os profissionais de saúde quando a base legal é a tutela da saúde. | Art. 11, II, f | F | BD, BE | Políticas de acesso (RLS, middleware, RBAC) que limitam o dado sensível aos perfis autorizados. |

## Finalidade e adequação

| ID | Requisito | Origem (LGPD) | Tipo | Camadas | O que verificar |
|---|---|---|---|---|---|
| RF-12 | O sistema deve registrar a finalidade de cada tratamento realizado. | Art. 6º, I | F | BE, BD | Cada operação registrada traz a finalidade. |
| RF-13 | O sistema deve exigir a indicação de uma finalidade cadastrada para exportar ou compartilhar dados pessoais. | Arts. 6º, I e II; 9º, V | F | BE | Exportações e integrações exigem a finalidade e a recusam quando ausente. |

## Necessidade e qualidade dos dados

| ID | Requisito | Origem (LGPD) | Tipo | Camadas | O que verificar |
|---|---|---|---|---|---|
| RNF-02 | Os formulários do sistema devem coletar apenas campos associados a uma finalidade cadastrada. | Art. 6º, III | NF | FE, BE | Cada campo de formulário está ligado a uma finalidade; campos sem finalidade são sinal de coleta excessiva. |
| RF-14 | O sistema deve permitir a correção de dados incompletos, inexatos ou desatualizados, registrando a alteração. | Arts. 6º, V; 18, III | F | BE, FE | Fluxo de correção de dados com registro de quem alterou, quando e o valor anterior. |
| RNF-03 | O sistema deve validar o formato dos dados no momento da coleta. | Art. 6º, V | NF | FE, BE | Validação de formato (CPF, e-mail, datas) no momento da coleta, no cliente e no servidor. |

## Direitos do titular

| ID | Requisito | Origem (LGPD) | Tipo | Camadas | O que verificar |
|---|---|---|---|---|---|
| RF-15 | O sistema deve receber requisições do titular ou de seu representante legal. | Art. 18, § 3º | F | BE, FE | Canal para requisições do titular (tela, formulário ou endpoint), inclusive por representante legal. |
| RF-16 | O sistema deve confirmar a existência de tratamento e fornecer acesso aos dados em formato simplificado, imediatamente. | Arts. 18, I e II; 19, I | F | BE | Endpoint ou tela que mostra ao titular os próprios dados em formato simplificado. |
| RF-17 | O sistema deve gerar declaração completa com a origem dos dados, os critérios utilizados e a finalidade do tratamento. | Art. 19, II | F | BE | Geração de declaração completa: origem dos dados, critérios e finalidade. |
| RF-18 | O sistema deve permitir anonimizar, bloquear ou eliminar dados a pedido do titular, nas hipóteses previstas em lei. | Art. 18, IV e VI | F | BE, BD | Rotinas para anonimizar, bloquear ou eliminar dados de um titular a pedido. |
| RF-19 | O sistema deve informar ao titular as entidades com as quais seus dados foram compartilhados. | Art. 18, VII | F | BE | Registro dos compartilhamentos por titular e forma de informá-los. |
| RF-20 | O sistema deve exportar os dados do titular em formato eletrônico estruturado. | Arts. 18, V; 19, §§ 2º e 3º | F | BE | Exportação dos dados do titular em formato estruturado (JSON, CSV). |
| RF-21 | O sistema deve avisar os destinatários dos dados quando houver correção, eliminação, anonimização ou bloqueio. | Art. 18, § 6º | F | BE | Notificação aos destinatários (integrações, operadores) após correção ou eliminação. |
| RF-22 | O sistema deve registrar cada requisição, a resposta dada e, quando não atendida de imediato, a justificativa. | Art. 18, § 4º | F | BE, BD | Tabela de requisições com data, tipo, resposta e justificativa quando não atendida de imediato. |
| RNF-04 | A declaração completa deve ser emitida em até 15 dias a partir da requisição. | Art. 19, II | NF | BE | Controle do prazo de 15 dias para a declaração completa (alerta ou fila com vencimento). |
| RNF-05 | Os dados devem ser armazenados de forma que possam ser localizados por titular. | Art. 19, § 1º | NF | BD | Todas as tabelas com dado pessoal permitem localizar os registros de um titular. |

## Anonimização e pseudonimização

| ID | Requisito | Origem (LGPD) | Tipo | Camadas | O que verificar |
|---|---|---|---|---|---|
| RF-23 | O sistema deve armazenar os dados de identificação separados dos dados sensíveis, ligados por pseudônimo. | Arts. 13, § 4º; 46 | F | BD | Esquema do banco com identificação e dado sensível em tabelas (ou bancos) separados, ligados por pseudônimo. |
| RNF-06 | A informação que permite ligar o pseudônimo à identidade, seja a tabela de correspondência ou a chave usada para gerar o pseudônimo, deve ser mantida fora das bases de dados do sistema, com acesso restrito. | Arts. 13, § 4º; 46 | NF | BD, INF | Tabela de correspondência ou chave do pseudônimo fora das bases da aplicação, com acesso restrito. |
| RF-24 | O sistema deve gerar extrações e relatórios anonimizados para uso secundário. | Arts. 13, caput e § 1º; 16, II e IV | F | BE, BD | Rotina que gera extrações e relatórios anonimizados para uso secundário. |
| RNF-07 | Nos relatórios anonimizados, cada combinação de quase-identificadores deve corresponder a pelo menos k titulares. | Arts. 11, § 1º; 12 | NF | BE | Medição de k-anonimato antes de liberar o relatório. |
| RF-25 | O sistema deve registrar, para cada extração anonimizada, a técnica aplicada e o risco de reidentificação medido. | Arts. 6º, X; 12, § 1º | F | BE, BD | Registro, por extração, da técnica aplicada e do risco medido. |
| RNF-08 | Telas e relatórios acessíveis a perfis sem acesso ao dado sensível não devem permitir inferi-lo. | Art. 11, § 1º | NF | FE, BE | Respostas da API e telas de perfis sem acesso ao dado sensível não trazem campos que permitam inferi-lo (setor, medicamento, tipo de exame). |
| RNF-09* | Nos relatórios anonimizados, cada grupo de quase-identificadores deve conter pelo menos l valores distintos do atributo sensível. | Arts. 11, § 1º; 12 | NF | BE | Medição de l-diversidade nos relatórios anonimizados. |
| RNF-10* | O pseudônimo não deve poder ser recalculado a partir de dados do titular sem uma informação secreta mantida separadamente. | Arts. 12; 13, § 4º | NF | BD, BE | Pseudônimo gerado com segredo (HMAC com chave, token aleatório); nunca hash simples de CPF, e-mail ou telefone. |
| RNF-11* | Os dados sensíveis não devem conter informações que permitam ligá-los aos dados de identificação, como identificadores sequenciais ou datas e horas de criação coincidentes. | Arts. 12; 13, § 4º | NF | BD | Tabelas de dado sensível sem ID sequencial compartilhado e sem timestamps que coincidam com os da identificação. |
| RNF-12* | O acesso aos dados de identificação e aos dados sensíveis deve usar credenciais distintas. | Arts. 13, § 4º; 46 | NF | BD, INF | Usuários ou papéis de banco distintos para acessar identificação e dado sensível. |

## Ciclo de vida e eliminação

| ID | Requisito | Origem (LGPD) | Tipo | Camadas | O que verificar |
|---|---|---|---|---|---|
| RF-26 | O sistema deve registrar, para cada finalidade, o prazo ou o evento de término do tratamento. | Art. 15, I e II | F | BD, BE | Cadastro de prazo ou evento de término por finalidade. |
| RF-27 | O sistema deve, ao término do tratamento, eliminar ou anonimizar os dados, salvo hipótese de conservação registrada. | Art. 16 | F | BE, BD | Rotina agendada que elimina ou anonimiza ao fim do prazo, respeitando hipóteses de conservação. |
| RF-28 | O sistema deve registrar cada eliminação realizada. | Arts. 16; 37 | F | BD, BE | Registro de cada eliminação (o quê, quando, por qual regra). |
| RNF-13 | As cópias de segurança devem manter as mesmas proteções dos dados originais, inclusive após o término do tratamento. | Art. 47 | NF | INF, BD | Backups cifrados, com acesso restrito e incluídos nas regras de eliminação quando possível. |

## Segurança da informação

| ID | Requisito | Origem (LGPD) | Tipo | Camadas | O que verificar |
|---|---|---|---|---|---|
| RNF-14 | Todo acesso ao sistema deve exigir autenticação individual. | Art. 46 | NF | BE, FE | Login individual; nenhuma conta compartilhada ou genérica. |
| RF-29 | O sistema deve controlar o acesso por perfis definidos conforme a função do usuário. | Art. 46 | F | BE, BD | Perfis/papéis definidos e verificados no servidor, não só escondidos na interface. |
| RNF-15 | Os dados devem ser transmitidos e armazenados de forma ininteligível a terceiros não autorizados. | Arts. 46; 48, § 3º | NF | INF, BD | TLS em todo tráfego; criptografia em repouso (disco, banco, campos sensíveis). |
| RNF-16 | O sistema deve impedir alterações não autorizadas nos dados. | Art. 46 | NF | BE, BD | Escritas protegidas por autorização no servidor e no banco. |
| RNF-17 | As medidas de segurança devem ser consideradas desde a concepção do sistema. | Arts. 46, § 2º; 49 | NF | todas | Evidência de privacidade desde a concepção: revisão de segurança, ameaças e minimização documentadas no projeto. |
| RF-30* | O sistema deve exibir dados sensíveis apenas na visualização individual do titular, e nunca em listagens, agendas ou painéis gerais. | Arts. 11, § 1º; 46 | F | FE, BE | Listagens e painéis não exibem dado sensível; ele só aparece ao abrir o registro individual. |

## Trilha de auditoria

| ID | Requisito | Origem (LGPD) | Tipo | Camadas | O que verificar |
|---|---|---|---|---|---|
| RF-31 | O sistema deve registrar cada operação de tratamento com autor, data e hora, operação, registro afetado e finalidade. | Art. 37 | F | BE, BD | Trilha com autor, data/hora, operação, registro afetado e finalidade. |
| RNF-18* | A trilha de auditoria deve identificar o titular por identificador substituto, sem nome ou condição de saúde. | Arts. 6º, III; 46 | NF | BE, BD | Trilha identifica o titular por pseudônimo, sem nome nem dado sensível. |
| RNF-19 | A trilha de auditoria deve ser protegida contra alteração e exclusão. | Art. 46 | NF | BD, INF | Trilha somente de inclusão (append-only), com proteção contra alteração e exclusão. |
| RF-32 | O sistema deve gerar relatório das operações de tratamento para demonstração de conformidade. | Art. 6º, X | F | BE | Relatório das operações de tratamento gerado a partir da trilha. |

## Incidentes de segurança

| ID | Requisito | Origem (LGPD) | Tipo | Camadas | O que verificar |
|---|---|---|---|---|---|
| RF-33 | O sistema deve permitir consultar, na trilha de auditoria, os dados e os titulares acessados por uma conta ou em um período, para levantar o que foi afetado por um incidente. | Art. 48, § 1º, I e II | F | BE, BD | Consulta à trilha por conta ou período, para levantar dados e titulares afetados por um incidente. |

## Titulares vulneráveis

| ID | Requisito | Origem (LGPD) | Tipo | Camadas | O que verificar |
|---|---|---|---|---|---|
| RF-34 | O sistema deve identificar titulares crianças e adolescentes a partir da data de nascimento. | Art. 14 | F | BE, BD | Cálculo de idade a partir da data de nascimento para marcar crianças e adolescentes. |
| RF-35 | O sistema deve registrar o consentimento de pai, mãe ou responsável legal quando a base legal para o tratamento de dados de criança for o consentimento. | Art. 14, §§ 1º e 5º | F | BE, FE | Registro do consentimento do responsável quando a base é o consentimento e o titular é criança. |
| RNF-20* | As informações ao titular devem ser apresentadas em linguagem simples e acessível. | Arts. 14, § 6º; 55-J, XIX | NF | FE | Textos para o titular em linguagem simples (aviso, termos, telas de direitos). |
