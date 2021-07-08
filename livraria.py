from tkinter import *
import tkinter
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from tkinter.font import BOLD
from typing import ItemsView
from PIL import Image, ImageTk
import os
import ctypes
import cx_Oracle

os.chdir("C:")
os.chdir("C:\\Users\\carlo\\Downloads\\instantclient-basic-windows.x64-19.6.0.0.0dbru\\instantclient_19_6")

servidor = 'localhost/xe'

print("==============================")
print("CADASTRO DE LIVROS E AUTORES")
print("==============================\n")
print("ATENÇÃO: Para o correto funcionamento da aplicação, certifique de ter tudo instalado corretamente, conforme descrição.\n")

usuario  = str(input("Digite seu usuário do Banco de Dados: "))
senha    = str(input("Digite a senha do seu Banco de Dados: "))


janela = Tk()
janela.resizable(False,False)

try:
    conexao = cx_Oracle.connect(dsn=servidor,user=usuario,password=senha)
except cx_Oracle.DatabaseError:
    print ("Erro de conexão com o BD\n")
    print("Tente novamente :D")

janela.attributes("-topmost", 1)

lblmsg = None
txtNome = None
elementos_nome = list()
elementos_livros_tk = list()
elementos_nome_tk = list()
elementos_preco_tk = list()


def conectar():
    
    try:
        cursor  = conexao.cursor()
        Home()
    except:
        return

    try:
        cursor.execute("CREATE SEQUENCE seqAutores START WITH 1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 999 NOCACHE CYCLE")
        conexao.commit()
    except cx_Oracle.DatabaseError:
        pass # ignora, pois a sequência já existe

    try:
        cursor.execute("CREATE TABLE Autores (Id NUMBER(3) PRIMARY KEY, Nome NVARCHAR2(50) UNIQUE NOT NULL)")
        conexao.commit()
    except cx_Oracle.DatabaseError:
        pass # ignora, pois a tabela já existe

    try:
        cursor.execute("CREATE SEQUENCE seqLivros START WITH 1 INCREMENT BY 1 MAXVALUE 999 NOCACHE CYCLE")
        conexao.commit()
    except cx_Oracle.DatabaseError:
        pass # ignora, pois a tabela já existe

    try:
        cursor.execute("CREATE TABLE Livros (Codigo NUMBER(5) PRIMARY KEY, Nome NVARCHAR2(50) UNIQUE NOT NULL, Preco NUMBER(5,2) NOT NULL)")
        conexao.commit()
    except cx_Oracle.DatabaseError:
        pass # ignora, pois a tabela já existe

    try:
        cursor.execute("CREATE TABLE Autorias (Id NUMBER(3), Codigo NUMBER(5), FOREIGN KEY (Id) REFERENCES Autores(Id), FOREIGN KEY (Codigo) REFERENCES Livros(Codigo))")
        conexao.commit()
    except cx_Oracle.DatabaseError:
        pass # ignora, pois a tabela já existe

