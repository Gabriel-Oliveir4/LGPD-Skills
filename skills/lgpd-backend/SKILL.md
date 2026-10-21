---
name: lgpd-backend
description: Audita a camada de back-end quanto à LGPD - autorização no servidor por perfil, respostas da API que expõem ou permitem inferir dado sensível, dados pessoais em logs, consentimento verificado antes de usar a finalidade, canal e rotinas de direitos do titular, trilha de auditoria, exportações com finalidade, integrações com terceiros e decisões automatizadas. Use quando o usuário pedir auditoria de API, rotas, controllers ou serviços, ou quando o maestro lgpd-auditoria chamar a etapa de back-end.
---

# lgpd-backend

Audita rotas, serviços, *jobs* e integrações. Use o catálogo de `lgpd-requisitos` filtrado pela camada **BE** e o inventário de `.lgpd/inventario-dados.md`.

## Roteiro

### 1. Mapa de rotas
Liste as rotas que leem ou escrevem dado pessoal (Next.js `app/api` e `route.ts`, Express `router.*`, NestJS `@Controller`, Django `urls.py`, FastAPI `@app.*`). Para cada uma, anote: perfil que acessa, dados que retorna e se há verificação de permissão.

### 2. Autorização no servidor (RF-29, RF-11, RNF-16)
- A permissão é verificada no servidor ou só escondida na interface? Botão oculto não é controle de acesso.
- Acesso por ID na URL (`/pacientes/123`) confere se o usuário pode ver **aquele** registro? Se não, qualquer usuário autenticado lê qualquer titular.
- Rotas de administração separadas e restritas.

### 3. O que a API devolve (RNF-08, RF-30)
- Respostas com `SELECT *` ou o objeto inteiro do ORM devolvem campos que a tela não usa. Procure `findMany()` sem `select`, serializers com `fields = '__all__'`.
- Perfis sem acesso ao dado sensível recebem campos que permitem inferi-lo (especialidade, medicamento, setor)?
- Listagens trazem dado sensível que só deveria aparecer no registro individual?

### 4. Dados pessoais em logs
- `console.log(req.body)`, `logger.info(user)`, logs de erro com o payload completo, ferramentas de APM que capturam corpo da requisição.
- Mensagens de erro que devolvem dados ao cliente.

### 5. Consentimento e finalidade (RF-02, RF-04, RF-05, RF-06, RF-12, RF-13)
- Rotinas que dependem de consentimento (e-mail de marketing, analytics, compartilhamento) consultam o consentimento **vigente** antes de agir?
- Existe rota para revogar?
- Exportações e integrações exigem e registram a finalidade?

### 6. Direitos do titular (RF-15 a RF-22, RNF-04)
- Canal de requisição, acesso simplificado imediato, declaração completa em até 15 dias, exportação estruturada, eliminação/anonimização/bloqueio, aviso aos destinatários.
- Verificação de identidade antes de entregar dados.

Para implementar, use `lgpd-direitos-titular`.

### 7. Trilha (RF-31, RNF-18, RF-32, RF-33)
- Cada leitura e escrita de dado pessoal gera registro com autor, data e hora, operação, registro afetado e finalidade?
- O titular aparece por pseudônimo?
- Há consulta da trilha por conta ou período (RF-33), para incidentes?

Para implementar, use `lgpd-trilha-auditoria`.

### 8. Ciclo de vida (RF-27, RF-28)
- Existe *job* agendado que elimina ou anonimiza no fim do prazo? Ele registra o que eliminou?

### 9. Terceiros e operadores
- Integrações que enviam dado pessoal (e-mail, SMS, pagamentos, CRM, IA, analytics). Cada uma é um **operador** ou um compartilhamento: precisa de finalidade, base legal e contrato (art. 39). Se o serviço está fora do Brasil, há transferência internacional (arts. 33 a 36; Res. CD/ANPD nº 19/2024).
- Envio de dado pessoal ou sensível para APIs de IA: registre e pergunte ao usuário sobre contrato e finalidade.

### 10. Decisões automatizadas (art. 20)
- Pontuação, aprovação, recusa ou perfilamento feito só por algoritmo. O titular pode pedir revisão e tem direito a informações sobre os critérios. Registre como ponto de atenção e sinalize ao maestro.

### 11. Autenticação (RNF-14)
- Login individual, sem contas compartilhadas; sessões com expiração; *tokens* não registrados em logs.

## Buscas úteis

```bash
grep -rnE "console\.(log|info|debug)\(.*(req\.body|user|paciente|cliente|cpf|email)" --include=*.{ts,js} .
grep -rnE "findMany\(\s*\)|findMany\(\{\s*where" --include=*.ts .
grep -rnE "fields\s*=\s*['\"]__all__" --include=*.py .
grep -rniE "openai|anthropic|sendgrid|twilio|mailchimp|segment|mixpanel|hotjar|stripe" --include=*.{ts,js,py} . | grep -v node_modules
```

## Saída

Linhas da camada **BE** em `.lgpd/matriz-rastreabilidade.md`, com arquivo e linha. Liste os terceiros encontrados em `.lgpd/descoberta.md` (seção "Operadores e compartilhamentos"). Peça aprovação antes de alterar qualquer rota.
