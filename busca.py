"""
busca.py — uma unica funcao de busca, que muda de UCS pra Gulosa pra A*
so trocando a funcao f(g, h):

    UCS    -> f = g          (so o custo ja pago)
    Gulosa -> f = h          (so o palpite do que falta)
    A*     -> f = g + h      (os dois)
"""

import heapq
import math
import time
from dataclasses import dataclass, field
from itertools import count
from typing import Callable, List, Optional


@dataclass
class Problema:
    estado_inicial: object
    sucessores: Callable  # sucessores(estado) -> [(movimento, novo_estado, custo), ...]
    teste_objetivo: Callable
    heuristica: Callable


@dataclass
class ResultadoBusca:
    sucesso: bool
    caminho: Optional[List] = field(default_factory=list)
    custo: Optional[float] = None
    nos_expandidos: int = 0
    nos_gerados: int = 0
    tempo: float = 0.0
    motivo: str = ""


def busca(problema: Problema, funcao_f: Callable, limite_tempo: float = 60.0,
          limite_nos: Optional[int] = None) -> ResultadoBusca:
    """funcao_f(g, h) decide a prioridade de cada nó — é o único ponto
    que muda entre UCS, Gulosa e A*."""
    inicio = time.perf_counter()
    desempate = count()  # evita comparar 'estado' quando o heap empata em prioridade

    g0 = 0
    h0 = problema.heuristica(problema.estado_inicial)
    no_inicial = {"estado": problema.estado_inicial, "g": g0, "caminho": []}

    fronteira = [(funcao_f(g0, h0), next(desempate), no_inicial)]
    melhor_g_conhecido = {problema.estado_inicial: g0}

    nos_gerados = 1
    nos_expandidos = 0

    while fronteira:
        tempo_decorrido = time.perf_counter() - inicio
        if tempo_decorrido > limite_tempo:
            return ResultadoBusca(sucesso=False, nos_expandidos=nos_expandidos,
                                   nos_gerados=nos_gerados, tempo=tempo_decorrido,
                                   motivo=f"não concluiu em {limite_tempo:.0f}s")

        _, _, no = heapq.heappop(fronteira)
        estado = no["estado"]

        # entrada obsoleta: já achamos um caminho melhor para este estado
        if no["g"] > melhor_g_conhecido.get(estado, math.inf):
            continue

        if problema.teste_objetivo(estado):
            tempo_total = time.perf_counter() - inicio
            return ResultadoBusca(sucesso=True, caminho=no["caminho"], custo=no["g"],
                                   nos_expandidos=nos_expandidos, nos_gerados=nos_gerados,
                                   tempo=tempo_total)

        nos_expandidos += 1
        if limite_nos is not None and nos_expandidos > limite_nos:
            tempo_total = time.perf_counter() - inicio
            return ResultadoBusca(sucesso=False, nos_expandidos=nos_expandidos,
                                   nos_gerados=nos_gerados, tempo=tempo_total,
                                   motivo=f"excedeu limite de {limite_nos} nós expandidos")

        for movimento, novo_estado, custo_passo in problema.sucessores(estado):
            novo_g = no["g"] + custo_passo
            if novo_g < melhor_g_conhecido.get(novo_estado, math.inf):
                melhor_g_conhecido[novo_estado] = novo_g
                h = problema.heuristica(novo_estado)
                novo_no = {"estado": novo_estado, "g": novo_g,
                           "caminho": no["caminho"] + [movimento]}
                heapq.heappush(fronteira, (funcao_f(novo_g, h), next(desempate), novo_no))
                nos_gerados += 1

    tempo_total = time.perf_counter() - inicio
    return ResultadoBusca(sucesso=False, nos_expandidos=nos_expandidos,
                           nos_gerados=nos_gerados, tempo=tempo_total,
                           motivo="fronteira esvaziou sem achar solução")


def f_ucs(g, h):
    return g


def f_gulosa(g, h):
    return h


def f_astar(g, h):
    return g + h
