import os
import csv
import random
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable

import config
from modelos import DicionarioManager, PerfilManager, GramaticaGuarani

class TelaLogin:
    def __init__(self, root: tk.Tk, on_login_success: Callable[[Optional[str]], None]):
        self.root = root
        self.on_login_success = on_login_success
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill="both")
        
        self.var_title = tk.StringVar()
        self.var_sub = tk.StringVar()
        self.var_btn_enter = tk.StringVar()
        self.var_or = tk.StringVar()
        self.var_btn_new = tk.StringVar()
        self.var_btn_guest = tk.StringVar()
        self.var_btn_theme = tk.StringVar()

        frame_top = tk.Frame(self.frame)
        frame_top.pack(fill="x", padx=10, pady=5)
        
        self.btn_theme = tk.Button(frame_top, textvariable=self.var_btn_theme, command=self.alternar_tema)
        self.btn_theme.pack(side="left", padx=5)

        for lang in ["pt", "es", "gn"]:
            btn = tk.Button(frame_top, text=lang.upper(), command=lambda l=lang: self.mudar_idioma(l), width=4)
            btn.pack(side="right", padx=2)

        self.lbl_title = tk.Label(self.frame, textvariable=self.var_title, font=("Trebuchet MS", 22, "bold"))
        self.lbl_title.pack(pady=(20, 15))
        
        self.lbl_sub = tk.Label(self.frame, textvariable=self.var_sub, font=("Helvetica", 12))
        self.lbl_sub.pack(pady=10)

        perfis_existentes = PerfilManager.listar_perfis()
        self.combo_perfis = ttk.Combobox(self.frame, values=perfis_existentes, font=("Helvetica", 12), state="readonly", width=25)
        if perfis_existentes: self.combo_perfis.current(0)
        self.combo_perfis.pack(pady=5)

        self.btn_enter = tk.Button(self.frame, textvariable=self.var_btn_enter, font=("Helvetica", 11, "bold"), width=22, command=self.login_existente)
        self.btn_enter.pack(pady=8)
        
        self.lbl_or = tk.Label(self.frame, textvariable=self.var_or, font=("Helvetica", 10))
        self.lbl_or.pack(pady=10)

        self.entrada_novo = tk.Entry(self.frame, font=("Helvetica", 12), width=27)
        self.entrada_novo.pack(pady=5)

        self.btn_new = tk.Button(self.frame, textvariable=self.var_btn_new, font=("Helvetica", 11, "bold"), width=22, command=self.login_novo)
        self.btn_new.pack(pady=8)
        
        self.btn_guest = tk.Button(self.frame, textvariable=self.var_btn_guest, font=("Helvetica", 10), width=22, command=lambda: self.finalizar_login(None))
        self.btn_guest.pack(pady=(25, 10))

        self.aplicar_tema()
        self.mudar_idioma(config.GerenciadorIdiomas.idioma_ativo)

    def alternar_tema(self):
        config.GerenciadorTemas.alternar()
        self.aplicar_tema()

    def mudar_idioma(self, idioma: str):
        config.GerenciadorIdiomas.idioma_ativo = idioma
        t = config.GerenciadorIdiomas.TEXTOS[idioma]
        self.root.title(t["title_app"])
        self.var_title.set(t["login_title"])
        self.var_sub.set(t["login_sub"])
        self.var_btn_enter.set(t["login_btn_enter"])
        self.var_or.set(t["login_or"])
        self.var_btn_new.set(t["login_btn_new"])
        self.var_btn_guest.set(t["login_btn_guest"])
        self.var_btn_theme.set(t.get("btn_theme", "Tema"))

    def aplicar_tema(self):
        cores = config.GerenciadorTemas.get()
        self.frame.configure(bg=cores["bg"])
        self.atualizar_cores()
        
    def atualizar_cores(self):
        cores = config.GerenciadorTemas.get()
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=cores["bg"])
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button):
                        child.configure(bg=cores["btn_bg"], fg=cores["fg"], activebackground=cores["accent"])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=cores["bg"], fg=cores["fg"])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=cores["btn_bg"], fg=cores["fg"], activebackground=cores["accent"])
            elif isinstance(widget, tk.Entry) and not isinstance(widget, ttk.Combobox):
                widget.configure(bg=cores["input_bg"], fg=cores["fg"], insertbackground=cores["fg"])

    def login_existente(self):
        nome = self.combo_perfis.get()
        if nome: self.finalizar_login(nome)

    def login_novo(self):
        nome = self.entrada_novo.get().strip()
        if nome: self.finalizar_login(nome)

    def finalizar_login(self, nome: Optional[str]):
        self.frame.destroy()
        self.on_login_success(nome)


