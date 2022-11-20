from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import telaInicial
import banco

#Variaveis auxiliares
nEspaco = 60

#exibe a lista de todos os Clientes
def listarClientes():
    def popular():
        tv.delete(*tv.get_children())
        vquery = 'select * from clientes order by 1'
        linhas = banco.dql(vquery)
        for i in linhas:
            tv.insert("", "end", values=i)

    def cadastrpCliente():
        valores = []
        app.destroy()
        cadastroClientes("I",valores )#incluir

    def deletar():

        vid = -1
        itemSelecionado = tv.selection()[0]
        valores = tv.item(itemSelecionado, "values")
        vid = valores[0]

        vquery = 'select count(*) as tot from vendas where cd_cliente = ' + str(vid)
        dados = str(banco.dql(vquery)).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',','')
        if int(dados) > 0:
            texto = "O cliente não pode ser deletado, pois esta vinculado a uma venda"
            messagebox.showinfo(title="Erro", message=texto)
        else:
            try:

                vquery = 'delete from clientes where cd_cliente = ' + str(vid)
                linhas = banco.dql(vquery)
                tv.delete(itemSelecionado)
            except:
                messagebox.showinfo(title="Erro", message="Selecione um registro a deletar")

    def alterar():
        try:
            vid = -1
            itemSelecionado = tv.selection()[0]
            valores = tv.item(itemSelecionado, "values")
            vid = valores[0]
            app.destroy()
            cadastroClientes("A",valores)#Alterar
        except:
            messagebox.showinfo(title="Erro", message="Selecione um registro a Alterar")

    def voltar():
        app.destroy()
        telaInicial.telaInicio()

    app = Tk()
    app.title("Listar Clientes")
    app.state("zoomed")
    app.configure(background='white')

    # variaveis de ajuste de tela
    altMonitor = app.winfo_screenheight()
    largMonitor = app.winfo_screenwidth()
    altIni = (altMonitor - (altMonitor * 0.99))
    larIni = int((largMonitor - (largMonitor * 0.99)))

    largMonitor = app.winfo_screenwidth()
    largGrid    = int(largMonitor/5)-larIni

    tv = ttk.Treeview(app,height=40 ,columns=('cd_cliente', 'nm_cliente', 'tel_cliente', 'cpf_cliente', 'end_cliente'),show='headings')

    tv.column('cd_cliente', minwidth=0, width=largGrid)
    tv.heading('#1', text='Codigo')

    tv.column('nm_cliente', minwidth=0, width=largGrid)
    tv.heading('#2', text='Nome')

    tv.column('tel_cliente', minwidth=0, width=largGrid)
    tv.heading('#3', text='Telefone')

    tv.column('cpf_cliente', minwidth=0, width=largGrid)
    tv.heading('#4', text='Cpf/Cgc')

    tv.column('end_cliente', minwidth=0, width=largGrid)
    tv.heading('#5', text='Endereco')

    btnInserir=Button(app,text="Inserir", command=cadastrpCliente)
    btnAlterar = Button(app, text="Alterar", command=alterar)
    btnDeletar = Button(app, text="Deletar", command=deletar)
    btVoltar = Button(app, text="Voltar", command=voltar)


    btnInserir.place(x=larIni,y=altIni)
    btnAlterar.place(x=larIni*6, y=altIni)
    btnDeletar.place(x=larIni*12,y=altIni)
    btVoltar.place(x=larIni*18,y=altIni)

    altIni += 30
    tv.place(x=10,y=altIni)

    popular()
    app.mainloop()


import sqlite3


