import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from translatepy import Translator  # Biblioteca alternativa ao googletrans

# Função principal para traduzir os arquivos de texto na pasta escolhida
def traduzir_arquivos():
    pasta = pasta_var.get()
    idioma_destino = "Portuguese"
    if not pasta:
        messagebox.showerror("Erro", "Selecione uma pasta!")
        return

    arquivos = [f for f in os.listdir(pasta) if f.endswith(".txt")]
    if not arquivos:
        messagebox.showinfo("Informação", "Nenhum arquivo .txt encontrado na pasta.")
        return

    total_arquivos = len(arquivos)
    progresso["value"] = 0
    janela.update_idletasks()

    tradutor = Translator()

    for i, arquivo in enumerate(arquivos, start=1):
        caminho_arquivo = os.path.join(pasta, arquivo)
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read()

            # Traduzindo o conteúdo para português
            traducao = tradutor.translate(conteudo, idioma_destino)

            # Salvando o arquivo traduzido
            novo_nome = os.path.splitext(arquivo)[0] + "_traduzido.txt"
            caminho_novo_arquivo = os.path.join(pasta, novo_nome)
            with open(caminho_novo_arquivo, "w", encoding="utf-8") as f:
                f.write(traducao.result)

        except Exception as e:
            messagebox.showwarning("Aviso", f"Erro ao traduzir {arquivo}: {e}")

        # Atualizando a barra de progresso
        progresso["value"] = (i / total_arquivos) * 100
        janela.update_idletasks()

    messagebox.showinfo("Concluído", "Tradução concluída!")

# Função para escolher a pasta
def escolher_pasta():
    pasta = filedialog.askdirectory(title="Escolha uma pasta")
    if pasta:
        pasta_var.set(pasta)

# Criando a janela principal
janela = tk.Tk()
janela.title("Tradutor de Textos")
janela.geometry("500x300")
janela.resizable(False, False)

# Variável para armazenar o caminho da pasta
pasta_var = tk.StringVar()

# Interface da aplicação
tk.Label(janela, text="Tradutor de Textos", font=("Arial", 16)).pack(pady=10)
tk.Label(janela, text="Escolha uma pasta com arquivos .txt para traduzir:").pack(pady=5)

# Entrada e botão para escolher pasta
frame_pasta = tk.Frame(janela)
frame_pasta.pack(pady=5)
entrada_pasta = tk.Entry(frame_pasta, textvariable=pasta_var, width=40, state="readonly")
entrada_pasta.pack(side="left", padx=5)
botao_escolher = tk.Button(frame_pasta, text="Escolher Pasta", command=escolher_pasta)
botao_escolher.pack(side="left", padx=5)

# Barra de progresso
progresso = Progressbar(janela, orient="horizontal", length=400, mode="determinate")
progresso.pack(pady=20)

# Botão para iniciar a tradução
botao_traduzir = tk.Button(janela, text="Traduzir", command=traduzir_arquivos)
botao_traduzir.pack(pady=10)

# Botão para sair
botao_sair = tk.Button(janela, text="Sair", command=janela.destroy)
botao_sair.pack(pady=5)

# Rodar a aplicação
janela.mainloop()
