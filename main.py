from customtkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

import subprocess
import platform

from view import atualizar_comando, deletar_comando, inserir_comando, montar_grid

app = CTk()
app.title("PSRunner")
app.geometry("800x510")
app.resizable(False, False)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=2)

app.iconbitmap('./assets/icon.ico')

tema_layout = "dark"
set_appearance_mode(tema_layout)

modo_edicao = False
id_comando_edicao = None

### FUNÇÕES ###
def adicionar_comando():
    global modo_edicao, id_comando_edicao
    
    nome = nome_comando_input.get()
    descricao = descricao_comando_input.get("1.0", END)
    codigo = comando_input.get("1.0", END)

    lista_comandos = [nome, descricao, codigo]

    for i in lista_comandos:
        if i == "":
            messagebox.showerror("Erro", "Preencha todos os campos")
            return

    if modo_edicao:
        lista_comandos.append(id_comando_edicao)
        atualizar_comando(lista_comandos)
        messagebox.showinfo("Sucesso", "Comando atualizado com sucesso")
        modo_edicao = False
        id_comando_edicao = None
        button_cadastrar.configure(text="Cadastrar")
    else:
        inserir_comando(lista_comandos)
        messagebox.showinfo("Sucesso", "Comando cadastrado com sucesso")
    
    nome_comando_input.delete(0, END)
    descricao_comando_input.delete("1.0", END)
    comando_input.delete("1.0", END)

    carregar_comandos()



# Frame do header
frame_header = CTkFrame(app)
frame_header.grid(row=0, column=0, columnspan=2, sticky='ew')

# Logo
logo = Image.open("./assets/logo.png")
logo = logo.resize((130, 17))
ctk_logo = CTkImage(light_image=logo, dark_image=logo, size=(130, 17))
logo_label = CTkLabel(frame_header, text="", image=ctk_logo)
logo_label.pack(side='left', pady=20, padx=320)

# Frame do header
frame_switch = CTkFrame(app, corner_radius=0)
frame_switch.grid(row=0, column=1, columnspan=2, sticky='ne')

# Switch de dark mode
def alternar_modo():
    global tema_layout
    if tema_layout == "dark":
        set_appearance_mode("light")
        tema_layout = "light"
    else:
        set_appearance_mode("dark")
        tema_layout = "dark"

switch_dark = CTkSwitch(frame_switch, text="Dark Mode", command=alternar_modo)
switch_dark.select()
switch_dark.pack(side='right', pady=5, padx=10)

# Grid de dados
def carregar_comandos():
    tabela_head = ['Comando', 'Descrição', 'ID', 'Código']
    lista_itens = montar_grid()

    global grid

    grid_frame = CTkFrame(app)
    grid_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
    
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    style = ttk.Style()
    style.configure("Treeview", rowheight=20)

    grid = ttk.Treeview(grid_frame, selectmode="extended", columns=tabela_head, show="headings", style="Treeview")

    # Vertical scrollbar
    vsb = CTkScrollbar(grid_frame, orientation="vertical", command=grid.yview)

    grid.configure(yscrollcommand=vsb.set)
    grid.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')

    grid_frame.grid_columnconfigure(0, weight=1)
    grid_frame.grid_rowconfigure(0, weight=1)

    # Configuração das colunas
    grid.heading('Comando', text='Comando', anchor=CENTER)
    grid.heading('Descrição', text='Descrição', anchor=CENTER)
    grid.column('Comando', width=75, anchor="w")
    grid.column('Descrição', width=275, anchor="w")

    # Ocultando as colunas ID e Código
    grid.column('ID', width=0, stretch=NO)
    grid.column('Código', width=0, stretch=NO)
    grid.heading('ID', text='')
    grid.heading('Código', text='')

    # Ordenando os itens alfabeticamente pela coluna "Comando"
    lista_itens = sorted(lista_itens, key=lambda x: x[1].lower())

    for item in lista_itens:
        grid.insert('', 'end', values=[item[1], item[2], item[0], item[3]])

    grid["displaycolumns"] = ("Comando", "Descrição")

carregar_comandos()

# Frame para os botões Editar e Excluir
frame_botoes = CTkFrame(master=app, fg_color="transparent")
frame_botoes.grid(row=2, column=0, pady=10)

