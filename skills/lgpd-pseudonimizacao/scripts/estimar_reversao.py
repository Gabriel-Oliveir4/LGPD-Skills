#!/usr/bin/env python3
"""
estimar_reversao.py — mostra, em números, por que hash de CPF sem chave não é pseudônimo seguro.

  python3 estimar_reversao.py              # mede a velocidade desta máquina e estima o tempo
  python3 estimar_reversao.py --demo 20    # gera 20 CPFs fictícios num intervalo e reverte os hashes

O que o script faz
------------------
1. Mede quantos SHA-256 por segundo esta máquina calcula em Python puro (bem mais lento que GPU).
2. Estima o tempo para percorrer todos os CPFs possíveis: 10^9 bases de 9 dígitos
   (os 2 dígitos verificadores são calculados, não adivinhados).
3. Com --demo, gera CPFs fictícios cujas bases ficam num intervalo pequeno, calcula
   sha256(cpf) e HMAC-SHA256(chave, cpf), e tenta reverter percorrendo o intervalo.
   O hash sem chave é revertido; o HMAC, sem a chave, não.

A LGPD avalia a reversão pelo esforço razoável, considerando custo e tempo (art. 12, § 1º).
"""
import argparse
import hashlib
import hmac
import random
import secrets
import time


def dv(base: str) -> str:
    nums = [int(c) for c in base]
    for peso in (10, 11):
        s = sum(d * (peso - i) for i, d in enumerate(nums))
        r = (s * 10) % 11
        nums.append(0 if r == 10 else r)
    return "".join(map(str, nums))


def sha(cpf: str) -> str:
    return hashlib.sha256(cpf.encode()).hexdigest()


def medir_velocidade(segundos=2.0) -> float:
    n, ini = 0, time.perf_counter()
    while time.perf_counter() - ini < segundos:
        for i in range(10_000):
            sha(dv(f"{(n + i) % 10**9:09d}"))
        n += 10_000
    return n / (time.perf_counter() - ini)


def legivel(seg: float) -> str:
    if seg < 120:
        return f"{seg:.0f} segundos"
    if seg < 7200:
        return f"{seg / 60:.0f} minutos"
    if seg < 172800:
        return f"{seg / 3600:.1f} horas"
    return f"{seg / 86400:.1f} dias"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--demo", type=int, help="quantidade de CPFs fictícios para a demonstração")
    p.add_argument("--intervalo", type=int, default=2_000_000, help="tamanho do intervalo da demo")
    a = p.parse_args()

    print("Medindo velocidade (2 s)...")
    v = medir_velocidade()
    total = 10**9
    print(f"Velocidade nesta máquina (Python puro): {v:,.0f} CPFs/s".replace(",", "."))
    print(f"Tempo para percorrer todos os CPFs: {legivel(total / v)} em um núcleo")
    print("Uma GPU comum calcula bilhões de SHA-256 por segundo: o mesmo trabalho cai para segundos.\n")

    if not a.demo:
        return

    rng = random.Random()
    inicio = rng.randint(0, 10**9 - a.intervalo)
    chave = secrets.token_bytes(32)
    cpfs = [dv(f"{rng.randint(inicio, inicio + a.intervalo - 1):09d}") for _ in range(a.demo)]
    alvo_sha = {sha(c) for c in cpfs}
    alvo_hmac = {hmac.new(chave, c.encode(), hashlib.sha256).hexdigest() for c in cpfs}

    print(f"Demo: {a.demo} CPFs fictícios com base entre {inicio:09d} e {inicio + a.intervalo - 1:09d}")
    ini = time.perf_counter()
    rev_sha, rev_hmac = 0, 0
    chave_errada = secrets.token_bytes(32)  # o atacante não tem a chave verdadeira
    for b in range(inicio, inicio + a.intervalo):
        c = dv(f"{b:09d}")
        if sha(c) in alvo_sha:
            rev_sha += 1
        if hmac.new(chave_errada, c.encode(), hashlib.sha256).hexdigest() in alvo_hmac:
            rev_hmac += 1
    dur = time.perf_counter() - ini
    print(f"  sha256(cpf) sem chave revertidos: {rev_sha} de {a.demo}")
    print(f"  HMAC-SHA256 com chave revertidos sem a chave: {rev_hmac} de {a.demo}")
    print(f"  Tempo da busca no intervalo: {legivel(dur)}")


if __name__ == "__main__":
    main()
