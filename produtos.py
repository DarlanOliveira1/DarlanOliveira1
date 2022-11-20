from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import telaInicial
import banco

#Variaveis auxiliares
nEspaco = 60

def listarProdutos():

    #popula a tela de inicio de produtos
    def popular():
        tv.delete(*tv.get_children())
        vquery = 'select * from produtos order by 1'
        linhas = banco.dql(vquery)
        for i in linhas:
            tv.insert("", "end", values=i)

    #Volta para tela anterior
    def voltar():
        app.destroy()
        telaInicial.telaInicio()

    #Cadastra produtos
    def cadastrarProdutos():
        valores = []
        app.destroy()
        cadastroprodutos("I",valores )#incluir


    #Alterar
    def alterar():
        try:
            vid = -1
            itemSelecionado = tv.selection()[0]
            valores = tv.item(itemSelecionado, "values")
            vid = valores[0]
            app.destroy()
            cadastroprodutos("A",valores)#Alterar
        except:
            messagebox.showinfo(title="Erro", message="Selecione um registro a Alterar")


    #Deletar
    def deletar():

        vid = -1
        itemSelecionado = tv.selection()[0]
        valores = tv.item(itemSelecionado, "values")
        vid = valores[0]
        vquery = 'select count(*) as tot from vendas where cd_prod = ' + str(vid)
        dados = str(banco.dql(vquery)).replace('[','').replace(']','').replace('(','').replace(')','').replace(',','')

        if int(dados)>0:
            texto = "O produto não pode ser deletado, pois esta vinculado a uma venda"
            messagebox.showinfo(title="Erro", message=texto)
        else:
            try:
                vquery = 'delete from produtos where cd_prod = ' + str(vid)
                linhas = banco.dql(vquery)
                tv.delete(itemSelecionado)
            except:
                messagebox.showinfo(title="Erro", message="Selecione um registro a deletar")

    app = Tk()
    app.title("Listar produtos")
    app.state("zoomed")
    app.configure(background='white')

    # variaveis de ajuste de tela
    altMonitor = app.winfo_screenheight()
    largMonitor = app.winfo_screenwidth()
    altIni = (altMonitor - (altMonitor * 0.99))
    larIni = int((largMonitor - (largMonitor * 0.99)))

    largMonitor = app.winfo_screenwidth()
    largGrid    = int(largMonitor/5)-larIni

    tv = ttk.Treeview(app,height=40 ,columns=('cd_prod', 'dsc_prod', 'vlr_unit','cd_forne','nm_forne'),show='headings')

    tv.column('cd_prod', minwidth=0, width=largGrid)
    tv.heading('#1', text='Codigo Produto')

    tv.column('dsc_prod', minwidth=0, width=largGrid)
    tv.heading('#2', text='Descricao Produto')

    tv.column('vlr_unit', minwidth=0, width=largGrid)
    tv.heading('#3', text='Valor unitario')

    tv.column('cd_forne', minwidth=0, width=largGrid)
    tv.heading('#4', text='Codigo Fornecedor')

    tv.column('nm_forne', minwidth=0, width=largGrid)
    tv.heading('#5', text='Nome Fornecedor')

    btnInserir=Button(app,text="Inserir", command=cadastrarProdutos)
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


