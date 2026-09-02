import os
import csv
import json
import datetime
from tkinter import messagebox
from typing import Dict, List, Optional, Any
import config

class GramaticaGuarani:
    TABELA_NORM = str.maketrans("áéíóúýãẽĩõũỹñ", "aeiouyaeiouyn", "\u0303'")
    VOGAIS_NASAIS = {'a': 'ã', 'e': 'ẽ', 'i': 'ĩ', 'o': 'õ', 'u': 'ũ', 'y': 'ỹ', 'g': 'g̃', 'n': 'ñ'}
    
    PREFIXOS = {
        "areal": {
            "afirm": {"1s": ("a","a"), "2s": ("re","re"), "3": ("o","o"), "1pi": ("ja","ña"), "1pe": ("ro","ro"), "2p": ("pe","pe")},
            "neg": {"1s": ("nda","na"), "2s": ("ndere","nere"), "3": ("ndo","no"), "1pi": ("ndaja","naña"), "1pe": ("ndoro","noro"), "2p": ("ndape","nape")}
        },
        "aireal": {
            "afirm": {"1s": ("ai","ai"), "2s": ("rei","rei"), "3": ("oi","oi"), "1pi": ("jai","ñai"), "1pe": ("roi","roi"), "2p": ("pei","pei")},
            "neg": {"1s": ("ndai","nai"), "2s": ("nderei","nerei"), "3": ("ndoi","noi"), "1pi": ("ndajai","nañai"), "1pe": ("ndoroi","noroi"), "2p": ("ndapei","napei")}
        },
        "chendal": {
            "afirm": {"1s": ("che ","che "), "2s": ("nde ","ne "), "3": ("i","iñ"), "1pi": ("ñande ","ñane "), "1pe": ("ore ","ore "), "2p": ("pende ","pene ")}
        }
    }

    @staticmethod
    def detectar_nasalidade(palavra: str) -> str:
        letras_nasais = ['ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ỹ', 'g̃', 'm', 'n', 'ñ']
        return "nasal" if any(l in palavra.lower() for l in letras_nasais) else "oral"

    @staticmethod
    def normalizar(texto: str) -> str:
        return texto.lower().translate(GramaticaGuarani.TABELA_NORM)

    @classmethod
    def descobrir_infinitivo(cls, palavra_conjugada: str, raizes_conhecidas: list = None) -> dict:
        palavra = palavra_conjugada.lower().strip()
        if raizes_conhecidas is None: 
            raizes_conhecidas = []
            
        mapa_pessoas = {"1s": "1ª Sing", "2s": "2ª Sing", "3": "3ª", 
                        "1pi": "1ª Plur Incl", "1pe": "1ª Plur Excl", "2p": "2ª Plur"}
        
        irregulares = {
            "aha": {"raiz": "ho", "pessoa": "1ª Sing", "pol": "Afirmativo"}, "ndahái": {"raiz": "ho", "pessoa": "1ª Sing", "pol": "Negativo"},
            "reho": {"raiz": "ho", "pessoa": "2ª Sing", "pol": "Afirmativo"}, "nderehói": {"raiz": "ho", "pessoa": "2ª Sing", "pol": "Negativo"},
            "oho": {"raiz": "ho", "pessoa": "3ª", "pol": "Afirmativo"}, "ndohói": {"raiz": "ho", "pessoa": "3ª", "pol": "Negativo"},
            "jaha": {"raiz": "ho", "pessoa": "1ª Plur Incl", "pol": "Afirmativo"}, "ndajahái": {"raiz": "ho", "pessoa": "1ª Plur Incl", "pol": "Negativo"},
            "ñaha": {"raiz": "ho", "pessoa": "1ª Plur Incl", "pol": "Afirmativo"}, "nañahái": {"raiz": "ho", "pessoa": "1ª Plur Incl", "pol": "Negativo"},
            "roho": {"raiz": "ho", "pessoa": "1ª Plur Excl", "pol": "Afirmativo"}, "ndorohói": {"raiz": "ho", "pessoa": "1ª Plur Excl", "pol": "Negativo"},
            "peho": {"raiz": "ho", "pessoa": "2ª Plur", "pol": "Afirmativo"}, "ndapehói": {"raiz": "ho", "pessoa": "2ª Plur", "pol": "Negativo"},

            "aju": {"raiz": "ju", "pessoa": "1ª Sing", "pol": "Afirmativo"}, "ndajúi": {"raiz": "ju", "pessoa": "1ª Sing", "pol": "Negativo"},
            "reju": {"raiz": "ju", "pessoa": "2ª Sing", "pol": "Afirmativo"}, "nderejúi": {"raiz": "ju", "pessoa": "2ª Sing", "pol": "Negativo"},
            "ou": {"raiz": "ju", "pessoa": "3ª", "pol": "Afirmativo"}, "ndoúi": {"raiz": "ju", "pessoa": "3ª", "pol": "Negativo"},
            "jaju": {"raiz": "ju", "pessoa": "1ª Plur Incl", "pol": "Afirmativo"}, "ndajajúi": {"raiz": "ju", "pessoa": "1ª Plur Incl", "pol": "Negativo"},
            "ñaju": {"raiz": "ju", "pessoa": "1ª Plur Incl", "pol": "Afirmativo"}, "nañajúi": {"raiz": "ju", "pessoa": "1ª Plur Incl", "pol": "Negativo"},
            "roju": {"raiz": "ju", "pessoa": "1ª Plur Excl", "pol": "Afirmativo"}, "ndorojúi": {"raiz": "ju", "pessoa": "1ª Plur Excl", "pol": "Negativo"},
            "peju": {"raiz": "ju", "pessoa": "2ª Plur", "pol": "Afirmativo"}, "ndapejúi": {"raiz": "ju", "pessoa": "2ª Plur", "pol": "Negativo"},

            "ha'u": {"raiz": "'u", "pessoa": "1ª Sing", "pol": "Afirmativo"}, "nda'úi": {"raiz": "'u", "pessoa": "1ª Sing", "pol": "Negativo"},
            "re'u": {"raiz": "'u", "pessoa": "2ª Sing", "pol": "Afirmativo"}, "ndere'úi": {"raiz": "'u", "pessoa": "2ª Sing", "pol": "Negativo"},
            "ho'u": {"raiz": "'u", "pessoa": "3ª", "pol": "Afirmativo"}, "ndo'úi": {"raiz": "'u", "pessoa": "3ª", "pol": "Negativo"},
            "ja'u": {"raiz": "'u", "pessoa": "1ª Plur Incl", "pol": "Afirmativo"}, "ndaja'úi": {"raiz": "'u", "pessoa": "1ª Plur Incl", "pol": "Negativo"},
            "ña'u": {"raiz": "'u", "pessoa": "1ª Plur Incl", "pol": "Afirmativo"}, "naña'úi": {"raiz": "'u", "pessoa": "1ª Plur Incl", "pol": "Negativo"},
            "ro'u": {"raiz": "'u", "pessoa": "1ª Plur Excl", "pol": "Afirmativo"}, "ndoro'úi": {"raiz": "'u", "pessoa": "1ª Plur Excl", "pol": "Negativo"},
            "pe'u": {"raiz": "'u", "pessoa": "2ª Plur", "pol": "Afirmativo"}, "ndape'úi": {"raiz": "'u", "pessoa": "2ª Plur", "pol": "Negativo"},
            
            "ha'e": {"raiz": "e", "pessoa": "1ª Sing", "pol": "Afirmativo"}, "nda'éi": {"raiz": "e", "pessoa": "1ª Sing", "pol": "Negativo"},
            "ere": {"raiz": "e", "pessoa": "2ª Sing", "pol": "Afirmativo"}, "ndere'éi": {"raiz": "e", "pessoa": "2ª Sing", "pol": "Negativo"},
            "he'i": {"raiz": "e", "pessoa": "3ª", "pol": "Afirmativo"}, "nde'íi": {"raiz": "e", "pessoa": "3ª", "pol": "Negativo"},
            "ja'e": {"raiz": "e", "pessoa": "1ª Plur Incl", "pol": "Afirmativo"}, "ndaja'éi": {"raiz": "e", "pessoa": "1ª Plur Incl", "pol": "Negativo"},
            "ña'e": {"raiz": "e", "pessoa": "1ª Plur Incl", "pol": "Afirmativo"}, "naña'éi": {"raiz": "e", "pessoa": "1ª Plur Incl", "pol": "Negativo"},
            "ro'e": {"raiz": "e", "pessoa": "1ª Plur Excl", "pol": "Afirmativo"}, "ndoro'éi": {"raiz": "e", "pessoa": "1ª Plur Excl", "pol": "Negativo"},
            "peje": {"raiz": "e", "pessoa": "2ª Plur", "pol": "Afirmativo"}, "ndapejéi": {"raiz": "e", "pessoa": "2ª Plur", "pol": "Negativo"}
        }

        def extrair_prefixo(p):
            if p in irregulares:
                d = irregulares[p]
                return d["raiz"], d["pessoa"], "Irregular", "neg" if d["pol"] == "Negativo" else "afirm", True
                
            prefixos_possiveis = []
            for paradigma, polaridades in cls.PREFIXOS.items():
                for pol, pessoas in polaridades.items():
                    for pes_cod, formas in pessoas.items():
                        for forma in formas:
                            if forma:
                                prefixos_possiveis.append((forma, paradigma, pes_cod, pol))
                                
            prefixos_possiveis.sort(key=lambda x: len(x[0]), reverse=True)
            
            for pref, paradigma, pes_cod, pol in prefixos_possiveis:
                if p.startswith(pref):
                    raiz = p[len(pref):].strip()
                    if pol == "neg":
                        if raiz.endswith("ri"): raiz = raiz[:-2]
                        elif raiz.endswith("i"): raiz = raiz[:-1]
                    if raiz:
                        return raiz, pes_cod, paradigma, pol, True
            return p, "Infinitivo/Base", "Desconhecido", "afirm", False

        raiz_pres, pes_pres, par_pres, pol_pres, suc_pres = extrair_prefixo(palavra)
        if suc_pres and raiz_pres in raizes_conhecidas:
            return {
                "raiz": raiz_pres, "pessoa": mapa_pessoas.get(pes_pres, pes_pres),
                "paradigma": par_pres, "polaridade": "Negativo" if pol_pres == "neg" else "Afirmativo",
                "tempo": "Presente", "sucesso": True
            }

        tempo = "Presente"
        palavra_corte = palavra
        if palavra.endswith("kuri"):
            tempo = "Passado"
            palavra_corte = palavra[:-4].strip()
        elif palavra.endswith("ta"):
            tempo = "Futuro"
            palavra_corte = palavra[:-2].strip()

        raiz_tmp, pes_tmp, par_tmp, pol_tmp, suc_tmp = extrair_prefixo(palavra_corte)
        
        if suc_tmp and raiz_tmp in raizes_conhecidas:
            return {
                "raiz": raiz_tmp, "pessoa": mapa_pessoas.get(pes_tmp, pes_tmp),
                "paradigma": par_tmp, "polaridade": "Negativo" if pol_tmp == "neg" else "Afirmativo",
                "tempo": tempo, "sucesso": True
            }
            
        if suc_tmp and tempo != "Presente":
            return {
                "raiz": raiz_tmp, "pessoa": mapa_pessoas.get(pes_tmp, pes_tmp),
                "paradigma": par_tmp, "polaridade": "Negativo" if pol_tmp == "neg" else "Afirmativo",
                "tempo": tempo, "sucesso": True
            }
            
        return {
            "raiz": raiz_pres, "pessoa": mapa_pessoas.get(pes_pres, pes_pres),
            "paradigma": par_pres, "polaridade": "Negativo" if pol_pres == "neg" else "Afirmativo",
            "tempo": "Presente" if not suc_pres else "-", 
            "sucesso": suc_pres
        }

