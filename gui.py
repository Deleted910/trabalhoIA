"""
gui.py — interface grafica opcional (+10%). Desenha o tabuleiro, anima
a solucao e compara os nos expandidos dos 3 algoritmos. So usa tkinter.

    python gui.py
"""

import tkinter as tk
from tkinter import ttk

import hanoi
from resolver import resolver, custo_otimo_conhecido, ALGORITMOS

# mesmas cores usadas nos slides do seminario, pra manter consistencia visual
COR_UCS = "#2a6fd6"
COR_GULOSA = "#d9631f"
COR_ASTAR = "#1c9c6e"
COR_ALG = {"UCS": COR_UCS, "Gulosa": COR_GULOSA, "A*": COR_ASTAR}

COR_FUNDO = "#f4f3f0"
COR_PAINEL = "#ffffff"
COR_HASTE = "#8a7d6d"
COR_BASE = "#5c5347"
COR_DESTAQUE = "#e0393e"
COR_TEXTO = "#2b2b2b"
COR_TEXTO_FRACO = "#767267"

CANVAS_W = 620
CANVAS_H = 300
BASE_Y = 250
TOPO_HASTE_Y = 50
DISCO_ALTURA = 16
DISCO_LARG_MIN = 40
DISCO_LARG_MAX = 150


def cor_disco(indice, n):
    """Rampa bege->marrom só pra diferenciar os discos (sem ligação com
    as cores dos algoritmos)."""
    t = 0.0 if n <= 1 else indice / (n - 1)
    r1, g1, b1 = 0xE6, 0xD6, 0xB0
    r2, g2, b2 = 0x8A, 0x6A, 0x3E
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


