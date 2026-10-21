#!/usr/bin/env python3
"""
anonimizar.py — mede e reduz o risco de reidentificação de uma extração tabular (CSV).

Sem dependências: só a biblioteca padrão do Python 3.9+.

Modos
-----
  medir     mede o risco do arquivo como está.
  aplicar   aplica generalização e supressão (k e, opcionalmente, l) e grava o CSV anonimizado.
  comparar  roda as configurações C0 a C4 e gera uma tabela de risco e utilidade.

Exemplos
--------
  python3 anonimizar.py medir dados.csv --qi idade,sexo,bairro,data_diag --sensivel resultado

  python3 anonimizar.py comparar dados.csv \
      --qi idade,sexo,bairro,data_diag --sensivel resultado \
      --remover nome,cpf \
      --faixa idade=10 --data data_diag=trimestre --mapa bairro=regioes.csv \
      --k 2,5,10 --l 2 --estatistica bairro --risco-aceitavel 0.2

Métricas (esquema do estudo preliminar da ANPD sobre anonimização, 2023)
-----------------------------------------------------------------------
  grupo            registros com a mesma combinação de quase-identificadores
  k                tamanho do menor grupo
  risco médio      média, entre os registros, de 1 / tamanho do grupo do registro
  risco máximo     1 / k (pior caso, atacante que conhece a vítima)
  únicos           % de registros sozinhos no seu grupo
  l                menor número de valores distintos do atributo sensível em um grupo
  homogêneos       grupos em que todos têm o mesmo valor do atributo sensível
  suprimidos       % de registros removidos
  distorção        maior diferença, em pontos percentuais, na proporção por categoria
                   da coluna --estatistica entre a base original e a liberada
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


# ---------------------------------------------------------------- leitura

def ler_csv(caminho: str) -> tuple[list[str], list[dict]]:
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        amostra = f.read(4096)
        f.seek(0)
        try:
            dialeto = csv.Sniffer().sniff(amostra, delimiters=",;\t")
        except csv.Error:
            dialeto = csv.excel
        leitor = csv.DictReader(f, dialect=dialeto)
        linhas = [dict(l) for l in leitor]
        return list(leitor.fieldnames or []), linhas


def gravar_csv(caminho: str, colunas: list[str], linhas: list[dict]) -> None:
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=colunas, extrasaction="ignore")
        w.writeheader()
        w.writerows(linhas)


def lista(txt: str | None) -> list[str]:
    return [c.strip() for c in (txt or "").split(",") if c.strip()]


def pares(valores: list[str] | None) -> dict[str, str]:
    out = {}
    for v in valores or []:
        if "=" not in v:
            sys.exit(f"Use coluna=valor: {v}")
        c, x = v.split("=", 1)
        out[c.strip()] = x.strip()
    return out


# ---------------------------------------------------------------- generalização

def faixa(valor: str, largura: int) -> str:
    try:
        n = int(float(valor.replace(",", ".")))
    except ValueError:
        return "*"
    ini = (n // largura) * largura
    return f"{ini}-{ini + largura - 1}"


def ler_data(valor: str) -> dt.date | None:
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return dt.datetime.strptime(valor[:19], fmt).date()
        except ValueError:
            continue
    return None


def generalizar_data(valor: str, nivel: str) -> str:
    d = ler_data(valor)
    if d is None:
        return "*"
    if nivel == "ano":
        return f"{d.year}"
    if nivel == "semestre":
        return f"{d.year}-S{1 if d.month <= 6 else 2}"
    if nivel == "trimestre":
        return f"{d.year}-T{(d.month - 1) // 3 + 1}"
    if nivel == "mes":
        return f"{d.year}-{d.month:02d}"
    sys.exit(f"Nível de data desconhecido: {nivel} (use mes, trimestre, semestre ou ano)")


def ler_mapa(caminho: str) -> dict[str, str]:
    """CSV com duas colunas: valor original, valor generalizado."""
    _, linhas = ler_csv(caminho)
    mapa = {}
    for l in linhas:
        v = list(l.values())
        if len(v) >= 2:
            mapa[str(v[0]).strip().lower()] = str(v[1]).strip()
    return mapa


class Regras:
    def __init__(self, args):
        self.faixas = {c: int(v) for c, v in pares(args.faixa).items()}
        self.datas = pares(args.data)
        self.truncar = {c: int(v) for c, v in pares(args.truncar).items()}
        self.mapas = {c: ler_mapa(v) for c, v in pares(args.mapa).items()}

    def existe(self) -> bool:
        return any([self.faixas, self.datas, self.truncar, self.mapas])

    def aplicar(self, coluna: str, valor: str) -> str:
        valor = (valor or "").strip()
        if coluna in self.faixas:
            return faixa(valor, self.faixas[coluna])
        if coluna in self.datas:
            return generalizar_data(valor, self.datas[coluna])
        if coluna in self.truncar:
            n = self.truncar[coluna]
            digitos = "".join(ch for ch in valor if ch.isalnum())
            return digitos[:n] + "*" * max(0, len(digitos) - n)
        if coluna in self.mapas:
            return self.mapas[coluna].get(valor.lower(), "Outros")
        return valor

    def descrever(self) -> list[str]:
        d = [f"{c}: faixas de {v}" for c, v in self.faixas.items()]
        d += [f"{c}: {v}" for c, v in self.datas.items()]
        d += [f"{c}: {v} primeiros caracteres" for c, v in self.truncar.items()]
        d += [f"{c}: mapa de agrupamento" for c in self.mapas]
        return d


# ---------------------------------------------------------------- métricas

def chave(linha: dict, qi: list[str]) -> tuple:
    return tuple((linha.get(c) or "").strip() for c in qi)


def medir(linhas: list[dict], qi: list[str], sensivel: str | None) -> dict:
    n = len(linhas)
    if n == 0:
        return {"registros": 0, "grupos": 0, "k": 0, "risco_medio": 0.0, "risco_maximo": 0.0,
                "unicos_pct": 0.0, "l": None, "homogeneos": None}
    grupos: dict[tuple, list[dict]] = defaultdict(list)
    for l in linhas:
        grupos[chave(l, qi)].append(l)
    tamanhos = [len(g) for g in grupos.values()]
    k = min(tamanhos)
    risco_medio = sum(1 / len(g) for g in grupos.values() for _ in g) / n
    unicos = sum(1 for t in tamanhos if t == 1)
    res = {
        "registros": n,
        "grupos": len(grupos),
        "k": k,
        "risco_medio": risco_medio,
        "risco_maximo": 1 / k,
        "unicos_pct": 100 * unicos / n,
        "l": None,
        "homogeneos": None,
    }
    if sensivel:
        distintos = [len({(x.get(sensivel) or "").strip() for x in g}) for g in grupos.values()]
        res["l"] = min(distintos)
        res["homogeneos"] = sum(1 for d in distintos if d == 1)
    return res


def distorcao(originais: list[dict], liberados_idx: list[int], coluna: str, regras: Regras) -> tuple[float, float]:
    """Maior e média das diferenças, em pontos percentuais, por categoria."""
    if not coluna or not originais:
        return 0.0, 0.0
    analitico = [regras.aplicar(coluna, l.get(coluna, "")) for l in originais]
    antes = Counter(analitico)
    depois = Counter(analitico[i] for i in liberados_idx)
    n0, n1 = len(originais), max(len(liberados_idx), 1)
    difs = [abs(100 * antes[c] / n0 - 100 * depois.get(c, 0) / n1) for c in antes]
    if not liberados_idx:
        return 100.0, 100.0
    return max(difs), sum(difs) / len(difs)


# ---------------------------------------------------------------- transformações

def generalizar(linhas: list[dict], qi: list[str], regras: Regras) -> list[dict]:
    out = []
    for l in linhas:
        nova = dict(l)
        for c in qi:
            nova[c] = regras.aplicar(c, l.get(c, ""))
        out.append(nova)
    return out


def suprimir(linhas: list[dict], idx: list[int], qi: list[str], k: int,
             sensivel: str | None, l_min: int | None) -> list[int]:
    """Remove os registros de grupos com menos de k registros ou menos de l valores sensíveis."""
    grupos: dict[tuple, list[int]] = defaultdict(list)
    for i in idx:
        grupos[chave(linhas[i], qi)].append(i)
    manter = []
    for membros in grupos.values():
        if len(membros) < k:
            continue
        if l_min and sensivel:
            if len({(linhas[i].get(sensivel) or "").strip() for i in membros}) < l_min:
                continue
        manter.extend(membros)
    return sorted(manter)


# ---------------------------------------------------------------- configurações

def rodar(config: str, originais, qi, sensivel, regras, k=1, l_min=None):
    idx = list(range(len(originais)))
    if config in ("C1", "C3", "C4"):
        base = generalizar(originais, qi, regras)
    else:
        base = [dict(l) for l in originais]
    if config == "C2":
        idx = suprimir(base, idx, qi, 2, None, None)
    elif config in ("C3", "C4"):
        idx = suprimir(base, idx, qi, k, sensivel, l_min if config == "C4" else None)
    liberadas = [base[i] for i in idx]
    return liberadas, idx


def linha_resultado(nome, desc, m, n0, idx, originais, est, regras, aceitavel):
    d_max, d_med = distorcao(originais, idx, est, regras) if est else (0.0, 0.0)
    sup = 100 * (n0 - len(idx)) / n0 if n0 else 0
    ok = None if aceitavel is None else (m["registros"] > 0 and m["risco_medio"] <= aceitavel)
    return {
        "config": nome, "descricao": desc, **m,
        "suprimidos_pct": sup, "distorcao_max_pp": d_max, "distorcao_media_pp": d_med,
        "abaixo_do_aceitavel": ok,
    }


def fmt(x, casas=3):
    if x is None:
        return "—"
    if isinstance(x, bool):
        return "sim" if x else "não"
    if isinstance(x, float):
        return f"{x:.{casas}f}".replace(".", ",")
    return str(x)


def tabela_md(resultados: list[dict], tem_sensivel: bool, tem_est: bool, tem_aceitavel: bool) -> str:
    cab = ["Config.", "Tratamento", "Registros", "k", "Risco médio", "Risco máximo", "Únicos (%)"]
    if tem_sensivel:
        cab += ["l", "Grupos homogêneos"]
    cab += ["Suprimidos (%)"]
    if tem_est:
        cab += ["Distorção máx. (p.p.)"]
    if tem_aceitavel:
        cab += ["Abaixo do aceitável"]
    linhas = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    for r in resultados:
        v = [r["config"], r["descricao"], fmt(r["registros"]), fmt(r["k"]), fmt(r["risco_medio"]),
             fmt(r["risco_maximo"]), fmt(r["unicos_pct"], 1)]
        if tem_sensivel:
            v += [fmt(r["l"]), fmt(r["homogeneos"])]
        v += [fmt(r["suprimidos_pct"], 1)]
        if tem_est:
            v += [fmt(r["distorcao_max_pp"], 1)]
        if tem_aceitavel:
            v += [fmt(r["abaixo_do_aceitavel"])]
        linhas.append("| " + " | ".join(v) + " |")
    return "\n".join(linhas)


def relatorio(args, regras, resultados, entrada, removidas) -> str:
    hoje = dt.date.today().isoformat()
    tem_s = bool(args.sensivel)
    tem_e = bool(args.estatistica)
    tem_a = args.risco_aceitavel is not None
    partes = [
        f"# Relatório de anonimização — {Path(entrada).name}",
        "",
        f"- **Data:** {hoje}",
        f"- **Quase-identificadores:** {', '.join(args.qi_lista)}",
        f"- **Atributo sensível:** {args.sensivel or 'não informado'}",
        f"- **Identificadores diretos removidos:** {', '.join(removidas) or 'nenhum informado'}",
        f"- **Generalização:** {'; '.join(regras.descrever()) or 'nenhuma'}",
        f"- **Risco aceitável definido pelo controlador:** "
        + (fmt(args.risco_aceitavel) if tem_a else "não definido"),
        "",
        "## Resultados",
        "",
        tabela_md(resultados, tem_s, tem_e, tem_a),
        "",
        "## Como ler",
        "",
        "- **Risco médio:** probabilidade média de acerto de um atacante que tenta reidentificar "
        "qualquer pessoa da base (perfil jornalista). Calculado como a média de 1/tamanho do grupo.",
        "- **Risco máximo:** pior caso para quem conhece a vítima e sabe que ela está na base "
        "(perfil promotor): 1/k.",
        "- **Grupos homogêneos:** grupos em que todos têm o mesmo valor sensível. Mesmo com k "
        "atendido, revelam a condição de quem pertence ao grupo (risco de inferência).",
        "- **Distorção:** quanto a proporção por categoria mudou depois da supressão. É a perda "
        "de utilidade para a finalidade do relatório.",
        "",
        "## Limites desta medição",
        "",
        "- A medição considera apenas os quase-identificadores informados. Um atacante com outra "
        "informação auxiliar pode ter risco diferente.",
        "- O risco aceitável é decisão do controlador e depende do contexto (art. 12, § 1º). "
        "A ANPD não fixa um valor.",
        "- Dados anonimizados podem voltar a ser pessoais se a reversão se tornar possível com "
        "esforço razoável (art. 12). Reavalie quando a base ou o contexto mudarem.",
    ]
    return "\n".join(partes) + "\n"


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(description="Mede e reduz o risco de reidentificação de um CSV.")
    p.add_argument("modo", choices=["medir", "aplicar", "comparar"])
    p.add_argument("csv")
    p.add_argument("--qi", required=True, help="quase-identificadores, separados por vírgula")
    p.add_argument("--sensivel", help="atributo sensível (para l-diversidade)")
    p.add_argument("--remover", help="identificadores diretos a remover (nome, cpf, email...)")
    p.add_argument("--faixa", action="append", help="coluna=largura (ex.: idade=10)")
    p.add_argument("--data", action="append", help="coluna=mes|trimestre|semestre|ano")
    p.add_argument("--truncar", action="append", help="coluna=n (mantém n caracteres; ex.: cep=5)")
    p.add_argument("--mapa", action="append", help="coluna=arquivo.csv (valor,grupo)")
    p.add_argument("--k", default="5", help="k mínimo; no modo comparar aceita lista: 2,5,10")
    p.add_argument("--l", type=int, help="l mínimo (l-diversidade)")
    p.add_argument("--estatistica", help="coluna cuja distribuição o relatório precisa preservar")
    p.add_argument("--risco-aceitavel", type=float, help="limite de risco médio definido pelo controlador")
    p.add_argument("--saida", default=".lgpd/anonimizacao", help="pasta de saída")
    p.add_argument("--json", action="store_true", help="imprime os resultados em JSON")
    args = p.parse_args()

    colunas, originais = ler_csv(args.csv)
    args.qi_lista = lista(args.qi)
    faltando = [c for c in args.qi_lista + ([args.sensivel] if args.sensivel else []) if c not in colunas]
    if faltando:
        sys.exit(f"Colunas não encontradas no CSV: {', '.join(faltando)}")
    removidas = [c for c in lista(args.remover) if c in colunas]
    colunas_saida = [c for c in colunas if c not in removidas]
    regras = Regras(args)
    ks = [int(x) for x in lista(args.k)] or [5]
    n0 = len(originais)
    qi = args.qi_lista
    resultados = []

    if args.modo == "medir":
        m = medir(originais, qi, args.sensivel)
        resultados.append(linha_resultado("Atual", "Como está", m, n0, list(range(n0)),
                                          originais, args.estatistica, regras, args.risco_aceitavel))
    elif args.modo == "aplicar":
        k = ks[0]
        conf = "C4" if args.l else "C3"
        liberadas, idx = rodar(conf, originais, qi, args.sensivel, regras, k, args.l)
        m = medir(liberadas, qi, args.sensivel)
        desc = f"Generalização + k={k}" + (f" + l={args.l}" if args.l else "")
        resultados.append(linha_resultado(conf, desc, m, n0, idx, originais, args.estatistica,
                                          regras, args.risco_aceitavel))
        destino = Path(args.saida) / (Path(args.csv).stem + "_anonimizado.csv")
        gravar_csv(str(destino), colunas_saida, liberadas)
        print(f"CSV anonimizado: {destino}")
    else:
        if not regras.existe():
            print("Aviso: sem regras de generalização, C1, C3 e C4 equivalem a C0 e C2.", file=sys.stderr)
        plano = [("C0", "Sem tratamento", None, None), ("C1", "Generalização", None, None),
                 ("C2", "Supressão dos únicos", None, None)]
        plano += [("C3", f"Generalização + k={k}", k, None) for k in ks]
        if args.l:
            plano += [("C4", f"C3 (k={k}) + l={args.l}", k, args.l) for k in ks]
        for nome, desc, k, l_min in plano:
            liberadas, idx = rodar(nome, originais, qi, args.sensivel, regras, k or 1, l_min)
            m = medir(liberadas, qi, args.sensivel)
            resultados.append(linha_resultado(nome, desc, m, n0, idx, originais, args.estatistica,
                                              regras, args.risco_aceitavel))

    rel = relatorio(args, regras, resultados, args.csv, removidas)
    destino_rel = Path(args.saida) / f"relatorio-{Path(args.csv).stem}-{args.modo}.md"
    destino_rel.parent.mkdir(parents=True, exist_ok=True)
    destino_rel.write_text(rel, encoding="utf-8")
    if args.json:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    else:
        print(tabela_md(resultados, bool(args.sensivel), bool(args.estatistica),
                        args.risco_aceitavel is not None))
    print(f"\nRelatório: {destino_rel}")


if __name__ == "__main__":
    main()
