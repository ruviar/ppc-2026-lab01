"""Extra do Lab 01 — o mesmo problema com 1 core, com processos e com threads.

Corre duas vezes e compara:
    uv run python comparar.py                                  # Python normal (GIL ativo)
    uv run --no-project --python 3.14t python comparar.py      # Python free-threaded (sem GIL)

Opcional: um limite mais pequeno para testar rápido, ex.: python comparar.py 500000
"""

import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from demo_docente import LIMITE, N_BLOCOS, blocos, contar_intervalo


def cronometrar(nome: str, funcao) -> float:
    t0 = time.perf_counter()
    total = funcao()
    t = time.perf_counter() - t0
    print(f"{nome:<24}: {t:6.2f} s  -> {total} primos")
    return t


def main() -> None:
    limite = int(sys.argv[1]) if len(sys.argv) > 1 else LIMITE
    cores = os.cpu_count()
    gil = sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else True
    print(f"Python {sys.version.split()[0]} · GIL ativo: {gil} · {cores} cores lógicos · primos até {limite:,}\n")

    t_seq = cronometrar("1 core (sequencial)",
                        lambda: sum(contar_intervalo(b) for b in blocos(limite, N_BLOCOS)))

    def com(executor_cls):
        with executor_cls(max_workers=cores) as pool:
            return sum(pool.map(contar_intervalo, blocos(limite, N_BLOCOS)))

    t_proc = cronometrar(f"{cores} processos", lambda: com(ProcessPoolExecutor))
    t_thr = cronometrar(f"{cores} threads", lambda: com(ThreadPoolExecutor))

    print(f"\nSpeedup processos: {t_seq / t_proc:.1f}x")
    print(f"Speedup threads  : {t_seq / t_thr:.1f}x")


if __name__ == "__main__":
    main()
