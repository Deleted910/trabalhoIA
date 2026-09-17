Trabalho Avaliativo de Inteligencia Artificial
Implementacao e comparacao de UCS, Busca Gulosa e A*
Problema escolhido: Problema 2 - Torre de Hanoi

INTEGRANTES
-----------
- Kaua Cardoso Benini
- Gabriel Benini
- Felipe Donatoni

LINGUAGEM E VERSAO
-------------------
Python 3.12 (testado com Python 3.12.10). Nao usa nenhuma biblioteca
externa - so a biblioteca padrao (heapq, time, math, dataclasses).

COMO RODAR
----------
python main.py
    -> roda o benchmark (3 a 10 discos) e depois uma demonstracao com
       4 discos, imprimindo a sequencia de movimentos encontrada.

python main.py --so-bench
    -> roda so o benchmark (mais rapido, sem a demonstracao no final).

python gui.py
    -> abre a interface grafica opcional (extra +10%, ver Secao 8 do
       roteiro): desenha o tabuleiro, anima a solucao encontrada e
       compara os nos expandidos dos tres algoritmos com um grafico de
       barras. So usa tkinter (biblioteca padrao do Python).

Se aparecerem acentos quebrados no console do Windows (cmd.exe antigo),
rodem antes:  chcp 65001

ESTRUTURA DOS ARQUIVOS
-----------------------
hanoi.py      -> regras da Torre de Hanoi (estado, movimentos legais,
                 aplicacao de movimentos, heuristica sugerida pela
                 ficha do problema: discos fora do pino destino).

busca.py      -> A FUNCAO UNICA DE BUSCA (busca()), parametrizada pela
                 funcao f(g, h). UCS, Gulosa e A* sao so tres chamadas
                 dessa mesma funcao trocando o f (f_ucs, f_gulosa,
                 f_astar, no fim do arquivo).

resolver.py   -> monta o problema de busca (Problema, do busca.py) a
                 partir do numero de discos, e a funcao resolver()
                 que roda qualquer um dos tres algoritmos sobre ele.
                 Tambem tem a formula do gabarito conhecido (2^n - 1)
                 usada para conferir se a implementacao esta certa.

main.py       -> ponto de entrada. Roda o benchmark com 3 a 10 discos
                 (sugerido pela ficha do problema) e uma demonstracao
                 com 4 discos, imprimindo a sequencia de movimentos.

gui.py        -> interface grafica opcional (+10%). Desenha o tabuleiro,
                 anima a solucao passo a passo, e mostra um grafico de
                 barras comparando os nos expandidos por UCS, Gulosa e
                 A* para o numero de discos escolhido.

relatorio.pdf -> relatorio final do trabalho.

guia_seminario.pdf -> roteiro e preparo para a apresentacao.

OBSERVACOES IMPORTANTES
-------------------------
- Todos os tres algoritmos saem da MESMA funcao busca(), so trocando o
  parametro funcao_f. Isso atende a regra mais importante do trabalho.
- Contador de nos expandidos: incrementa so quando um no e RETIRADO da
  fronteira e tem seus filhos gerados (nao quando e so gerado e colocado
  na fronteira). Essa distincao esta comentada em busca.py.
- Limite de tempo: cada chamada de busca() recebe limite_tempo (padrao
  60s). Nos testes feitos (3 a 10 discos), a busca mais lenta levou
  menos de 1 segundo - o limite nunca foi atingido. Acima de 10 discos
  (nao usado no benchmark oficial do relatorio) o tempo cresce rapido:
  com 12 discos a UCS ja leva mais de 20 segundos, o que e esperado e
  esta comentado no relatorio (explosao combinatoria do espaco de
  estados, que e 3^n).
- Gabarito de conferencia: a Torre de Hanoi tem uma vantagem que poucos
  problemas da lista tem - a solucao otima e conhecida por formula
  matematica (2^n - 1 movimentos). Em TODOS os testes rodados (3 a 12
  discos), os tres algoritmos encontraram exatamente esse valor,
  confirmando que a implementacao esta correta.