##############################################
## Tela de cadastro de produtos             ##
##############################################
import sqlite3
def cadastroprodutos(tipo,valores):

    def getTelaIniprodutos():

        janela3.destroy()
        listarProdutos() #retorna a tela anterior

    def listarFornecedores():

        def impFornecedor():
            getCp5.delete(0, END)
            getCp6.delete(0, END)

            var1 = str(lb_esportes.get(ACTIVE))
            var2 = str(lb_esportes.get(ACTIVE))

            getCp5.insert(0, var1[1])
            getCp6.insert(0, var1[3:len(var1)].replace(')','').replace('(','').replace("'","").replace('{','').replace('}',''))

            bt.destroy()

            getCp5.config(state="disabled")
            getCp6.config(state="disabled")

        vquery = 'select cd_forne,nm_forne  from fornecedores order by 1'
        linhas = banco.dql(vquery)

        bt = Tk()
        bt.title("Fornecedores")
        bt.geometry("300x300")
        bt.configure(background='white')

        listaEsportes=linhas
        lb_esportes=Listbox(bt)
        for esportes in listaEsportes:
            lb_esportes.insert(END,esportes)

        lb_esportes.pack()

        btn_produto=Button(bt,text='Escolher',command=impFornecedor)
        btn_produto.pack()
        bt.mainloop()


    def getCodProdutos():

        vquery = " select"
        vquery += "      case "
        vquery += "          when "
        vquery += "              max(cd_prod) is null then 1 "
        vquery += "          else "
        vquery += "              max(cd_prod) + 1  "
        vquery += "      end as cod "
        vquery += " from produtos "
        linhas = banco.dql(vquery)
        return(linhas)

    def gravaProdutos():

        cd_prod = getCp1.get()
        dsc_prod = getCp2.get()
        vlr_unit = getCp4.get().replace(" ","").replace(".","").replace("(","").replace(")","").replace("-","")
        cod_forne = getCp5.get()
        nome_forn = getCp6.get()


        sqliteConect = sqlite3.connect('banco/pdv2.db')
        cursor = sqliteConect.cursor()

        if dsc_prod == '':
            texto = "A descricao do produto deve ser preenchida"
            messagebox.showwarning(title='Alerta', message=texto)
        elif vlr_unit == '':
            texto = "Valor unitario do produto deve ser preenchido"
            messagebox.showwarning(title='Alerta', message=texto)
        elif cod_forne == '':
            texto = "Use a busca por fonecedores para preencher o campo de cd fornecedor"
            messagebox.showwarning(title='Alerta', message=texto)
        elif nome_forn == '':
            texto = "Use a busca por fonecedores para preencher o campo de nm fornecedor"
            messagebox.showwarning(title='Alerta', message=texto)
        else:

            if tipo == 'I':

                scriptGrava = " insert into produtos "
                scriptGrava += "    (dsc_prod,"
                scriptGrava += "    cd_forne,"
                scriptGrava += "    nm_forne,"
                scriptGrava += "    vlr_unit)"
                scriptGrava += " values ("
                scriptGrava += "'" + dsc_prod + "',"
                scriptGrava += "" + cod_forne + ","
                scriptGrava += "'" + nome_forn + "',"
                scriptGrava += "" + vlr_unit + ")"
                messagebox.showinfo(title="Incluido", message="Registro gravado com sucesso")
            elif tipo == 'A':
                scriptGrava = "update "
                scriptGrava += " produtos "
                scriptGrava += " set "
                scriptGrava += "    dsc_prod  = '" + dsc_prod + "',"
                scriptGrava += "    cd_forne  = " + cod_forne + ","
                scriptGrava += "    nm_forne  = '" + nome_forn + "',"
                scriptGrava += "    vlr_unit = "  + vlr_unit + " "
                scriptGrava += " where"
                scriptGrava += "    cd_prod = " + cd_prod  + ""
                messagebox.showinfo(title="Alterado", message="Registro alterado com sucesso")

        count = cursor.execute(scriptGrava)
        sqliteConect.commit()
        cursor.close()
        getTelaIniprodutos()

    janela3 = Tk()
    janela3.state("zoomed")

    if tipo == 'I':
        janela3.title("Cadastrar de produtos")
    elif tipo == 'A':
        janela3.title("Alterar produtos")

    janela3.configure(background='white')

    # variaveis de ajuste de tela
    altMonitor = janela3.winfo_screenheight()
    largMonitor = janela3.winfo_screenwidth()
    larIni = 10
    altMenu = (altMonitor - (altMonitor * 0.99))
    largMenu = (largMonitor - (largMonitor * 0.2))

    # Menus Cadastro

    if tipo == 'I':
        textUsu = Label(janela3, text="Cadastro de produtos - Incluir", font="Arial 20 bold", bg="#FFFFFF")
    elif tipo == 'A':
        textUsu = Label(janela3, text="Cadastro de produtos - Alterar", font="Arial 20 bold", bg="#FFFFFF")

    textUsu.place(x=larIni, y=altMenu)

    if tipo == 'I':
        btCadastro = Button(janela3, text="Cadastrar", font="Arial 14 bold", bg="#FFFFFF", command=gravaProdutos)
    elif tipo == 'A':
        btCadastro = Button(janela3, text="Salvar Alteracao", font="Arial 14 bold", bg="#FFFFFF", command=gravaProdutos)
    btCadastro.place(x=largMenu, y=altMenu)

    menu = Button(janela3, text="Voltar", font="Arial 14 bold", bg="#FFFFFF", command=getTelaIniprodutos)
    menu.place(x=largMenu + 180, y=altMenu)


    altMenu += nEspaco

    #Campo de codigo
    textCp1 = Label(janela3, text="Cod Produtos", font="Arial 14 bold", bg="#FFFFFF")
    textCp1.place(x=10, y=altMenu)

    if tipo == 'I':
        getCp1 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp1.insert(0,getCodProdutos())
        getCp1.config(state="disabled")
        getCp1.place(x=10, y=altMenu + 30)
    elif tipo == 'A':
        getCp1 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp1.insert(0,valores[0])
        getCp1.config(state="disabled")
        getCp1.place(x=10, y=altMenu + 30)


    #Campo de Descricao
    textCp2 = Label(janela3, text="Descricao Produtos", font="Arial 14 bold", bg="#FFFFFF")
    textCp2.place(x=200, y=altMenu)

    if tipo == 'I':
        getCp2 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp2.place(x=200, y=altMenu + 30)
    elif tipo == 'A':
        getCp2 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp2.insert(0, valores[1])
        getCp2.place(x=200, y=altMenu + 30)

    # Vlr Unitario
    textCp4 = Label(janela3, text="Vlr Unitario Produtos", font="Arial 14 bold", bg="#FFFFFF")
    textCp4.place(x=900, y=altMenu)
    if tipo == 'I':
        getCp4 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=15)
        getCp4.place(x=900, y=altMenu + 30)
    elif tipo == 'A':
        getCp4 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=15)
        getCp4.insert(0, valores[2])
        getCp4.place(x=900, y=altMenu + 30)


    altMenu += nEspaco + 30


    #Campo de codigo Fornecedor
    textCp5 = Label(janela3, text="Cod Fornecedor", font="Arial 14 bold", bg="#FFFFFF")
    textCp5.place(x=10, y=altMenu)

    if tipo == 'I':
        getCp5 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp5.place(x=10, y=altMenu + 30)
    elif tipo == 'A':
        getCp5 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp5.place(x=10, y=altMenu + 30)
        getCp5.insert(0, valores[3])

    #Campo de nome Fornecedor
    textCp6 = Label(janela3, text="Nome Fornecedor", font="Arial 14 bold", bg="#FFFFFF")
    textCp6.place(x=200, y=altMenu)

    if tipo == 'I':
        getCp6 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp6.place(x=200, y=altMenu + 30)
    elif tipo == 'A':
        getCp6 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp6.insert(0, valores[4])
        getCp6.place(x=200, y=altMenu + 30)

    menu = Button(janela3, text="Buscar Fornecedor", font="Arial 10 bold", bg="#FFFFFF", command=listarFornecedores)
    menu.place(x=900, y=altMenu + 30)

    janela3.mainloop()
