import os
import csv
import shutil

def preparar_arquivos_dicionario(arquivo_es="terere_es.csv", arquivo_pt="terere_pt.csv"):
    if os.path.exists("terere_mais_completo.csv") and not os.path.exists(arquivo_es):
        shutil.copy("terere_mais_completo.csv", arquivo_es)
    elif os.path.exists("terere.csv") and not os.path.exists(arquivo_es):
        shutil.copy("terere.csv", arquivo_es)
        
    if not os.path.exists(arquivo_es):
        return False

    if not os.path.exists(arquivo_pt):
        try:
            verbetes = []
            with open(arquivo_es, "r", encoding="utf-8") as f_in:
                leitor = csv.reader(f_in, delimiter=";")
                for linha in leitor:
                    if len(linha) >= 4:
                        verbetes.append(linha)

            with open(arquivo_pt, "w", encoding="utf-8", newline="") as f_out:
                escritor = csv.writer(f_out, delimiter=";")
                for linha in verbetes:
                    guarani = linha[0]
                    classe_gramatical = linha[2]
                    tipo = linha[3]
                    escritor.writerow([guarani, "", classe_gramatical, tipo, "", ""])
            print(f"✓ Template Guarani-Português criado: '{arquivo_pt}'")
        except Exception as e:
            print(f"Erro ao processar os dados para português: {e}")
            return False
    return True