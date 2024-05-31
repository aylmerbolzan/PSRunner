from customtkinter import *
from tkinter import ttk
from tkinter import messagebox

from view import inserir_comando, ver_comandos

app = CTk()
app.title("pyRunner")
app.geometry("800x470")
app.resizable(False, False)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=2)

tema_layout = "dark"
set_appearance_mode(tema_layout)


### FUNÇÕES ###
def adicionar_comando(): # Acesse a variável global
    nome = nome_comando_input.get()
    descricao = descricao_comando_input.get("1.0", END)
    codigo = comando_input.get("1.0", END)

    lista_comandos = [nome, descricao, codigo]

    for i in lista_comandos:
        if i == "":
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
        
    inserir_comando(lista_comandos)
    messagebox.showinfo("Sucesso", "Comando cadastrado com sucesso")

    nome_comando_input.delete(0, END)
    descricao_comando_input.delete("1.0", END)
    comando_input.delete("1.0", END)

    # Recarregue os comandos disponíveis
    comandos_lista = ver_comandos()
    comandos = [str(item[1]) for item in comandos_lista]


# Frame do header
frame_header = CTkFrame(app)
frame_header.grid(row=0, columnspan=2, sticky='ew')

# Switch de dark mode
def alternar_modo():
    global tema_layout
    if tema_layout == "dark":
        set_appearance_mode("light")
        tema_layout = "light"
    else:
        set_appearance_mode("dark")
        tema_layout = "dark"

switch_dark = CTkSwitch(frame_header, text="Dark Mode", command=alternar_modo)
switch_dark.select()
switch_dark.pack(side='right', pady=5, padx=10)

# Grid de dados
def carregar_comandos():
    tabela_head = ['Comando', 'Descrição']
    lista_itens = [
        ["Comando A", "Faz isso, aquilo e aquilo outro"],
        ["Comando B", "Faz isso, aquilo e aquilo outro"],
        ["Comando C", "Faz isso, aquilo e aquilo outro"],
        ["Comando D", "Faz isso, aquilo e aquilo outro"],
        ["Comando E", "Faz isso, aquilo e aquilo outro"],
        ["Comando F", "Faz isso, aquilo e aquilo outro"],
        ["Comando G", "Faz isso, aquilo e aquilo outro"],
        ["Comando H", "Faz isso, aquilo e aquilo outro"],
        ["Comando I", "Faz isso, aquilo e aquilo outro"]
    ]

    global tree

    tree_frame = CTkFrame(app)
    tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
    

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    style = ttk.Style()
    style.configure("Treeview", rowheight=20)

    tree = ttk.Treeview(tree_frame, selectmode="extended", columns=tabela_head, show="headings", style="Treeview")

    # Vertical scrollbar
    vsb = CTkScrollbar(tree_frame, orientation="vertical", command=tree.yview)

    tree.configure(yscrollcommand=vsb.set)
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')

    tree_frame.grid_columnconfigure(0, weight=1)
    tree_frame.grid_rowconfigure(0, weight=1)

    hd = ["center", "w"]
    h = [75, 275]
    n = 0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n], anchor=hd[n])
        n += 1

    for item in lista_itens:
        tree.insert('', 'end', values=item)

carregar_comandos()

# Frame para os botões Editar e Excluir
frame_botoes = CTkFrame(master=app, fg_color="transparent")
frame_botoes.grid(row=2, column=0, pady=10)

# Executar o comando selecionado
def executar_comando():
    codigo_comando = comando_input.get("1.0", END)
    try:
        exec(codigo_comando)
        print("Comando executado com sucesso")
    except Exception as e:
        print(f"Ocorreu um erro ao executar o comando: {e}")

# Botão para executar o comando
button_executar = CTkButton(frame_botoes, text="Executar", command=executar_comando)
button_executar.pack(side="left", padx=10)

def editar_comando():
    print("Editar comando")

button_editar = CTkButton(master=frame_botoes, text="Editar", command=editar_comando)
button_editar.pack(side="left", padx=10)
    
def excluir_comando():
    print("Excluir comando")

button_excluir = CTkButton(master=frame_botoes, text="Excluir", command=excluir_comando)
button_excluir.pack(side="left", padx=10)

# Tabs
frame_cadastro = CTkFrame(app)
frame_cadastro.grid(row=1, column=1, padx=10, pady=10, rowspan=2)

### EXECUTAR ###

# Dropdown para escolher o comando
comandos_lista = ver_comandos()
comandos = [str(item[1]) for item in comandos_lista]

descricao_lista = ver_comandos()
descricao = [str(item[2]) for item in descricao_lista]


### CADASTRAR ###

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
def cadastrar_comando():
    print("Cadastrar comando")

button_cadastrar = CTkButton(frame_cadastro, text="Cadastrar", command=adicionar_comando)
button_cadastrar.pack(pady=10)

app.mainloop()