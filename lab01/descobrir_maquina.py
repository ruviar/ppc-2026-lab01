"""Universidade Politécnica da Guarda · LCDIA · Programação Paralela e Concorrente · 2026/2027

Lab 01 — Descobrir a máquina.

Mostra quantos cores tem o computador, quanta memória, que Python e que sistema
operativo. Corre em qualquer máquina só com a biblioteca padrão; se o psutil
estiver instalado, mostra também os cores físicos e a memória.
"""

import os
import platform
import sys


def main() -> None:
    print("=" * 60)
    print("A TUA MÁQUINA")
    print("=" * 60)
    print(f"Sistema operativo : {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Python            : {sys.version.split()[0]}  ({sys.executable})")
    print(f"Cores lógicos     : {os.cpu_count()}   <- o que o sistema mostra ao Python")

    try:
        import psutil  # opcional: uv add psutil
    except ImportError:
        print("Cores físicos     : (instala o psutil para ver)")
        print("Memória           : (instala o psutil para ver)")
    else:
        fisicos = psutil.cpu_count(logical=False)
        mem = psutil.virtual_memory()
        print(f"Cores físicos     : {fisicos}   <- 'verdadeiros'; os lógicos podem ser SMT/hyperthreading")
        print(f"Memória           : {mem.total / 2**30:.1f} GiB total, {mem.available / 2**30:.1f} GiB disponíveis")
        freq = psutil.cpu_freq()
        if freq and freq.max:
            print(f"Frequência máxima : {freq.max:.0f} MHz")

    # Informação sobre o GIL (Python 3.13+): 1 = GIL ativo, 0 = build free-threaded
    if hasattr(sys, "_is_gil_enabled"):
        print(f"GIL ativo         : {sys._is_gil_enabled()}   <- vamos falar disto na aula 24")

    print("=" * 60)
    print("Pergunta: quantos programas CPU-bound consegues correr ao mesmo tempo")
    print("sem que se atrasem uns aos outros? (pista: cores físicos)")


if __name__ == "__main__":
    main()
