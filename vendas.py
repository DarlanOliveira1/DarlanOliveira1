from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import telaInicial
import banco

#Variaveis auxiliares
nEspaco = 60

def listarVendas():

    #popula a tela de inicio de produtos
    def popular():
        tv.delete(*tv.get_children())
        vquery = 'select * from vendas order by 1'
        linhas = banco.dql(vquery)
        for i in linhas:
            tv.insert("", "end", values=i)


    #Cadastra vendas
    def cadastrarVendas():
        valores = []
        app.destroy()
        cadastroVendas("I",valores )#incluir


    #Alterar
    def alterar():
        try:
            vid = -1
            itemSelecionado = tv.selection()[0]
            valores = tv.item(itemSelecionado, "values")
            vid = valores[0]
            app.destroy()
            cadastroVendas("A",valores)#Alterar
        except:
            messagebox.showinfo(title="Erro", message="Selecione um registro a Alterar")

    def voltar():
        app.destroy()
        telaInicial.telaInicio()


    #Deletar
    def deletar():
        try:
            vid=-1
            itemSelecionado=tv.selection()[0]
            valores=tv.item(itemSelecionado,"values")
            vid=valores[1]
            qtd = valores[5]
            vquery = 'delete from vendas where cd_prod = ' + str(vid)
            linhas = banco.dql(vquery)
            tv.delete(itemSelecionado)

            vquery = 'update saldos set qtd_prod = qtd_prod + ' + str(qtd) + ' where cd_prod = ' + str(vid)
            banco.dql(vquery)


        except:
            messagebox.showinfo(title="Erro", message="Selecione um registro a deletar")

    app = Tk()
    app.title("Listar vendas")
    app.state("zoomed")
    app.configure(background='white')

    # variaveis de ajuste de tela
    altMonitor = app.winfo_screenheight()
    largMonitor = app.winfo_screenwidth()
    altIni = (altMonitor - (altMonitor * 0.99))
    larIni = int((largMonitor - (largMonitor * 0.99)))

    largMonitor = app.winfo_screenwidth()
    largGrid    = int(largMonitor/8)-larIni+10

    tv = ttk.Treeview(app,height=40 ,columns=('cd_venda', 'cd_prod', 'dsc_prod','vlr_unitario','cd_cliente','nm_cliente','qtd_venda','vlr_venda'),show='headings')

    tv.column('cd_venda', minwidth=0, width=largGrid)
    tv.heading('#1', text='Codigo Venda')

    tv.column('cd_prod', minwidth=0, width=largGrid)
    tv.heading('#2', text='Codigo Produto')

    tv.column('dsc_prod', minwidth=0, width=largGrid)
    tv.heading('#3', text='Descricao Produto')

    tv.column('vlr_unitario', minwidth=0, width=largGrid)
    tv.heading('#8', text='Valor unitario Produto')

    tv.column('cd_cliente', minwidth=0, width=largGrid)
    tv.heading('#4', text='Codigo Cliente')

    tv.column('nm_cliente', minwidth=0, width=largGrid)
    tv.heading('#5', text='Nome Cliente')

    tv.column('qtd_venda', minwidth=0, width=largGrid)
    tv.heading('#6', text='Qtd Venda')

    tv.column('vlr_venda', minwidth=0, width=largGrid)
    tv.heading('#7', text='Vlr Venda')

    btnInserir=Button(app,text="Inserir", command=cadastrarVendas)
    btnAlterar = Button(app, text="Alterar", command=alterar)
    btnDeletar = Button(app, text="Deletar", command=deletar)
    btVoltar = Button(app, text="Voltar", command=voltar)


    btnInserir.place(x=larIni,y=altIni)
    btnDeletar.place(x=larIni*12,y=altIni)
    btVoltar.place(x=larIni*18,y=altIni)

    altIni += 30
    tv.place(x=10,y=altIni)

    popular()
    app.mainloop()


##############################################
## Tela de cadastro de Vendas             ##
##############################################
import sqlite3


