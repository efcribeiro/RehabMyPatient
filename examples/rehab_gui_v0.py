import tkinter as tk
from tkinter import ttk
import subprocess

# Lista de opções para a ComboBox
opcoes = ["Jéssica Prado", "Fred Ribeiro", "Daisy Terra", "Ana Júlia Reis", "Luiz Fernando Martins"]

def executar_script():
    try:
        # Execute o script main.py
        resultado = subprocess.run(["python3", "mod_arm.py"], capture_output=True, text=True)

        # Exiba a saída na janela
        resultado_text.config(state="normal")
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, resultado.stdout)
        resultado_text.config(state="disabled")
        

    except Exception as e:
        resultado_text.config(state="normal")
        resultado_text.delete(0, tk.END)
        resultado_text.insert(tk.END, f"Erro ao executar o script: {str(e)}")
        resultado_text.config(state="disabled")

# Crie a janela principal
janela = tk.Tk()
janela.title("RehabMyPacient 1.0")
janela.geometry("400x300")

# Campo de entrada para nome
# nome_label = tk.Label(janela, text="Nome:")
# nome_label.pack(anchor="w", padx=10)
# nome_entry = tk.Entry(janela, width=100)
# nome_entry.pack(anchor="w", padx=10)

nome_lbl = tk.Label(janela, text="Nome:")
nome_lbl.pack(anchor="w", padx=10)
nome_cb = ttk.Combobox(janela, values=opcoes, width=100)
nome_cb.pack(anchor="w", padx=10)

# Botão para executar o script
executar_btn = tk.Button(janela, text="Modulo ARM", command=executar_script)
executar_btn.pack()

# Texto de saída
resultado_text = tk.Text(janela, height=10, width=40)
resultado_text.pack()
resultado_text.config(state="disabled")

# Inicie a interface gráfica
janela.mainloop()

"""
import tkinter as tk
from tkinter import ttk  # Importe ttk para usar a Combobox

# Lista de opções para a ComboBox
opcoes = ["Opção 1", "Opção 2", "Opção 3", "Opção 4", "Opção 5"]

# Função para lidar com a seleção da ComboBox
def selecionar_opcao(event):
    opcao_selecionada = combobox.get()
    label_resultado.config(text="Opção selecionada: " + opcao_selecionada)

# Crie a janela principal
janela = tk.Tk()
janela.title("ComboBox com Lista de Opções")

# Crie a ComboBox e configure as opções
combobox = ttk.Combobox(janela, values=opcoes)
combobox.pack()

# Botão para obter a opção selecionada
botao_selecionar = tk.Button(janela, text="Selecionar", command=selecionar_opcao)
botao_selecionar.pack()

# Rótulo para exibir a opção selecionada
label_resultado = tk.Label(janela, text="")
label_resultado.pack()

# Inicie a interface gráfica
janela.mainloop()
"""