class TerereApp:
    def __init__(self, root: tk.Tk, nome_perfil: Optional[str], on_logout: Callable[[], None]):
        self.root = root
        self.on_logout = on_logout
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(expand=True, fill="both")
        
        self.var_dic_lang = tk.StringVar(value="pt" if config.GerenciadorIdiomas.idioma_ativo == "pt" else "es")
        
        self.dicionario = DicionarioManager()
        self.dicionario.carregar(self.var_dic_lang.get())
        
        self.perfil = PerfilManager()
        self.perfil.carregar(nome_perfil)
        self.timer_busca = None
        
        self.vars_textos = {chave: tk.StringVar() for chave in config.GerenciadorIdiomas.TEXTOS["pt"].keys()}
        self.construir_interface_principal()

    def construir_interface_principal(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        frame_top = ttk.Frame(self.frame_principal)
        frame_top.pack(fill="x", padx=10, pady=(10, 5))
        
        ttk.Label(frame_top, textvariable=self.vars_textos["lbl_lang"], font=("Helvetica", 11, "bold")).pack(side="left", padx=(0,5))
        for lang in ["pt", "es", "gn"]:
            ttk.Button(frame_top, text=lang.upper(), command=lambda l=lang: self.mudar_idioma(l), width=4).pack(side="left", padx=2)
        
        ttk.Button(frame_top, textvariable=self.vars_textos["btn_theme"], command=self.alternar_tema).pack(side="right", padx=5)

        self.construir_teclado_inteligente()

        self.abas = ttk.Notebook(self.frame_principal)
        self.aba_perfil = ttk.Frame(self.abas)
        self.aba_lab = ttk.Frame(self.abas)
        self.aba_dicionario = ttk.Frame(self.abas)
        self.aba_quiz = ttk.Frame(self.abas)
        self.aba_guia = ttk.Frame(self.abas)
        
        self.abas.add(self.aba_perfil, text="Perfil") 
        self.abas.add(self.aba_lab, text="Laboratório")
        self.abas.add(self.aba_dicionario, text="Dicionário")
        self.abas.add(self.aba_quiz, text="Praticar")
        self.abas.add(self.aba_guia, text="Guia Prático")
        self.abas.pack(expand=True, fill="both", padx=10, pady=10)

        self.construir_aba_perfil()
        self.construir_aba_laboratorio()
        self.construir_aba_dicionario()
        self.construir_aba_quiz()
        self.construir_aba_guia()
        
        self.aplicar_tema()
        self.mudar_idioma(config.GerenciadorIdiomas.idioma_ativo)
        self.buscar_dicionario()

    def construir_teclado_inteligente(self):
        frame_teclado = ttk.Frame(self.frame_principal)
        frame_teclado.pack(fill="x", padx=10, pady=5)
        ttk.Label(frame_teclado, textvariable=self.vars_textos["lbl_keyboard"], font=("Helvetica", 11, "bold")).pack(side="left", padx=(0,5))
        
        for char in ['ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ỹ', 'g̃', 'ñ']:
            ttk.Button(frame_teclado, text=char, width=3, takefocus=False, command=lambda c=char: self.inserir_texto(c)).pack(side="left", padx=1)
        
        ttk.Button(frame_teclado, text="Nasalizar (~)", width=12, takefocus=False, command=self.acao_nasalizar).pack(side="left", padx=5)
        ttk.Button(frame_teclado, text="Puso (')", width=8, takefocus=False, command=lambda: self.inserir_texto("'")).pack(side="left", padx=1)

    def inserir_texto(self, char: str):
        widget = self.root.focus_get()
        if isinstance(widget, (tk.Entry, tk.Text)):
            widget.insert(tk.INSERT, char)
            
    def acao_nasalizar(self):
        widget = self.root.focus_get()
        if isinstance(widget, tk.Entry):
            txt = widget.get()
            for i in range(len(txt)-1, -1, -1):
                if txt[i].lower() in GramaticaGuarani.VOGAIS_NASAIS:
                    novo_char = GramaticaGuarani.VOGAIS_NASAIS[txt[i].lower()]
                    novo_char = novo_char.upper() if txt[i].isupper() else novo_char
                    widget.delete(i)
                    widget.insert(i, novo_char)
                    break

    def alternar_tema(self):
        config.GerenciadorTemas.alternar()
        self.aplicar_tema()

    def aplicar_tema(self):
        t = config.GerenciadorTemas.get()
        is_dark = config.GerenciadorTemas.tema_ativo == "dark"
        
        self.root.configure(bg=t["bg"])
        self.style.configure("TFrame", background=t["bg"])
        self.style.configure("TLabel", background=t["bg"], foreground=t["fg"], font=("Helvetica", 11))
        self.style.configure("Titulo.TLabel", font=("Trebuchet MS", 16, "bold"))
        self.style.configure("Destacado.TLabel", font=("Trebuchet MS", 18, "bold"), foreground=t["accent"])
        
        self.style.configure("TButton", background=t["btn_bg"], foreground=t["fg"], font=("Helvetica", 10, "bold"))
        self.style.map("TButton", background=[("active", t["accent"])], foreground=[("active", t["bg"])])
        
        self.style.configure("Treeview", background=t["input_bg"], foreground=t["fg"], fieldbackground=t["input_bg"], borderwidth=0)
        self.style.configure("Treeview.Heading", background=t["btn_bg"], foreground=t["fg"], font=("Helvetica", 11, "bold"))
        
        self.style.configure("TNotebook", background=t["bg"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=t["bg"], foreground=t["fg"], font=("Helvetica", 11, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", t["btn_bg"])], foreground=[("selected", t["accent"])])
        
        self.style.configure("TLabelframe", background=t["bg"], foreground=t["fg"])
        self.style.configure("TLabelframe.Label", background=t["bg"], foreground=t["fg"])
        
        if hasattr(self, 'tab_dic'):
            cor_texto = "#1e1e2e" if is_dark else "#ffffff"
            self.tab_dic.tag_configure("Verbo", background="#ff8787" if is_dark else "#c92a2a", foreground=cor_texto)
            self.tab_dic.tag_configure("Substantivo", background="#4dabf7" if is_dark else "#1864ab", foreground=cor_texto)
            self.tab_dic.tag_configure("Adjetivo", background="#69db7c" if is_dark else "#2b8a3e", foreground=cor_texto)
            self.tab_dic.tag_configure("Adverbio", background="#ffa94d" if is_dark else "#d9480f", foreground=cor_texto)
            self.tab_dic.tag_configure("Indefinido", background="#da77f2" if is_dark else "#862e9c", foreground=cor_texto)
            self.tab_dic.tag_configure("Outros", background=t["input_bg"], foreground=t["fg"])
        
        for widget in self.frame_principal.winfo_children():
            self._atualizar_cores_filhos(widget, t)

    def _atualizar_cores_filhos(self, widget, cores):
        if isinstance(widget, (tk.Entry, tk.Text)) and not isinstance(widget, ttk.Widget):
            try: widget.configure(bg=cores["input_bg"], fg=cores["fg"], insertbackground=cores["fg"], relief="flat")
            except tk.TclError: pass
        elif isinstance(widget, tk.Button) and not isinstance(widget, ttk.Widget):
            try:
                if widget.cget("bg") not in [cores.get("accent"), cores.get("err")]:
                    widget.configure(bg=cores["btn_bg"], fg=cores["fg"])
            except tk.TclError: pass

        for child in widget.winfo_children():
            self._atualizar_cores_filhos(child, cores)

    def mudar_idioma(self, idioma: str):
        config.GerenciadorIdiomas.idioma_ativo = idioma
        t = config.GerenciadorIdiomas.TEXTOS[idioma]
        self.root.title(t.get("title_app", "Terere"))
        
        for chave, var in self.vars_textos.items():
            if chave in t: var.set(t[chave])
            
        if hasattr(self, 'abas') and self.abas.winfo_exists():
            self.abas.tab(self.aba_perfil, text=t.get("tab_profile", "Perfil"))
            self.abas.tab(self.aba_lab, text=t.get("tab_lab", "Laboratório"))
            self.abas.tab(self.aba_dicionario, text=t.get("tab_dict", "Dicionário"))
            self.abas.tab(self.aba_quiz, text=t.get("tab_quiz", "Praticar"))
            self.abas.tab(self.aba_guia, text=t.get("tab_guide", "Guia"))
            
            if hasattr(self, 'tab_conj'):
                self.tab_conj.heading("pessoa", text=t.get("col_pronoun", "Pessoa"))
                self.tab_conj.heading("presente", text=t.get("col_present", "Presente"))
                self.tab_conj.heading("passado", text=t.get("col_past", "Passado"))
                self.tab_conj.heading("futuro", text=t.get("col_future", "Futuro"))
            
            if hasattr(self, 'tab_dic'):
                self.tab_dic.heading("gn", text=t.get("col_gn", "Guarani"))
                nome_col_trad = t.get("col_es", "Tradução") if self.var_dic_lang.get() == "es" else t.get("col_pt", "Português")
                self.tab_dic.heading("es", text=nome_col_trad)
                self.tab_dic.heading("tipo", text=t.get("col_tipo", "Classe"))

        if hasattr(self, 'caixa_texto_guia'):
            self.lbl_titulo_guia.config(text=t.get("guide_title", ""))
            self.caixa_texto_guia.config(state="normal")
            self.caixa_texto_guia.delete("1.0", tk.END)
            self.caixa_texto_guia.insert(tk.END, t.get("guide_text", ""))
            self.caixa_texto_guia.config(state="disabled")
            
        if hasattr(self, 'var_dic_lang'):
            self.dicionario.carregar(self.var_dic_lang.get())
            
        self.buscar_dicionario()
        self.atualizar_contadores()
        self.atualizar_ui_perfil()
        if hasattr(self, 'lbl_quiz_score'): self.atualizar_placar_quiz()

    def construir_aba_perfil(self):
        ttk.Label(self.aba_perfil, textvariable=self.vars_textos["prof_title"], style="Titulo.TLabel").pack(pady=20)
        
        frame_contas = ttk.Frame(self.aba_perfil)
        frame_contas.pack(pady=10)
        ttk.Label(frame_contas, textvariable=self.vars_textos["prof_sel_lbl"]).pack(side="left", padx=5)
        
        self.combo_perfis = ttk.Combobox(frame_contas, font=("Helvetica", 11), state="readonly", width=15)
        self.combo_perfis.pack(side="left", padx=5)
        
        ttk.Button(frame_contas, textvariable=self.vars_textos["btn_load"], command=lambda: self.carregar_perfil_ui(self.combo_perfis.get())).pack(side="left", padx=2)
        ttk.Button(frame_contas, textvariable=self.vars_textos["btn_del"], command=self.excluir_perfil).pack(side="left", padx=2)

        self.lbl_aviso_visitante = ttk.Label(self.aba_perfil, textvariable=self.vars_textos["prof_guest_warn"])
        self.lbl_dias_ativos = ttk.Label(self.aba_perfil)
        self.lbl_stats_quiz = ttk.Label(self.aba_perfil)
        
        self.lbl_aviso_visitante.pack(pady=10)
        self.lbl_dias_ativos.pack(pady=5)
        self.lbl_stats_quiz.pack(pady=5)
        
        ttk.Button(self.aba_perfil, textvariable=self.vars_textos["btn_logout"], command=self.deslogar).pack(pady=25)
        
        self.atualizar_combo_perfis()
        self.atualizar_ui_perfil()

    def atualizar_combo_perfis(self):
        perfis = self.perfil.listar_perfis()
        self.combo_perfis.config(values=perfis + ["Visitante"])
        self.combo_perfis.set(self.perfil.nome_atual if self.perfil.nome_atual in perfis else "Visitante")

    def carregar_perfil_ui(self, nome: Optional[str]):
        if nome == "Visitante" or not nome: nome = None
        self.perfil.carregar(nome)
        self.atualizar_combo_perfis()
        self.atualizar_ui_perfil()

    def excluir_perfil(self):
        nome = self.combo_perfis.get()
        if nome and nome != "Visitante":
            if messagebox.askyesno("Confirmar", f"Excluir '{nome}'?"):
                if os.path.exists(f"perfil_{nome}.json"):
                    os.remove(f"perfil_{nome}.json")
                self.carregar_perfil_ui(None)

    def atualizar_ui_perfil(self):
        t = config.GerenciadorIdiomas.TEXTOS[config.GerenciadorIdiomas.idioma_ativo]
        if self.perfil.nome_atual:
            self.lbl_aviso_visitante.pack_forget()
            dias = len(self.perfil.dados["dias_ativos"])
            acertos = self.perfil.dados["estatisticas"]["acertos"]
            erros = self.perfil.dados["estatisticas"]["erros"]
        else:
            self.lbl_aviso_visitante.pack(pady=10)
            dias, acertos, erros = 0, self.perfil.pontuacao_sessao["acertos"], self.perfil.pontuacao_sessao["erros"]

        total = acertos + erros
        taxa = round((acertos / total * 100), 1) if total > 0 else 0
        self.lbl_dias_ativos.config(text=t["prof_days"].format(dias))
        self.lbl_stats_quiz.config(text=t["prof_quiz_stats"].format(acertos, erros, taxa))

    def deslogar(self):
        self.frame_principal.destroy()
        self.on_logout()

    def construir_aba_laboratorio(self):
        ttk.Label(self.aba_lab, textvariable=self.vars_textos["lab_title"], style="Titulo.TLabel").pack(pady=15)
        
        frame_busca = ttk.Frame(self.aba_lab)
        frame_busca.pack(pady=5)
        ttk.Label(frame_busca, textvariable=self.vars_textos["lab_sub"]).pack(side="left", padx=5)
        self.entrada_lab = tk.Entry(frame_busca, width=25, font=("Trebuchet MS", 14), justify="center")
        self.entrada_lab.pack(side="left", padx=5)
        self.entrada_lab.bind('<Return>', lambda e: self.acao_conjugar())
        
        ttk.Label(frame_busca, textvariable=self.vars_textos["lab_paradigma"]).pack(side="left", padx=(10,2))
        self.combo_paradigma = ttk.Combobox(frame_busca, values=["Automático", "Areal", "Aireal", "Chendal"], state="readonly", width=12)
        self.combo_paradigma.current(0)
        self.combo_paradigma.pack(side="left", padx=5)
        
        ttk.Button(frame_busca, textvariable=self.vars_textos["btn_conjugate"], command=self.acao_conjugar).pack(side="left", padx=5)

        self.lbl_tipo_verbo = ttk.Label(self.aba_lab, font=("Helvetica", 11, "bold"))
        self.lbl_tipo_verbo.pack(pady=5)

        frame_corpo = ttk.Frame(self.aba_lab)
        frame_corpo.pack(fill="both", expand=True, padx=10, pady=5)
        
        scroll_lab = ttk.Scrollbar(frame_corpo, orient="vertical")
        scroll_lab.pack(side="right", fill="y")
        
        self.tab_conj = ttk.Treeview(frame_corpo, columns=("pessoa", "presente", "passado", "futuro"), show="headings", height=7, yscrollcommand=scroll_lab.set)
        self.tab_conj.column("pessoa", width=120, anchor="center")
        self.tab_conj.column("presente", width=150, anchor="center")
        self.tab_conj.column("passado", width=150, anchor="center")
        self.tab_conj.column("futuro", width=150, anchor="center")
        self.tab_conj.pack(side="left", fill="both", expand=True)
        scroll_lab.config(command=self.tab_conj.yview)

        self.lbl_triforme = ttk.Label(self.aba_lab, font=("Helvetica", 12, "bold"))
        self.lbl_triforme.pack(pady=10)

    def acao_conjugar(self):
        entrada = self.entrada_lab.get().strip().lower()
        if not entrada: return
            
        raizes_dicionario = list(self.dicionario.palavras.keys())
        analise = GramaticaGuarani.descobrir_infinitivo(entrada, raizes_dicionario)
        
        if entrada in self.dicionario.palavras:
            raiz = entrada
            texto_analise = f"Raiz identificada: '{raiz}' (Encontrada no dicionário)"
        else:
            raiz = analise["raiz"]
            if analise["sucesso"]:
                texto_analise = f"Análise Completa: Infinitivo '{raiz}' | Pessoa: {analise['pessoa']} | Tempo: {analise['tempo']} | {analise['polaridade']}"
            else:
                texto_analise = f"Infinitivo assumido: '{raiz}'"

        harmonia = GramaticaGuarani.detectar_nasalidade(raiz)
        idx_harmonia = 1 if harmonia == "nasal" else 0
        
        paradigma_sel = self.combo_paradigma.get().lower()
        if paradigma_sel == "automático":
            dados_dict = self.dicionario.palavras.get(raiz, {})
            subtipo = dados_dict.get("subtipo", "").lower()
            if subtipo in ["areal", "aireal", "chendal"]:
                paradigma_sel = subtipo
            elif analise["sucesso"] and analise["paradigma"].lower() in ["areal", "aireal", "chendal"]:
                paradigma_sel = analise["paradigma"].lower()
            else:
                paradigma_sel = "areal"
                
        texto_analise += f"  (Harmonia: {harmonia.capitalize()} | Paradigma: {paradigma_sel.capitalize()})"
        self.lbl_tipo_verbo.config(text=texto_analise)

        self.tab_conj.delete(*self.tab_conj.get_children())
        ordem_pessoas = ["1s", "2s", "3", "1pi", "1pe", "2p"]
        nomes_pessoas = ["Che", "Nde", "Ha'e", "Ñande", "Ore", "Peẽ"]
        
        prefixos_afirm = GramaticaGuarani.PREFIXOS[paradigma_sel]["afirm"]
        
        for i, cod_pes in enumerate(ordem_pessoas):
            pref_tupla = prefixos_afirm.get(cod_pes, ("", ""))
            pref = pref_tupla[idx_harmonia] if len(pref_tupla) > 1 else pref_tupla[0]
            
            forma_base = f"{pref}{raiz}"
            self.tab_conj.insert("", "end", values=(nomes_pessoas[i], forma_base, f"{forma_base}kuri", f"{forma_base}ta"))

        dados_dict = self.dicionario.palavras.get(raiz, {})
        if dados_dict.get("subtipo", "").lower() == "triforme" and len(raiz) > 1:
            r_form = 'r' + raiz[1:]
            h_form = 'h' + raiz[1:]
            self.lbl_triforme.config(text=f"Triforme: {raiz} (Absoluto) | che {r_form} (Meu) | {h_form} (Dele/a)")
        else:
            self.lbl_triforme.config(text="")

    def construir_aba_dicionario(self):
        ttk.Label(self.aba_dicionario, textvariable=self.vars_textos["title_dict"], style="Titulo.TLabel").pack(pady=(10, 0))

        self.lbl_total_verbetes = ttk.Label(self.aba_dicionario, font=("Helvetica", 10, "italic"))
        self.lbl_total_verbetes.pack(pady=(0, 10))

        frame_base = ttk.Frame(self.aba_dicionario)
        frame_base.pack(pady=5)
        ttk.Label(frame_base, textvariable=self.vars_textos["lbl_base_estudo"]).pack(side="left", padx=5)
        
        ttk.Radiobutton(frame_base, textvariable=self.vars_textos["rad_gn_pt"], variable=self.var_dic_lang, value="pt", command=self.trocar_dicionario).pack(side="left", padx=5)
        ttk.Radiobutton(frame_base, textvariable=self.vars_textos["rad_gn_es"], variable=self.var_dic_lang, value="es", command=self.trocar_dicionario).pack(side="left", padx=5)

        frame_busca = ttk.Frame(self.aba_dicionario)
        frame_busca.pack(fill="x", padx=10, pady=(5,0))
        ttk.Label(frame_busca, textvariable=self.vars_textos["subtitle_dict"]).pack(side="left")
        self.entrada_filtro = tk.Entry(frame_busca, width=40, font=("Helvetica", 11))
        self.entrada_filtro.pack(side="left", padx=10)
        self.entrada_filtro.bind("<KeyRelease>", self.ao_digitar_filtro)

        frame_tabela = ttk.Frame(self.aba_dicionario)
        frame_tabela.pack(pady=5, fill="both", expand=True, padx=10)
        
        scroll_dic = ttk.Scrollbar(frame_tabela, orient="vertical")
        scroll_dic.pack(side="right", fill="y")
        
        self.tab_dic = ttk.Treeview(frame_tabela, columns=("gn", "es", "tipo"), show="headings", height=6, yscrollcommand=scroll_dic.set)
        self.tab_dic.column("gn", width=120)
        self.tab_dic.column("es", width=180)
        self.tab_dic.column("tipo", width=100)
        self.tab_dic.pack(side="left", fill="both", expand=True)
        scroll_dic.config(command=self.tab_dic.yview)

        self.tab_dic.bind("<<TreeviewSelect>>", self.selecionar_item_dic)

        self.frame_editor = ttk.LabelFrame(self.aba_dicionario, text="Detalhes e Edição")
        self.frame_editor.pack(fill="x", padx=10, pady=5)
        
        f1 = ttk.Frame(self.frame_editor); f1.pack(fill="x", pady=2)
        self.ed_gn = tk.Entry(f1, width=15, font=("Helvetica", 11)); self.ed_gn.pack(side="left", padx=5)
        self.ed_tr = tk.Entry(f1, width=25, font=("Helvetica", 11)); self.ed_tr.pack(side="left", padx=5)
        self.ed_tipo = ttk.Combobox(f1, values=["Verbo", "Substantivo", "Adjetivo", "Adverbio", "Indefinido", "Outros"], width=12); self.ed_tipo.pack(side="left", padx=5)
        
        f2 = ttk.Frame(self.frame_editor); f2.pack(fill="x", pady=2)
        ttk.Label(f2, textvariable=self.vars_textos["lbl_ex_gn"]).pack(side="left", padx=5)
        self.ed_ex_gn = tk.Entry(f2, width=35, font=("Helvetica", 11)); self.ed_ex_gn.pack(side="left", padx=5)
        ttk.Label(f2, textvariable=self.vars_textos["lbl_ex_es"]).pack(side="left", padx=5)
        self.ed_ex_pt = tk.Entry(f2, width=35, font=("Helvetica", 11)); self.ed_ex_pt.pack(side="left", padx=5)

        f3 = ttk.Frame(self.frame_editor); f3.pack(fill="x", pady=2)
        ttk.Button(f3, textvariable=self.vars_textos["ed_save"], command=self.salvar_palavra).pack(side="left", padx=5)
        ttk.Button(f3, textvariable=self.vars_textos["ed_del_word"], command=self.excluir_palavra).pack(side="left", padx=5)

    def trocar_dicionario(self):
        idioma_alvo = self.var_dic_lang.get()
        self.dicionario.carregar(idioma_alvo)
        self.buscar_dicionario()
        self.atualizar_contadores()
        
        t = config.GerenciadorIdiomas.TEXTOS[config.GerenciadorIdiomas.idioma_ativo]
        nome_coluna = t.get("col_es", "Tradução") if idioma_alvo == "es" else t.get("col_pt", "Português")
        self.tab_dic.heading("es", text=nome_coluna)
        
        if hasattr(self, 'lbl_quiz_score'):
            self.gerar_pergunta_quiz()

    def atualizar_contadores(self):
        if not hasattr(self, 'lbl_total_verbetes'): return
        contagens = {"es": 0, "pt": 0}
        
        for lang, arquivo in [("es", "terere_es.csv"), ("pt", "terere_pt.csv")]:
            if os.path.exists(arquivo):
                try:
                    with open(arquivo, "r", encoding="utf-8") as f:
                        leitor = csv.reader(f, delimiter=";")
                        contagens[lang] = sum(1 for linha in leitor if len(linha) >= 2 and linha[1].strip() != "")
                except Exception:
                    pass
                    
        t = config.GerenciadorIdiomas.TEXTOS[config.GerenciadorIdiomas.idioma_ativo]
        texto = t.get("lbl_total_dict", "Traduzidos: {} (ES) | {} (PT)").format(contagens["es"], contagens["pt"])
        self.lbl_total_verbetes.config(text=texto)

    def limpar_campos_editor(self):
        for c in [self.ed_gn, self.ed_tr, self.ed_ex_gn, self.ed_ex_pt]: c.delete(0, tk.END)

    def ao_digitar_filtro(self, event):
        if self.timer_busca: self.root.after_cancel(self.timer_busca)
        self.timer_busca = self.root.after(300, self.buscar_dicionario)

    def buscar_dicionario(self):
        termo = self.entrada_filtro.get().strip().lower()
        termo_norm = GramaticaGuarani.normalizar(termo)
        self.tab_dic.delete(*self.tab_dic.get_children())
        
        for avanee, dados in self.dicionario.palavras.items():
            if termo_norm in dados["gn_norm"] or termo in dados["traduccion"].lower():
                tipo = dados.get("tipo", "Outros")
                if dados["traduccion"] != "":
                    self.tab_dic.insert("", "end", values=(avanee, dados["traduccion"], tipo), tags=(tipo,))

    def selecionar_item_dic(self, event):
        selecionado = self.tab_dic.selection()
        if selecionado:
            raiz = self.tab_dic.item(selecionado[0])['values'][0]
            dados = self.dicionario.palavras.get(raiz, {})
            self.limpar_campos_editor()
            self.ed_gn.insert(0, raiz)
            self.ed_tr.insert(0, dados.get("traduccion", ""))
            self.ed_tipo.set(dados.get("tipo", "Outros"))
            self.ed_ex_gn.insert(0, dados.get("ex_gn", ""))
            self.ed_ex_pt.insert(0, dados.get("ex_pt", ""))

    def salvar_palavra(self):
        gn, tr, tp = self.ed_gn.get().strip().lower(), self.ed_tr.get().strip(), self.ed_tipo.get().strip()
        ex_g, ex_p = self.ed_ex_gn.get().strip(), self.ed_ex_pt.get().strip()
        
        sub_existente = self.dicionario.palavras.get(gn, {}).get("subtipo", "Normal")
        
        if gn and tr:
            self.dicionario.adicionar_ou_atualizar(gn, tr, tp, sub_existente, ex_g, ex_p)
            self.buscar_dicionario()
            self.atualizar_contadores()
            messagebox.showinfo("Sucesso", "Dicionário atualizado!")
            self.aplicar_tema()

    def excluir_palavra(self):
        gn = self.ed_gn.get().strip().lower()
        if gn in self.dicionario.palavras:
            self.dicionario.excluir(gn)
            self.buscar_dicionario()
            self.atualizar_contadores()
            self.limpar_campos_editor()

    def construir_aba_quiz(self):
        ttk.Label(self.aba_quiz, textvariable=self.vars_textos["quiz_title"], style="Titulo.TLabel").pack(pady=(25, 10))
        self.lbl_quiz_palavra = ttk.Label(self.aba_quiz, style="Destacado.TLabel")
        self.lbl_quiz_palavra.pack(pady=10)
        
        self.lbl_quiz_exemplo = ttk.Label(self.aba_quiz, font=("Helvetica", 11, "italic"))
        self.lbl_quiz_exemplo.pack(pady=(0,15))
        
        self.frame_quiz_btns = ttk.Frame(self.aba_quiz)
        self.frame_quiz_btns.pack(pady=5)
        
        self.botoes_quiz = []
        for i in range(4):
            btn = tk.Button(self.frame_quiz_btns, font=("Helvetica", 12), width=35, pady=6, command=lambda idx=i: self.checar_resposta_quiz(idx))
            btn.pack(pady=4)
            self.botoes_quiz.append(btn)
            
        self.lbl_quiz_score = ttk.Label(self.aba_quiz, font=("Helvetica", 12, "bold"))
        self.lbl_quiz_score.pack(pady=15)
        ttk.Button(self.aba_quiz, textvariable=self.vars_textos["btn_next"], command=self.gerar_pergunta_quiz).pack()
        self.gerar_pergunta_quiz()

    def atualizar_placar_quiz(self):
        t = config.GerenciadorIdiomas.TEXTOS[config.GerenciadorIdiomas.idioma_ativo]
        stats = self.perfil.dados['estatisticas'] if self.perfil.nome_atual else self.perfil.pontuacao_sessao
        self.lbl_quiz_score.config(text=t["quiz_score"].format(stats['acertos'], stats['erros']))

    def gerar_pergunta_quiz(self):
        palavras_validas = [k for k, v in self.dicionario.palavras.items() if v.get("traduccion") != ""]
        if len(palavras_validas) < 4: return
        
        pesos = []
        for r in palavras_validas:
            if self.perfil.nome_atual and r in self.perfil.dados.get("palavras_info", {}):
                erros = self.perfil.dados["palavras_info"][r].get("erros", 0)
                acertos = self.perfil.dados["palavras_info"][r].get("acertos", 0)
                peso = max(1, 10 + (erros * 5) - (acertos * 2))
            else: peso = 10
            pesos.append(peso)
            
        self.palavra_atual_quiz = random.choices(palavras_validas, weights=pesos, k=1)[0]
        dados_palavra = self.dicionario.palavras[self.palavra_atual_quiz]
        trad_correta = dados_palavra["traduccion"]
        
        opcoes = [trad_correta]
        while len(opcoes) < 4:
            errada = self.dicionario.palavras[random.choice(palavras_validas)]["traduccion"]
            if errada not in opcoes: opcoes.append(errada)
            
        random.shuffle(opcoes)
        self.resposta_correta_quiz = opcoes.index(trad_correta)
        
        self.lbl_quiz_palavra.config(text=self.palavra_atual_quiz.upper())
        exemplo = dados_palavra.get("ex_gn", "")
        self.lbl_quiz_exemplo.config(text=f'"{exemplo}"' if exemplo else "")
        
        t = config.GerenciadorTemas.get()
        for i, btn in enumerate(self.botoes_quiz):
            btn.config(text=opcoes[i], bg=t["btn_bg"], fg=t["fg"])
            
        self.atualizar_placar_quiz()

    def checar_resposta_quiz(self, idx_escolhido):
        if not hasattr(self, 'resposta_correta_quiz') or self.resposta_correta_quiz is None: return
        acertou = (idx_escolhido == self.resposta_correta_quiz)
        
        self.perfil.registrar_resposta_srs(self.palavra_atual_quiz, acertou)
        self.atualizar_ui_perfil()
        self.atualizar_placar_quiz()
        
        t = config.GerenciadorTemas.get()
        if acertou:
            self.botoes_quiz[idx_escolhido].config(bg=t["accent"], fg=t["btn_fg"]) 
        else:
            self.botoes_quiz[idx_escolhido].config(bg=t["err"], fg=t["btn_fg"]) 
            self.botoes_quiz[self.resposta_correta_quiz].config(bg=t["accent"], fg=t["btn_fg"])
            
        self.resposta_correta_quiz = None 
        self.root.after(1500, self.gerar_pergunta_quiz)

    def construir_aba_guia(self):
        self.lbl_titulo_guia = ttk.Label(self.aba_guia, style="Titulo.TLabel")
        self.lbl_titulo_guia.pack(pady=15)
        
        self.caixa_texto_guia = tk.Text(self.aba_guia, font=("Helvetica", 11), wrap="word", padx=15, pady=15, relief="flat", state="disabled")
        self.caixa_texto_guia.pack(fill="both", expand=True, padx=10, pady=10)