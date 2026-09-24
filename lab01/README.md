# Lab 01 — Report / Registo

[English](#english) · [Português](#português)

---

## English

**Machine:** AMD Ryzen 7 8840HS (Windows 11) · confirmed with `descobrir_maquina.py` and `Get-CimInstance Win32_Processor`

### B — Your machine

- Logical cores: 16
- Physical cores: 8
- Memory: 15.3 GiB total
- GIL enabled: True

**Question B2:** I can run 8 CPU-bound programs at the same time without them slowing each other down (one per physical core); beyond that, the 16 logical "threads" share only 8 real cores (SMT/hyperthreading) and start competing with each other.

### C — First measurement (`medir.py`, 3 runs)

| Task      | 1st    | 2nd    | 3rd    | median |
|-----------|--------|--------|--------|--------|
| CPU-bound | 9.58 s | 9.39 s | 9.24 s | 9.39 s |
| I/O-bound | 5.01 s | 5.02 s | 5.01 s | 5.01 s |

The I/O-bound task barely changes between runs, because it is just waiting (`time.sleep`). The CPU-bound task varies more, because it depends on what else is running on the machine at that moment.

### Prediction vs demonstration (`demo_docente.py`)

**Prediction before running:** with 8 physical cores, I expected a speedup between 6× and 8×.

**Measured result:**

```
1 core (sequencial)   :  31.95 s  -> 283146 primos
16 cores (processos)  :   3.78 s  -> 283146 primos
Speedup = 31.95 / 3.78 = 8.4x
```

The prediction held and was even slightly exceeded. The number of primes matches on both lines (283146), so the parallel result is correct.

Why is the speedup not equal to the number of cores (16)?

- There are only 8 physical cores; the other 8 are SMT, which does not double the computing power, it only uses the moments when a core is idle waiting for memory. The realistic ceiling is ~8–10×, not 16×.
- Creating 16 processes on Windows (each one starts a new Python) and distributing the work has a cost that the sequential version does not pay.
- Blocks with larger numbers take longer, so at the end some cores sit idle waiting for the last one.
- With all cores at 100% the laptop lowers its frequency (less turbo).

The 8.4× is somewhat inflated: the sequential version took 31.95 s, versus 25.79 s in an earlier run of the same code (little free RAM, background programs, heat). With that value the speedup would be 25.79 / 3.78 ≈ 6.8×, so the real value lies between 6.8× and 8.4×. A first run inside a coding assistant's terminal gave only 1.7×, because that environment limited the child processes.

### Difference between CPU-bound and I/O-bound

In a CPU-bound task the processor is always computing (one core goes up to 100%) and only more cores help; in an I/O-bound task the processor is almost idle, waiting for the network or disk, so overlapping several waits at the same time (threads or asyncio) helps more than having more cores.

---

## Português

**Máquina:** AMD Ryzen 7 8840HS (Windows 11) · confirmada com `descobrir_maquina.py` e `Get-CimInstance Win32_Processor`

### B — A tua máquina

- Cores lógicos: 16
- Cores físicos: 8
- Memória: 15.3 GiB total
- GIL ativo: True

**Pergunta B2:** consigo correr 8 programas CPU-bound ao mesmo tempo sem que se atrasem uns aos outros (um por cada core físico); acima disso, os 16 "fios" lógicos partilham só 8 cores reais (SMT/hyperthreading) e começam a competir entre si.

### C — Primeira medição (`medir.py`, 3 execuções)

| Tarefa    | 1.ª    | 2.ª    | 3.ª    | mediana |
|-----------|--------|--------|--------|---------|
| CPU-bound | 9.58 s | 9.39 s | 9.24 s | 9.39 s  |
| I/O-bound | 5.01 s | 5.02 s | 5.01 s | 5.01 s  |

A tarefa I/O-bound quase não varia entre execuções, porque é só espera (`time.sleep`). A CPU-bound varia mais, porque depende de que mais está a correr na máquina nesse momento.

### Previsão vs demonstração (`demo_docente.py`)

**Previsão antes de correr:** com 8 cores físicos, esperava um speedup entre 6× e 8×.

**Resultado medido:**

```
1 core (sequencial)   :  31.95 s  -> 283146 primos
16 cores (processos)  :   3.78 s  -> 283146 primos
Speedup = 31.95 / 3.78 = 8.4x
```

A previsão cumpriu-se e até foi ligeiramente ultrapassada. O número de primos coincide nas duas linhas (283146), por isso o resultado paralelo está correto.

Porque é que o speedup não é igual ao número de cores (16)?

- Só há 8 cores físicos; os outros 8 são SMT, que não duplica a potência, apenas aproveita os momentos em que o core está parado à espera da memória. O teto realista fica em ~8–10×, não 16×.
- Criar 16 processos em Windows (cada um arranca um Python novo) e distribuir o trabalho tem um custo que a versão sequencial não paga.
- Os blocos com números grandes demoram mais, por isso no fim há cores parados à espera do último.
- Com todos os cores a 100% o portátil baixa a frequência (menos turbo).

O 8,4× está um pouco inflacionado: a versão sequencial demorou 31,95 s, contra 25,79 s numa execução anterior com o mesmo código (pouca RAM livre, programas em segundo plano, aquecimento). Com esse valor o speedup seria 25,79 / 3,78 ≈ 6,8×, por isso o valor real anda entre 6,8× e 8,4×. Uma primeira execução dentro do terminal de um assistente de programação deu só 1,7×, porque esse ambiente limitava os processos filhos.

### Diferença entre CPU-bound e I/O-bound

Numa tarefa CPU-bound o processador está sempre a calcular (um core sobe a 100%) e só ajuda ter mais cores; numa tarefa I/O-bound o processador está quase parado à espera de rede ou disco, por isso ajuda mais sobrepor várias esperas ao mesmo tempo (threads ou asyncio) do que ter mais cores.
