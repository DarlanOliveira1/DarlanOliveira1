from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import telaInicial
import banco

#Variaveis auxiliares
nEspaco = 60

def listarSaldos():

    #popula a tela de inicio de saldos
    def popular():
        tv.delete(*tv.get_children())
        vquery = 'select * from saldos order by 1'
        linhas = banco.dql(vquery)
        for i in linhas:
            tv.insert("", "end", values=i)

    #Volta para tela anterior
    def voltar():
        app.destroy()
        telaInicial.telaInicio()

    #Cadastra saldos
    def cadastrarSaldos():
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
        try:
            vid=-1
            itemSelecionado=tv.selection()[0]
            valores=tv.item(itemSelecionado,"values")
            vid=valores[0]
            vquery = 'delete from saldos where cod_mov = ' + str(vid)
            linhas = banco.dql(vquery)
            tv.delete(itemSelecionado)
        except:
            messagebox.showinfo(title="Erro", message="Selecione um registro a deletar")

    app = Tk()
    app.title("Listar saldos")
    app.state("zoomed")
    app.configure(background='white')

    # variaveis de ajuste de tela
    altMonitor = app.winfo_screenheight()
    largMonitor = app.winfo_screenwidth()
    altIni = (altMonitor - (altMonitor * 0.99))
    larIni = int((largMonitor - (largMonitor * 0.99)))

    largMonitor = app.winfo_screenwidth()
    largGrid    = int(largMonitor/4)-larIni

    tv = ttk.Treeview(app,height=40 ,columns=('cod_mov', 'cd_prod', 'dsc_prod','qtd_prod'),show='headings')

    tv.column('cod_mov', minwidth=0, width=largGrid)
    tv.heading('#1', text='Codigo')

    tv.column('cd_prod', minwidth=0, width=largGrid)
    tv.heading('#2', text='Cod Produto')

    tv.column('dsc_prod', minwidth=0, width=largGrid)
    tv.heading('#3', text='Descricao Produto')

    tv.column('qtd_prod', minwidth=0, width=largGrid)
    tv.heading('#4', text='Quantidade')


    btnInserir=Button(app,text="Inserir", command=cadastrarSaldos)
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
## Tela de cadastro de saldos             ##
##############################################
def cadastroprodutos(tipo,valores):

    def getTelaIniprodutos():

        janela3.destroy()
        listarSaldos() #retorna a tela anterior

    def getCodSaldos():

        vquery = " select"
        vquery += "      case "
        vquery += "          when "
        vquery += "              max(cod_mov) is null then 1 "
        vquery += "          else "
        vquery += "              max(cod_mov) + 1  "
        vquery += "      end as cod "
        vquery += " from saldos "
        linhas = banco.dql(vquery)
        return(linhas)

    def gravaSaldos():

        cod_mov = getCp1.get()
        cd_prod = getCp2.get()
        qtd_prod = getCp4.get().replace(" ","").replace(".","").replace("(","").replace(")","").replace("-","")
        dsc_prod = str(getCp3.get())

        sqliteConect = sqlite3.connect('banco/pdv2.db')
        cursor = sqliteConect.cursor()
        if tipo == 'I':

            scriptGrava = " insert into saldos "
            scriptGrava += "    (cd_prod,"
            scriptGrava += "    dsc_prod,"
            scriptGrava += "    qtd_prod)"
            scriptGrava += " values ("
            scriptGrava += " " + cd_prod + ","
            scriptGrava += " '" + dsc_prod + "',"
            scriptGrava += "" + qtd_prod + ")"
            messagebox.showinfo(title="Incluido", message="Registro gravado com sucesso")

        elif tipo == 'A':
            scriptGrava = "update "
            scriptGrava += " saldos "
            scriptGrava += " set "
            scriptGrava += "    cd_prod  = " + cd_prod + ","
            scriptGrava += "    dsc_prod  = '" + dsc_prod + "',"
            scriptGrava += "    qtd_prod = "  + qtd_prod + " "
            scriptGrava += " where"
            scriptGrava += "    cod_mov = '" + cod_mov  + "'"
            messagebox.showinfo(title="Alterado", message="Registro alterado com sucesso")

        count = cursor.execute(scriptGrava)
        sqliteConect.commit()
        cursor.close()
        getTelaIniprodutos()

    #listagemProdutos
    def listagemProdutos():

        def impProd():

            getCp2.delete(0, END)
            getCp3.delete(0, END)

            var1 = str(lb_esportes.get(ACTIVE))
            var2 = str(lb_esportes.get(ACTIVE))

            getCp2.insert(0, var1[1])
            getCp3.insert(0, var1[3:len(var1)].replace(')','').replace('(','').replace("'",""))

            bt.destroy()

            getCp2.config(state="disabled")
            getCp3.config(state="disabled")

        vquery = 'select cd_prod,dsc_prod  from produtos order by 1'
        linhas = banco.dql(vquery)

        if 'bt' in locals() or 'bt' in globals():
            bt.destroy()
        bt = Tk()
        bt.title("Produtos")
        bt.geometry("500x500")
        bt.configure(background='white')

        listaEsportes=linhas
        lb_esportes=Listbox(bt)
        for esportes in listaEsportes:
            lb_esportes.insert(END,esportes)

        lb_esportes.pack()

        btn_produto=Button(bt,text='Escolher',command=impProd)
        btn_produto.pack()
        bt.mainloop()

    janela3 = Tk()
    janela3.state("zoomed")

    if tipo == 'I':
        janela3.title("Cadastrar de saldos")
    elif tipo == 'A':
        janela3.title("Alterar saldos")

    janela3.configure(background='white')

    # variaveis de ajuste de tela
    altMonitor = janela3.winfo_screenheight()
    largMonitor = janela3.winfo_screenwidth()
    larIni = 10
    altMenu = (altMonitor - (altMonitor * 0.99))
    largMenu = (largMonitor - (largMonitor * 0.2))

    # Menus Cadastro

    if tipo == 'I':
        textUsu = Label(janela3, text="Cadastro de saldos - Incluir", font="Arial 20 bold", bg="#FFFFFF")
    elif tipo == 'A':
        textUsu = Label(janela3, text="Cadastro de saldos - Alterar", font="Arial 20 bold", bg="#FFFFFF")

    textUsu.place(x=larIni, y=altMenu)

    if tipo == 'I':
        btCadastro = Button(janela3, text="Cadastrar", font="Arial 14 bold", bg="#FFFFFF", command=gravaSaldos)
    elif tipo == 'A':
        btCadastro = Button(janela3, text="Salvar Alteracao", font="Arial 14 bold", bg="#FFFFFF", command=gravaSaldos)
    btCadastro.place(x=largMenu, y=altMenu)

    menu = Button(janela3, text="Voltar", font="Arial 14 bold", bg="#FFFFFF", command=getTelaIniprodutos)
    menu.place(x=largMenu + 180, y=altMenu)


    altMenu += nEspaco

    #Campo de codigo
    textCp1 = Label(janela3, text="Cod saldos", font="Arial 14 bold", bg="#FFFFFF")
    textCp1.place(x=10, y=altMenu)

    if tipo == 'I':
        getCp1 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp1.insert(0,getCodSaldos())
        getCp1.config(state="disabled")
        getCp1.place(x=10, y=altMenu + 30)
    elif tipo == 'A':
        getCp1 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp1.insert(0,valores[0])
        getCp1.config(state="disabled")
        getCp1.place(x=10, y=altMenu + 30)



    #Campo de codigo
    textCp2 = Label(janela3, text="Cod Produto", font="Arial 14 bold", bg="#FFFFFF")
    textCp2.place(x=200, y=altMenu)

    #Campo de Descricao
    textCp2 = Label(janela3, text="Descricao Produto", font="Arial 14 bold", bg="#FFFFFF")
    textCp2.place(x=350, y=altMenu)

    #cod movimentacao
    if tipo == 'I':
        getCp2 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp2.place(x=200, y=altMenu + 30)

    elif tipo == 'A':
        getCp2 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp2.insert(0, valores[1])
        getCp2.config(state="disabled")
        getCp2.place(x=200, y=altMenu + 30)


    #Desc prod
    if tipo == 'I':
        getCp3 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp3.place(x=350, y=altMenu + 30)

    elif tipo == 'A':
        getCp3 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp3.insert(0, valores[2])
        getCp3.config(state="disabled")
        getCp3.place(x=350, y=altMenu + 30)


    menu = Button(janela3, text="Buscar Produtos", font="Arial 10 bold", bg="#FFFFFF", command=listagemProdutos)

    if tipo == 'A':
        menu.config(state="disabled")
    menu.place(x=1030, y=altMenu + 30)

    altMenu += 80

    # Vlr Unitario
    textCp4 = Label(janela3, text="Quantidade Estoque", font="Arial 14 bold", bg="#FFFFFF")
    textCp4.place(x=10, y=altMenu)
    if tipo == 'I':
        getCp4 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=15)
        getCp4.place(x=10, y=altMenu + 30)

    elif tipo == 'A':
        getCp4 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=15)
        getCp4.insert(0, valores[3])
        getCp4.place(x=10, y=altMenu + 30)

    janela3.mainloop()