class AppHanoi:
    def __init__(self, root):
        self.root = root
        root.title("Torre de Hanói — UCS, Busca Gulosa e A*")
        root.configure(bg=COR_FUNDO)
        root.resizable(False, False)

        self.n_discos = tk.IntVar(value=4)
        self.algoritmo_animar = tk.StringVar(value="A*")
        self.velocidade = tk.IntVar(value=450)  # ms por movimento
        self.status_var = tk.StringVar(value="Escolha o número de discos e clique em Resolver.")

        self.estado = hanoi.estado_inicial(self.n_discos.get())
        self.movimentos = []
        self.passo_idx = 0
        self.animando = False
        self.pausado = False
        self._job_id = None       # id da chamada agendada (pra poder cancelar)
        self._proxima_chamada = None  # (funcao, args) a rodar quando despausar
        self.disco_destacado = None
        self.resultados = {}  # {algoritmo: ResultadoBusca}

        self._montar_controles()
        self._montar_tabuleiro()
        self._montar_comparacao()
        self._montar_status()

        self.desenhar_tabuleiro()

    # ---------------- construção da interface ----------------

    def _montar_controles(self):
        f = tk.Frame(self.root, bg=COR_FUNDO, padx=14, pady=12)
        f.grid(row=0, column=0, columnspan=2, sticky="ew")

        tk.Label(f, text="Discos:", bg=COR_FUNDO, fg=COR_TEXTO).grid(row=0, column=0, padx=(0, 4))
        tk.Spinbox(f, from_=3, to=10, width=3, textvariable=self.n_discos).grid(row=0, column=1, padx=(0, 16))

        tk.Label(f, text="Animar com:", bg=COR_FUNDO, fg=COR_TEXTO).grid(row=0, column=2, padx=(0, 4))
        combo = ttk.Combobox(f, textvariable=self.algoritmo_animar, values=list(ALGORITMOS.keys()),
                              state="readonly", width=8)
        combo.grid(row=0, column=3, padx=(0, 16))

        self.btn_resolver = tk.Button(f, text="Resolver", command=self.resolver_clicado,
                                       bg="#2b2b2b", fg="white", padx=10, pady=4, relief="flat")
        self.btn_resolver.grid(row=0, column=4, padx=(0, 10))

        self.btn_animar = tk.Button(f, text="▶ Animar", command=self.animar_clicado,
                                     state="disabled", padx=10, pady=4, relief="flat")
        self.btn_animar.grid(row=0, column=5, padx=(0, 10))

        self.btn_pausar = tk.Button(f, text="⏸ Pausar", command=self.pausar_clicado,
                                     state="disabled", padx=10, pady=4, relief="flat")
        self.btn_pausar.grid(row=0, column=6, padx=(0, 16))

        tk.Label(f, text="Velocidade:", bg=COR_FUNDO, fg=COR_TEXTO).grid(row=0, column=7, padx=(0, 4))
        tk.Scale(f, from_=800, to=100, orient="horizontal", variable=self.velocidade,
                 length=110, showvalue=False, bg=COR_FUNDO, highlightthickness=0).grid(row=0, column=8)

    def _montar_tabuleiro(self):
        self.canvas = tk.Canvas(self.root, width=CANVAS_W, height=CANVAS_H,
                                 bg=COR_PAINEL, highlightthickness=1, highlightbackground="#d8d5cd")
        self.canvas.grid(row=1, column=0, padx=(14, 8), pady=(0, 10))

    def _montar_comparacao(self):
        painel = tk.Frame(self.root, bg=COR_PAINEL, width=220, height=CANVAS_H,
                           highlightthickness=1, highlightbackground="#d8d5cd")
        painel.grid(row=1, column=1, padx=(0, 14), pady=(0, 10), sticky="n")
        painel.grid_propagate(False)

        tk.Label(painel, text="Nós expandidos", bg=COR_PAINEL, fg=COR_TEXTO,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12, pady=(12, 8))

        self.labels_comparacao = {}
        for alg in ("UCS", "Gulosa", "A*"):
            lbl = tk.Label(painel, text=f"{alg}: —", bg=COR_PAINEL, fg=COR_ALG[alg],
                           font=("Consolas", 12, "bold"))
            lbl.pack(anchor="w", padx=12, pady=3)
            self.labels_comparacao[alg] = lbl

        self.label_gabarito = tk.Label(painel, text="", bg=COR_PAINEL, fg=COR_TEXTO_FRACO,
                                        font=("Segoe UI", 8), justify="left", wraplength=196)
        self.label_gabarito.pack(anchor="w", padx=12, pady=(14, 12))

    def _montar_status(self):
        f = tk.Frame(self.root, bg=COR_FUNDO, padx=14)
        f.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        tk.Label(f, textvariable=self.status_var, bg=COR_FUNDO, fg=COR_TEXTO,
                 font=("Consolas", 10), anchor="w", justify="left").pack(fill="x")

    # ---------------- desenho do tabuleiro ----------------

    def desenhar_tabuleiro(self):
        c = self.canvas
        c.delete("all")
        n = len(self.estado)

        peg_xs = [CANVAS_W * 0.2, CANVAS_W * 0.5, CANVAS_W * 0.8]
        nomes = "ABC"

        # base
        c.create_rectangle(30, BASE_Y, CANVAS_W - 30, BASE_Y + 10, fill=COR_BASE, outline="")

        # hastes
        for x in peg_xs:
            c.create_rectangle(x - 3, TOPO_HASTE_Y, x + 3, BASE_Y, fill=COR_HASTE, outline="")

        # discos, pino a pino
        for p in range(3):
            discos_no_pino = sorted((d for d in range(n) if self.estado[d] == p), reverse=True)
            for nivel, d in enumerate(discos_no_pino):
                # disco 0 = o menor (largura minima), disco n-1 = o maior (largura maxima)
                largura = DISCO_LARG_MIN + (DISCO_LARG_MAX - DISCO_LARG_MIN) * (
                    0 if n <= 1 else d / (n - 1))
                x_centro = peg_xs[p]
                y_baixo = BASE_Y - nivel * (DISCO_ALTURA + 2)
                y_cima = y_baixo - DISCO_ALTURA
                cor = cor_disco(d, n)
                contorno = COR_DESTAQUE if d == self.disco_destacado else "#d8cdb8"
                largura_contorno = 3 if d == self.disco_destacado else 1
                c.create_rectangle(x_centro - largura / 2, y_cima, x_centro + largura / 2, y_baixo,
                                    fill=cor, outline=contorno, width=largura_contorno)
                c.create_text(x_centro, (y_cima + y_baixo) / 2, text=str(d + 1),
                               fill="#2b2b2b", font=("Segoe UI", 8))

            c.create_text(peg_xs[p], BASE_Y + 26, text=nomes[p], fill=COR_TEXTO_FRACO,
                          font=("Consolas", 11, "bold"))

    def desenhar_comparacao(self):
        for alg, lbl in self.labels_comparacao.items():
            r = self.resultados.get(alg)
            valor = f"{r.nos_expandidos:,}".replace(",", ".") if r and r.sucesso else "—"
            lbl.config(text=f"{alg}: {valor}")

    # ---------------- eventos ----------------

    def resolver_clicado(self):
        if self.animando:
            return
        n = self.n_discos.get()
        self.estado = hanoi.estado_inicial(n)
        self.passo_idx = 0
        self.disco_destacado = None

        self.resultados = {}
        for alg in ("UCS", "Gulosa", "A*"):
            self.resultados[alg] = resolver(n, algoritmo=alg, limite_tempo=30.0, limite_nos=2_000_000)

        alg_escolhido = self.algoritmo_animar.get()
        resultado = self.resultados[alg_escolhido]
        self.movimentos = resultado.caminho if resultado.sucesso else []

        otimo = custo_otimo_conhecido(n)
        if resultado.sucesso:
            bate = "== gabarito (2^n-1)" if resultado.custo == otimo else "DIVERGIU DO GABARITO!"
            self.status_var.set(
                f"{alg_escolhido}: custo={resultado.custo} ({bate})  passos={len(resultado.caminho)}  "
                f"nós_expandidos={resultado.nos_expandidos}  tempo={resultado.tempo:.4f}s  "
                f"— pronto pra animar.")
            self.btn_animar.config(state="normal")
        else:
            self.status_var.set(f"{alg_escolhido}: {resultado.motivo}")
            self.btn_animar.config(state="disabled")

        self.pausado = False
        self._job_id = None
        self._proxima_chamada = None
        self.btn_pausar.config(state="disabled", text="⏸ Pausar")

        self.label_gabarito.config(text=f"Gabarito (fórmula 2^n−1) para {n} discos: {otimo} movimentos.")

        self.desenhar_tabuleiro()
        self.desenhar_comparacao()

    def animar_clicado(self):
        if self.animando or not self.movimentos:
            return
        self.estado = hanoi.estado_inicial(self.n_discos.get())
        self.passo_idx = 0
        self.animando = True
        self.pausado = False
        self._job_id = None
        self._proxima_chamada = None
        self.btn_animar.config(state="disabled")
        self.btn_resolver.config(state="disabled")
        self.btn_pausar.config(state="normal", text="⏸ Pausar")
        self.desenhar_tabuleiro()
        self._agendar(200, self._animar_proximo)

    def pausar_clicado(self):
        if not self.animando:
            return
        self.pausado = not self.pausado
        if self.pausado:
            # cancela o passo já agendado, senão ele roda mesmo pausado
            if self._job_id is not None:
                self.root.after_cancel(self._job_id)
                self._job_id = None
            self.btn_pausar.config(text="▶ Continuar")
        else:
            self.btn_pausar.config(text="⏸ Pausar")
            if self._proxima_chamada is not None:
                callback, args = self._proxima_chamada
                self._job_id = self.root.after(30, callback, *args)

    def _agendar(self, delay, callback, *args):
        self._proxima_chamada = (callback, args)
        if not self.pausado:
            self._job_id = self.root.after(delay, callback, *args)

    def _animar_proximo(self):
        if self.passo_idx >= len(self.movimentos):
            self.animando = False
            self.disco_destacado = None
            self.desenhar_tabuleiro()
            self.status_var.set(f"Concluído! {len(self.movimentos)} movimentos executados.")
            self.btn_animar.config(state="normal")
            self.btn_resolver.config(state="normal")
            self.btn_pausar.config(state="disabled", text="⏸ Pausar")
            return

        mov = self.movimentos[self.passo_idx]
        self.disco_destacado = mov[0]
        self.desenhar_tabuleiro()
        self.status_var.set(
            f"Movimento {self.passo_idx + 1}/{len(self.movimentos)}: {hanoi.texto_movimento(mov)}")

        delay = self.velocidade.get()
        self._agendar(max(30, delay // 2), self._aplicar_movimento, mov)

    def _aplicar_movimento(self, mov):
        self.estado = hanoi.aplicar_movimento(self.estado, mov)
        self.passo_idx += 1
        self.desenhar_tabuleiro()
        delay = self.velocidade.get()
        self._agendar(max(30, delay // 2), self._animar_proximo)


def main():
    root = tk.Tk()
    AppHanoi(root)
    root.mainloop()


if __name__ == "__main__":
    main()
