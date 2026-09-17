"""
resolver.py — monta o problema de busca e roda UCS/Gulosa/A* nele.

Heuristica: numero de discos fora do pino destino (sugerida na ficha do
problema). E admissivel porque todo disco fora do lugar precisa de pelo
menos 1 movimento ainda -- nunca superestima. E fraca de proposito: nao
diferencia um disco que falta 1 movimento de um que falta vários
(detalhes no relatorio).
"""

import hanoi
from busca import Problema, busca, f_ucs, f_gulosa, f_astar

ALGORITMOS = {
    "UCS": f_ucs,
    "Gulosa": f_gulosa,
    "A*": f_astar,
}


def montar_problema(n_discos, pino_destino=2):
    def sucessores(estado):
        return [(mov, hanoi.aplicar_movimento(estado, mov), 1)
                for mov in hanoi.movimentos_legais(estado)]

    def teste_objetivo(estado):
        return hanoi.objetivo(estado, pino_destino)

    def heuristica(estado):
        return hanoi.discos_fora_do_destino(estado, pino_destino)

    return Problema(estado_inicial=hanoi.estado_inicial(n_discos),
                     sucessores=sucessores, teste_objetivo=teste_objetivo,
                     heuristica=heuristica)


def resolver(n_discos, algoritmo="A*", limite_tempo=60.0, limite_nos=None,
             pino_destino=2):
    problema = montar_problema(n_discos, pino_destino)
    return busca(problema, ALGORITMOS[algoritmo], limite_tempo=limite_tempo,
                 limite_nos=limite_nos)


def custo_otimo_conhecido(n_discos):
    """Formula da Torre de Hanoi: solucao otima = 2^n - 1 movimentos."""
    return 2 ** n_discos - 1