class DicionarioManager:
    def __init__(self):
        self.palavras: Dict[str, Dict[str, str]] = {}
        self.arquivo_atual = "terere_es.csv"
        self.carregar("pt" if config.GerenciadorIdiomas.idioma_ativo == "pt" else "es")

    def carregar(self, idioma: str) -> None:
        self.arquivo_atual = "terere_pt.csv" if idioma == "pt" else "terere_es.csv"
        self.palavras.clear()
        
        if not os.path.exists(self.arquivo_atual):
            return
            
        try:
            with open(self.arquivo_atual, mode="r", encoding="utf-8") as f:
                conteudo = f.read(1024)
                f.seek(0)
                if not conteudo: return
                
                try:
                    dialect = csv.Sniffer().sniff(conteudo, delimiters=[',', ';'])
                    reader = csv.reader(f, dialect)
                except csv.Error:
                    reader = csv.reader(f, delimiter=';')
                
                for linha in reader:
                    if len(linha) >= 2:
                        raiz = linha[0].strip().lower()
                        self.palavras[raiz] = {
                            "traduccion": linha[1].strip(),
                            "gn_norm": GramaticaGuarani.normalizar(raiz),
                            "tipo": linha[2].strip().capitalize() if len(linha) > 2 else "Outros",
                            "subtipo": linha[3].strip() if len(linha) > 3 else "Normal",
                            "ex_gn": linha[4].strip() if len(linha) > 4 else "",
                            "ex_pt": linha[5].strip() if len(linha) > 5 else "",
                            "harmonia": GramaticaGuarani.detectar_nasalidade(raiz)
                        }
        except Exception as e:
            print(f"Erro ao carregar o dicionário ({self.arquivo_atual}): {e}")

    def salvar_tudo(self) -> None:
        try:
            with open(self.arquivo_atual, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                linhas = [
                    [r, d["traduccion"], d["tipo"], d.get("subtipo",""), d.get("ex_gn",""), d.get("ex_pt","")] 
                    for r, d in sorted(self.palavras.items(), key=lambda item: item[0].lower())
                ]
                writer.writerows(linhas)
        except PermissionError:
            messagebox.showerror("Erro de Permissão", f"Feche o arquivo '{self.arquivo_atual}' em outros programas antes de salvar.")

    def adicionar_ou_atualizar(self, raiz: str, trad: str, tipo: str, subtipo: str, ex_gn: str, ex_pt: str) -> None:
        self.palavras[raiz] = {
            "traduccion": trad, "gn_norm": GramaticaGuarani.normalizar(raiz),
            "tipo": tipo.capitalize(), "subtipo": subtipo, "ex_gn": ex_gn, "ex_pt": ex_pt,
            "harmonia": GramaticaGuarani.detectar_nasalidade(raiz)
        }
        self.palavras = dict(sorted(self.palavras.items(), key=lambda item: item[0].lower()))
        self.salvar_tudo()

    def excluir(self, raiz: str) -> None:
        if raiz in self.palavras:
            del self.palavras[raiz]
            self.salvar_tudo()

class PerfilManager:
    def __init__(self):
        self.nome_atual: Optional[str] = None
        self.dados: Dict[str, Any] = self.estrutura_padrao()
        self.pontuacao_sessao = {"acertos": 0, "erros": 0}

    def estrutura_padrao(self) -> Dict[str, Any]:
        return {"estatisticas": {"acertos": 0, "erros": 0}, "palavras_info": {}, "dias_ativos": []}

    @staticmethod
    def listar_perfis() -> List[str]:
        return [f.replace("perfil_", "").replace(".json", "") for f in os.listdir(".") if f.startswith("perfil_") and f.endswith(".json")]

    def carregar(self, nome: Optional[str]) -> None:
        self.nome_atual = nome
        if nome and os.path.exists(f"perfil_{nome}.json"):
            try:
                with open(f"perfil_{nome}.json", "r", encoding="utf-8") as f:
                    self.dados = json.load(f)
            except json.JSONDecodeError:
                self.dados = self.estrutura_padrao()
        else:
            self.dados = self.estrutura_padrao()
            if nome: self.salvar()

    def salvar(self) -> None:
        if self.nome_atual:
            hoje = datetime.date.today().isoformat()
            if hoje not in self.dados["dias_ativos"]:
                self.dados["dias_ativos"].append(hoje)
            try:
                with open(f"perfil_{self.nome_atual}.json", "w", encoding="utf-8") as f:
                    json.dump(self.dados, f, ensure_ascii=False, indent=4)
            except PermissionError:
                pass

    def registrar_resposta_srs(self, raiz: str, acertou: bool) -> None:
        stats = self.dados["estatisticas"] if self.nome_atual else self.pontuacao_sessao
        if acertou:
            stats["acertos"] += 1
        else:
            stats["erros"] += 1

        if self.nome_atual:
            info = self.dados.setdefault("palavras_info", {}).setdefault(raiz, {"acertos": 0, "erros": 0})
            if acertou: info["acertos"] += 1
            else: info["erros"] += 1
            self.salvar()