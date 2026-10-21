#!/usr/bin/env python3
"""
gerar_exemplo.py — gera uma base FICTÍCIA de atendimentos de uma clínica para testar anonimizar.py.

  python3 gerar_exemplo.py --n 2000 --semente 1 --saida exemplo/

Cria:
  exemplo/atendimentos.csv  nome, cpf, idade, sexo, bairro, data_diag, resultado
  exemplo/regioes.csv       bairro -> região (para --mapa bairro=exemplo/regioes.csv)

Os CPFs gerados são aleatórios e os nomes são combinações de listas curtas: não correspondem a pessoas reais.
Gere várias versões com sementes diferentes para repetir a medição e reportar média e desvio padrão.
"""
import argparse
import csv
import datetime as dt
import random
from pathlib import Path

NOMES = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Fábio", "Gabriela", "Hugo", "Isabel", "João",
         "Larissa", "Marcos", "Natália", "Otávio", "Paula", "Rafael", "Sofia", "Tiago", "Vera", "Wagner"]
SOBRENOMES = ["Almeida", "Barbosa", "Cardoso", "Dias", "Esteves", "Ferreira", "Gomes", "Lima",
              "Martins", "Nunes", "Oliveira", "Pereira", "Ramos", "Souza", "Teixeira"]
REGIOES = {
    "Centro": ["Centro", "Bonfim", "Nossa Senhora de Fátima"],
    "Norte": ["Salgado Filho", "Itararé", "Perpétuo Socorro", "Chácara das Flores"],
    "Sul": ["Urlândia", "Tomazetti", "Lorenzi", "Dom Antônio Reis"],
    "Leste": ["Camobi", "Pains", "Diácono João Luiz Pozzobon"],
    "Oeste": ["Juscelino Kubitschek", "Tancredo Neves", "Agroindustrial", "Boi Morto"],
}
RESULTADOS = [("Negativo", 0.70), ("Inconclusivo", 0.08), ("Positivo - tipo A", 0.14),
              ("Positivo - tipo B", 0.08)]


def cpf_aleatorio(rng):
    base = [rng.randint(0, 9) for _ in range(9)]
    for peso in (10, 11):
        s = sum(d * (peso - i) for i, d in enumerate(base))
        dv = (s * 10) % 11
        base.append(0 if dv == 10 else dv)
    d = "".join(map(str, base))
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=2000)
    p.add_argument("--semente", type=int, default=1)
    p.add_argument("--saida", default="exemplo")
    a = p.parse_args()
    rng = random.Random(a.semente)
    out = Path(a.saida)
    out.mkdir(parents=True, exist_ok=True)

    bairros = [(b, r) for r, bs in REGIOES.items() for b in bs]
    pesos_bairro = [3 if r == "Centro" else 2 if r == "Leste" else 1 for _, r in bairros]
    inicio = dt.date(2025, 1, 1)

    with open(out / "regioes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["bairro", "regiao"])
        w.writerows(bairros)

    with open(out / "atendimentos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["nome", "cpf", "idade", "sexo", "bairro", "data_diag", "resultado"])
        for _ in range(a.n):
            idade = max(0, min(99, int(rng.gauss(42, 18))))
            sexo = rng.choice(["F", "M"])
            bairro = rng.choices([b for b, _ in bairros], weights=pesos_bairro)[0]
            data = inicio + dt.timedelta(days=rng.randint(0, 364))
            resultado = rng.choices([r for r, _ in RESULTADOS], weights=[p for _, p in RESULTADOS])[0]
            nome = f"{rng.choice(NOMES)} {rng.choice(SOBRENOMES)} {rng.choice(SOBRENOMES)}"
            w.writerow([nome, cpf_aleatorio(rng), idade, sexo, bairro, data.isoformat(), resultado])
    print(f"Base fictícia gerada em {out}/ ({a.n} registros, semente {a.semente})")


if __name__ == "__main__":
    main()
