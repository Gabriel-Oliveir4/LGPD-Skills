---
name: lgpd-frontend
description: Audita a camada de front-end quanto à LGPD - aviso de privacidade, consentimento por finalidade com opções desmarcadas, banner de cookies conforme o guia da ANPD, scripts de terceiros, dados pessoais guardados no navegador, formulários com coleta excessiva, dado sensível em listagens e linguagem simples. Use quando o usuário pedir auditoria de telas, páginas, componentes, cookies ou formulários, ou quando o maestro lgpd-auditoria chamar a etapa de front-end.
---

# lgpd-frontend

Audita o que o titular vê e o que o navegador guarda. Use o catálogo de `lgpd-requisitos` filtrado pela camada **FE**.

## Roteiro

### 1. Aviso de privacidade (RF-01, RNF-20)
- Existe página acessível **sem login**, com os itens do art. 9º: finalidade, forma e duração do tratamento, identificação e contato do controlador, compartilhamentos, responsabilidades e direitos do titular, além do contato do encarregado (art. 41, § 1º)?
- Linguagem simples, sem juridiquês (art. 14, § 6º, para crianças; boa prática para todos).

Para redigir, use `lgpd-documentos`.

### 2. Consentimento (RF-02, RF-03, RF-05, RNF-01)
- Uma opção por finalidade. Aceite único para "termos e privacidade e marketing" é consentimento genérico (art. 8º, § 4º).
- Checkboxes e *toggles* iniciam desmarcados no código (`defaultChecked`, `checked={true}`, `v-model` com valor inicial `true`).
- Botão de recusar visível e consequências explicadas.
- Revogar é tão fácil quanto consentir: existe tela de preferências?

### 3. Cookies e rastreadores
O **Guia orientativo da ANPD sobre cookies** (2022) recomenda, quando a base for o consentimento:
- cookies não necessários desativados por padrão;
- botão de rejeitar com o mesmo destaque do de aceitar, já no primeiro nível do banner;
- segundo nível com categorias e finalidades descritas de forma simples;
- forma fácil de revogar depois.

Verifique também se scripts de analytics, *pixels* e gravação de sessão (Google Analytics, Meta Pixel, Hotjar, Clarity) **carregam antes** do consentimento. Ferramentas de gravação de sessão podem capturar o que o usuário digita: confira se mascaram campos.

### 4. O que fica no navegador
- `localStorage` e `sessionStorage` com dados pessoais ou sensíveis.
- *Service worker* ou PWA guardando respostas da API com dado pessoal em cache.
- Tokens de sessão em `localStorage` (prefira cookie `HttpOnly`).
- Dado pessoal em parâmetros de URL (`?cpf=`, `?email=`): fica em histórico, logs e cabeçalho `Referer`.

### 5. Formulários (RNF-02, RNF-03)
- Cada campo tem finalidade? Campos "por via das dúvidas" (RG, estado civil, renda) são coleta excessiva (art. 6º, III).
- Validação de formato no cliente e no servidor.
- Campos de dado sensível com `autocomplete="off"` quando fizer sentido.

### 6. Exibição (RF-30, RNF-08)
- Dado sensível aparece em listagens, agendas ou painéis? Deve aparecer só no registro individual.
- Telas de perfis sem acesso ao dado sensível exibem pistas (especialidade, setor, medicamento)?
- Dados mascarados quando a tela não precisa do valor inteiro (CPF `***.456.789-**`).

### 7. Crianças e adolescentes (RF-34, RF-35)
- Público infantojuvenil: fluxo de consentimento do responsável quando a base é o consentimento; textos adaptados.

### 8. Build
- *Source maps* publicados em produção expõem o código; chaves de API em variáveis públicas (`NEXT_PUBLIC_*`, `VITE_*`, `REACT_APP_*`) devem ser só chaves públicas por natureza.

## Buscas úteis

```bash
grep -rnE "defaultChecked|checked=\{true\}|checked: true" --include=*.{tsx,jsx,vue,svelte} .
grep -rnE "localStorage|sessionStorage" --include=*.{ts,tsx,js,jsx,vue} . | grep -v node_modules
grep -rniE "gtag|googletagmanager|fbq\(|hotjar|clarity|mixpanel|segment" --include=*.{ts,tsx,js,jsx,html,vue} . | grep -v node_modules
grep -rnE "NEXT_PUBLIC_|VITE_|REACT_APP_" .env* 2>/dev/null
```

## Saída

Linhas da camada **FE** em `.lgpd/matriz-rastreabilidade.md`. Se possível, inclua capturas ou o caminho da tela. Peça aprovação antes de alterar componentes.
