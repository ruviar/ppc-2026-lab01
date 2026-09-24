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

## Diferença entre CPU-bound e I/O-bound

Numa tarefa CPU-bound o processador está sempre a calcular (um core sobe a 100%) e só ajuda ter mais cores; numa tarefa I/O-bound o processador está quase parado à espera de rede ou disco, por isso ajuda mais sobrepor várias esperas ao mesmo tempo (threads ou asyncio) do que ter mais cores.
