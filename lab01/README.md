# Lab 01 — Registo

**Máquina:** AMD Ryzen 7 8840HS (Windows 11) · confirmada com `descobrir_maquina.py` e `Get-CimInstance Win32_Processor`

## B — A tua máquina

- Cores lógicos: 16
- Cores físicos: 8
- Memória: 15.3 GiB total
- GIL ativo: True

**Pergunta B2:** consigo correr 8 programas CPU-bound ao mesmo tempo sem que se atrasem uns aos outros (um por cada core físico); acima disso, os 16 "fios" lógicos partilham só 8 cores reais (SMT/hyperthreading) e começam a competir entre si.

## C — Primeira medição (`medir.py`, 3 execuções)

| Tarefa    | 1.ª    | 2.ª    | 3.ª    | mediana |
|-----------|--------|--------|--------|---------|
| CPU-bound | 9.58 s | 9.39 s | 9.24 s | 9.39 s  |
| I/O-bound | 5.01 s | 5.02 s | 5.01 s | 5.01 s  |

A tarefa I/O-bound quase não varia entre execuções, porque é só espera (`time.sleep`). A CPU-bound varia mais, porque depende de que mais está a correr na máquina nesse momento.

## Previsão vs demonstração (`demo_docente.py`)

**Previsão antes de correr:** com 8 cores físicos, esperava um speedup entre 6× e 8×.

**Resultado medido:**

```
1 core (sequencial)   :  25.79 s  -> 283146 primos
16 cores (processos)  :  15.33 s  -> 283146 primos
Speedup = 25.79 / 15.33 = 1.7x
```

O speedup real (1,7×) ficou bem abaixo da previsão. O número de primos coincide nas duas linhas (283146), por isso o resultado está correto — só o tempo variou menos do que o esperado. Isto foi corrido dentro do terminal de um assistente de programação, que pode limitar os recursos dados a processos filhos; a repetir num terminal normal (PowerShell) para confirmar o valor definitivo.

## Diferença entre CPU-bound e I/O-bound

Numa tarefa CPU-bound o processador está sempre a calcular (um core sobe a 100%) e só ajuda ter mais cores; numa tarefa I/O-bound o processador está quase parado à espera de rede ou disco, por isso ajuda mais sobrepor várias esperas ao mesmo tempo (threads ou asyncio) do que ter mais cores.