# Executar o comando selecionado
def executar_comando():
    try:
        treev_dados = grid.focus()
        treev_dicionario = grid.item(treev_dados)
        treev_lista = treev_dicionario['values']
        codigo_comando = treev_lista[3]
        nome_comando = treev_lista[0]

        # Detecta o sistema operacional e atribui o caminho correto
        if platform.system() == "Windows":
            os_path = "C:/el/projetos/"
        else:
            os_path = "/opt/el/projetos/"

        # Substitui a variável $osPath no comando pelo caminho correspondente
        codigo_comando = codigo_comando.replace("$osPath", os_path)

        # Executa o comando PowerShell
        subprocess.run(["powershell", "-Command", codigo_comando])
        print(f"Comando '{nome_comando}' executado com sucesso")
    except IndexError:
        messagebox.showerror("Erro", "Selecione um comando para executar")
    except Exception as e:
        print(f"Ocorreu um erro ao executar o comando: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro ao executar o comando: {e}")

button_executar = CTkButton(frame_botoes, text="Executar", command=executar_comando)
button_executar.pack(side="left", padx=10)

def editar_comando():
    global modo_edicao, id_comando_edicao

    try:
        treev_dados = grid.focus()
        treev_dicionario = grid.item(treev_dados)
        treev_lista = treev_dicionario['values']
        
        id_comando_edicao = treev_lista[2]
        nome_comando = treev_lista[0]
        descricao_comando = treev_lista[1]
        codigo_comando = treev_lista[3]

        nome_comando_input.delete(0, END)
        nome_comando_input.insert(0, nome_comando)
        
        descricao_comando_input.delete("1.0", END)
        descricao_comando_input.insert("1.0", descricao_comando)

        comando_input.delete("1.0", END)
        comando_input.insert("1.0", codigo_comando)

        modo_edicao = True
        button_cadastrar.configure(text="Atualizar")
    except IndexError:
        messagebox.showerror("Erro", "Selecione um comando para editar")
    except Exception as e:
        print(f"Ocorreu um erro ao editar o comando: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro ao editar o comando: {e}")


button_editar = CTkButton(master=frame_botoes, text="Editar", command=editar_comando)
button_editar.pack(side="left", padx=10)

    
def excluir_comando():
    try:
        treev_dados = grid.focus()
        treev_dicionario = grid.item(treev_dados)
        treev_lista = treev_dicionario['values']
        id_comando = treev_lista[2]

        deletar_comando([id_comando])
        messagebox.showinfo("Sucesso", "O comando foi apagado com sucesso")
        carregar_comandos() 
    except IndexError:
        messagebox.showerror("Erro", "Selecione um comando para excluir")
    except Exception as e:
        print(f"Ocorreu um erro ao excluir o comando: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro ao excluir o comando: {e}")

button_excluir = CTkButton(master=frame_botoes, text="Excluir", command=excluir_comando, fg_color="darkgray", hover_color="gray")
button_excluir.pack(side="left", padx=10)

# Tabs
frame_cadastro = CTkFrame(app)
frame_cadastro.grid(row=1, column=1, padx=10, pady=10, rowspan=2)

# Input do nome do comando
label_comando = CTkLabel(frame_cadastro, text="Comando:")
label_comando.pack()
nome_comando_input = CTkEntry(frame_cadastro, width=300)
nome_comando_input.pack(pady=5, padx=10)

# Input da descrição do comando
label_descricao = CTkLabel(frame_cadastro, text="Descrição:")
label_descricao.pack()
descricao_comando_input = CTkTextbox(frame_cadastro, width=300, height=65, border_width=2, scrollbar_button_color="black")
descricao_comando_input.pack(pady=5, padx=10)

# Input do código do comando
label_comando = CTkLabel(frame_cadastro, text="Código:")
label_comando.pack()
comando_input = CTkTextbox(frame_cadastro, width=300, height=160, border_width=2)
comando_input.pack(pady=5, padx=10)

# Botão para cadastrar o comando
button_cadastrar = CTkButton(frame_cadastro, text="Cadastrar", command=adicionar_comando)
button_cadastrar.pack(pady=10)

app.mainloop()