def abrirAutores():

    autores = Tk()
    autores.title("Janela Autores")
    autores.resizable(False,False)
    

    def fecharAutores():
        autores.destroy()

    def cadastreAutor ():
        
        cursor = conexao.cursor()
        nome   = txtNome.get()

        try:
            cursor.execute("INSERT INTO Autores (Id,Nome) VALUES (seqAutores.nextval,'"+nome+"')")
            conexao.commit()
            lblmsg["text"] = "Autor cadastrado com sucesso"
            painelDeMensagens.place(x= -45)
        except cx_Oracle.DatabaseError:
            lblmsg["text"] = "Autor repetido"
            painelDeMensagens.place(x= 0)

    def removaAutor():

        cursor = conexao.cursor()
        nome   = txtNome.get()

        cursor.execute("SELECT Id FROM Autores WHERE Nome='"+nome+"'")
        conexao.commit ()

        linha = cursor.fetchone()
        if not linha:
            lblmsg["text"] = "Autor inexistente"
            painelDeMensagens.place(x= -20)
        else:
            try:
                cursor.execute("DELETE FROM Autores WHERE Nome='"+nome+"'")
                conexao.commit ()
                lblmsg["text"] = "Autor removido com sucesso!"
                painelDeMensagens.place(x= -50)
            except:
                lblmsg["text"] = "Antes de excluir o autor, exclua seu livro na janela Livros!"
                painelDeMensagens.place(x= -130)


    def listeAutores ():
        name = str(tree.get_children())
        if name != "()":
            ctypes.windll.user32.MessageBoxW(0, "Antes de consultar novamente, precisa limpar a consulta!!", "Ops algo de errado aconteceu...")
        else:
            cursor=conexao.cursor()
            cursor.execute("SELECT Autores.nome FROM Autores")

            linha = cursor.fetchone()
            if not linha:
                lblmsg["text"] = "Não há autores cadastrados"
                return

            while linha:
                elementos_nome = [linha[0]]
                linha = cursor.fetchone()
                tree.insert("","end",values=(elementos_nome[0],))
            

    def limpar():
        name = str(tree.get_children())
        if name != "()":
            tree.delete(*tree.get_children())
            
            


    fonte = ("Verdana", "10", "bold")
    
    autores.geometry("400x600")
    autores["pady"] = 10
    janela.wm_title("Livraria")

    homeFrame = tkinter.LabelFrame(autores)
    homeFrame.place(relwidth=1, relheight=1)

    titulo = Label(autores, text="Informe os dados :")
    titulo["font"] = ("Calibri", "14", "bold")
    titulo.pack ()

    titulo2 = Label(autores, text="Autores", background= "white")
    titulo2["font"] = ("Calibri", "15")
    titulo2.pack ()

    
    #---

    painelDeNome = Frame(autores)
    painelDeNome["padx"] = 10
    painelDeNome["pady"] = 5
    painelDeNome.pack()

    lblnome = Label(painelDeNome, text="Nome:", font=fonte, width=10)
    lblnome.pack(ipadx= 10)

    txtNome = Entry(painelDeNome)
    txtNome["width"] = 25
    txtNome["font"] = ("Calibri", "13")
    txtNome.pack(side=LEFT)


    #---
    
    painelDeBotoes = Frame(autores)
    painelDeBotoes["padx"] = 20
    painelDeBotoes["pady"] = 10
    painelDeBotoes.pack()

    

    bntInsert = Button(painelDeBotoes, text="Inserir autor", font=fonte, width=12)
    bntInsert["command"] = cadastreAutor
    bntInsert.place(x=10, y=180, width=150, height= 150)
    bntInsert.pack()


    bntExcluir = Button(painelDeBotoes, text="Remover autor", font=fonte, width=12)
    bntExcluir["command"] = removaAutor
    bntExcluir.place(x=10, y=180, width=150, height= 150)
    bntExcluir.pack()

    bntAlterar = Button(painelDeBotoes, text="Terminar", font=fonte, width=12)
    bntAlterar["command"] = fecharAutores
    bntAlterar.pack()

    bntAlterar = Button(painelDeBotoes, text="Listar Autores", font=fonte, width=12)
    bntAlterar["command"] = listeAutores
    bntAlterar.pack()


    #---
    
    painelDeMensagens = Frame(autores)
    painelDeMensagens.place(rely= 0.45, relx= 0.40)

    

    lblmsg = Label(painelDeMensagens, text="Mensagem: ")
    lblmsg["font"] = ("Verdana", "9", "italic")
    lblmsg.pack()
    
    
    resultados = Frame(autores)
    #resultados["pady"] = 60
    resultados.place(x=100,y=300)

    tree = ttk.Treeview(resultados, column=("column1"), show="headings")

    tree.column("column1", minwidth=0, width=200,anchor="center")
    tree.heading("column1",text="Nome do autor")
    tree.pack()

    btn_clear = Frame(autores)
    btn_clear.place(x=150, y= 530)

    btn_limpar = Button(btn_clear, text="Limpar consulta", font=fonte, width=12)
    btn_limpar["command"] = limpar
    btn_limpar["font"] = ("sans-serif", "8")
    btn_limpar.pack()


    janela.destroy()

def Home():

    janela.geometry("400x400")
    janela.resizable(False,False)
    janela.wm_title("Livraria")

    homeFrame = tkinter.LabelFrame(janela, background="#c5ffff")
    homeFrame.place(relwidth=1, relheight=0.5)
    txtHome=Label(homeFrame, font=("Sans-serif",15)   ,text= "BEM VINDO A LIVRARIA DA PUC", background="#c5ffff")
    txtHome.place(relx=0.10, rely=0.5,y=-50)

    image = Image.open("C:\\Users\\carlo\\Desktop\\PROJETOS\\Python\\Cadastro_de_livros\\logo_puc.png")
    resize_image  = image.resize((200,100))
    img = ImageTk.PhotoImage(resize_image)
    label1 = Label(image=img)
    label1.image = img
    label1.place(x=100, y=90)


    optionsFrame = tkinter.LabelFrame(janela, text="Mensagem: ")
    optionsFrame.place(relwidth=1, relheight=0.5, rely=0.5)

    txtAviso = Label(optionsFrame, text= "")
    txtAviso.pack()


    btnAutores = tkinter.Button(optionsFrame, text="Autores", background="gray",command= abrirAutores)
    btnAutores.place(relwidth=0.4, relheight=0.4, relx=0.05, rely=0.30)

    btnLivros = tkinter.Button(optionsFrame, text="Livros", background="gray", command= Livros)
    btnLivros.place(relwidth=0.4, relheight=0.4, relx=0.55, rely=0.30)

    janela.mainloop()

