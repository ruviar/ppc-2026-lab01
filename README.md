# PPC 2026 — Programação Paralela e Concorrente

Universidade Politécnica da Guarda · Licenciatura em Ciência de Dados e Inteligência Artificial · 2026/2027

## Laboratórios

| Pasta | Conteúdo |
|---|---|
| [lab01/](lab01/) | Lab 01: ambiente, descobrir a máquina, CPU-bound vs I/O-bound, 1 core vs todos os cores |

## Ambiente

Os ficheiros da raiz definem o ambiente partilhado por todos os labs:

- `pyproject.toml` e `uv.lock`: dependências e versões exatas
- `.python-version`: Python 3.13

```powershell
uv sync                  # cria .venv com Python 3.13, psutil e matplotlib
cd lab01
./script.ps1             # executa o Lab 01 completo
```

Instruções e resultados do laboratório: [lab01/README.md](lab01/README.md).
