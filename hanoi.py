"""
hanoi.py — regras da Torre de Hanoi.

Estado: tupla de N posicoes (uma por disco, 0 = o menor). O valor em
cada posicao e o pino (0=A, 1=B, 2=C) onde aquele disco esta.
Ex.: (0,0,2,1) com 4 discos -> discos 0 e 1 em A, disco 2 em C, disco 3 em B.

Em cada pino, so o disco de menor indice (o do topo) pode se mover, e
so pra um pino vazio ou com um disco maior no topo.
"""

N_PINOS = 3
PINOS_NOME = "ABC"


def estado_inicial(n_discos, pino_origem=0):
    return tuple(pino_origem for _ in range(n_discos))


def topo_de_cada_pino(estado):
    topo = [None] * N_PINOS
    for disco, pino in enumerate(estado):
        if topo[pino] is None or disco < topo[pino]:
            topo[pino] = disco
    return topo


def movimentos_legais(estado):
    topo = topo_de_cada_pino(estado)
    movs = []
    for origem in range(N_PINOS):
        disco = topo[origem]
        if disco is None:
            continue
        for destino in range(N_PINOS):
            if destino == origem:
                continue
            disco_destino = topo[destino]
            if disco_destino is None or disco_destino > disco:
                movs.append((disco, origem, destino))
    return movs


def aplicar_movimento(estado, mov):
    disco, _origem, destino = mov
    novo = list(estado)
    novo[disco] = destino
    return tuple(novo)


def objetivo(estado, pino_destino=2):
    return all(p == pino_destino for p in estado)


def discos_fora_do_destino(estado, pino_destino=2):
    """Heuristica: numero de discos que ainda nao estao no pino destino."""
    return sum(1 for p in estado if p != pino_destino)


def texto_movimento(mov):
    disco, origem, destino = mov
    return f"disco {disco + 1}: {PINOS_NOME[origem]}->{PINOS_NOME[destino]}"


def imprimir_estado(estado, titulo=None):
    if titulo:
        print(titulo)
    n = len(estado)
    for pino in range(N_PINOS):
        discos = sorted((d for d in range(n) if estado[d] == pino), reverse=True)
        discos_txt = " ".join(str(d + 1) for d in discos) if discos else "(vazio)"
        print(f"  Pino {PINOS_NOME[pino]}: {discos_txt}")
    print()