##############################################
## Tela de cadastro de clientes             ##
##############################################
def cadastroClientes(tipo,valores):

    def getTelaIniClientes():

        janela3.destroy()
        listarClientes()  #retorna a tela anterior

    def getCodCli():

        vquery = " select"
        vquery += "      case "
        vquery += "          when "
        vquery += "              max(cd_cliente) is null then 1 "
        vquery += "          else "
        vquery += "              max(cd_cliente) + 1  "
        vquery += "      end as cod "
        vquery += " from clientes "
        linhas = banco.dql(vquery)
        return(linhas)

    def gravaCliente():

        cd_cliente = getCp1.get()
        nm_cliente = getCp2.get()
        telCliente = getCp3.get().replace(" ","").replace(".","").replace("(","").replace(")","").replace("-","")
        cpfCliente = getCp4.get().replace(" ","").replace(",","").replace(".","").replace("-","").replace("_","")
        endCliente = getCp5.get()

        sqliteConect = sqlite3.connect('banco/pdv2.db')
        cursor = sqliteConect.cursor()

        if nm_cliente == '':
            texto = "O nome do cliente deve ser preenchido"
            messagebox.showwarning(title='Alerta', message=texto)
        elif telCliente == '':
            texto = "O telefone do cliente deve ser preenchido"
            messagebox.showwarning(title='Alerta', message=texto)
        elif cpfCliente == '':
            texto = "O CPF do cliente deve ser preenchido"
            messagebox.showwarning(title='Alerta', message=texto)
        else:
            if tipo == 'I':

                scriptGrava = " insert into clientes "
                scriptGrava += "    (nm_cliente,"
                scriptGrava += "    tel_cliente,"
                scriptGrava += "    cpf_cliente,"
                scriptGrava += "    end_cliente)"
                scriptGrava += " values ("
                scriptGrava += "'" + nm_cliente + "',"
                scriptGrava += telCliente + ","
                scriptGrava += cpfCliente + ","
                scriptGrava += "'" + endCliente + "')"
                messagebox.showinfo(title="Incluido", message="Registro gravado com sucesso")

            elif tipo == 'A':
                scriptGrava = "update "
                scriptGrava += " clientes "
                scriptGrava += " set "
                scriptGrava += "    nm_cliente  = '" + nm_cliente + "',"
                scriptGrava += "    tel_cliente = "  + telCliente + ","
                scriptGrava += "    cpf_cliente = " + cpfCliente + ","
                scriptGrava += "    end_cliente = '" + endCliente + "'"
                scriptGrava += "where"
                scriptGrava += "    cd_cliente = '" + cd_cliente  + "'"
                messagebox.showinfo(title="Alterado", message="Registro alterado com sucesso")

        count = cursor.execute(scriptGrava)
        sqliteConect.commit()
        cursor.close()
        getTelaIniClientes()



    janela3 = Tk()
    janela3.state("zoomed")

    if tipo == 'I':
        janela3.title("Cadastrar de clientes")
    elif tipo == 'A':
        janela3.title("Alterar clientes")

    janela3.configure(background='white')

    # variaveis de ajuste de tela
    altMonitor = janela3.winfo_screenheight()
    largMonitor = janela3.winfo_screenwidth()
    larIni = 10
    altMenu = (altMonitor - (altMonitor * 0.99))
    largMenu = (largMonitor - (largMonitor * 0.2))

    # Menus Cadastro

    if tipo == 'I':
        textUsu = Label(janela3, text="Cadastro de Clientes - Incluir", font="Arial 20 bold", bg="#FFFFFF")
    elif tipo == 'A':
        textUsu = Label(janela3, text="Cadastro de Clientes - Alterar", font="Arial 20 bold", bg="#FFFFFF")

    textUsu.place(x=larIni, y=altMenu)

    if tipo == 'I':
        btCadastro = Button(janela3, text="Cadastrar", font="Arial 14 bold", bg="#FFFFFF", command=gravaCliente)
    elif tipo == 'A':
        btCadastro = Button(janela3, text="Salvar Alteracao", font="Arial 14 bold", bg="#FFFFFF", command=gravaCliente)
    btCadastro.place(x=largMenu, y=altMenu)

    menu = Button(janela3, text="Voltar", font="Arial 14 bold", bg="#FFFFFF", command=getTelaIniClientes)
    menu.place(x=largMenu + 180, y=altMenu)


    altMenu += nEspaco

    #Campo de codigo
    textCp1 = Label(janela3, text="Cod Cliente", font="Arial 14 bold", bg="#FFFFFF")
    textCp1.place(x=10, y=altMenu)

    if tipo == 'I':
        getCp1 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp1.insert(0,getCodCli())
        getCp1.config(state="disabled")
        getCp1.place(x=10, y=altMenu + 30)
    elif tipo == 'A':
        getCp1 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp1.insert(0,valores[0])
        getCp1.config(state="disabled")
        getCp1.place(x=10, y=altMenu + 30)


    #Campo de nome
    textCp2 = Label(janela3, text="Nome Cliente", font="Arial 14 bold", bg="#FFFFFF")
    textCp2.place(x=200, y=altMenu)

    if tipo == 'I':
        getCp2 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp2.place(x=200, y=altMenu + 30)
    elif tipo == 'A':
        getCp2 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp2.insert(0, valores[1])
        getCp2.place(x=200, y=altMenu + 30)

    # Cpf do cliente
    textCp4 = Label(janela3, text="Cpf Cliente", font="Arial 14 bold", bg="#FFFFFF")
    textCp4.place(x=900, y=altMenu)
    if tipo == 'I':
        getCp4 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=15)
        getCp4.place(x=900, y=altMenu + 30)
    elif tipo == 'A':
        getCp4 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=15)
        getCp4.insert(0, valores[3])
        getCp4.place(x=900, y=altMenu + 30)


    #Telefone
    textCp3 = Label(janela3, text="Tel Cliente", font="Arial 14 bold", bg="#FFFFFF")
    textCp3.place(x=1100, y=altMenu)
    if tipo == 'I':
        getCp3 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=15)
        getCp3.place(x=1100, y=altMenu + 30)
    elif tipo == 'A':
        getCp3 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=15)
        getCp3.insert(0, valores[2])
        getCp3.place(x=1100, y=altMenu + 30)

    altMenu += nEspaco + 30

    # Endereco
    textCp5 = Label(janela3, text="End Cliente", font="Arial 14 bold", bg="#FFFFFF")
    textCp5.place(x=10, y=altMenu)
    if tipo == 'I':
        getCp5 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp5.place(x=10, y=altMenu + 30)
    elif tipo == 'A':
        getCp5 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp5.insert(0, valores[4])
        getCp5.place(x=10, y=altMenu + 30)
    altMenu += nEspaco-20


    janela3.mainloop()