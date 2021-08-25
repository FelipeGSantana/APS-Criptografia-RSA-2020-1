from random import randrange
from secrets import randbits, randbelow
from math import gcd, sqrt, ceil
from tkinter import messagebox
import base64


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------FUNÇÕES AUXILIARES--------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Realiza exponenciações modulares convertendo o expoente em binário
def expo(base, expoente, modulo):

    expoente_bin = list(bin(expoente))
    del(expoente_bin[:2])
    resultado = 1

    for bit in expoente_bin:
        resultado = (resultado ** 2) % modulo
        if bit == "1":
            resultado = (resultado * base) % modulo

    return resultado


# Verifica se um número é primo utilizando o teste de Fermat
# e tirando o MDC entre o número testado e um número gerado aleatóriamente.
# Realiza o teste 100 vezes para diminuir a probabilidade de erro.
def verifica_primos(primo):
    lista_aleatorios = []
    if sqrt(primo) < 101:
        return print("escolha número maior")
    while len(lista_aleatorios) < 101:
        aleatorio = randrange(2, ceil(sqrt(primo)))
        if aleatorio not in lista_aleatorios:
            if gcd(aleatorio, primo) != 1 or expo(aleatorio, primo-1, primo) != 1:
                return False
            lista_aleatorios.append(aleatorio)
    return True


# Funções que codificam e decodificam as saídas/entradas em base64.
def b64_codifica(texto):

    texto_ascii = texto.encode('ascii')
    bytes_base64 = base64.b64encode(texto_ascii)
    texto_base64 = bytes_base64.decode('ascii')
    return texto_base64


def b64_decodifica(texto_base64):

    texto_ascii = texto_base64.encode('ascii')
    texto_bytes = base64.b64decode(texto_ascii)
    texto = texto_bytes.decode('ascii')
    return texto

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------FUNÇÕES PRINCIPAIS--------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def gera_chaves(tamanho):

    # Gera os números primos com a metada do tamanho em bits que a chave pública 1 terá na saida

    while True:
        primo1 = randbits(tamanho//2)
        if verifica_primos(primo1):
            break

    while True:
        primo2 = randbits(tamanho//2)
        if verifica_primos(primo2):
            break

    # Calcula a primeira chave pública e  o Fi dos números primos

    chave_p1 = primo1 * primo2
    phi_aux = (primo1 - 1) * (primo2 - 1)

    # Laço feito até que a chave pública 2 e a chave privada sejam inversos no módulo de phi_aux
    while True:

        # Gera a segunda chave pública
        while True:
            chave_p2 = randbelow((phi_aux - 1))
            if chave_p2 < phi_aux and gcd(chave_p2, phi_aux) == 1:
                break

        # variaveis auxiliares para o algoritmo de Euclides estendido
        quociente = []
        termo_x = [1, 0]
        termo_y = [0, 1]
        euclides_indice = 0
        a = chave_p2
        b = phi_aux

        # Algoritmo de Euclides estendido para calcular o inverso da chave pública 2 no módulo de phi_aux
        while True:

            # Trecho de código que calcula o MDC para obter os quocientes necessário
            quociente.append(a // b)
            resto = a % b
            a = b
            b = resto

            # Este algoritmos só usa os valores que deram resto diferente de zero
            if resto != 0:

                # trecho que calcula os termos que faltam
                termo_x2 = termo_x[euclides_indice] - (quociente[euclides_indice] * termo_x[euclides_indice + 1])
                termo_y2 = termo_y[euclides_indice] - (quociente[euclides_indice] * termo_y[euclides_indice + 1])

                termo_x.append(termo_x2)
                termo_y.append(termo_y2)

                # verifica se a formula já é verdadeira
                if (chave_p2 * termo_x2) + (phi_aux * termo_y2) == gcd(chave_p2, phi_aux):
                    chave_pr = termo_x2
                    break

                euclides_indice += 1

        # Verifica se o termo calculado pelo algoritmo de euclides é valido para os cálculos
        if termo_x2 > 0 and (chave_p2 * chave_pr) % phi_aux == 1:
            # combina o conjunto de chaves necessário para criptografar e descriptografar em uma única string
            chave_publica = str(chave_p1) + " " + str(chave_p2)
            chave_privada = str(chave_p1) + " " + str(chave_pr)

            # Retorna o valor dos conjuntos codificados em base64
            return b64_codifica(chave_publica), b64_codifica(chave_privada)


# Criptografa a mensagem
def criptografar(chave_publica, mensagem):
    try:
        chave_publica = b64_decodifica(chave_publica).split(" ")
        chave_p1 = int(chave_publica[0])
        chave_p2 = int(chave_publica[1])
    except:
        messagebox.showinfo('Erro De Execução', 'Há algum problema com sua chave pública.'
                                                '\nContate o emissor das chaves e verifique se estas estão corretas')
        return
    texto = list(mensagem)
    valor_calculado = []

    for c in texto:
        valor_calculado.append(expo(int(ord(c)), chave_p2, chave_p1))

    texto_criptografado = " ".join(map(str, valor_calculado))

    return b64_codifica(texto_criptografado)


# Descriptografa as mensagens
def descriptografar(chave_privada, mensagem):
    try:
        chaves = b64_decodifica(chave_privada).split(" ")
        chave_p1 = int(chaves[0])
        chave_pr = int(chaves[1])
    except:
        messagebox.showinfo('Erro De Execução', 'Há algum problema com sua chave privada.'
                                                '\nVerifique se ela está codificada em Base64 e tente novamente!')
        return
    try:
        texto = b64_decodifica(mensagem)
        lista_caracteres = texto.split(" ")
        valor_calculado = []
    except:
        messagebox.showinfo('Erro De Execução', 'Há algum problema com sua mensagem.'
                                                '\nVerifique se ela está codificada em Base64 e tente novamente!')
        return

    try:
        for c in lista_caracteres:
            valor_calculado.append(chr(expo(int(c), chave_pr, chave_p1)))
    except:
        messagebox.showinfo('Erro De Execução', 'Há algum problema com sua mensagem ou chave privada.'
                                                '\ncontate o emissor e verifique se a mensagem foi codificada '
                                                'com a chave pública correspondente.')
        return
    texto_descriptografado = "".join(valor_calculado)
    return texto_descriptografado