import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import datetime
import mod_elbow as elbow
import mod_hands as hands
import mod_shoulder as shoulder
import mysql.connector

#NOTA: Para executar o código, é necessário instalar o pacote mysql-connector-python
#      Para instalar, execute o comando abaixo no terminal:
#      pip install mysql-connector-python --no-dependencies

registro_window = None 

acesso_mysql = {
    "host": "18.231.13.62",
    "user": "projete",
    "password": "D10m05@Daj",
    "database": "projete"
}

exames = [
    "Abdução e adução da mão",
    "Abdução e adução de ombro",
    "Flexão e extenção de cotovelo",
    "Flexão e extenção da mão",
    "Flexão e extenção de ombro"
]

# Função para conectar ao banco de dados MySQL usando as configurações predefinidas
def conecta_mysql():
    try:
        conexao = mysql.connector.connect(**acesso_mysql)
        cursor = conexao.cursor()
        return conexao, cursor

    except mysql.connector.Error as err:
        # print(f"Erro MySQL: {err}")
        messagebox.showinfo("Informação", f"Erro: {err}")
        return None, None

# Função para carregar pacientes do MySQL
def carregar_pacientes():
    try:
        conexao, cursor = conecta_mysql()

        cursor.execute("SELECT id, cpf, nome FROM pacientes")
        for item in pacientes_tree.get_children():
            pacientes_tree.delete(item)

        # Adicionar dados dos pacientes à Treeview
        for row in cursor.fetchall():
            pacientes_tree.insert("", "end", values=row)

        conexao.close()

    except mysql.connector.Error as err:
        # print(f"Erro MySQL: {err}")
        messagebox.showinfo("Informação", f"Erro: {err}")

# Função para carregar exames do paciente selecionado
def carregar_exames(event):
    selected_item = pacientes_tree.selection()

    if selected_item:
        selected_item = selected_item[0]  
        selected_data = pacientes_tree.item(selected_item, 'values')
            
        if selected_data:
            for item in exames_tree.get_children():
                exames_tree.delete(item)

            try:
                conexao, cursor = conecta_mysql()
                cursor.execute("SELECT id, data, nome_do_exame FROM exames WHERE id_paciente = %s", (selected_data[0],))

                for row in cursor.fetchall():
                    exames_tree.insert("", "end", values=row)

                conexao.close()

            except mysql.connector.Error as err:
                # print(f"Erro MySQL: {err}")
                messagebox.showinfo("Informação", f"Erro: {err}")
        else:
            pass

# Função para abrir a janela de registro de novo paciente
def abrir_janela_registro():
    global registro_window  # Declare a variável global

    registro_window = tk.Toplevel(root)
    registro_window.title("Registro de Novo Paciente")

    # Obtém as dimensões da tela e centraliza nova janela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    largura_nova_janela = 400  
    altura_nova_janela = 430   
    
    x = (largura_tela - largura_nova_janela) // 2
    # y = (altura_tela - altura_nova_janela) // 2
    y = 150
    
    registro_window.geometry(f"{largura_nova_janela}x{altura_nova_janela}+{x}+{y}")

    # Labels e campos para inserir detalhes do paciente
    cpf_label = ttk.Label(registro_window, text="CPF:")
    nome_label = ttk.Label(registro_window, text="Nome:")
    endereco_label = ttk.Label(registro_window, text="Endereço:")
    cidade_label = ttk.Label(registro_window, text="Cidade:")
    estado_label = ttk.Label(registro_window, text="UF:")
    idade_label = ttk.Label(registro_window, text="Idade:")
    altura_label = ttk.Label(registro_window, text="Altura:")
    peso_label = ttk.Label(registro_window, text="Peso:")
    problema_label = ttk.Label(registro_window, text="Problema:")

    cpf_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    nome_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    endereco_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    cidade_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    estado_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    idade_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    altura_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    peso_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
    problema_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

    cpf_entry = ttk.Entry(registro_window)
    nome_entry = ttk.Entry(registro_window)
    endereco_entry = ttk.Entry(registro_window)
    cidade_entry = ttk.Entry(registro_window)
    estado_entry = ttk.Entry(registro_window)
    idade_entry = ttk.Entry(registro_window)
    altura_entry = ttk.Entry(registro_window)
    peso_entry = ttk.Entry(registro_window)
    problema_entry = tk.Text(registro_window, height=4, width=40)

    cpf_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    nome_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    endereco_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    cidade_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    estado_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    idade_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    altura_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")
    peso_entry.grid(row=7, column=1, padx=10, pady=5, sticky="w")
    problema_entry.grid(row=8, column=1, padx=10, pady=5, sticky="w")

    # Botão para salvar o novo paciente
    salvar_button = ttk.Button(registro_window, text="Salvar", 
                               command=lambda: salvar_paciente(
                                    cpf_entry.get(),
                                    nome_entry.get(),
                                    endereco_entry.get(),
                                    cidade_entry.get(),
                                    estado_entry.get(),
                                    idade_entry.get(),
                                    altura_entry.get(),
                                    peso_entry.get(),
                                    problema_entry.get("1.0", "end")
                            ))
    salvar_button.grid(row=9, columnspan=2, padx=10, pady=10)

