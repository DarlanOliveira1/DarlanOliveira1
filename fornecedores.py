from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import telaInicial
import banco

#Variaveis auxiliares
nEspaco = 60

def listarFonecedores():

    #popula a tela de inicio de fornecedores
    def popular():
        tv.delete(*tv.get_children())
        vquery = 'select * from fornecedores order by 1'
        linhas = banco.dql(vquery)
        for i in linhas:
            tv.insert("", "end", values=i)

    #Volta para tela anterior
    def voltar():
        app.destroy()
        telaInicial.telaInicio()

    #Cadastra fornecedores
    def cadastrarFornecedor():
        valores = []
        app.destroy()
        cadastrofornecedores("I",valores )#incluir


    #Alterar
    def alterar():
        try:
            vid = -1
            itemSelecionado = tv.selection()[0]
            valores = tv.item(itemSelecionado, "values")
            vid = valores[0]
            app.destroy()
            cadastrofornecedores("A",valores)#Alterar
        except:
            messagebox.showinfo(title="Erro", message="Selecione um registro a Alterar")


    #Deletar
    def deletar():

        vid = -1
        itemSelecionado = tv.selection()[0]
        valores = tv.item(itemSelecionado, "values")
        vid = valores[0]
        vquery = 'select count(*) as tot from produtos where cd_forne = ' + str(vid)
        dados = str(banco.dql(vquery)).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',',                                                                                                                   '')

        if int(dados) > 0:
            texto = "O cliente não pode ser deletado, pois esta vinculado a um produto"
            messagebox.showinfo(title="Erro", message=texto)
        else:
            try:
                vquery = 'delete from fornecedores where cd_forne = ' + str(vid)
                linhas = banco.dql(vquery)
                tv.delete(itemSelecionado)
            except:
                messagebox.showinfo(title="Erro", message="Selecione um registro a deletar")

    app = Tk()
    app.title("Listar Fornecedores")
    app.state("zoomed")
    app.configure(background='white')

    # variaveis de ajuste de tela
    altMonitor = app.winfo_screenheight()
    largMonitor = app.winfo_screenwidth()
    altIni = (altMonitor - (altMonitor * 0.99))
    larIni = int((largMonitor - (largMonitor * 0.99)))

    largMonitor = app.winfo_screenwidth()
    largGrid    = int(largMonitor/5)-larIni

    tv = ttk.Treeview(app,height=40 ,columns=('cd_forne', 'nm_forne', 'tel_forne', 'cnpj_forne', 'end_forne'),show='headings')

    tv.column('cd_forne', minwidth=0, width=largGrid)
    tv.heading('#1', text='Codigo')

    tv.column('nm_forne', minwidth=0, width=largGrid)
    tv.heading('#2', text='Nome')

    tv.column('tel_forne', minwidth=0, width=largGrid)
    tv.heading('#3', text='Telefone')

    tv.column('cnpj_forne', minwidth=0, width=largGrid)
    tv.heading('#4', text='Cpf/Cgc')

    tv.column('end_forne', minwidth=0, width=largGrid)
    tv.heading('#5', text='Endereco')

    btnInserir=Button(app,text="Inserir", command=cadastrarFornecedor)
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
##################################################
## Tela de cadastro de fornecedores             ##
##################################################
def cadastrofornecedores(tipo,valores):

    def getTelaInifornecedores():

        janela3.destroy()
        listarFonecedores() #retorna a tela anterior

    def getCodFornecedor():

        vquery = " select"
        vquery += "      case "
        vquery += "          when "
        vquery += "              max(cd_forne) is null then 1 "
        vquery += "          else "
        vquery += "              max(cd_forne) + 1  "
        vquery += "      end as cod "
        vquery += " from fornecedores "
        linhas = banco.dql(vquery)
        return(linhas)

    def gravaFornecedor():

        cd_forne = getCp1.get()
        nm_forne = getCp2.get()
        telFornecedor = getCp3.get().replace(" ","").replace(".","").replace("(","").replace(")","").replace("-","")
        cpfFornecedor = getCp4.get().replace(" ","").replace(",","").replace(".","").replace("-","").replace("_","")
        endForncedor = getCp5.get()

        sqliteConect = sqlite3.connect('banco/pdv2.db')
        cursor = sqliteConect.cursor()
        
        if nm_forne == '':
            texto = "O nome do fornecedor deve ser preenchido"
            messagebox.showwarning(title='Alerta', message=texto)
        elif telFornecedor == '':
            texto = "O telefone do fornecedor deve ser preenchido"
            messagebox.showwarning(title='Alerta', message=texto)
        elif cpfFornecedor == '':
            texto = "O CPF do fornecedor deve ser preenchido"
            messagebox.showwarning(title='Alerta', message=texto)
        elif endForncedor == '':
            texto = "O endereco do fornecedor deve ser preenchido"
            messagebox.showwarning(title='Alerta', message=texto)
        else:
        
            if tipo == 'I':
    
                scriptGrava = " insert into fornecedores "
                scriptGrava += "    (nm_forne,"
                scriptGrava += "    tel_forne,"
                scriptGrava += "    cnpj_forne,"
                scriptGrava += "    end_forne)"
                scriptGrava += " values ("
                scriptGrava += "'" + nm_forne + "',"
                scriptGrava += telFornecedor + ","
                scriptGrava += cpfFornecedor + ","
                scriptGrava += "'" + endForncedor + "')"
                messagebox.showinfo(title="Incluido", message="Registro gravado com sucesso")
    
            elif tipo == 'A':
                scriptGrava = "update "
                scriptGrava += " fornecedores "
                scriptGrava += " set "
                scriptGrava += "    nm_forne  = '" + nm_forne + "',"
                scriptGrava += "    tel_forne = "  + telFornecedor + ","
                scriptGrava += "    cnpj_forne = " + cpfFornecedor + ","
                scriptGrava += "    end_forne = '" + endForncedor + "'"
                scriptGrava += "where"
                scriptGrava += "    cd_forne = '" + cd_forne  + "'"
                messagebox.showinfo(title="Alterado", message="Registro alterado com sucesso")

        count = cursor.execute(scriptGrava)
        sqliteConect.commit()
        cursor.close()
        getTelaInifornecedores()

    janela3 = Tk()
    janela3.state("zoomed")

    if tipo == 'I':
        janela3.title("Cadastrar de fornecedores")
    elif tipo == 'A':
        janela3.title("Alterar fornecedores")

    janela3.configure(background='white')

    # variaveis de ajuste de tela
    altMonitor = janela3.winfo_screenheight()
    largMonitor = janela3.winfo_screenwidth()
    larIni = 10
    altMenu = (altMonitor - (altMonitor * 0.99))
    largMenu = (largMonitor - (largMonitor * 0.2))

    # Menus Cadastro

    if tipo == 'I':
        textUsu = Label(janela3, text="Cadastro de fornecedores - Incluir", font="Arial 20 bold", bg="#FFFFFF")
    elif tipo == 'A':
        textUsu = Label(janela3, text="Cadastro de fornecedores - Alterar", font="Arial 20 bold", bg="#FFFFFF")

    textUsu.place(x=larIni, y=altMenu)

    if tipo == 'I':
        btCadastro = Button(janela3, text="Cadastrar", font="Arial 14 bold", bg="#FFFFFF", command=gravaFornecedor)
    elif tipo == 'A':
        btCadastro = Button(janela3, text="Salvar Alteracao", font="Arial 14 bold", bg="#FFFFFF", command=gravaFornecedor)
    btCadastro.place(x=largMenu, y=altMenu)

    menu = Button(janela3, text="Voltar", font="Arial 14 bold", bg="#FFFFFF", command=getTelaInifornecedores)
    menu.place(x=largMenu + 180, y=altMenu)


    altMenu += nEspaco

    #Campo de codigo
    textCp1 = Label(janela3, text="Cod Fornecedor", font="Arial 14 bold", bg="#FFFFFF")
    textCp1.place(x=10, y=altMenu)

    if tipo == 'I':
        getCp1 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp1.insert(0,getCodFornecedor())
        getCp1.config(state="disabled")
        getCp1.place(x=10, y=altMenu + 30)
    elif tipo == 'A':
        getCp1 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=10)
        getCp1.insert(0,valores[0])
        getCp1.config(state="disabled")
        getCp1.place(x=10, y=altMenu + 30)


    #Campo de nome
    textCp2 = Label(janela3, text="Nome Fornecedor", font="Arial 14 bold", bg="#FFFFFF")
    textCp2.place(x=200, y=altMenu)

    if tipo == 'I':
        getCp2 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp2.place(x=200, y=altMenu + 30)
    elif tipo == 'A':
        getCp2 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=60)
        getCp2.insert(0, valores[1])
        getCp2.place(x=200, y=altMenu + 30)

    # Cpf do Fornecedor
    textCp4 = Label(janela3, text="Cpf Fornecedor", font="Arial 14 bold", bg="#FFFFFF")
    textCp4.place(x=900, y=altMenu)
    if tipo == 'I':
        getCp4 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=15)
        getCp4.place(x=900, y=altMenu + 30)
    elif tipo == 'A':
        getCp4 = Entry(janela3, font="Arial 14 bold", bg="#FFFFFF", width=15)
        getCp4.insert(0, valores[3])
        getCp4.place(x=900, y=altMenu + 30)


    #Telefone
    textCp3 = Label(janela3, text="Tel Fornecedor", font="Arial 14 bold", bg="#FFFFFF")
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
    textCp5 = Label(janela3, text="End Fornecedor", font="Arial 14 bold", bg="#FFFFFF")
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