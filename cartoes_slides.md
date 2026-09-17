# Pontos-chave para os Slides (Canva)
## Torre de Hanói — UCS, Busca Gulosa e A*

Cada bloco abaixo = **1 slide**. Título primeiro, depois os pontos-chave — cole cada bloco num
slide novo do Canva. Os pontos não são frase pronta: são o gatilho pra vocês lembrarem da fala
completa (que está no `guia_seminario.pdf`, seção 4).

---

### Slide 1 — Título
Torre de Hanói
UCS · Busca Gulosa · A*

- Kauã Cardoso Benini · Gabriel Benini · Felipe Donatoni
- Problema 2 do catálogo — escolhido pelo gabarito exato (2^n − 1)

---

### Slide 2 — O problema
Mover N discos, um por vez, sem erro

- 3 pinos: A = origem, B = auxiliar, C = destino
- Regra única: disco maior nunca sobre um menor
- Vantagem rara: fórmula exata (2^n − 1) confere cada teste

---

### Slide 3 — Por que escolhemos Torre de Hanói
- Gabarito exato → sabemos na hora se o código errou
- Espaço de estados 3^n → explosão combinatória visível de verdade
- Regras curtas → dá pra defender o código inteiro no seminário

---

### Slide 4 — Modelagem
- Estado = tupla de N posições (disco 0 = menor … disco N-1 = maior)
- Tupla, não lista → precisa ser *hashable* (dicionário de estados vistos)
- Ações = mover disco do topo pra outro pino válido
- Custo = 1 por movimento · Objetivo = tudo no pino C

---

### Slide 5 — Regras de movimento
- Só o disco do topo de cada pino pode mover
- Só pra pino vazio, ou com disco maior no topo
- Nunca o contrário — essa é a única regra real do jogo

---

### Slide 6 — A regra mais importante (função única)
- g(n) = custo já pago · h(n) = palpite do que falta
- UCS → f = g · Gulosa → f = h · A\* → f = g + h
- Uma função `busca(problema, f)` só — nenhuma busca copiada e colada

---

### Slide 7 — Heurística
- Sugerida na própria ficha: discos fora do pino destino
- Admissível: todo disco fora precisa de ≥ 1 movimento → nunca superestima
- Confirmado na prática: A* nunca passou do gabarito em 24 testes

---

### Slide 8 — Heurística fraca (de propósito)
- Disco livre → 1 movimento
- Disco enterrado (sob outros) → vários movimentos
- A heurística conta os dois casos igual — "1 disco fora do lugar"
- Por isso ela guia a busca menos do que podia

---

### Slide 9 — Resultados (tabela)
- Testado com 3 a 10 discos
- Custo bateu com 2^n − 1 em TODOS os 24 testes (8 tamanhos × 3 algoritmos)
- UCS sempre expandiu mais nós que Gulosa/A\*

---

### Slide 10 — Gráfico: explosão combinatória
- Escala logarítmica
- Cada disco a mais multiplica os nós por ~3
- Coerente com o espaço de estados 3^n

---

### Slide 11 — O imprevisto: Gulosa
- Com 9 discos: Gulosa expande MENOS nós que UCS e A*
- Com 10 discos: Gulosa expande MAIS que os dois
- Heurística fraca → vantagem de eficiência não é garantida

---

### Slide 12 — Quando usar cada um
- UCS → sem heurística confiável, mas custo tem que ser ótimo
- Gulosa → velocidade importa mais que otimalidade
- A\* → heurística admissível disponível, quer os dois (rápido + ótimo)

---

### Slide 13 — Demonstração ao vivo
- Rodar: `python main.py`
- Benchmark completo + sequência de 4 discos (15 movimentos, bate o gabarito)
- Se der tempo: `python gui.py` — tabuleiro, animação, pausa, comparação ao vivo

---

### Slide 14 — Conclusão / Se recomeçássemos
- Testar heurística mais forte (recursiva, não só "conta discos fora")
- Rodar mais cenários de benchmark
- Extra já entregue: interface gráfica (+10%)
- Aprendizado: heurística admissível ≠ heurística que ajuda muito

---

### Slide 15 — Obrigado
- Perguntas?
- Kauã · Gabriel · Felipe
