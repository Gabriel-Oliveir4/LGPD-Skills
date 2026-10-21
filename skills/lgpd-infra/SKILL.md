---
name: lgpd-infra
description: Audita a infraestrutura de um projeto quanto à LGPD - TLS, segredos e chaves fora do repositório, local de hospedagem e transferência internacional, backups, logs com dados pessoais, separação de ambientes, acesso administrativo e guarda da chave do pseudônimo. Lê Dockerfile, docker-compose, arquivos .env de exemplo, Terraform, CI/CD e configurações de nuvem. Use quando o usuário pedir auditoria de infra, deploy, nuvem ou servidores, ou quando o maestro lgpd-auditoria chamar a etapa de infra.
---

# lgpd-infra

Audita onde o sistema roda e como os dados circulam fora do código. Muitos itens só podem ser confirmados pelo usuário (painel da nuvem, contratos): pergunte e registre a resposta como evidência.

## Entradas

`Dockerfile`, `docker-compose*.yml`, `.env.example`, `vercel.json`, `netlify.toml`, `terraform/`, `k8s/`, `.github/workflows/`, `nginx.conf`, configuração do Supabase/Firebase.

## Roteiro

### 1. Tráfego (RNF-15)
- TLS em todo o tráfego externo, inclusive entre serviços quando passam por rede pública.
- Conexão com o banco usando `sslmode=require` ou equivalente.
- Cabeçalho HSTS e redirecionamento de HTTP para HTTPS.

### 2. Segredos e chaves (RNF-06)
- `.env` com valores reais versionado? `git log --all -- .env` mostra se já esteve no histórico. Segredo que já foi publicado deve ser trocado, não só apagado.
- A chave do HMAC ou a tabela de correspondência do pseudônimo fica em cofre de segredos ou serviço separado, com acesso restrito, **fora** dos bancos da aplicação.
- Segredos no CI/CD guardados como *secrets*, não no YAML.

### 3. Onde os dados ficam
- Região da nuvem e dos serviços terceiros. Dados armazenados ou processados fora do Brasil configuram **transferência internacional** (art. 33), que precisa de mecanismo válido (Res. CD/ANPD nº 19/2024; União Europeia com decisão de adequação pela Res. nº 32/2026). Registre e sinalize para `lgpd-organizacional`.
- Provedores de nuvem e SaaS são operadores: precisam de contrato (art. 39).

### 4. Backups (RNF-13)
- Backups automáticos, cifrados, com acesso restrito e prazo de guarda definido.
- Restauração testada.
- Backups considerados nas regras de eliminação, quando tecnicamente possível, ou com prazo de expiração.

### 5. Logs
- Logs de aplicação, proxy e balanceador com dados pessoais (corpo de requisição, CPF em URL).
- Prazo de guarda definido. Para provedores de aplicação de internet, o Marco Civil (Lei nº 12.965/2014, art. 15) exige guardar os registros de acesso por 6 meses: sinalize, não audite.
- Acesso aos logs restrito.

### 6. Ambientes
- Homologação e desenvolvimento com cópia do banco de produção? Use dados fictícios ou anonimizados.
- Ambientes de *preview* públicos apontando para o banco de produção.

### 7. Acesso administrativo (RNF-14, RF-29)
- Acesso ao painel da nuvem e ao banco com usuários individuais e autenticação em dois fatores.
- Portas de banco expostas à internet (`ports: "5432:5432"` em produção, regras de firewall abertas).

### 8. Monitoramento e incidentes
- Alertas de acesso anômalo, falhas de login em massa, exportações grandes.
- Existe contato definido para incidentes? Ligue com `lgpd-incidentes`.

## Buscas úteis

```bash
git ls-files | grep -E "(^|/)\.env($|\.)" | grep -v example
git log --all --oneline -- .env .env.local .env.production 2>/dev/null | head
grep -rnE "ports:\s*$|[\"']?(5432|3306|27017|6379):" docker-compose*.yml 2>/dev/null
grep -rniE "region|location" --include=*.{tf,json,toml,yml,yaml} . | grep -v node_modules | head -30
grep -rniE "sslmode=disable|ssl:\s*false|rejectUnauthorized:\s*false" .
```

## Saída

Linhas da camada **INF** em `.lgpd/matriz-rastreabilidade.md`. Liste em `.lgpd/descoberta.md` os provedores e as regiões encontradas. Nunca copie valores de segredos para o relatório: indique só onde estão.
