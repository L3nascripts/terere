import tkinter as tk
from typing import Optional

from utilitarios import preparar_arquivos_dicionario
from interface import TelaLogin, TerereApp

def iniciar_sistema():
    preparar_arquivos_dicionario()
    
    root = tk.Tk()
    root.title("Terere - Estudo de Guarani 🇵🇾 🇧🇴 🧉")
    root.minsize(950, 680)
    
    try:
        icone = tk.PhotoImage(file="terere.png")
        root.iconphoto(True, icone)
    except Exception:
        pass

    def abrir_app_principal(nome_perfil: Optional[str]):
        TerereApp(root, nome_perfil, voltar_login)
        
    def voltar_login():
        TelaLogin(root, abrir_app_principal)

    TelaLogin(root, abrir_app_principal)
    root.mainloop()

if __name__ == "__main__":
    iniciar_sistema()