# Função para salvar um novo paciente no banco de dados
def salvar_paciente(cpf,nome, endereco, cidade, estado,idade, altura,peso, problema):
    global registro_window  # Declare a variável global

    if nome:
        try:
            conexao, cursor = conecta_mysql()

            sql = """
                INSERT INTO pacientes (
                    cpf, nome, endereco, cidade, uf, idade, altura, peso, problema) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

            cursor.execute(sql, (cpf, nome, endereco, cidade, estado, idade, altura, peso, problema))
            conexao.commit()
            conexao.close()

            carregar_pacientes()

            registro_window.destroy()

        except mysql.connector.Error as err:
            # print(f"Erro MySQL: {err}")
            messagebox.showinfo("Informação", f"Erro: {err}")

# Função para chamar a tela de exame
def chamar_tela_exame():
    selected_paciente = pacientes_tree.selection()
    selected_exame = combobox_exame.get()

    if selected_paciente and selected_exame:

        selected_item = pacientes_tree.selection()[0]
        selected_data = pacientes_tree.item(selected_item, 'values')

        if selected_data:

            data_exame = datetime.datetime.now().date()
            id_exame = combobox_exame.current()
            id_paciente = selected_data[0]
            nome_exame = combobox_exame.get()

            print("Identificador do exame:", id_exame)
            print(f"Exame para o paciente ID: {selected_data[0]} - Data: {data_exame}")

            '''
            ---------------
            Tipos de exames
            ---------------
            0 - Abdução e adução da mão
            1 - Abdução e adução de ombro
            2 - Flexão e extenção de cotovelo
            3 - Flexão e extenção da mão
            4 - Flexão e extenção de ombro
            '''
            
            if id_exame == 1:
                shoulder.main() # Abdução e adução de ombro
                laudo = ', '.join(map(str, shoulder.angle_records))
                e = shoulder.angle_records # Atribui lista para variavel
            elif id_exame == 2:
                elbow.main() # Flexão e extenção de cotovelo
                laudo = ', '.join(map(str, elbow.angle_records))
                e = elbow.angle_records # Atribui lista para variavel
            else:
                messagebox.showinfo("Informação", f"Exame {nome_exame} não implementado :(")
                return
            
            # Se todos os elementos da lista são iguais a zero
            # o exame não será gravado e será excibida uma mensagem para o usuário
            verifica_lista = all(elemento == 0 for elemento in e)
            if verifica_lista:
                messagebox.showinfo("Informação", "Dado(s) não registrado(s). Exame não realizado! :(")
                return
            
            # Grava resultado exame no banco de dados
            try:
                conexao, cursor = conecta_mysql()

                cursor.execute("INSERT INTO exames (data, id_paciente, nome_do_exame, resultado) VALUES (%s, %s, %s, %s)", (data_exame, id_paciente, nome_exame, laudo))
                conexao.commit()
                conexao.close()

                carregar_exames(selected_item)

            except mysql.connector.Error as err:
                messagebox.showinfo("Informação", f"Erro ao gravar os dados: {err}")
                # print(f"Erro MySQL: {err}")
    else:
        messagebox.showinfo("Informação", "Selecione um paciente e o tipo do exame.")

# Função para realizar a busca de pacientes no banco de dados
def buscar_paciente():
    texto_busca = campo_busca.get()
    
    for item in pacientes_tree.get_children():
        pacientes_tree.delete(item)
    
    try:
        conexao, cursor = conecta_mysql()

        query = "SELECT * FROM pacientes WHERE nome LIKE %s"
        cursor.execute(query, (f"%{texto_busca}%",))

        pacientes_encontrados = cursor.fetchall()

        for paciente in pacientes_encontrados:
            pacientes_tree.insert("", "end", values=paciente)

        conexao.close()

        if not pacientes_encontrados:
            messagebox.showinfo("Informação", "Nenhum paciente foi encontrado com o critério de busca.")
            
        exames_tree.delete(*exames_tree.get_children())
    
    except mysql.connector.Error as err:
        print(f"Erro MySQL: {err}")
        messagebox.showinfo("Informação", f"Erro: {err}")

# Função para apagar um exame
def apagar_exame():

    resultado = messagebox.askokcancel("Caixa de Diálogo", "Você deseja excluir o exame?")
    if resultado == False:
        return

    selected_exame = exames_tree.selection()

    if selected_exame:

        selected_item = exames_tree.selection()[0]
        selected_data = exames_tree.item(selected_item, 'values')

        if selected_data:

            id_exame = selected_data[0]
            try:
                conexao, cursor = conecta_mysql()
                cursor.execute("DELETE FROM exames WHERE id = %s", (id_exame,))
                conexao.commit()
                conexao.close()

                carregar_exames(selected_item)

            except mysql.connector.Error as err:
                messagebox.showinfo("Informação", f"Erro ao excluir os dados: {err}")
                # print(f"Erro MySQL: {err}")
    else:
        messagebox.showinfo("Informação", "Selecione um paciente e o exame que você desejada excluir.")

# Função para apagar um paciente
def apagar_paciente():

    resultado = messagebox.askokcancel("Caixa de Diálogo", "Você deseja excluir o paciente?")
    if resultado == False:
        return

    selected_paciente = pacientes_tree.selection()

    if selected_paciente:

        selected_item = pacientes_tree.selection()[0]
        selected_data = pacientes_tree.item(selected_item, 'values')

        if selected_data:

            id_paciente = selected_data[0]
            try:
                conexao, cursor = conecta_mysql()
                cursor.execute("DELETE FROM exames WHERE id_paciente = %s", (id_paciente,))
                conexao.commit()

                cursor.execute("DELETE FROM pacientes WHERE id = %s", (id_paciente,))
                conexao.commit()

                conexao.close()

                carregar_pacientes()
                # carregar_exames(selected_item)
                exames_tree.delete(*exames_tree.get_children())

            except mysql.connector.Error as err:
                messagebox.showinfo("Informação", f"Erro ao excluir os dados: {err}")
                # print(f"Erro MySQL: {err}")
    else:
        messagebox.showinfo("Informação", "Selecione um paciente e o tipo do exame.")

def criar_label_entrada(master, texto_label, valor_entry):
    frame = ttk.Frame(master)
    frame.pack(fill="both", padx=10, pady=5)

    label = ttk.Label(frame, text=texto_label, anchor="w")
    label.pack(side="left")

    entry = ttk.Entry(frame)
    entry.insert(0, valor_entry)
    entry.pack(side="left")

# Função para exibir detalhes exame em uma nova janela
def detalhes_exame():

    selected_exame = exames_tree.selection()

    if selected_exame:

        selected_item = exames_tree.selection()[0]
        selected_data = exames_tree.item(selected_item, 'values')

        selected_paciente = pacientes_tree.selection()[0]
        selected_paciente = pacientes_tree.item(selected_paciente, 'values')

        if selected_data:
            try:
                id_exame = selected_data[0]
                conexao, cursor = conecta_mysql()
                cursor.execute("SELECT * FROM exames WHERE id = %s", (id_exame,))

                resultado = cursor.fetchone()

                # Atribui resultado a uma lista
                if resultado:
                    valores = list(resultado)

                # Separa os valores da coluna resultado
                angulacao = valores[4].split(",")
                
                conexao.close()

               # Obtém as dimensões da tela e centraliza nova janela
                largura_tela = root.winfo_screenwidth()
                # altura_tela = root.winfo_screenheight()

                largura_nova_janela = 500  
                altura_nova_janela = 300   
                
                x = (largura_tela - largura_nova_janela) // 2
                y = 150
                
                detalhes_janela = tk.Toplevel(root)
                detalhes_janela.title("Detalhes do exame")
                font_mono = ("Courier New", 14, "bold")

                detalhes_janela.geometry(f"{largura_nova_janela}x{altura_nova_janela}+{x}+{y}")
                
                detalhes_label = ttk.Label(
                    detalhes_janela, 
                    text=f"Identificador: {valores[0]}\n"
                        f"Data: {valores[1]}\n"
                        f"\n"
                        f"Paciente: {selected_paciente[2]}\n"
                        f"Nome do exame: {valores[3]}\n"
                        f"\n"
                        f"---- Resultado ----\n"
                        f"\n"
                        f"Ângulo inicial (DIR): {angulacao[0]}\n"
                        f"Ângulo final   (DIR): {angulacao[1].strip()}\n"
                        f"Ângulo inicial (ESQ): {angulacao[2].strip()}\n"
                        f"Ângulo final   (ESQ): {angulacao[3].strip()}\n",
                        font=font_mono
                )
                detalhes_label.pack(padx=20, pady=20)
                botao_fechar = tk.Button(detalhes_janela, text="Fechar", command=detalhes_janela.destroy)
                botao_fechar.pack()

            except mysql.connector.Error as err:
                # print(f"Erro MySQL: {err}")
                messagebox.showinfo("Informação", f"Erro: {err}")
            
    else:
        messagebox.showinfo("Informação", "Selecione um paciente e o exame que você desejada obter os detalhes.")

def detalhes_paciente():
    messagebox.showinfo("Informação", "Função não implementada :(")
    return

# Criar a janela principal
root = tk.Tk()
root.title("RehabMyPacient 1.0 (beta)")

# clam
# alt
# default
# classic
# vista
# xpnative
# winnative

# style=ttk.Style()
# style.theme_use("default")

# Obtém as dimensões da tela para centralizar janela - root
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

largura_root = 1024  
altura_root = 600  

x = (largura_tela - largura_root) // 2
# y = (altura_tela - altura_root) // 2
y = 50

root.geometry(f"{largura_root}x{altura_root}+{x}+{y}")

# Evita redimensionamento da janela principal
root.resizable(False, False)

# FRAME BUSCA E NOVO PACIENTE
frame_busca = ttk.Frame(root)
frame_busca.grid(row=0, column=0, padx=10, pady=10, sticky="w")
rotulo_busca = ttk.Label(frame_busca, text="Paciente:")
rotulo_busca.grid(row=0, column=0, padx=(0, 5), sticky="w")
campo_busca = ttk.Entry(frame_busca, width=30)
campo_busca.grid(row=0, column=1, padx=(0, 5))
buscar_button = ttk.Button(frame_busca, text="Buscar", command=buscar_paciente)
buscar_button.grid(row=0, column=2, padx=(0, 5))
cadastrar_paciente_button = ttk.Button(frame_busca, text="+ Novo paciente", command=abrir_janela_registro)
cadastrar_paciente_button.grid(row=0, column=3, padx=5, pady=10)
chamar_paciente_button = ttk.Button(frame_busca, text="Detalhes paciente", command=detalhes_paciente)
chamar_paciente_button.grid(row=0, column=4, padx=5, pady=10)
apagar_paciente_button = ttk.Button(frame_busca, text="- Excluir paciente", command=apagar_paciente)
apagar_paciente_button.grid(row=0, column=5, padx=50, pady=0)

# PACIENTES
pacientes_tree = ttk.Treeview(root, columns=("ID", "CPF", "Nome"), show="headings", selectmode ='browse')
pacientes_tree.heading("ID", text="ID")
pacientes_tree.heading("CPF", text="CPF")
pacientes_tree.heading("Nome", text="Nome")
pacientes_tree.column("ID", width=50)
pacientes_tree.column("CPF", width=150, anchor="w")
pacientes_tree.column("Nome", width=550, anchor="w")
pacientes_tree.grid(row=1, column=0, padx=0, pady=10, sticky="nsew")
pacientes_scrollbar = ttk.Scrollbar(root, orient="vertical", command=pacientes_tree.yview)
pacientes_scrollbar = ttk.Scrollbar(root, orient="vertical", command=pacientes_tree.yview)
pacientes_scrollbar.grid(row=1, column=1, padx=0, pady=10, sticky="nsew")
pacientes_tree.configure(yscrollcommand=pacientes_scrollbar.set)

carregar_pacientes()

# EXAMES
exames_tree = ttk.Treeview(root, columns=("Id","Data","Exame"), show="headings")
exames_tree.heading("Id", text="ID")
exames_tree.heading("Data", text="Data")
exames_tree.heading("Exame", text="Exame")
exames_tree.column("Id", width=50)
exames_tree.column("Data", width=100)
exames_tree.column("Exame", width=600)
exames_tree.grid(row=2, column=0, padx=0, pady=10, sticky="nsew")
exames_scrollbar = ttk.Scrollbar(root, orient="vertical", command=exames_tree.yview)
exames_scrollbar.grid(row=2, column=1, padx=0, pady=10,sticky="ns")
exames_tree.configure(yscrollcommand=exames_scrollbar.set)

pacientes_tree.bind("<<TreeviewSelect>>", carregar_exames)

# FRAME EXAMES
frame_exame = ttk.Frame(root)
frame_exame.grid(row=3, column=0, padx=10, pady=10, sticky="w")
rotulo_exame = ttk.Label(frame_exame, text="Tipo exame:")
rotulo_exame.grid(row=3, column=0, padx=(0, 5), sticky="w")
combobox_exame = ttk.Combobox(frame_exame, values=exames, width=20)
combobox_exame.grid(row=3, column=1, padx=(0, 5), sticky="w")
chamar_exame_button = ttk.Button(frame_exame, text="+ Iniciar exame", command=chamar_tela_exame)
chamar_exame_button.grid(row=3, column=2, padx=5, pady=10)
chamar_exame_button = ttk.Button(frame_exame, text="Detalhes exame", command=detalhes_exame)
chamar_exame_button.grid(row=3, column=3, padx=5, pady=10)
apagar_exame_button = ttk.Button(frame_exame, text="- Excluir exame", command=apagar_exame)
apagar_exame_button.grid(row=3, column=4, padx=250, pady=10)

# Configurar o redimensionamento das linhas e colunas usando o grid
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Iniciar o loop principal
root.mainloop()
