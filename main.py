"""
main.py — ponto de entrada. Roda o benchmark (3 a 10 discos) e uma
demonstração com 4 discos, imprimindo os movimentos encontrados.

    python main.py             -> benchmark + demonstração
    python main.py --so-bench  -> só o benchmark
"""

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")  # evita acentos quebrados no console do Windows
except AttributeError:
    pass

import hanoi
from resolver import resolver, custo_otimo_conhecido

LIMITE_TEMPO = 60.0  # segundos por busca; ajustem se a máquina de vocês for mais lenta/rápida
FAIXA_BENCHMARK = [3, 4, 5, 6, 7, 8, 9, 10]


def demonstracao(n_discos=4):
    print("=" * 70)
    print(f"DEMONSTRAÇÃO: Torre de Hanói com {n_discos} discos")
    hanoi.imprimir_estado(hanoi.estado_inicial(n_discos), "Estado inicial (todos no pino A):")

    otimo = custo_otimo_conhecido(n_discos)
    print(f"Gabarito conhecido (fórmula 2^n - 1): {otimo} movimentos\n")

    resultados = {}  # guarda os 3 resultados pra reaproveitar o do A* depois
    for alg in ("UCS", "Gulosa", "A*"):
        r = resultados[alg] = resolver(n_discos, algoritmo=alg, limite_tempo=LIMITE_TEMPO)
        if r.sucesso:
            bate = "== gabarito" if r.custo == otimo else "!= gabarito (ERRO)"
            print(f"{alg:8s} -> custo={r.custo} ({bate})  passos={len(r.caminho)}  "
                  f"nós_expandidos={r.nos_expandidos}  tempo={r.tempo:.4f}s")
        else:
            print(f"{alg:8s} -> {r.motivo}")

    caminho = resultados["A*"].caminho  # ja rodado no loop acima, nao roda de novo
    print(f"\nSequência de movimentos (A*), {len(caminho)} no total:")
    for i, mov in enumerate(caminho, 1):
        print(f"  {i:2d}. {hanoi.texto_movimento(mov)}")
    print()


def roda_benchmark():
    print("=" * 70)
    print("BENCHMARK: UCS x Busca Gulosa x A*, variando o número de discos")
    print(f"{'Discos':>6s} | {'Algoritmo':8s} | {'Custo':>6s} | {'Gabarito ok?':>12s} | "
          f"{'Nós exp.':>9s} | {'Tempo (s)':>10s}")
    print("-" * 70)

    for n in FAIXA_BENCHMARK:  # 3 a 10 discos
        otimo = custo_otimo_conhecido(n)
        for alg in ("UCS", "Gulosa", "A*"):  # os 3 algoritmos, pra cada n
            r = resolver(n, algoritmo=alg, limite_tempo=LIMITE_TEMPO, limite_nos=3_000_000)
            if r.sucesso:
                ok = "sim" if r.custo == otimo else "NÃO (!)"
                print(f"{n:>6d} | {alg:8s} | {r.custo:>6d} | {ok:>12s} | "
                      f"{r.nos_expandidos:>9d} | {r.tempo:>10.4f}")
            else:
                print(f"{n:>6d} | {alg:8s} | {'-':>6s} | {'-':>12s} | "
                      f"{r.nos_expandidos:>9d} | não concluiu em {r.tempo:.1f}s")
    print()


if __name__ == "__main__":
    roda_benchmark()
    if "--so-bench" not in sys.argv:
        demonstracao(4)
