#bibliotecas
from tkinter import *
from tkinter import messagebox

import matplotlib.pyplot as plt
import telaInicial

def showMessage(message, type='info', timeout=2500):
    import tkinter as tk
    from tkinter import messagebox as msgb

    root = tk.Tk()
    root.withdraw()
    try:
        root.after(timeout, root.destroy)
        if type == 'info':
            msgb.showinfo('Info', message, master=root)
        elif type == 'warning':
            msgb.showwarning('Warning', message, master=root)
        elif type == 'error':
            msgb.showerror('Error', message, master=root)
    except:
        pass

def scale(im, nR, nC):
    number_rows = len(im)     # source number of rows
    number_columns = len(im[0])  # source number of columns
    return [[ im[int(number_rows * r / nR)][int(number_columns * c / nC)]
                 for c in range(nC)] for r in range(nR)]

def login():

    if (textoGetSenha.get() == '' and textGetUsu.get() == ''):
        texto = "Usuario e senha não informados"
        #messagebox.showwarning(title='Alerta', message=texto)
        showMessage(texto, type='info', timeout=2000)

    elif (textGetUsu.get() == ''):
        texto = "Usuario não informado"
        #messagebox.showwarning(title='Alerta', message=texto)
        showMessage(texto, type='info', timeout=2000)

    elif (textoGetSenha.get() == ''):
        texto = "Senha não informada"
        #messagebox.showwarning(title='Alerta', message=texto)
        showMessage(texto, type='info', timeout=2000)

    elif ((textoGetSenha.get() != '' and textoGetSenha.get() != 'admin') and (textGetUsu.get() != '' and textGetUsu.get() != 'admin')):
        texto = "Usuario ou senha incorretos"
        #messagebox.showwarning(title='Alerta', message=texto, TimeoutError=4000)
        showMessage(texto, type='info', timeout=2000)

    elif (textGetUsu.get() == 'admin' or textoGetSenha.get() == 'admin'):

        #Destroi a tela de login
        janela.destroy()

        #Chama a tela inicial
        telaInicial.telaInicio()


janela = Tk()
janela.title("Login")
#Seta tela cheia
janela.state("zoomed")

#Variaveis auxiliares
nEspaco = 50

#variaveis de ajuste de tela
altMonitor = janela.winfo_screenheight()
largMonitor = janela.winfo_screenwidth()
altLogin = (altMonitor - (altMonitor*0.4))
largLogin = (largMonitor - (largMonitor*0.7))

janela.configure(background='black')

# Add image file
bg = PhotoImage(file="background/pdv.png")

# Show image using label
label1 = Label(janela, image=bg)
label1.place(x=0, y=0)

#Cp usuario
textUsu = Label(janela, text="Usuario:", font="Arial 30 bold", bg="#FFFFFF")
textUsu.place(x=largLogin,y=altLogin)

#Cp Get Usuario
textGetUsu = Entry(janela, font="Arial 30 bold", bg="#FFFFFF", width=10)
textGetUsu.place(x=largLogin + 180 ,y=altLogin)

altLogin += nEspaco

#Cp senha
textSenha = Label(janela, text="Senha:", font="Arial 30 bold", bg="#FFFFFF")
textSenha.place(x=largLogin,y=altLogin)

#Cp Get Senha
textoGetSenha = Entry(janela, font="Arial 30 bold", bg="#FFFFFF", width=10, show="*")
textoGetSenha.place(x=largLogin + 180 ,y=altLogin)

altLogin += nEspaco

#Bt login
botao = Button(janela, text="Entrar", font="Arial 20 bold", bg="#FFFFFF", command=login)
botao.place(x=largLogin + 180 ,y=altLogin + 20)

janela.mainloop()