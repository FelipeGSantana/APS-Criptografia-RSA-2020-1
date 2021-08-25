from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import criptografia_rsa as rsa
from time import time

corFundo = '#272D32'
corCaixa = '#bcc1c4'
corBotao = '#393F46'
corLetras = 'White'
fonte = "-weight bold -size 10"

tela = Tk()
tela.geometry("500x375")
tela.resizable(False, False)
tela.title("Criptografia RSA")
tela.configure(bg=corFundo, bd= 20)

lblcpub = Label(tela, text='Chave Pública', bg=corFundo, font=fonte, foreground=corLetras)
lblcpub.place(x=5, y=0,)
txtcpub = scrolledtext.ScrolledText(tela, width=25, bg=corCaixa, font=fonte)
txtcpub.place(x=8, y=20, height=100)

lblcpriv = Label(tela, text='Chave Privada', bg=corFundo, font=fonte, foreground=corLetras)
lblcpriv.place(x=250, y=0)
txtcpriv = scrolledtext.ScrolledText(tela, width=25, bg=corCaixa, font=fonte)
txtcpriv.place(x=254, y=20, height=100)


def entrada_caracter(event):
    entrada = txtpuro.get('1.0', 'end-1c')
    tamanho = len(entrada)
    restante = 128 - tamanho
    if restante <= 0:
        sobra = 'end-' + str(tamanho - 127)+'c'
        txtpuro.delete(sobra, END)
        lblpuro['text'] = 0
    lblpuro['text'] = restante


lblpuro = Label(tela, text='128', bg=corFundo, font=fonte, foreground=corLetras)
lblpuro.place(x=178, y=175)
lblpuro2 = Label(tela, text='Texto puro                 max:', bg=corFundo, font=fonte, foreground=corLetras)
lblpuro2.place(x=5, y=175)

txtpuro = scrolledtext.ScrolledText(tela, width=25, bg=corCaixa, font=fonte)
txtpuro.place(x=8, y=195, height=100)


txtpuro.bind('<KeyPress>', entrada_caracter)
txtpuro.bind('<KeyRelease>', entrada_caracter)

lblcifrado = Label(tela, text='Texto cifrado', bg=corFundo, font=fonte, foreground=corLetras)
lblcifrado.place(x=250, y=175,)
txtcifrado = scrolledtext.ScrolledText(tela, width=25, bg=corCaixa, font=fonte,)
txtcifrado.place(x=254, y=195, height=100)


def gerar():
    inicio = time()

    txtcpub.delete(1.0, END)
    txtcpriv.delete(1.0, END)
    chaves = rsa.gera_chaves(var.get())

    txtcpub.insert(1.0, chaves[0])
    txtcpriv.insert(1.0, chaves[1])
    fim = time()

    tempo1['text'] = "Gerado em " + str(round(fim - inicio, 3)) + " seg."

def cifrar():

    if len(txtcpub.get('1.0', 'end-1c')) == 0:
        messagebox.showinfo('Erro', 'Preencha a chave pública')
    elif len(txtpuro.get('1.0', 'end-1c')) == 0:
        messagebox.showinfo('Erro', 'Preencha texto puro')
    else:
        inicio = time()
        chave = txtcpub.get(1.0, END).strip()
        cifrado = rsa.criptografar(chave, txtpuro.get(1.0, END))
        txtpuro.delete(1.0, END)
        txtcifrado.delete(1.0, END)
        txtcifrado.insert(1.0, cifrado)
        entrada_caracter('<KeyPress>')
        fim = time()
        tempo2['text'] = "Cifrado em " + str(round(fim - inicio, 3)) + " seg."

def decifrar():
    if len(txtcpriv.get('1.0', 'end-1c')) == 0:
        messagebox.showinfo('Erro', 'Preencha a chave privada')
    elif len(txtcifrado.get('1.0', 'end-1c')) == 0:
        messagebox.showinfo('Erro', 'Preencha texto cifrado')
    else:
        inicio = time()
        chave = txtcpriv.get(1.0, END).strip()
        decifrado = rsa.descriptografar(chave, txtcifrado.get(1.0, END).strip())
        txtcifrado.delete(1.0, END)
        txtpuro.delete(1.0, END)
        txtpuro.insert(1.0, decifrado)
        entrada_caracter('<KeyPress>')
        fim = time()
        tempo2['text'] = "Decifrado em " + str(round(fim - inicio, 3)) + " seg."


btngerar = Button(tela, text='Gerar chaves', command=gerar, cursor='hand2', bg=corBotao, foreground=corLetras, font=fonte)
btngerar.place(x=180, y=125, width=100)

tempo1 = Label(tela, text='', bg=corFundo, font=fonte, foreground=corLetras)
tempo1.place(x=280, y=127)

tempo2 = Label(tela, text='', bg=corFundo, font=fonte, foreground=corLetras)
tempo2.place(x=150, y=305)

var = IntVar()
R1 = Radiobutton(tela, text="512 bits", variable=var, value=512, bg=corFundo, cursor='hand2', font=fonte, foreground=corLetras, selectcolor = corFundo)

R1.place(x=110, y=153, width=80)

R2 = Radiobutton(tela, text="1024 bits", variable=var, value=1024, bg=corFundo, cursor='hand2', font=fonte, foreground=corLetras, selectcolor = corFundo)
R2.place(x=190, y=153, width=80)
R2.select()

R3 = Radiobutton(tela, text="2048 bits", variable=var, value=2048, bg=corFundo, cursor='hand2', font=fonte, foreground=corLetras, selectcolor = corFundo)
R3.place(x=270, y=153, width=80)


btncifrar = Button(tela, text='Cifrar', command=cifrar, cursor='hand2', bg=corBotao, foreground=corLetras, font=fonte)
btncifrar.place(x=65, y=305, width=80)

btndecifrar = Button(tela, text='Decifrar', command=decifrar, cursor='hand2', bg=corBotao, foreground=corLetras, font=fonte)
btndecifrar.place(x=315, y=305, width=80)


tela.mainloop()
