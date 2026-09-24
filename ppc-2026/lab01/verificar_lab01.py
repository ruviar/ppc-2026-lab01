"""Universidade Politécnica da Guarda · LCDIA · Programação Paralela e Concorrente · 2026/2027

Lab 01 — Verificador: confirma, na TUA máquina, que o laboratório ficou completo.

Uso (dentro da pasta lab01 do teu projeto):
    uv run python verificar_lab01.py

Funciona igual em macOS, Windows e Linux. Cada linha começa por:
    [OK]     está feito
    [AVISO]  não impede a entrega, mas lê a sugestão
    [FALHA]  falta fazer; a sugestão diz o quê
"""

import importlib
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
contagem = {"OK": 0, "AVISO": 0, "FALHA": 0}


def linha(estado: str, texto: str, sugestao: str = "") -> None:
    contagem[estado] += 1
    print(f"[{estado}]".ljust(8), texto)
    if sugestao and estado != "OK":
        print(" " * 8, "->", sugestao)


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=AQUI, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def main() -> int:
    print("Verificador do Lab 01\n" + "-" * 60)

    # 1. Python e ambiente do projeto
    v = sys.version_info
    if v >= (3, 13):
        linha("OK", f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        linha("FALHA", f"Python {v.major}.{v.minor}: a UC usa 3.13 ou superior", "uv python install 3.13 e corre com 'uv run python ...'")
    if sys.prefix != sys.base_prefix:
        linha("OK", "a correr no ambiente do projeto (.venv)")
    else:
        linha("FALHA", "não estás no ambiente do projeto", "corre com 'uv run python verificar_lab01.py' dentro de ppc-2026/lab01")

    # 2. Bibliotecas
    for modulo in ("psutil", "matplotlib"):
        try:
            importlib.import_module(modulo)
            linha("OK", f"biblioteca {modulo} instalada")
        except ImportError:
            linha("FALHA", f"biblioteca {modulo} em falta", f"uv add {modulo}")

    # 3. Ficheiros do laboratório
    em_falta = [f for f in ("descobrir_maquina.py", "medir.py", "demo_docente.py") if not os.path.exists(os.path.join(AQUI, f))]
    if not em_falta:
        linha("OK", "ficheiros do lab presentes (descobrir_maquina, medir, demo_docente)")
    else:
        linha("FALHA", "ficheiros em falta: " + ", ".join(em_falta), "descarrega-os do Moodle da UC para esta pasta")

    # 4. O código dá o resultado certo? (há 1229 primos abaixo de 10 000, em qualquer máquina)
    try:
        from medir import contar_primos
        n = contar_primos(10_000)
        if n == 1229:
            linha("OK", "contar_primos(10000) = 1229")
        else:
            linha("FALHA", f"contar_primos(10000) = {n}, devia ser 1229", "o medir.py foi alterado; volta a descarregá-lo")
    except Exception as erro:  # noqa: BLE001
        linha("FALHA", f"não consegui importar medir.py ({erro})", "confirma que medir.py está nesta pasta")

    # 5. O teu README
    readme = os.path.join(AQUI, "README.md")
    if not os.path.exists(readme):
        linha("FALHA", "falta o lab01/README.md", "cria-o com a tabela de tempos, a previsão e a tua frase")
    else:
        texto = open(readme, encoding="utf-8", errors="replace").read()
        linhas_uteis = [l for l in texto.splitlines() if l.strip()]
        if "|" in texto and len(linhas_uteis) >= 8:
            linha("OK", f"README.md com tabela ({len(linhas_uteis)} linhas)")
        else:
            linha("AVISO", "README.md existe mas parece incompleto", "precisa da tabela de tempos (com |), da previsão vs resultado e da tua frase")

    # 6. git
    if not shutil.which("git"):
        linha("FALHA", "git não está instalado", "macOS: xcode-select --install | Windows: winget install Git.Git | Linux: sudo apt install git")
    elif git("rev-parse", "--is-inside-work-tree") != "true":
        linha("FALHA", "esta pasta não está dentro de um repositório git", "cria o projeto com 'uv init' (passo A2) ou corre 'git init' em ppc-2026")
    else:
        commits = git("rev-list", "--count", "HEAD")
        if commits and int(commits) >= 1:
            linha("OK", f"repositório git com {commits} commit(s)")
        else:
            linha("FALHA", "ainda não fizeste nenhum commit", 'git add . ; git commit -m "Lab 01"')
        if git("status", "--porcelain"):
            linha("AVISO", "há alterações por guardar no git", 'git add . ; git commit -m "Lab 01"')
        if git("remote"):
            linha("OK", "repositório ligado a um remoto (GitHub)")
        else:
            linha("AVISO", "ainda não ligaste o repositório ao GitHub", "VS Code: Source Control > Publish to GitHub (privado). Não bloqueia a entrega; o docente ajuda")

    print("-" * 60)
    total = sum(contagem.values())
    print(f"Resultado: {contagem['OK']} de {total} OK, {contagem['AVISO']} aviso(s), {contagem['FALHA']} falha(s)")
    return 1 if contagem["FALHA"] else 0


if __name__ == "__main__":
    sys.exit(main())