def Livros ():
    janela2 = Tk()
    janela2.title("Janela Livros")
    janela2.geometry("600x800")
    janela2.resizable(False,False)
    #---


    def cadastreLivro ():
        cursor    = conexao.cursor()
        nomeLivro = txtNomeLivro.get()
        nomeAutor = txtNomeAutor.get()
        
        
        try:
            precoLivro = txtPreco.get()
        except ValueError:
            lblmsg["text"] = "Preço invalido"
        else:   

            cursor.execute("SELECT Id FROM Autores WHERE Nome='"+nomeAutor+"'")
            linha = cursor.fetchone()
            if not linha:
                lblmsg["text"] = "Autor inexistente"
            else:
                idAutor = linha[0]

                try:
                    cursor.execute("INSERT INTO Livros (Codigo,Nome,Preco) VALUES (seqLivros.nextval,'"+nomeLivro+"',"+str(precoLivro)+")")
                    conexao.commit ()
                except cx_Oracle.DatabaseError:
                    lblmsg["text"] = "Autor repetido"
                else:
                    cursor.execute("SELECT Codigo FROM Livros WHERE Nome='"+nomeLivro+"'")
                    linha  = cursor.fetchone()
                    CodigoLivro = linha[0]
                    
                    cursor.execute("INSERT INTO Autorias (Id,Codigo) VALUES ("+str(idAutor)+","+str(CodigoLivro)+")")
                    conexao.commit ()
                    lblmsg["text"] = "Livro cadastrado com sucesso"
    
    def removaLivro ():

        cursor = conexao.cursor()
        nomeLivro = txtNomeLivro.get()

        cursor.execute("SELECT Codigo FROM Livros WHERE Nome='"+nomeLivro+"'")
        linha = cursor.fetchone()
            
        if not linha:
            lblmsg["text"] = "Livro inexistente"
        else:
            CodigoLivro = linha[0]
            
            cursor.execute("SELECT Id FROM Autorias WHERE Codigo="+str(CodigoLivro))
            linha   = cursor.fetchone()
            idAutor = linha[0]
            
            cursor.execute("DELETE FROM Autorias WHERE Id="     + str(idAutor))
            cursor.execute("DELETE FROM Livros   WHERE Codigo=" + str(CodigoLivro))
            conexao.commit ()
            
            lblmsg["text"] = "Autor removido com sucesso"

    def listeLivros_todos ():

        cursor=conexao.cursor()
        cursor.execute("SELECT Livros.Nome, Autores.Nome, Livros.Preco FROM Livros, Autorias, Autores WHERE Livros.Codigo=Autorias.Codigo AND Autorias.Id=Autores.Id")

        linha = cursor.fetchone()
        if not linha:
            lblmsg["text"] = "Não há livros cadastrados"
            return
            
        while linha:
            #elementos_livros = (linha[0]+" "+linha[1]+" "+str(linha[2])
            elementos_livros_tk = [linha[0]]
            elementos_nome_tk = [linha[1]]
            elementos_preco_tk = [linha[2]]
            linha = cursor.fetchone()
            tree.insert("","end",values=(elementos_nome_tk[0], elementos_livros_tk[0], elementos_preco_tk[0]))

            #elementos_nome = [linha[0]]
            #linha = cursor.fetchone()
            #tree.insert("","end",values=(elementos_nome[0],))
    
    def listelivros_max ():
        maximo = str(txtprecomax.get())
        cursor=conexao.cursor()
        cursor.execute("SELECT Livros.Nome, Autores.Nome, Livros.Preco FROM Livros, Autorias, Autores WHERE Livros.Codigo=Autorias.Codigo AND Autorias.Id=Autores.Id AND Livros.Preco<"+maximo+"" )

        linha = cursor.fetchone()
        if not linha:
            lblmsg["text"] = "Não há livros abaixo deste valor!"
            return
            
        while linha:
            elementos_livros_tk = [linha[0]]
            elementos_nome_tk = [linha[1]]
            elementos_preco_tk = [linha[2]]
            linha = cursor.fetchone()
            tree.insert("","end",values=(elementos_nome_tk[0], elementos_livros_tk[0], elementos_preco_tk[0]))

    def listelivros_min ():
        minimo = str(txtprecomin.get())
        cursor=conexao.cursor()
        cursor.execute("SELECT Livros.Nome, Autores.Nome, Livros.Preco FROM Livros, Autorias, Autores WHERE Livros.Codigo=Autorias.Codigo AND Autorias.Id=Autores.Id AND Livros.Preco>"+minimo+"" )

        linha = cursor.fetchone()
        if not linha:
            lblmsg["text"] = "Não há livros acima deste valor!"
            return
            
        while linha:
            elementos_livros_tk = [linha[0]]
            elementos_nome_tk = [linha[1]]
            elementos_preco_tk = [linha[2]]
            linha = cursor.fetchone()
            tree.insert("","end",values=(elementos_nome_tk[0], elementos_livros_tk[0], elementos_preco_tk[0]))

    def listelivros_entre ():
        minimo = str(txtprecomin.get())
        maximo = str(txtprecomax.get())
        cursor=conexao.cursor()
        cursor.execute("SELECT Livros.Nome, Autores.Nome, Livros.Preco FROM Livros, Autorias, Autores WHERE Livros.Codigo=Autorias.Codigo AND Autorias.Id=Autores.Id AND Livros.Preco BETWEEN "+minimo+" AND " +maximo+"")

        linha = cursor.fetchone()
        if not linha:
            lblmsg["text"] = "Não há livros acima deste valor!"
            return
            
        while linha:
            elementos_livros_tk = [linha[0]]
            elementos_nome_tk = [linha[1]]
            elementos_preco_tk = [linha[2]]
            linha = cursor.fetchone()
            tree.insert("","end",values=(elementos_nome_tk[0], elementos_livros_tk[0], elementos_preco_tk[0]))

    def limpar():
        name = str(tree.get_children())
        if name != "()":
            tree.delete(*tree.get_children())
    
    
    def encerrar():
        janela2.destroy()


    fonte = ("Verdana", "10")
    
    #---
    
    painelDeOrientacao = Frame(janela2)
    painelDeOrientacao["pady"] = 10
    painelDeOrientacao.pack()

    titulo = Label(painelDeOrientacao, text="Informe os dados :")
    titulo["font"] = ("Calibri", "9", "bold")
    titulo.pack ()

    titulo2 = Label(painelDeOrientacao, text="Livros")
    titulo2["font"] = ("Calibri", "9")
    titulo2.pack ()

    #---
    
    painelDeBusca = Frame(janela2)
    painelDeBusca["padx"] = 20
    painelDeBusca["pady"] = 5
    painelDeBusca.pack()

    
    #---
    paineldeNomeAutor = Frame(janela2)
    paineldeNomeAutor["padx"] = 25
    paineldeNomeAutor["pady"] = 5
    paineldeNomeAutor.pack()

    lblAutor = Label(paineldeNomeAutor, text="Autor", font=fonte, width=10)
    lblAutor.pack(side=LEFT, padx=5)

    txtNomeAutor = Entry(paineldeNomeAutor)
    txtNomeAutor["width"] = 20
    txtNomeAutor["font"] = fonte
    txtNomeAutor.pack(side=LEFT)

    painelDeNome = Frame(janela2)
    painelDeNome["padx"] = 20
    painelDeNome["pady"] = 5
    painelDeNome.pack()


    lblnome = Label(painelDeNome, text="Livro:", font=fonte, width=10)
    lblnome.pack(side=LEFT)

    txtNomeLivro = Entry(painelDeNome)
    txtNomeLivro["width"] = 20
    txtNomeLivro["font"] = fonte
    txtNomeLivro.pack(side=LEFT)

      #---

    painelDePreco = Frame(janela2)
    painelDePreco["padx"] = 20
    painelDePreco["pady"] = 5
    painelDePreco.pack()

    lblPreco = Label(painelDePreco, text="Preço:", font=fonte, width=10)
    lblPreco.pack(side=LEFT)

    txtPreco = Entry(painelDePreco)
    txtPreco["width"] = 20
    txtPreco["font"] = fonte
    txtPreco.pack(side=LEFT)

    #---
    
    paineldeprecos2 = Frame(janela2)
    paineldeprecos2["padx"] = 20
    paineldeprecos2["pady"] = 5
    paineldeprecos2.pack()

    lblprecomin = Label(paineldeprecos2, text="Preço Mínimo:", font=fonte, width=15)
    lblprecomin.pack(side=LEFT)

    txtprecomin = Entry(paineldeprecos2)
    txtprecomin["width"] = 25
    txtprecomin["font"] = fonte
    txtprecomin.pack(side=LEFT)

    #---
    
    paineldeprecos = Frame(janela2)
    paineldeprecos["padx"] = 20
    paineldeprecos["pady"] = 5
    paineldeprecos.pack()

    lblprecomax= Label(paineldeprecos, text="Preço Máximo:", font=fonte, width=15)
    lblprecomax.pack(side=LEFT)

    txtprecomax = Entry(paineldeprecos)
    txtprecomax["width"] = 25
    txtprecomax["font"] = fonte
    txtprecomax.pack(side=LEFT)


    #---
    
    painelDeBotoes = Frame(janela2)
    painelDeBotoes["padx"] = 10
    painelDeBotoes["pady"] = 10
    painelDeBotoes.pack()

    bntInsert = Button(painelDeBotoes, text="Cadastrar", font=fonte, width=12)
    bntInsert["command"] = cadastreLivro
    bntInsert.pack (side=TOP)

    #---
    
    painelDeBotoes2 = Frame(janela2)
    painelDeBotoes2["padx"] = 10
    painelDeBotoes2["pady"] = 10
    painelDeBotoes2.pack()
    

    bntAlterar = Button(painelDeBotoes2, text="Remover", font=fonte, width=12)
    bntAlterar["command"] = removaLivro
    bntAlterar.pack (side=TOP)

    #---
    painelDeBotoes3 = Frame(janela2)
    painelDeBotoes3["padx"] = 10
    painelDeBotoes3["pady"] = 10
    painelDeBotoes3.pack()

    def verificar_valores ():
        name = str(tree.get_children())

        if name != "()":
            ctypes.windll.user32.MessageBoxW(0, "Antes de consultar novamente, precisa limpar a consulta!!", "Ops algo de errado aconteceu...")
        else:

            if (txtprecomin.get()) != "" and (txtprecomax.get() == ""):
                listelivros_min()
                txtprecomin.delete(0,END)
            elif (txtprecomin.get()) == "" and (txtprecomax.get()) != "" :
                listelivros_max()
                txtprecomax.delete(0,END)
            elif (txtprecomin.get()) != "" and (txtprecomax.get()) != "" :
                listelivros_entre()
                txtprecomin.delete(0,END)
                txtprecomax.delete(0,END)
            else:
                listeLivros_todos()
        

    bntExcluir = Button(painelDeBotoes3, text="Listar por valor", font=fonte, width=12)
    bntExcluir["command"] = verificar_valores
    bntExcluir.pack(side=TOP)

    painelDeBotoes4 = Frame(janela2)
    painelDeBotoes4["padx"] = 10
    painelDeBotoes4["pady"] = 10
    painelDeBotoes4.pack()


    bntExcluir = Button(painelDeBotoes4, text="Terminar", font=fonte, width=12)
    bntExcluir["command"] = encerrar
    bntExcluir.pack(side=TOP)

    #---
    
    painelDeMensagens = Frame(janela2)
    painelDeMensagens["pady"] = 15
    painelDeMensagens.pack()

    lblmsg = Label(painelDeMensagens, text="Mensagem: ")
    lblmsg["font"] = ("Verdana", "9", "italic")
    lblmsg.pack()

    resultados = Frame(janela2)
    #resultados["pady"] = 60
    resultados.place(x=30,y=500)

    tree = ttk.Treeview(resultados, column=("column1","column2","column3"), show="headings")

    tree.column("column1", minwidth=0, width=180,anchor="center")
    tree.heading("column1",text="Nome do autor")
    tree.column("column2", minwidth=0, width=180,anchor="center")
    tree.heading("column2",text="Livro")
    tree.column("column3", minwidth=0, width=180,anchor="center")
    tree.heading("column3",text="Preço")
    tree.place()
    tree.pack()

    btn_clear = Frame(janela2)
    btn_clear.place(x=480,y=450)

    btn_limpar = Button(btn_clear, text="Limpar consulta", font=fonte, width=12)
    btn_limpar["command"] = limpar
    btn_limpar["font"] = ("sans-serif", "8")
    btn_limpar.pack()


    

    #---
    janela.destroy()
    janela2.mainloop()


conectar()