def cadastroVendas(tipo,valores):

    def getTelaIniVendas():

        janela3.destroy()
        listarVendas()  # retorna a tela anterior

    def listarProdutos():

        def impProdutos():
            getCp2.delete(0, END)
            getCp3.delete(0, END)
            getCp8.delete(0, END)

            var = str(lb_esportes.get(ACTIVE)).replace('(','').replace(')','')
            var1 = var.replace("'","").replace('[','').replace(']','').split(",")

            getCp2.insert(0, var1[0])
            getCp3.insert(0, var1[1])
            getCp8.insert(0, var1[2])

            bt.destroy()

            getCp2.config(state="disabled")
            getCp3.config(state="disabled")
            getCp8.config(state="disabled")

        vquery = 'select cd_prod,dsc_prod,vlr_unit from produtos order by 1'
        linhas = banco.dql(vquery)

        bt = Tk()
        bt.title("Produto")
        bt.geometry("300x300")
        bt.configure(background='white')

        listaEsportes = linhas
        lb_esportes = Listbox(bt)
        for esportes in listaEsportes:
            lb_esportes.insert(END, esportes)

        lb_esportes.pack()

        btn_produto = Button(bt, text='Escolher', command=impProdutos)
        btn_produto.pack()
        bt.mainloop()

    def getConsultaSaldoProd():

        vquery = 'select qtd_prod from saldos where cd_prod =' + getCp2.get()
        linhas = banco.dql(vquery)

        try:
            nSaldoProd = int(str(linhas).split(',')[0].replace('[','').replace(']','').replace('(','').replace(')',''))
            return(nSaldoProd)
        except:
            nSaldoProd = 0
            return(nSaldoProd)

    def atuSaldoEstoque():

        sqliteConect = sqlite3.connect('banco/pdv2.db')
        cursor = sqliteConect.cursor()
        saldo = getConsultaSaldoProd()
        saldoAtu = saldo - int(getCp6.get())

        scriptGrava = "update "
        scriptGrava += " saldos "
        scriptGrava += " set "
        scriptGrava += "    qtd_prod     =  " + str(saldoAtu) + " "
        scriptGrava += " where"
        scriptGrava += "    cd_prod = " + getCp2.get() + ""

        messagebox.showinfo(title="Alterado", message="Saldo atualizado")

        count = cursor.execute(scriptGrava)
        sqliteConect.commit()
        cursor.close()




    def listarClientes():


        def impClientes():
            getCp4.delete(0, END)
            getCp5.delete(0, END)

            var1 = str(lb_esportes.get(ACTIVE))
            var2 = str(lb_esportes.get(ACTIVE))

            getCp4.insert(0, var1[1])
            getCp5.insert(0,
                          var1[3:len(var1)].replace(')', '').replace('(', '').replace("'", "").replace('{', '').replace(
                              '}', ''))

            bt.destroy()

            getCp4.config(state="disabled")
            getCp5.config(state="disabled")

        vquery = 'select cd_cliente,nm_cliente  from clientes order by 1'
        linhas = banco.dql(vquery)

        bt = Tk()
        bt.title("Produto")
        bt.geometry("300x300")
        bt.configure(background='white')

        listaEsportes = linhas
        lb_esportes = Listbox(bt)
        for esportes in listaEsportes:
            lb_esportes.insert(END, esportes)

        lb_esportes.pack()

        btn_produto = Button(bt, text='Escolher', command=impClientes)
        btn_produto.pack()
        bt.mainloop()

    def getCodVendas():

        vquery = " select"
        vquery += "      case "
        vquery += "          when "
        vquery += "              max(cd_venda) is null then 1 "
        vquery += "          else "
        vquery += "              max(cd_venda) + 1  "
        vquery += "      end as cod "
        vquery += " from vendas "
        linhas = banco.dql(vquery)
        return (linhas)

    def getVlrProd():

        getCp7.delete(0, END)
        getCp7.insert(0, int(getCp8.get())*int(getCp6.get()))

        return()


    def gravaVendas():

        cd_venda = getCp1.get()
        cd_prod = getCp2.get()
        dsc_prod = getCp3.get()
        cd_cliente = getCp4.get()
        nm_cliente = getCp5.get()
        qtd_venda = getCp6.get()
        vlr_venda = getCp7.get()
        vlr_unitario = getCp8.get()
        sqliteConect = sqlite3.connect('banco/pdv2.db')
        cursor = sqliteConect.cursor()

        if getConsultaSaldoProd() == 0:
            texto = "Saldo não cadastrado"
            messagebox.showwarning(title='Alerta', message=texto)
        elif getConsultaSaldoProd() < int(qtd_venda):
            texto = "Saldo insuficiente"
            messagebox.showwarning(title='Alerta', message=texto)
        else:
            if tipo == 'I':

                atuSaldoEstoque()

                scriptGrava = " insert into vendas "
                scriptGrava += "    (cd_prod,"
                scriptGrava += "    dsc_prod,"
                scriptGrava += "    cd_cliente,"
                scriptGrava += "    nm_cliente,"
                scriptGrava += "    qtd_venda,"
                scriptGrava += "    vlr_unitario,"
                scriptGrava += "    vlr_venda)"
                scriptGrava += " values ("
                scriptGrava += ""   + cd_prod       + ","
                scriptGrava += "'"  + dsc_prod      + "',"
                scriptGrava += ""   + cd_cliente    + ","
                scriptGrava += "'"  + nm_cliente    + "',"
                scriptGrava += ""   + qtd_venda     + ","
                scriptGrava += "" + vlr_unitario + ","
                scriptGrava += ""   + vlr_venda     + ")"

                messagebox.showinfo(title="Incluido", message="Registro gravado com sucesso")

            elif tipo == 'A':
                scriptGrava = "update "
                scriptGrava += " vendas "
                scriptGrava += " set "
                scriptGrava += "    cd_prod     =  " + cd_prod + ","
                scriptGrava += "    dsc_prod    = '" + dsc_prod + "',"
                scriptGrava += "    cd_cliente  =  " + cd_cliente + ","
                scriptGrava += "    nm_cliente  = '" + nm_cliente + "',"
                scriptGrava += "    qtd_venda   = '" + qtd_venda + "',"
                scriptGrava += "    vlr_unitario   = '" + vlr_unitario + "',"
                scriptGrava += "    vlr_venda   = " + vlr_venda + " "
                scriptGrava += " where"
                scriptGrava += "    cd_venda = " + cd_venda + ""
                messagebox.showinfo(title="Alterado", message="Registro alterado com sucesso")

        count = cursor.execute(scriptGrava)
        sqliteConect.commit()
        cursor.close()
        getTelaIniVendas()

    janela3 = Tk()
    janela3.state("zoomed")

    if tipo == 'I':
        janela3.title("Cadastrar de Vendas")
    elif tipo == 'A':
        janela3.title("Alterar Vendas")

    janela3.configure(background='white')

    # variaveis de ajuste de tela
    altMonitor = janela3.winfo_screenheight()
    largMonitor = janela3.winfo_screenwidth()
    larIni = 10
    altMenu = (altMonitor - (altMonitor * 0.99))
    largMenu = (largMonitor - (largMonitor * 0.2))

    # Menus Cadastro

    if tipo == 'I':
        textUsu = Label(janela3, text="Cadastro de Vendas - Incluir", font="Arial 20 bold", bg="#FFFFFF")
    elif tipo == 'A':
        textUsu = Label(janela3, text="Cadastro de Vendas - Alterar", font="Arial 20 bold", bg="#FFFFFF")

    textUsu.place(x=larIni, y=altMenu)

    if tipo == 'I':
        btCadastro = Button(janela3, text="Cadastrar", font="Arial 14 bold", bg="#FFFFFF", command=gravaVendas)
    elif tipo == 'A':
        btCadastro = Button(janela3, text="Salvar Alteracao", font="Arial 14 bold", bg="#FFFFFF", command=gravaVendas)
    btCadastro.place(x=largMenu, y=altMenu)

    menu = Button(janela3, text="Voltar", font="Arial 14 bold", bg="#FFFFFF", command=getTelaIniVendas)
    menu.place(x=largMenu + 180, y=altMenu)

    altMenu += nEspaco

    # Campo de codigo
    textCp1 = Label(janela3, text="Cod Vendas", font="Arial 14 bold", bg="#FFFFFF")
    textCp1.place(x=10, y=altMenu)

    if tipo == 'I':
        getCp1 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp1.insert(0, getCodVendas())
        getCp1.config(state="disabled")
        getCp1.place(x=10, y=altMenu + 30)
    elif tipo == 'A':
        getCp1 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp1.insert(0, valores[0])
        getCp1.config(state="disabled")
        getCp1.place(x=10, y=altMenu + 30)

    altMenu += nEspaco

    #Campo do Produto
    textCp2 = Label(janela3, text="Cod Produto", font="Arial 14 bold", bg="#FFFFFF")
    textCp2.place(x=10, y=altMenu)

    if tipo == 'I':
        getCp2 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp2.place(x=10, y=altMenu + 30)
    elif tipo == 'A':
        getCp2 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        #getCp2.insert(0, valores[1])
        getCp2.place(x=10, y=altMenu + 30)



    # Campo de Descricao do Produto
    textCp3 = Label(janela3, text="Descricao Produtos", font="Arial 14 bold", bg="#FFFFFF")
    textCp3.place(x=160, y=altMenu)

    if tipo == 'I':
        getCp3 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp3.place(x=160, y=altMenu + 30)
    elif tipo == 'A':
        getCp3 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp3.insert(0, valores[2])
        getCp3.place(x=160, y=altMenu + 30)


    # Campo valor unitario produto
    textCp8 = Label(janela3, text="Vlr Unit Produto", font="Arial 14 bold", bg="#FFFFFF")
    textCp8.place(x=850, y=altMenu)

    if tipo == 'I':
        getCp8 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=15)
        getCp8.place(x=850, y=altMenu + 30)
    elif tipo == 'A':
        getCp8 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=15)
        getCp8.insert(0, valores[2])
        getCp8.place(x=850, y=altMenu + 30)



    menu = Button(janela3, text="Buscar Produto", font="Arial 10 bold", bg="#FFFFFF", command=listarProdutos)
    menu.place(x=1050, y=altMenu + 30)

    altMenu += nEspaco

    #Codigo do cliente
    textCp4 = Label(janela3, text="Cod Cliente", font="Arial 14 bold", bg="#FFFFFF")
    textCp4.place(x=10, y=altMenu)
    if tipo == 'I':
        getCp4 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp4.place(x=10, y=altMenu + 30)
    elif tipo == 'A':
        getCp4 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp4.insert(0, valores[3])
        getCp4.place(x=10, y=altMenu + 30)


    ## Nome do cliente
    textCp5 = Label(janela3, text="Nome Cliente", font="Arial 14 bold", bg="#FFFFFF")
    textCp5.place(x=160, y=altMenu)

    if tipo == 'I':
        getCp5 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp5.place(x=160, y=altMenu + 30)
    elif tipo == 'A':
        getCp5 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp5.insert(0, valores[4])
        getCp5.place(x=160, y=altMenu + 30)

    menu = Button(janela3, text="Buscar Cliente", font="Arial 10 bold", bg="#FFFFFF", command=listarClientes)
    menu.place(x=1050, y=altMenu + 30)

    altMenu += nEspaco

    #Quantidade de venda
    textCp6 = Label(janela3, text="Qtd vendida", font="Arial 14 bold", bg="#FFFFFF")
    textCp6.place(x=10, y=altMenu)
    if tipo == 'I':
        getCp6 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp6.place(x=10, y=altMenu + 30)
    elif tipo == 'A':
        getCp6 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp6.insert(0, valores[5])
        getCp6.place(x=10, y=altMenu + 30)



    # Valor Total
    textCp7 = Label(janela3, text="Valor Venda", font="Arial 14 bold", bg="#FFFFFF")
    textCp7.place(x=160, y=altMenu)
    if tipo == 'I':
        getCp7 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp7.place(x=160, y=altMenu + 30)
    elif tipo == 'A':
        getCp7 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp7.insert(0, valores[6])
        getCp7.place(x=160, y=altMenu + 30)

    altMenu += nEspaco + 30

    menu = Button(janela3, text="Simula Venda", font="Arial 10 bold", bg="#FFFFFF", command=getVlrProd)
    menu.place(x=850, y=altMenu + 30)


    janela3.mainloop()
