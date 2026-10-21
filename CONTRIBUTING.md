# Contribuindo com o lgpd-kit

Obrigado pelo interesse! Algumas orientações para manter o kit confiável.

## O que mais ajuda

- **Correções normativas.** A ANPD publica resoluções com frequência. Ao propor uma mudança, inclua o link da fonte oficial (Planalto, Diário Oficial ou página da ANPD).
- **Novos nichos** em `skills/lgpd-descoberta/references/nichos.md`, com sinais, dados sensíveis prováveis, quase-identificadores e normas setoriais a sinalizar.
- **Novos formatos de esquema** no script `skills/lgpd-descoberta/scripts/inventario.py` (Mongoose, Sequelize, Drizzle etc.).
- **Exemplos de código** para outras stacks nas skills de ferramentas.

## Regras de conteúdo

1. **Cite a fonte.** Todo requisito aponta o artigo da LGPD; toda regra de resolução indica a resolução.
2. **Não invente.** Se um ponto não foi conferido no texto oficial, marque como "a confirmar".
3. **Requisito descreve comportamento, não tecnologia.** Tecnologia vai nos exemplos de implementação.
4. **Sem dados reais.** Exemplos usam dados fictícios.
5. **Português do Brasil**, linguagem direta.

## Como propor

1. Abra uma *issue* descrevendo a mudança.
2. Faça um *fork*, crie um *branch* e envie o *pull request* referenciando a *issue*.
3. Se alterar o script, rode-o em um projeto de exemplo e cole a saída no PR.
4. Atualize o `CHANGELOG.md`.
