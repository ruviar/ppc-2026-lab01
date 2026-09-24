# Lab 01: cómo ejecutar cada cosa

Todo se ejecuta desde **PowerShell**, dentro de la carpeta `lab01`.

```powershell
cd C:\Users\ruvia\OneDrive\Desktop\kk\Ingenieria\ErasmusGuarda\PSCD\ppc-2026\lab01
```

> **Ejecútalo desde un PowerShell normal.**
> Para medir, **enchufa el portátil** y cierra el navegador y otros programas pesados.

---

## 0. Requisitos (solo la primera vez)

| Qué | Comprobar | Si falta |
|---|---|---|
| uv | `uv --version` | Paso A1 del lab (instalar uv) |
| Python 3.13 | `uv run python --version` | `uv python install 3.13` |
| Librerías | lo dice el verificador | `uv add psutil` / `uv add matplotlib` |
| git | `git --version` | `winget install Git.Git` |

**`uv run` delante de todo:** usa el Python y las librerías del proyecto (`.venv`), no los del sistema ni los de conda. El `(base)` que aparece en el prompt es conda; no afecta si usas `uv run`.

---

## 1. Todo de golpe

```powershell
./script.ps1
```

Ejecuta en orden: descobrir_maquina → medir → demo_docente → verificar_lab01.
Al final dice **"Todos os passos terminaram sem erro."** (verde) o qué pasos fallaron (rojo).

Si Windows no te deja ejecutar scripts:
```powershell
powershell -ExecutionPolicy Bypass -File .\script.ps1
```

Tarda unos 50 s (la mayoría es la demo).

---

## 2. Cada script por separado

Si ves los acentos rotos (`mÃ¡quina`), ejecuta antes esto (dura lo que dure la ventana):
```powershell
$env:PYTHONUTF8 = 1
```

### 2.1 ¿Qué máquina tengo?
```powershell
uv run python descobrir_maquina.py
```
- Muestra cores lógicos (16), físicos (8), RAM y si el GIL está activo.
- Tarda un instante.

### 2.2 CPU-bound frente a I/O-bound
```powershell
uv run python medir.py
```
- Primos hasta 2 M (unos 9 s, 1 core al 100 %) + 20 esperas simuladas (5 s, CPU parada).
- **Mira el Administrador de tareas** (Ctrl+Shift+Esc → Rendimiento → CPU) mientras corre.

Con descargas reales en vez de `sleep` (necesita internet):
```powershell
uv run python medir.py --real
```

### 2.3 Demo: 1 core frente a todos
```powershell
uv run python demo_docente.py
```
- Primos hasta 4 M, primero secuencial (unos 26–32 s) y luego con 16 procesos (unos 4 s).
- Da el speedup. **Los dos números de primos tienen que coincidir (283146).**

### 2.4 Verificador (antes de entregar)
```powershell
uv run python verificar_lab01.py
```
- `[OK]` = hecho · `[AVISO]` = no bloquea · `[FALHA]` = falta algo, y debajo dice cómo arreglarlo.
- Objetivo: `0 falha(s)`.

---

## 3. Extra: procesos frente a hilos, con y sin GIL (`comparar.py`)

Cuenta los primos 3 veces: 1 core, 16 procesos y 16 hilos.

### Con GIL (tu Python 3.13 normal)
```powershell
uv run python comparar.py
```

### Sin GIL (Python 3.14 free-threaded)
```powershell
uv run --no-project --python 3.14t python comparar.py
```
- `--python 3.14t`: usa **otro Python**, compilado sin GIL (la `t` = free-threaded). La primera vez uv lo descarga (unos 30 MB).
- `--no-project`: **no toca el `.venv` del lab** (que sigue con 3.13). Aquí no hay psutil ni matplotlib, pero comparar.py no los necesita.
- Comprueba la primera línea: tiene que decir `GIL ativo: False`.

### Prueba rápida (límite más pequeño)
```powershell
uv run python comparar.py 200000
```
Con tareas tan pequeñas, los procesos salen **más lentos** que 1 core: arrancar 16 Pythons tarda más que el cálculo.

### Qué esperar con 4 M

| | Con GIL | Sin GIL |
|---|---|---|
| Hilos | ~1× (se turnan el GIL) | ~7–9× |
| Procesos | ~7–8× | parecido |
| 1 core | referencia | algo más lento |

---

## 4. Guardar y entregar (git)

```powershell
git status                       # qué ha cambiado
git add README.md                # o "git add ." para todo
git commit -m "Lab 01: ..."
git push                         # sube a GitHub
```

Después, vuelve a pasar el verificador: no debería salir el aviso de "alterações por guardar".

> `NOTAS.md` y `comparar.py` son extras tuyos. Si no quieres entregarlos, no los añadas al commit (el verificador solo mostrará un `[AVISO]`, que no bloquea).

---

## 5. Problemas típicos

| Síntoma | Causa | Solución |
|---|---|---|
| `uv no esta instalado` | falta uv | paso A1 del lab |
| Acentos rotos | consola sin UTF-8 | `$env:PYTHONUTF8 = 1` |
| `[FALHA] não estás no ambiente do projeto` | ejecutaste `python ...` sin `uv run` | ponle `uv run` delante |
| `[FALHA] biblioteca X em falta` | librería no instalada | `uv add X` |
| Speedup muy bajo (~1–2×) | batería, programas abiertos | PowerShell normal, enchufado, cerrar programas |
| Speedup distinto en cada ejecución | es normal (turbo, temperatura, otros programas) | ejecutar 3 veces y quedarse con la mediana |
| `GIL ativo: True` con 3.14t | alguna librería en C lo ha reactivado | con comparar.py no debería pasar |

---

## 6. Chuleta de conceptos

- **CPU-bound**: tarda porque calcula. Se acelera con **más cores** (procesos).
- **I/O-bound**: tarda porque espera (red, disco). Se acelera **solapando esperas** (hilos, asyncio). Más cores no ayudan.
- **Cores físicos (8) frente a lógicos (16)**: los lógicos son SMT; el límite real para calcular está en ~8–10×.
- **GIL**: candado que deja ejecutar Python a un solo hilo por proceso a la vez.
  - Hilos + GIL: no sirven para calcular, sí para esperar (el GIL se suelta mientras esperan).
  - Procesos: cada uno tiene su propio GIL, así que calculan a la vez.
  - Sin GIL (3.14t): los hilos también calculan a la vez, pero con 1 hilo va algo más lento y hay que protegerse de las *race conditions*.
- **Speedup** = tiempo con 1 core ÷ tiempo en paralelo. Nunca llega al número de cores: SMT, arranque de procesos, reparto desigual, bajada del turbo.
- **`if __name__ == "__main__":`** es obligatorio con procesos en Windows; si no, cada hijo vuelve a lanzar el programa.
