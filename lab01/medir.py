"""Universidade Politécnica da Guarda · LCDIA · Programação Paralela e Concorrente · 2026/2027

Lab 01 — A primeira medição: uma tarefa CPU-bound e uma tarefa I/O-bound.

Uso:
    python medir.py            # I/O simulado com time.sleep (funciona sem internet)
    python medir.py --real     # I/O real: descarrega páginas da web

Só usa a biblioteca padrão. Lê o código: é curto de propósito.
"""

import sys
import time
import urllib.request

# ---------------------------------------------------------------- CPU-bound
# Uma tarefa CPU-bound passa o tempo todo a fazer contas. O processador está
# ocupado a 100% num core enquanto ela corre.


def eh_primo(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def contar_primos(limite: int) -> int:
    """Conta os primos em [2, limite). Só faz contas: CPU-bound."""
    return sum(1 for n in range(2, limite) if eh_primo(n))


# ---------------------------------------------------------------- I/O-bound
# Uma tarefa I/O-bound passa a maior parte do tempo À ESPERA: da rede, do disco,
# de uma base de dados. O processador está quase parado enquanto ela espera.

URLS = [f"https://pt.wikipedia.org/wiki/Special:Random?n={i}" for i in range(20)]


def pedido_simulado(i: int, espera: float = 0.25) -> int:
    """Simula um pedido à rede: espera 'espera' segundos sem usar o CPU."""
    time.sleep(espera)
    return i


def pedido_real(url: str) -> int:
    """Descarrega uma página e devolve o número de bytes recebidos."""
    with urllib.request.urlopen(url, timeout=15) as resp:
        return len(resp.read())


# ---------------------------------------------------------------- cronómetro


def cronometrar(nome: str, funcao, *args):
    inicio = time.perf_counter()          # relógio de alta resolução para medir durações
    resultado = funcao(*args)
    duracao = time.perf_counter() - inicio
    print(f"{nome:<34}{duracao:7.2f} s  ->  {resultado}")
    return duracao


def main() -> None:
    real = "--real" in sys.argv
    print(f"{'Tarefa':<34}{'Tempo':>9}      Resultado")
    print("-" * 56)

    # 1) CPU-bound: contar primos até 2 milhões
    cronometrar("CPU-bound: primos até 2 000 000", contar_primos, 2_000_000)

    # 2) I/O-bound: 20 pedidos, um a seguir ao outro
    if real:
        def vinte_pedidos_reais():
            return sum(pedido_real(u) for u in URLS)
        cronometrar("I/O-bound: 20 downloads reais", vinte_pedidos_reais)
    else:
        def vinte_pedidos_simulados():
            return sum(pedido_simulado(i) for i in range(20))
        cronometrar("I/O-bound: 20 pedidos simulados", vinte_pedidos_simulados)

    print("-" * 56)
    print("Enquanto cada tarefa corre, olha para o monitor de atividade:")
    print("  - na CPU-bound, um core está a 100%;")
    print("  - na I/O-bound, o processador está quase parado, à espera.")


if __name__ == "__main__":
    main()