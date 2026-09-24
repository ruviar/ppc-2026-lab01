"""Universidade Politécnica da Guarda · LCDIA · Programação Paralela e Concorrente · 2026/2027

Lab 01 — Demonstração: o mesmo problema em 1 core e em todos os cores.

NÃO é preciso perceber ainda como funciona: é só para ver a diferença.
Na aula 2 vamos usar isto como 'caixa preta'; na aula 14 abrimos a caixa.

Uso:
    python demo_docente.py
"""

import os
import time
from concurrent.futures import ProcessPoolExecutor

from medir import contar_primos  # a função tem de estar num módulo importável (aula 14)

LIMITE = 4_000_000
N_BLOCOS = 32  # dividimos o intervalo em 32 blocos para distribuir pelos cores


def blocos(limite: int, n_blocos: int):
    """Divide [2, limite) em n_blocos intervalos (inicio, fim)."""
    passo = limite // n_blocos
    for i in range(n_blocos):
        inicio = 2 if i == 0 else i * passo
        fim = limite if i == n_blocos - 1 else (i + 1) * passo
        yield inicio, fim


def contar_intervalo(intervalo):
    inicio, fim = intervalo
    from medir import eh_primo
    return sum(1 for n in range(inicio, fim) if eh_primo(n))


def main() -> None:
    cores = os.cpu_count()
    print(f"A contar os primos até {LIMITE:,} ...  (esta máquina tem {cores} cores lógicos)\n")

    t0 = time.perf_counter()
    total_seq = sum(contar_intervalo(b) for b in blocos(LIMITE, N_BLOCOS))
    t_seq = time.perf_counter() - t0
    print(f"{'1 core (sequencial)':<22}: {t_seq:6.2f} s  -> {total_seq} primos")

    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=cores) as pool:
        total_par = sum(pool.map(contar_intervalo, blocos(LIMITE, N_BLOCOS)))
    t_par = time.perf_counter() - t0
    rotulo = f"{cores} cores (processos)"
    print(f"{rotulo:<22}: {t_par:6.2f} s  -> {total_par} primos")

    print(f"\nSpeedup = {t_seq:.2f} / {t_par:.2f} = {t_seq / t_par:.1f}x")
    print("Pergunta: porque é que o speedup não é exatamente igual ao número de cores?")


if __name__ == "__main__":  # obrigatório com processos em macOS/Windows (aula 14)
    main()