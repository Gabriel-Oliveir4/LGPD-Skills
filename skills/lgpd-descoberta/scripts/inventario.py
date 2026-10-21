#!/usr/bin/env python3
"""Inventário inicial de dados pessoais de um projeto (lgpd-kit / lgpd-descoberta).

Varre o projeto em busca de definições de dados (Prisma, SQL, Django, TypeORM),
classifica cada campo pelo nome e sugere o nicho e as camadas presentes.

É um ponto de partida: a classificação é feita por palavras-chave e precisa ser
revisada por uma pessoa. Usa apenas a biblioteca padrão do Python.

Uso:
    python3 inventario.py <raiz-do-projeto> [--saida .lgpd/inventario-dados.md] [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict

IGNORAR_DIRS = {
    ".git", "node_modules", "dist", "build", ".next", ".nuxt", "out", "coverage",
    "venv", ".venv", "env", "__pycache__", ".lgpd", "vendor", "target", ".turbo",
}

# Categorias por palavra-chave (comparação sem acento e em minúsculas).
# A ordem importa: a primeira categoria que casar vence.
CATEGORIAS: list[tuple[str, list[str]]] = [
    ("autenticacao", ["senha", "password", "passwd", "secret", "api_key", "apikey",
                      "otp", "mfa", "totp", "refresh_token", "access_token"]),
    ("sensivel", ["diagnost", "cid10", "cid_10", "doenca", "disease", "exame", "exam_",
                  "resultado_exame", "lab_result", "medicament", "medication", "prescri",
                  "receita_med", "alergia", "allerg", "saude", "health", "hiv", "gestac",
                  "pregnan", "deficienc", "disabilit", "laudo", "prontuario", "medical_record",
                  "raca", "race", "etnia", "ethnic", "religi", "sindica", "union_member",
                  "orientacao_sexual", "sexual_orient", "vida_sexual", "sex_life",
                  "partido", "politic", "biometr", "fingerprint", "impressao_digital",
                  "face_id", "facial", "genetic", "genetico", "dna"]),
    ("financeiro", ["cartao", "card_number", "cc_number", "numero_cartao", "conta_bancaria",
                    "bank_account", "iban", "agencia", "saldo", "balance", "renda", "income",
                    "salario", "salary", "chave_pix", "pix_key", "score_credito", "credit_score"]),
    ("identificador_direto", ["cpf", "rg", "cnh", "passaporte", "passport", "cns", "nis",
                              "pis", "titulo_eleitor", "nome", "name", "email", "e_mail",
                              "telefone", "phone", "celular", "mobile", "whatsapp",
                              "endereco", "address", "logradouro", "street", "foto",
                              "photo", "avatar", "ip_address", "endereco_ip", "device_id",
                              "matricula", "username", "login"]),
    ("quase_identificador", ["nascimento", "birth", "dob", "idade", "age", "sexo", "gender",
                             "genero", "cep", "zip", "postal", "bairro", "neighborhood",
                             "cidade", "city", "municipio", "estado_civil", "marital",
                             "profiss", "occupation", "escolaridade", "education_level",
                             "nacionalidade", "nationality", "latitude", "longitude",
                             "geoloc", "location"]),
    ("tempo", ["created_at", "updated_at", "criado_em", "atualizado_em", "data_criacao",
               "timestamp", "data_hora", "datetime"]),
]

# Termos que não devem casar (falsos positivos comuns).
EXCECOES = {"name": ["file_name", "filename", "table_name", "column_name", "product_name",
                     "nome_produto", "nome_arquivo", "username"],
            "age": ["page", "image", "message", "storage", "usage", "language", "stage",
                    "package", "percentage", "average", "mileage", "damage", "manage"],
            "exam_": [], "race": ["trace", "grace"], "rg": ["org", "cargo", "charge", "merge"],
            "cid10": [], "login": ["last_login", "login_attempt"]}

NICHOS: dict[str, list[str]] = {
    "saúde": ["paciente", "patient", "prontuario", "consulta", "appointment", "exame", "diagnost",
              "receita", "prescri", "medicament", "convenio", "laudo", "triagem", "vacina"],
    "financeiro": ["conta", "account", "saldo", "transac", "cartao", "card", "pix", "boleto",
                   "emprestimo", "loan", "credito", "credit", "fatura", "invoice"],
    "varejo": ["pedido", "order", "produto", "product", "carrinho", "cart", "entrega",
               "shipping", "cupom", "coupon", "avaliacao", "review", "estoque", "inventory"],
    "educação": ["aluno", "student", "matricula", "enrollment", "turma", "nota", "grade",
                 "frequencia", "attendance", "responsavel", "guardian", "escola", "school"],
    "recursos humanos": ["funcionario", "employee", "colaborador", "salario", "salary", "folha",
                         "payroll", "ponto", "timesheet", "ferias", "admissao", "atestado"],
    "marketing": ["lead", "campanha", "campaign", "newsletter", "segmento", "segment",
                  "tracking", "utm", "opt_in", "opt_out"],
    "mobilidade": ["latitude", "longitude", "rota", "route", "corrida", "ride", "motorista",
                   "driver", "checkin"],
    "poder público": ["cidadao", "citizen", "protocolo", "beneficio_social", "secretaria",
                      "orgao"],
}

MARCADORES_STACK: dict[str, list[str]] = {
    "banco de dados": ["schema.prisma", "migrations", "supabase", "*.sql", "models.py",
                       "docker-compose.yml"],
    "back-end": ["package.json", "requirements.txt", "pyproject.toml", "go.mod", "pom.xml",
                 "build.gradle", "Gemfile", "composer.json", "app/api", "pages/api", "routes"],
    "front-end": ["*.tsx", "*.jsx", "*.vue", "*.svelte", "index.html", "next.config"],
    "infra": ["Dockerfile", "docker-compose.yml", "*.tf", "k8s", ".github/workflows",
              "vercel.json", "netlify.toml", "fly.toml", "serverless.yml"],
}


@dataclass
class Campo:
    arquivo: str
    linha: int
    tabela: str
    campo: str
    categoria: str


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", texto)  # camelCase -> snake_case
    return texto.lower()


def classificar(nome: str) -> str:
    n = normalizar(nome)
    for categoria, chaves in CATEGORIAS:
        for chave in chaves:
            if chave in n and not any(ex in n for ex in EXCECOES.get(chave, [])):
                return categoria
    return "outro"


# --- extratores -------------------------------------------------------------

RE_PRISMA_MODEL = re.compile(r"^\s*model\s+(\w+)\s*\{")
RE_PRISMA_CAMPO = re.compile(r"^\s*(\w+)\s+[A-Z]\w*[\[\]?]*")
RE_SQL_TABELA = re.compile(r"create\s+table\s+(?:if\s+not\s+exists\s+)?([\w.\"`]+)", re.I)
RE_SQL_ADD = re.compile(r"alter\s+table\s+([\w.\"`]+)\s+add\s+(?:column\s+)?([\w\"`]+)", re.I)
RE_SQL_COLUNA = re.compile(r"^\s*[\"`]?(\w+)[\"`]?\s+(?:[a-z]+)", re.I)
RE_DJANGO_MODEL = re.compile(r"^class\s+(\w+)\(.*models\.Model.*\):")
RE_DJANGO_CAMPO = re.compile(r"^\s+(\w+)\s*=\s*models\.\w+")
RE_TYPEORM_ENTITY = re.compile(r"@Entity\(")
RE_TYPEORM_CLASSE = re.compile(r"class\s+(\w+)")
RE_TYPEORM_COLUNA = re.compile(r"^\s*(?:public\s+|private\s+|readonly\s+)*(\w+)[!?]?\s*:")
PALAVRAS_SQL = {"primary", "foreign", "constraint", "unique", "check", "key", "index", "references"}


def extrair_prisma(caminho: str, linhas: list[str]) -> list[Campo]:
    campos, modelo = [], None
    for i, l in enumerate(linhas, 1):
        m = RE_PRISMA_MODEL.match(l)
        if m:
            modelo = m.group(1)
            continue
        if modelo and l.strip().startswith("}"):
            modelo = None
            continue
        if modelo:
            c = RE_PRISMA_CAMPO.match(l)
            if c and not l.strip().startswith(("@@", "//")):
                campos.append(Campo(caminho, i, modelo, c.group(1), classificar(c.group(1))))
    return campos


def extrair_sql(caminho: str, linhas: list[str]) -> list[Campo]:
    campos, tabela, profundidade = [], None, 0
    for i, l in enumerate(linhas, 1):
        add = RE_SQL_ADD.search(l)
        if add:
            t, c = add.group(1).strip('"`'), add.group(2).strip('"`')
            campos.append(Campo(caminho, i, t, c, classificar(c)))
            continue
        m = RE_SQL_TABELA.search(l)
        if m:
            tabela = m.group(1).strip('"`').split(".")[-1]
            profundidade = l.count("(") - l.count(")")
            continue
        if tabela:
            profundidade += l.count("(") - l.count(")")
            c = RE_SQL_COLUNA.match(l)
            if c and c.group(1).lower() not in PALAVRAS_SQL:
                campos.append(Campo(caminho, i, tabela, c.group(1), classificar(c.group(1))))
            if profundidade <= 0 and ")" in l:
                tabela = None
    return campos


def extrair_django(caminho: str, linhas: list[str]) -> list[Campo]:
    campos, modelo = [], None
    for i, l in enumerate(linhas, 1):
        m = RE_DJANGO_MODEL.match(l)
        if m:
            modelo = m.group(1)
            continue
        if modelo:
            c = RE_DJANGO_CAMPO.match(l)
            if c:
                campos.append(Campo(caminho, i, modelo, c.group(1), classificar(c.group(1))))
            elif l and not l[0].isspace():
                modelo = None
    return campos


def extrair_typeorm(caminho: str, linhas: list[str]) -> list[Campo]:
    campos, classe, esperando_coluna = [], None, False
    texto = "\n".join(linhas)
    if not RE_TYPEORM_ENTITY.search(texto):
        return campos
    for i, l in enumerate(linhas, 1):
        m = RE_TYPEORM_CLASSE.search(l)
        if m and "class" in l:
            classe = m.group(1)
        if "@Column" in l or "@PrimaryGeneratedColumn" in l or "@PrimaryColumn" in l:
            esperando_coluna = True
            continue
        if esperando_coluna and classe:
            c = RE_TYPEORM_COLUNA.match(l)
            if c:
                campos.append(Campo(caminho, i, classe, c.group(1), classificar(c.group(1))))
                esperando_coluna = False
    return campos


def tipo_arquivo(nome: str) -> str | None:
    if nome.endswith(".prisma"):
        return "prisma"
    if nome.endswith(".sql"):
        return "sql"
    if nome == "models.py" or nome.endswith("_models.py"):
        return "django"
    if nome.endswith((".entity.ts", ".entity.js")):
        return "typeorm"
    return None


def varrer(raiz: str):
    campos: list[Campo] = []
    arquivos_vistos: list[str] = []
    for pasta, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in IGNORAR_DIRS]
        for nome in arquivos:
            rel = os.path.relpath(os.path.join(pasta, nome), raiz)
            arquivos_vistos.append(rel)
            tipo = tipo_arquivo(nome)
            if not tipo:
                continue
            try:
                with open(os.path.join(pasta, nome), encoding="utf-8", errors="ignore") as f:
                    linhas = f.read().splitlines()
            except OSError:
                continue
            extrator = {"prisma": extrair_prisma, "sql": extrair_sql,
                        "django": extrair_django, "typeorm": extrair_typeorm}[tipo]
            campos.extend(extrator(rel, linhas))
    return campos, arquivos_vistos


def detectar_camadas(arquivos: list[str]) -> dict[str, list[str]]:
    achados: dict[str, list[str]] = defaultdict(list)
    for camada, marcadores in MARCADORES_STACK.items():
        for mk in marcadores:
            for a in arquivos:
                a_norm = a.replace(os.sep, "/")
                ok = (a_norm.endswith(mk[1:]) if mk.startswith("*") else
                      (os.path.basename(a_norm) == mk or f"/{mk}/" in f"/{a_norm}"
                       or a_norm.startswith(mk)))
                if ok:
                    achados[camada].append(mk)
                    break
    return {k: sorted(set(v)) for k, v in achados.items()}


def sugerir_nicho(campos: list[Campo]) -> list[tuple[str, int]]:
    contagem: Counter = Counter()
    nomes = {normalizar(c.tabela) for c in campos} | {normalizar(c.campo) for c in campos}
    for nicho, sinais in NICHOS.items():
        for n in nomes:
            if any(s in n for s in sinais):
                contagem[nicho] += 1
    return contagem.most_common()


ROTULOS = {
    "sensivel": "Sensível (art. 11)",
    "identificador_direto": "Identificador direto",
    "quase_identificador": "Quase-identificador",
    "financeiro": "Financeiro",
    "autenticacao": "Autenticação",
    "tempo": "Metadado de tempo",
    "outro": "Outro",
}


def relatorio_md(raiz: str, campos: list[Campo], camadas, nichos) -> str:
    pessoais = [c for c in campos if c.categoria != "outro"]
    por_cat = Counter(c.categoria for c in campos)
    out = ["# Inventário inicial de dados", "",
           f"Gerado por `lgpd-descoberta/scripts/inventario.py` a partir de `{raiz}`. "
           "A classificação é feita por nome de campo e **precisa de revisão humana**.", ""]
    out += ["## Camadas detectadas", ""]
    if camadas:
        for k, v in camadas.items():
            out.append(f"- **{k}:** {', '.join(v)}")
    else:
        out.append("- Nenhum marcador encontrado.")
    out += ["", "## Nicho sugerido", ""]
    if nichos:
        out.append("| Nicho | Sinais encontrados |")
        out.append("|---|---|")
        for n, q in nichos:
            out.append(f"| {n} | {q} |")
        out.append("")
        out.append("Confirme com o usuário antes de seguir.")
    else:
        out.append("Nenhum sinal claro: classifique como **geral** e pergunte ao usuário.")
    out += ["", "## Resumo por categoria", "", "| Categoria | Campos |", "|---|---|"]
    for cat in ["sensivel", "identificador_direto", "quase_identificador", "financeiro",
                "autenticacao", "tempo", "outro"]:
        out.append(f"| {ROTULOS[cat]} | {por_cat.get(cat, 0)} |")
    out += ["", "## Campos com possível dado pessoal", ""]
    if pessoais:
        out.append("| Tabela | Campo | Categoria | Onde |")
        out.append("|---|---|---|---|")
        ordem = list(ROTULOS)
        for c in sorted(pessoais, key=lambda x: (ordem.index(x.categoria), x.tabela, x.campo)):
            out.append(f"| {c.tabela} | {c.campo} | {ROTULOS[c.categoria]} | `{c.arquivo}:{c.linha}` |")
    else:
        out.append("Nenhum campo classificado. Verifique se o projeto define o esquema em "
                   "outro formato (ORM, JSON, NoSQL) e faça o inventário manualmente.")
    sens_tabs = {c.tabela for c in campos if c.categoria == "sensivel"}
    id_tabs = {c.tabela for c in campos if c.categoria == "identificador_direto"}
    juntos = sorted(sens_tabs & id_tabs)
    out += ["", "## Alertas iniciais", ""]
    alertas = []
    if juntos:
        alertas.append(f"Tabelas com identificador direto **e** dado sensível juntos: "
                       f"{', '.join(juntos)}. Verifique a separação por pseudônimo (RF-23).")
    if por_cat.get("autenticacao"):
        alertas.append("Há campos de autenticação: confira se senhas usam hash lento "
                       "(Argon2, bcrypt, scrypt) e se segredos não estão no banco em claro.")
    if any("responsavel" in normalizar(c.campo) or "guardian" in normalizar(c.campo)
           for c in campos):
        alertas.append("Há campos de responsável: possível tratamento de dados de crianças "
                       "ou adolescentes (art. 14).")
    out += [f"- {a}" for a in alertas] or ["- Nenhum alerta automático."]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("raiz", help="pasta raiz do projeto")
    ap.add_argument("--saida", help="arquivo Markdown de saída (padrão: imprime na tela)")
    ap.add_argument("--json", action="store_true", help="imprime o resultado em JSON")
    args = ap.parse_args()
    if not os.path.isdir(args.raiz):
        print(f"Pasta não encontrada: {args.raiz}", file=sys.stderr)
        return 1
    campos, arquivos = varrer(args.raiz)
    camadas = detectar_camadas(arquivos)
    nichos = sugerir_nicho(campos)
    if args.json:
        print(json.dumps({"camadas": camadas, "nichos": nichos,
                          "campos": [asdict(c) for c in campos]}, ensure_ascii=False, indent=2))
        return 0
    md = relatorio_md(args.raiz, campos, camadas, nichos)
    if args.saida:
        os.makedirs(os.path.dirname(os.path.abspath(args.saida)), exist_ok=True)
        with open(args.saida, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Inventário salvo em {args.saida} ({len(campos)} campos analisados).")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
