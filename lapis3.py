# -*- coding: utf-8 -*-
#modelo 01

#fazere deletar oda lista undo
#fazer o mesmo com os flags

#Importa as bibliotecas que nós usaremos para construir o progrma
from Tkinter import *
from PIL import Image
from PIL import ImageTk
from scipy import ndimage
from matplotlib import pyplot as plt
import tkFileDialog,tkMessageBox
import numpy as np
import FileDialog
import datetime
import argparse
import time 
import copy
import cv2
import ttk
import os

class Janela:

    #Nesta classe construtora criamos os primeiros atributos e os widgets da janela
    def __init__(self, root):
        #semente da biblioteca Tkinter
        self.root = root
        self.imgmostrando = None
        self.imagem= None
        w, h = raiz.winfo_screenwidth()-3, raiz.winfo_screenheight()-3#pega o tamanho da tela
        self.larg = w
        self.alt = h
        if self.larg > 1920 or self.alt > 1800:
            tkMessageBox.showerror("Error", "Unsupported screen size!")
            self.sai()
        #Além destes, criamos mais alguns atributos durante a continuidade do codigo

        ###MENU###
        #Cria os botões da barra de menu superior
        
        menu = Menu(root) #cria a barra de menu
        root.config(menu=menu)

        
        self.filemenu = Menu(menu) #cria o menu self.filemenu
        menu.add_cascade(label="File", menu=self.filemenu)#Associa o botão sel.filemenu à barra de menu e coloca o titulo de File
        #Adiciona as funções da seguinte forma:
        #botãoprincipal.add_comad(label = titulodobotão, command = função que sera chamada
        self.filemenu.add_command (label ="New file", command = lambda: arquivo.newfile())
        self.filemenu.add_command (label ="Open...", command = lambda: arquivo.importar())
        self.filemenu.add_separator()#separado entre os comandos
        self.filemenu.add_command (label ="Save", command = lambda: arquivo.save())
        self.filemenu.add_command (label ="Save as", command = lambda: arquivo.saveas())
        self.filemenu.add_separator()#separado entre os comandos
        self.filemenu.add_command (label ="Exit", command = self.sai)


        filtermenu = Menu(menu)#cria o menu filtersmenu
        menu.add_cascade(label="Filter", menu=filtermenu) #Associa o botão filtermenu à barra de menu e coloca o titulo de Filters
        #Adiciona os elementos do menu Filters
        filtermenu.add_command(label="Canny", command= lambda: filtrosb.canny())
        filtermenu.add_command(label="Roberts", command= lambda: filtrosb.roberts())
        filtermenu.add_command(label="Sobel X", command= lambda: auxiliar.auxsobelx())
        filtermenu.add_command(label="Sobel Y", command= lambda: auxiliar.auxsobely())
        filtermenu.add_command(label="Sobel", command= lambda: auxiliar.auxsobel())
        filtermenu.add_command(label="Prewitt", command= lambda: filtrosb.prewitt())


        videomenu = Menu(menu)#cria o menu opmenu
        menu.add_cascade(label="Video", menu=videomenu)#Associa o botão opmenu à barra de menu e coloca o titulo de Options
        #Adiciona os elementos do menu Options
        videomenu.add_command(label="Frame capture", command= lambda: arquivo.videotoimage())
        videomenu.add_command(label="Stop frame capture", command= lambda: arquivo.stopvti())
        videomenu.add_separator()
        videomenu.add_command(label="Options", command=lambda: configuracao.conf())

        

        personalizedmenu = Menu(menu)#cria o menu personalizedsmenu
        menu.add_cascade(label="Personalized", menu=personalizedmenu)#Associa o botão filtermenu à barra de menu e coloca o titulo de Personalized
        #Adiciona os elementos do menu Personalized
        personalizedmenu.add_command(label="Process sequence", command= lambda: ferramentas.sequence())


        editmenu = Menu(menu)#cria o menu helpmenu
        menu.add_cascade(label="Edit", menu=editmenu)#Associa o botão Helpmenu à barra de menu e coloca o titulo de Help
        #Adiciona os elementos do menu Help
        editmenu.add_command(label="Undo", command= lambda: ferramentas.undo())


        helpmenu = Menu(menu)#cria o menu helpmenu
        menu.add_cascade(label="Help", menu=helpmenu)#Associa o botão Helpmenu à barra de menu e coloca o titulo de Help
        #Adiciona os elementos do menu Help
        helpmenu.add_command(label="Help", command= lambda: informacao.helpi())
        helpmenu.add_command(label="About...", command= lambda: informacao.About())

        

        ###BOTOES###
        #Cria os botões da barra lateral

        icodirectory = (os.getcwd() + '/icones/') #pega o diretorio onde estao os icones

        #Botão undo
        #pega o icone do botão
        altb = 40
        largb = 50
        processicon = Image.open( icodirectory+'undo1.png')
        altb, largb, processicon = self.icones(altb, largb, processicon)
        #cria e configura o botão, associando ele ao método undo da classe ferramentas
        self.processb= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: ferramentas.undo())
        self.processb["bg"] = "#dcd9d8" #configura a cor do botão
        #adiciona o icone ao botão
        self.processb.config(image=processicon)
        self.processb.image = processicon
        self.processb.grid (row = 0, column = 0, padx = 1, sticky = W)#posiciona o botão

        #Botão Import
        importicon = Image.open ( icodirectory +"import2.png")
        altb = 40
        largb = 50
        altb, largb, importicon = self.icones(altb, largb, importicon)
        self.importb= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: arquivo.importar())#criae configura o botão, associando ele ao método importar
        self.importb["bg"] = "#dcd9d8"
        self.importb.config(image=importicon)
        self.importb.image = importicon
        self.importb.grid (row = 2, column = 0, padx = 1, sticky = W)

        #Botão Draw
        lapisicon = Image.open ( icodirectory + "desenha3.png")
        altb = 40
        largb = 50
        altb, largb, lapisicon = self.icones(altb, largb, lapisicon)
        self.desenhab= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: ferramentas.desenha())#criae configura o botão, associando ele ao método "desenha"
        self.desenhab["bg"] = "#dcd9d8"
        self.desenhab.config(image=lapisicon)
        self.desenhab.image = lapisicon
        self.desenhab.grid (row = 3, column = 0, padx = 1, sticky = W)

        #Botão Crop
        cortaricon = Image.open ( icodirectory + "cortar2.png")
        altb = 40
        largb = 50
        altb, largb, cortaricon = self.icones(altb, largb, cortaricon)
        self.cortarb= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: ferramentas.corta())#cria e configura o botão, associando ele ao método "corta"
        self.cortarb["bg"] = "#dcd9d8"
        self.cortarb.config(image=cortaricon)
        self.cortarb.image = cortaricon
        self.cortarb.grid (row = 4, column = 0, padx = 1, sticky = W)
        
        #Botão Grayscale
        f1icon = Image.open ( icodirectory + "filtro1.png")
        altb = 40
        largb = 50
        altb, largb, f1icon = self.icones(altb, largb, f1icon)
        self.f1b= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: filtrosg.gray())#cria e configura o botão, associando ele ao método "filtro1"
        self.f1b["bg"] = "#dcd9d8"
        self.f1b.config(image=f1icon)
        self.f1b.image = f1icon
        self.f1b.grid (row = 5, column = 0, padx = 1, sticky = W)
        
        #Botão Gamma
        f2icon = Image.open ( icodirectory + "filtro22.png")
        altb = 40
        largb = 50
        altb, largb, f2icon = self.icones(altb, largb, f2icon)
        self.f2b= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: filtrosg.gamma(0))#cria e configura o botão, associando ele ao método "filtro2"
        self.f2b["bg"] = "#dcd9d8"
        self.f2b.config(image=f2icon)
        self.f2b.image = f2icon
        self.f2b.grid (row = 6, column = 0, padx = 1, sticky = W)

        #Botão de Menu edgedetection
        f3icon = Image.open ( icodirectory + "filtro3.png")
        altb = 40
        largb = 54
        altb, largb, f3icon = self.icones(altb, largb, f3icon)
        #Cria e configura como botão de menu
        self.f3b= Menubutton (self.root, height = altb, width = largb, relief = 'flat')
        self.f3b["bg"] = "#dcd9d8"#configura cor de fundo
        #Adiciona o Icone
        self.f3b.config(image=f3icon)
        self.f3b.image = f3icon
        self.f3b.grid (row = 7, column = 0, padx = 1, sticky = W)#posiciona o menu
        #configura menu
        self.f3b.menu= Menu(self.f3b, tearoff=0)
        self.f3b ['menu'] = self.f3b.menu
        #adiciona elementos ao botão de menu
        self.f3b.menu.add_command(label="Canny", command= lambda: filtrosb.canny())#nomeia e associa este elemento ao método "canny"
        self.f3b.menu.add_command(label="Roberts", command= lambda: filtrosb.roberts())#nomeia e associa este elemento ao método "roberts"
        self.f3b.menu.add_command(label="Sobel X", command= lambda: auxiliar.auxsobelx())#nomeia e associa este elemento ao método "sobelx"
        self.f3b.menu.add_command(label="Sobel Y", command= lambda: auxiliar.auxsobely())#nomeia e associa este elemento ao método "sobely"
        self.f3b.menu.add_command(label="Sobel", command= lambda: auxiliar.auxsobel())#nomeia e associa este elemento ao método "sobel"
        self.f3b.menu.add_command(label="Prewitt", command= lambda: filtrosb.prewitt())#nomeia e associa este elemento ao método "prewitt"

        #Botão de threshold
        threshicon = Image.open ( icodirectory + "binery3.png")
        altb = 40
        largb = 50
        altb, largb, threshicon = self.icones(altb, largb, threshicon)
        self.threshb= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: auxiliar.auxthresh())#cria e configura o botão, associando ele ao método "thresh"
        self.threshb["bg"] = "#dcd9d8"
        self.threshb.config(image=threshicon)
        self.threshb.image = threshicon
        self.threshb.grid (row = 8, column = 0, padx = 1, sticky = W)

        #Botão invert
        inverticon = Image.open ( icodirectory + "invert2.png")
        altb = 40
        largb = 50
        altb, largb, inverticon = self.icones(altb, largb, inverticon)
        self.invertb= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: filtrosg.invert())#cria e configura o botão, associando ele ao método "invert"
        self.invertb["bg"] = "#dcd9d8"
        self.invertb.config(image=inverticon)
        self.invertb.image = inverticon
        self.invertb.grid (row = 9, column = 0, padx = 1, sticky = W)

        #Botão zoom in
        zoominicon = Image.open ( icodirectory + "zoomi.png")
        altb = 40
        largb = 50
        altb, largb, zoominicon = self.icones(altb, largb, zoominicon)
        self.zoominb= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: ferramentas.zoomin())#cria e configura o botão, associando ele ao método "zoomin"
        self.zoominb["bg"] = "#dcd9d8"
        self.zoominb.config(image=zoominicon)
        self.zoominb.image = zoominicon
        self.zoominb.grid (row = 10, column = 0, padx = 1, sticky = W)

        #Botão zoom out
        zoomouticon = Image.open ( icodirectory + "zoomo.png")
        altb = 40
        largb = 50
        altb, largb, zoomouticon = self.icones(altb, largb, zoomouticon)
        self.zoomoutb= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: ferramentas.zoomout())#cria e configura o botão, associando ele ao método "zoomout"
        self.zoomoutb["bg"] = "#dcd9d8"
        self.zoomoutb.config(image=zoomouticon)
        self.zoomoutb.image = zoomouticon
        self.zoomoutb.grid (row = 11, column = 0, padx = 1, sticky = W)

        #Botão play
        playicon = Image.open ( icodirectory + "play.png")
        altb = 40
        largb = 50
        altb, largb, playicon = self.icones(altb, largb, playicon)
        self.playb= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: auxiliar.auxplay())#cria e configura o botão, associando ele ao método "play"
        self.playb["bg"] = "#dcd9d8"
        self.playb.config(image=playicon)
        self.playb.image = playicon
        self.playb.grid (row = 13, column = 0, padx = 1, sticky = W)

        #Botão pause
        pauseicon = Image.open ( icodirectory + "pause.png")
        altb = 40
        largb = 50
        altb, largb, pauseicon = self.icones(altb, largb, pauseicon)
        self.pauseb= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: arquivo.pause())#cria e configura o botão, associando ele ao método "pause"
        self.pauseb["bg"] = "#dcd9d8"
        self.pauseb.config(image=pauseicon)
        self.pauseb.image = pauseicon
        self.pauseb.grid (row = 14, column = 0, padx = 1, sticky = W)

        #Botão Do
        doicon = Image.open ( icodirectory + "do2.png")
        altb = 40
        largb = 50
        altb, largb, doicon = self.icones(altb, largb, doicon)
        self.dob= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: ferramentas.do())#cria e configura o botão, associando ele ao método "do"
        self.dob["bg"] = "#dcd9d8"
        self.dob.config(image=doicon)
        self.dob.image = doicon
        self.dob.grid (row = 16, column = 0, padx = 1, sticky = W)

        #Botão Microscopio
        microicon = Image.open ( icodirectory + "microsp.png")
        altb = 40
        largb = 50
        altb, largb, microicon = self.icones(altb, largb, microicon)
        self.microb= Button (self.root, height = altb, width = largb, relief = 'flat', command = lambda: video.micro())#cria e configura o botão, associando ele ao método "micro"
        self.microb["bg"] = "#dcd9d8"
        self.microb.config(image=microicon)
        self.microb.image = microicon
        self.microb.grid (row = 18, column = 0, padx = 1, sticky = W)


        ###LABEL###
        #Cria outros elementos que visam uma melhor experiência com o programa e a área onde será mostrada à imagem

        #separador entre o botão process e o botão import
        separa = Image.open ( icodirectory + "separa6.png")#carrega a imgem do separador
        altb = 15
        largb = 54
        altb, largb, separa = self.icones(altb, largb, separa)
        self.separa = Label(root, width = largb, height = altb, bg = '#dcd9d8')#cria e configura um label, que será o separador
        #carrega a imagem do separador
        self.separa.configure(image=separa)
        self.separa.image = separa
        self.separa.grid (row = 12, column = 0, padx = 1, sticky= W)#posiciona o separador

        #separador entre o botão zoom out e play
        self.separa2 = Label(root,width = largb, height = altb, bg = '#dcd9d8')
        self.separa2.configure(image=separa)
        self.separa2.image = separa
        self.separa2.grid (row = 1, column = 0, padx = 1, sticky= W)

        #separador entre o botão pause e Do
        self.separa3 = Label(root, width = largb, height = altb, bg = '#dcd9d8')
        self.separa3.configure(image=separa)
        self.separa3.image = separa
        self.separa3.grid (row = 15, column = 0, padx = 1, sticky= W)

        #separador entre o botão DO e Micro
        self.separa4 = Label(root, width = largb, height = altb, bg = '#dcd9d8')
        self.separa4.configure(image=separa)
        self.separa4.image = separa
        self.separa4.grid (row = 17, column = 0, padx = 1, sticky= W)

        #Framer vazio, cujo propósito é apenas completar a barra lateral esquerda, para que ela ocupe toda à coluna
        altb = 235
        largb = 56
        altb, largb, fundo = self.icones(altb, largb, None)
        self.completa = Frame (root, bg = "#dcd9d8",height = altb, width = largb)#cria e configura o frame self.completa
        self.completa.grid (row = 19, column = 0, padx = 1, sticky = W)#posiona o self.completa


        #label vazio, cujo propósito é apenas completar a barra lateral esquerda, para que ela ocupe toda à coluna
        altb = 51
        largb = 13
        altb, largb, fundo = self.icones(altb, largb, None)
        self.completa2 = Label (root, bg = "#dcd9d8",height = altb, width = largb)#cria e configura o label self.completa2
        self.completa2.grid (row = 20, column = 0, sticky = W)#posiona o self.completa

        #label cujo propósito é exibir informações formando uma barra a baixo
        altb = 51
        largb = 21
        altb, largb, fundo = self.icones(altb, largb, None)
        self.info = Label (root, bg = "#dcd9d8",anchor = 'nw', height = altb, width = largb)#cria e configura o label self.info
        self.info.grid (row = 20, column = 1, sticky = W + E)#posiona o self.info

        #label vazio, cujo propósito é apenas completar a barra de informaçõe para que ela ocupe toda à linha
        altb = 51
        largb = 200
        altb, largb, fundo = self.icones(altb, largb, None)
        self.info2 = Label (root, bg = "#dcd9d8",height = altb, width = largb)#cria e configura o label self.info2
        self.info2.grid (row = 20, column = 2, columnspan = 2, sticky = W + E)#posiona o self.info2

        #cria um label que será a área em que será é colocada a imagem
        fundo = Image.open ( icodirectory + "box.gif")#carrega uma imagem totalmente branca, que funciona como um plano de fndo inicial
        altb = 950
        largb = 1710
        altb, largb, fundo = self.icones(altb, largb, fundo)
        self.set_fundospecifi(altb, largb)
        self.fundo = Label(root, width = largb, height = altb, bg = 'white')#cria e configura este label
        #carrega a imagem no label
        self.fundo.configure(image=fundo)
        self.fundo.image = fundo
        self.fundo.grid (row = 0, column = 1, pady = 10, padx = 10, rowspan = 20, sticky= N)#posiciona o label

    def mostrar (self, imagem):
            self.imagem = imagem#self.imagem recebe a imagem que foi passada como argumeto
            self.imgmostrando = imagem#self.imgmostrando recebe a imagem que foi passada como argumeto
            #a imagem em self.imagem é convertida para um formato que a biblioteca Pillow suporte
            self.imagem = Image.fromarray(self.imagem)
            #img = self.imagem
            #imagem.set_imgpil(img)#self_imgpil é setada para conter a imagem no "formato Pillow"
            pilimage = ImageTk.PhotoImage(self.imagem)
            #o label de fundo recebe a imagem selecionada
            self.fundo.configure(image=pilimage)
            self.fundo.image = pilimage

    def showinfo(self, txt):
        self.info['text'] = txt

    def icones(self, altico, largico, img):#nesta classe definimos o tamanho dos icones de acordo com o tamanho da tela
        #define a nova altura e largura do icone
        novaalt = int((altico*self.alt)/1080)
        novalarg = int((largico*self.larg)/1920)
        #se ouver uma imagem no icone ela tambem é redimenssionada 
        if img != None:
            img = img.resize((novalarg, novaalt), Image.ANTIALIAS)
            img2 = ImageTk.PhotoImage(img)
        else:
            img2 = None 
        return [novaalt, novalarg, img2]

    def set_fundospecifi(self, specalt, speclarg):
        self.specalt = specalt
        self.speclarg = speclarg
    def get_fundospecifi(self):
        return (self.specalt, self.speclarg)


    def sai (self):
            self.root.destroy()#destroi a jenela que está sendo exibida

    

class image(object):
    def __init__(self):
        #biblioteca nomeada de flag, utlizada para termos um maior controle dos eventos do programa
        self._flag = { 'img': 0, 'gray': 0, 'f1':0, 'f2': 0, 'f3' : 0, 'canny' : 0, 'roberts': 0, 'sobelx': 0 , 'sobely': 0, 'sobel': 0, 'prewitt': 0, 'process': 0, 'draw': 0, 'undo' :0, 'crop': 0}
        self._imgcv = None

    #metodos para pegar e alterar a imagem no formato compativel com as funções Opencv
    def set_imgcv (self, imgcv):
        self._imgcv = imgcv
    def get_imgcv (self):
        return self._imgcv
    #metodos para pegar e alterar a imagem anterior(para o metodo Undo)
    def set_imganterior(self, imganterior):
        self._imganterior = imganterior
        auxiliar.organiza_imganterior(imganterior)
        self._flag['undo'] = 1
    def get_imganteior (self):
        return self._imganterior
    #metodos para pegar e alterar a imagem no formato compativel com as funções Pillow
    def set_imgpil(self, imgpil):
        self._imgpil = imgpil
    def get_imgpil(self):
        return self._imgpil
    #metodos para pegar e alterar a biblioteca de flags
    def set_flag ( self, flag):
        self._flag = flag
    def get_flag (self):
        return self._flag
    #metodos para pegar e alterar a biblioteca de flag anterior(utilizado no método Undo)
    def set_flaganterior(self, flaganterior):
        self._flaganterior = flaganterior
        auxiliar.organiza_flaganterior(flaganterior)
    def get_flaganterior (self):
        return self._flaganterior



class ediction(object):#cria a classe ediction que é uma classe abstrata e esta será a classe base para as demais classes reponsáveis por editar a imagem
    def __init__(self):
        pass



class borderfilters(ediction):#classe derivada da classe edction responsável pelos filtros de borda 
    def canny (self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:
            image = imagem.get_imgcv()#image recebe a imagem no formato compativel com as funções do Opencv
            #fazemos uma cópia da imagem que é "recebida" pelo método e usamos ela como a imagem anterior, para, se necessário, ser usada pelo método undo da classe Janela
            imcv = copy.deepcopy (image)
            imagem.set_imganterior(imcv)
            #fazemos uma cópia do dicionario de flags que é recebido e utilizamos ele como flag anterior, para ser usado no método Undo
            flg = copy.deepcopy(flag)
            imagem.set_flaganterior(flg)
            #verifica se a image já esta em preto e branco ou escala de cinza, caso não esteja ela é convertida para escala de cinza antes de ser processada
            ver = auxiliar.verifica_cor(image)
            if ver == 0 and  flag ['gray'] == 0:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                flag ['gray'] = 1
            edged = cv2.Canny(image, 50, 100)#através de uma função do Opencv a imagem passa pelo filtro de detecção de borda, e a nova imagem é ligada à edged
            #os flags são "setados"
            flag ['canny'] = 1
            #imgcv recebe a imagem editada, após ela ser convertida novamente para o "formato Opencv"
            imgv = np.asarray(edged)
            imagem.set_imgcv(imgv)
            janela.mostrar (edged)#chamamos o método mostrar da classe janela para exibir a imagem editada na área de trabalho
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")



    def roberts (self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:
            #Estabelecemos os parametros que serão utilizados( Nil )
            roberts_cross_v = np.array( [[ 0, 0, 0 ],
                                         [ 0, 1, 0 ],
                                         [ 0, 0,-1 ]] )

            roberts_cross_h = np.array( [[ 0, 0, 0 ],
                                         [ 0, 0, 1 ],
                                         [ 0,-1, 0 ]] )
            img = imagem.get_imgcv()
            #fazemos uma cópia da imagem que é "recebida" pelo método e usamos ela como a imagem anterior, para, se necessário, ser usada pelo método undo 
            imcv = copy.deepcopy (img)
            imagem.set_imganterior(imcv)
            #fazemos uma cópia do dicionario de flags que é recebido e utilizamos ele como flag anterior, para ser usado no método Undo
            flg = copy.deepcopy(flag)
            imagem.set_flaganterior(flg)
            #verifica se a image já esta em preto e branco ou escala de cinza, caso não esteja ela é convertida para escala de cinza antes de ser processada
            ver = auxiliar.verifica_cor(img)
            if ver == 0 and  flag ['gray'] == 0:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                flag ['gray'] = 1
            image = np.asarray( img, dtype="int32" )#converte a imagem
            #a edição da imagem é feita em quatro etapas, utilizando funções da biblioteca scypi e numpy
            vertical = ndimage.convolve( image, roberts_cross_v )#fazemo a edição no eixo vertical da imagem utilizando uma função da biblioteca scypi e utilizamos os parametros anteriormente definidos
            horizontal = ndimage.convolve( image, roberts_cross_h )#fazemo a edição no eixo horizontal da imagem utilizando uma função da biblioteca scypi e utilizamos os parametros anteriormente definidos
            outimg1 = np.sqrt( np.square(horizontal) + np.square(vertical))#"fundimos" as duas edições, ou seja, basicamente fazemos horizontal + vertical 
            outimg2 = Image.fromarray( np.asarray( np.clip(outimg1,0,255), dtype="uint8"), "L" )#a imagem passa pela ultima etapa de edição e o "produto final" é colocado em outimg2 
            flag ['roberts'] = 1#seta o flag "roberts"
            imagem.set_flag(flag)
            #imgv recebe a imagem editada, após ela ser convertida novamente para um formato compativel com as funções da biblioteca Opencv
            imgv = np.asarray(outimg2)
            imagem.set_imgcv(imgv)#self._imgcv é setado com a imagem editada
            janela.mostrar (imgv)#chamamos o método mostrar da classe janela para exibir a imagem editada na área de trabalho                            
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")



    def sobelx (self, k):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:
            #prepara a imagem para edição, ou seja, image recebe a imagem para a edição, é feita uma copia da imagem recebida para self.imganterior e verifica se é necessário converter para escala de cinza
            image = imagem.get_imgcv()
            imcv = copy.deepcopy (image)
            imagem.set_imganterior(imcv)
            #fazemos uma cópia do dicionario de flags que é recebido e utilizamos ele como flag anterior, para ser usado no método Undo
            flg = copy.deepcopy(flag)
            imagem.set_flaganterior(flg)
            ver = auxiliar.verifica_cor(image)
            if ver == 0 and  flag ['gray'] == 0:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image2 = gray
                flag ['gray'] = 1
            else:
                image2 = image
            img_gaussian = cv2.GaussianBlur(image2,(3,3),0)#a imagem passa por um filtro inical, utilizando uma função Opencv    
            img_sobelx = cv2.Sobel(img_gaussian,cv2.CV_8U,1,0,ksize=k)#a imagem é editada utilizando uma função do Opencv e o valor definido anteriormente para o kernel é utilizado
            flag ['sobelx']= 1#o flag "sobelx" é setado
            imagem.set_flag(flag)
            #imgv recebe a imagem editada, após ela ser convertida novamente para um formato compativel com as funções da biblioteca Opencv
            imgv = np.asarray(img_sobelx)
            imagem.set_imgcv(imgv)#self._imgcv é setado com a imagem editada
            janela.mostrar (imgv)#chamamos o método mostrar da classe janela para exibir a imagem editada na área de trabalho
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")



    def sobely (self, k):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:
            #prepara a imagem para edição, ou seja, image recebe a imagem para a edição, é feita uma copia da imagem recebida para self.imganterior e verifica se é necessário converter para escala de cinza
            image = imagem.get_imgcv()
            imcv = copy.deepcopy (image)
            imagem.set_imganterior(imcv)
            #fazemos uma cópia do dicionario de flags que é recebido e utilizamos ele como flag anterior, para ser usado no método Undo
            flg = copy.deepcopy(flag)
            imagem.set_flaganterior(flg)
            ver = auxiliar.verifica_cor(image)
            if ver == 0 and  flag ['gray'] == 0:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image2 = gray
                flag ['gray'] = 1
            else:
                image2 = image
            img_gaussian = cv2.GaussianBlur(image2,(3,3),0)#a imagem passa por um filtro inical, utilizando uma função Opencv               
            img_sobely = cv2.Sobel(img_gaussian,cv2.CV_8U,0,1,ksize=k)#a imagem é editada utilizando uma função do Opencv e o valor definido anteriormente para o kernel é utilizado
            flag ['sobely']= 1 #o flag "sobely" é setado
            imagem.set_flag(flag)
            #imgv recebe a imagem editada, após ela ser convertida novamente para um formato compativel com as funções da biblioteca Opencv
            imgv = np.asarray(img_sobely)
            imagem.set_imgcv(imgv)#self._imgcv é setado com a imagem editada
            janela.mostrar (imgv)#chamamos o método mostrar da classe janela para exibir a imagem editada na área de trabalho

        else:
            tkMessageBox.showerror("Error", "Please import an image first!")



    def sobel (self, k):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:
            #prepara a imagem para edição, ou seja, image recebe a imagem para a edição, é feita uma copia da imagem recebida para self.imganterior e verifica se é necessário converter para escala de cinza
            image = imagem.get_imgcv()
            imcv = copy.deepcopy (image)
            imagem.set_imganterior(imcv)
            #fazemos uma cópia do dicionario de flags que é recebido e utilizamos ele como flag anterior, para ser usado no método Undo
            flg = copy.deepcopy(flag)
            imagem.set_flaganterior(flg)
            ver = auxiliar.verifica_cor(image)
            if ver == 0 and  flag ['gray'] == 0:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image2 = gray
                flag ['gray'] = 1
            else:
                image2 = image
            img_gaussian = cv2.GaussianBlur(image2,(3,3),0)#a imagem passa por um filtro inical, utilizando uma função Opencv
            #a imagem passa pelo filtro sobel x(eixo horizontal) e sobel y(eixo vertical) e após isso o resultado dos dois é somado para resultar na imagem em sobel 
            img_sobelx = cv2.Sobel(img_gaussian,cv2.CV_8U,1,0,ksize=k)
            img_sobely = cv2.Sobel(img_gaussian,cv2.CV_8U,0,1,ksize=k)
            img_sobel = img_sobelx + img_sobely
            flag ['sobel']= 1
            imagem.set_flag(flag)
            #imgv recebe a imagem editada, após ela ser convertida novamente para um formato compativel com as funções da biblioteca Opencv
            imgv = np.asarray(img_sobel)
            imagem.set_imgcv(imgv)#self._imgcv é setado com a imagem editada
            janela.mostrar (imgv)#chamamos o método mostrar da classe janela para exibir a imagem editada na área de trabalho            
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")

    def prewitt (self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:
            #fazemos uma cópia do dicionario de flags que é recebido e utilizamos ele como flag anterior, para ser usado no método Undo
            flg = copy.deepcopy(flag)
            imagem.set_flaganterior(flg)
            #prepara a imagem para edição, ou seja, image recebe a imagem para a edição, é feita uma copia da imagem recebida para self.imganterior e verifica se é necessário converter para escala de cinza
            image = imagem.get_imgcv()
            imcv = copy.deepcopy (image)
            imagem.set_imganterior(imcv)
            ver = auxiliar.verifica_cor(image)
            if ver == 0 and  flag ['gray'] == 0:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image2 = gray
                flag ['gray'] = 1
            else:
                image2 = image
            img_gaussian = cv2.GaussianBlur(image2,(3,3),0)#a imagem passa por um filtro inicial
            #define o kernel do eixo x e y
            kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
            kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
            #a imagem passa pelo filtro prewitt x(eixo horizontal) e prewitt y(eixo vertical) e após isso o resultado dos dois é somado para resultar na imagem em prewitt
            img_prewittx = cv2.filter2D(img_gaussian, -1, kernelx)
            img_prewitty = cv2.filter2D(img_gaussian, -1, kernely)
            img =  img_prewittx + img_prewitty
            flag ['prewitt'] = 1
            imagem.set_flag(flag)
            #imgv recebe a imagem editada, após ela ser convertida novamente para um formato compativel com as funções da biblioteca Opencv
            imgv = np.asarray(img)
            imagem.set_imgcv(imgv)#self._imgcv é setado com a imagem editada
            janela.mostrar (imgv)#chamamos o método mostrar da classe janela para exibir a imagem editada na área de trabalho
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")
            


class generalfilters(ediction):#classe derivada de edction, responsável pelos demais filtros
    def thresh (self, vmin, vmax):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:
            #fazemos uma cópia do dicionario de flags que é recebido e utilizamos ele como flag anterior, para ser usado no método Undo
            flg = copy.deepcopy(flag)
            imagem.set_flaganterior(flg)
            #prepara a imagem para edição, ou seja, image recebe a imagem para a edição, é feita uma copia da imagem recebida para self.imganterior e verifica se é necessário converter para escala de cinza
            image = imagem.get_imgcv()
            imcv = copy.deepcopy (image)
            imagem.set_imganterior(imcv)
            ver = auxiliar.verifica_cor(image)
            if ver == 0 and  flag ['draw'] == 0 and flag ['process'] == 0 and flag ['gray'] == 0:
                try:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                except TypeError:
                    pass
            img = np.zeros((1,400,3), np.uint8)
            #verifica se os valores definidos pelo usuário são válidos
            if vmin > vmax:
                tkMessageBox.showerror("Error", "Minimum value cant be bigger than maximum value!")
            else:
                ret,thresh1 = cv2.threshold(image,vmin,vmax,cv2.THRESH_BINARY)#através de uma função do Opencv a edição é realizada, sendo que a imagem é "colocada" em thresh1 
                #imgv recebe a imagem editada, após ela ser convertida novamente para um formato compativel com as funções da biblioteca Opencv
                imgv = np.asarray(thresh1)
                imagem.set_imgcv(imgv)#self._imgcv é setado com a imagem editada
                janela.mostrar (imgv)#chamamos o método mostrar da classe janela para exibir a imagem editada na área de trabalho
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")

    def invert (self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:
            image = imagem.get_imgcv()#image recebe a imagem em um formato compativel com as funções do Opencv
            #fazemos uma cópia da imagem que é "recebida" pelo método e usamos ela como a imagem anterior, para, se necessário, ser usada pelo método undo da classe Janela
            imcv = copy.deepcopy (image)
            imagem.set_imganterior(imcv)
            img = (255-image)#invertemos o espectro da imagem
            #imgv recebe a imagem editada, após ela ser convertida novamente para um formato compativel com as funções da biblioteca Opencv
            imgv = np.asarray(img)
            imagem.set_imgcv(imgv)#self._imgcv é setado com a imagem editada
            janela.mostrar (imgv)#chamamos o método mostrar da classe janela para exibir a imagem editada na área de trabalho
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")

    def gray(self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:
                image = imagem.get_imgcv()#image recebe a imagem compativel com as funções do Opencv
                ver = auxiliar.verifica_cor(image)#chama este método para verificar se a imagem é preto e branco
                #verifica se a imagem possui cores que permitem que ela seja convertida em escala de cinza
                if ver == 1 or flag ['draw'] == 1 and flag ['process'] == 1 or flag ['process'] == 1 or flag['gray'] == 1:
                    tkMessageBox.showerror("Error", "You can't convert to a grayscale!")
                else:#se for possivel converter:
                    #fazemos uma cópia da imagem que é "recebida" pelo método e usamos ela como a imagem anterior, para, se necessário, ser usada pelo método undo da classe Janela
                    imcv = copy.deepcopy (image)
                    imagem.set_imganterior(imcv)
                    #fazemos uma cópia do dicionario de flags que é recebido e utilizamos ele como flag anterior, para ser usado no método Undo
                    flg = copy.deepcopy(flag)
                    imagem.set_flaganterior(flg)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#utilizando uma função do Opencv convertemos a imagem para a escala de cinza
                    #_imgcv recebe a imagem editada, após ela ser convertida novamente para um formato compativel com as funções da biblioteca Opencv
                    imagem.set_imgcv(gray)
                    janela.mostrar (gray)#chamamos o método mostrar da classe janela para exibir a imagem editada na área de trabalho
                    flag ['gray'] = 1#"setamos" o flag gray
                    flag ['f1'] = 1#"setamos" o flag para o filtro 1
                    imagem.set_flag(flag)
                    janela.mostrar (gray)#chama o método mostrar da classe janela, para mostrar a imagem editada na área de trabalho
                
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")



    def gamma(self, ke):
        def adjust_gamma( image, gamma=1.0): #( Nil)
                    invGamma = 1.0 / gamma
                    table = np.array([((i / 255.0) ** invGamma) * 255
                                      for i in np.arange(0, 256)]).astype("uint8")
                    return cv2.LUT(image, table)
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:
            if flag ['process'] == 1:
                tkMessageBox.showerror("Error", "It is not possible make this change !")
            else:
                original = imagem.get_imgcv()#original recebe a imagem compativel com as funções do Opencv
                #fazemos uma cópia da imagem que é "recebida" pelo método e usamos ela como a imagem anterior, para, se necessário, ser usada pelo método undo da classe Janela
                imcv = copy.deepcopy (original)
                imagem.set_imganterior(imcv)
                if ke == 0:#se ke for zero signica que o usuário ainda não selecionou o valor do gamma
                    def nothing(x):
                        pass
                    tkMessageBox.showinfo("Notice", "Press 'esc' to go out and 'space' to save the chage")#mensagem explicando como utilizar a filtro
                    cv2.namedWindow('Images')#cria uma janela do opencv onde o usuário selecionará o gamma
                    cv2.createTrackbar('Gamma','Images',0,5, nothing)#cria um trackbar para selecionar o valr do gamma
                    while (1):
                        #recebe a posição da trackbar, e seleciona ao valor de gamma correspondente
                        s = cv2.getTrackbarPos('Gamma','Images')
                        if s == 0:
                            gamma = 0.5
                        elif s == 1:
                            gamma = 1.0 
                        elif s == 2:
                            gamma =1.5 
                        elif s == 3:
                            gamma =2.0 
                        elif s == 4:
                            gamma = 2.5 
                        elif s == 5:
                            gamma = 3.0

                        adjusted = adjust_gamma(original, gamma)#chama o método responsável por fazer a edição da imagem e passa a imagem e o valor de gamma selecionado como argumento, e adjusted recebe a imagem editada 
                        ver = auxiliar.verifica_cor(adjusted)#verifica se a imagem é preto e branco
                        if ver == 0 and flag['gray'] == 0 and flag['canny']==0 and flag['roberts']==0 and flag['prewitt']==0 and flag['sobel']==0 and flag['sobelx']==0 and flag['sobely']==0:
                            exibecv = cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)
                        else:
                            exibecv = adjusted
                        cv2.imshow("Images",  exibecv)#mostra a imagem editada na janela do Opencv
                        k=cv2.waitKey(1)&0xFF#espera o usuário digitar alguma tecla, e k recebe o valor desta tecla em ASCII 
                        if k==27:#se  usuário pressionar "esc", a janela fecha sem que a imagem editada seja salva
                            break
                        elif k == 32:#se o usário pressionar a tecla "space" a imagem é salva e enviada para a area de trabalho
                            ver = auxiliar.verifica_cor(adjusted)#verifica se a imagem é preto e branco
                            image2 = adjusted
                            imagem.set_imgcv(image2)#self._imgcv é setado com a imagem editada
                            janela.mostrar (image2)#chama o método mostrar da janela 
                            flag['f2'] = 1#seta o flag f2
                            imagem.set_flag(flag)
                            break
                    cv2.destroyAllWindows()#fecha a janela Opencv
                else:#se o valor de kernel já tiver sido escolhido pelo usário: 
                    adjusted = adjust_gamma(original, ke)#chama o método responsável por fazer a edição da imagem e passa a imagem e o valor de gamma selecionado como argumento, e adjusted recebe a imagem editada 
                    ver = auxiliar.verifica_cor(adjusted)#verifica se a imagem é preto e branco
                    #se a imagem não for preto e branco ou se não está em escala de cinza convertemos para RGB antes de mostrar na área de trabalho
                    if ver == 0 and  flag ['gray'] == 0:
                        image2 = cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)
                    else:
                        image2 = adjusted
                    imagem.set_imgcv(image2)#self._imgcv é setado com a imagem editada
                    janela.mostrar (image2)#chama o método mostrar da janela 
                    flag['f2'] = 1#seta o flag f2
                    imagem.set_flag(flag)
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")


    
class tools(ediction):#classe derivada de ediction responsável pelas ferramentas de edição
     def __init__ (self, root):
        self.root = root
         #estes atributos serão utilizados para receber o nome do evento na função Process sequence
        self.func1 = 'pass'
        self.func2 = 'pass'
        self.func3 = 'pass'
        self.func4 = 'pass'
        self.func5 = 'pass'
        #self.flag2 é a variavel que utilizamos para ter controle sobre a função Play e pause
        self.flag2 =  None
     def desenha (self):
        def nil_draw(event,former_x,former_y,flags,param): #( Nil)
            global current_former_x,current_former_y,drawing, m, mode
            if event==cv2.EVENT_LBUTTONDOWN:
                drawing=True
                current_former_x,current_former_y=former_x,former_y
            elif event==cv2.EVENT_MOUSEMOVE:
                if drawing==True:
                    if mode==True:
                        cv2.line(self.im,(current_former_x,current_former_y),(former_x,former_y),(255,0,0),3)
                        current_former_x = former_x
                        current_former_y = former_y
            elif event==cv2.EVENT_LBUTTONUP:
                drawing=False
                if mode==True:
                    cv2.line(self.im,(current_former_x,current_former_y),(former_x,former_y),(255,0,0),3)
                    current_former_x = former_x
                    current_former_y = former_y
            return former_x,former_y
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        #fazemos uma cópia do dicionario de flags que é recebido e utilizamos ele como flag anterior, para ser usado no método Undo
        flg = copy.deepcopy(flag)
        imagem.set_flaganterior(flg)
        self.im = imagem.get_imgcv()#self.im recebe a imagem compativel com as funções do Opencv
        #fazemos uma cópia da imagem que é "recebida" pelo método e usamos ela como a imagem anterior, para, se necessário, ser usada pelo método undo da classe Janela
        imcv = copy.deepcopy (self.im)
        imagem.set_imganterior(imcv)
        if flag['img'] == 1:
            tkMessageBox.showinfo("Notice", "Press 'esc' to go out and 'space' to save the chage")#instruções básicas de como utilizar esse recurso
            cv2.namedWindow("Deteccao Manual OpenCV")#cria uma janela Opencv onde será feita a alteração
            cv2.setMouseCallback('Deteccao Manual OpenCV', nil_draw)#se ocorrer algum evento com o mouse, ele chama a função nil_draw
            while(1):#enquanto não houver um break ele não sai do loop
                ver = auxiliar.verifica_cor(self.im)#verifica se a imagem é preto e branco
                if ver == 0 and flag['gray'] == 0 and flag['canny']==0 and flag['roberts']==0 and flag['prewitt']==0 and flag['sobel']==0 and flag['sobelx']==0 and flag['sobely']==0:
                    exibecv = cv2.cvtColor(self.im, cv2.COLOR_BGR2RGB)
                else:
                    exibecv = self.im
                cv2.imshow('Deteccao Manual OpenCV',exibecv)#exibe a imagem com a alteração em tempo real
                k=cv2.waitKey(1)&0xFF#espera o usuário digitar alguma tecla. k recebe o valor desta tecla em ASCII (se nenhuma tecla for selecionada ele recebe 255)
                if k==27:#se  usuário pressionar "esc", a janela fecha sem que a imagem editada seja salva
                    break
                elif k == 32:
                    imgv = np.asarray(self.im)#imgv recebe a imagem editata. Esta função da biblioteca numpy é utilizada para converter a imagem para um formato compativel com as funções do Opencv
                    imgm = imgv
                    imagem.set_imgcv(imgm)#self._imgcv é setado com a imagem editada
                    janela.mostrar (imgm)#chama o método mostrar da classe janela e passa a imagem editada como argumento
                    flag ['draw'] = 1#seta o flag draw
                    imagem.set_flag(flag)
                    break                    
            cv2.destroyAllWindows()#fecha a janela do Opencv
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")

     def zoomin(self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:
            image = imagem.get_imgcv()#image recebe a imagem compativel com as funções do Opencv
            #fazemos uma cópia da imagem que é "recebida" pelo método e usamos ela como a imagem anterior, para, se necessário, ser usada pelo método undo da classe Janela
            imcv = copy.deepcopy (image)
            imagem.set_imganterior(imcv)
            height, width = image.shape[:2]#pegamos a altura e a largura da imagem
            #pegamos a altura e a largura da area de trabalho
            altf, largf = janela.get_fundospecifi()
            #verifica se a imagem é menor que a área de trabalho
            if height >= altf or width >= largf:
                 tkMessageBox.showerror("Error", "Maximun size reached !")
            else:
                altura = image.shape[0]#altura rece a altura da imagem, em pixels.
                altura2 = altura
                largura = image.shape[1]#largura recebe a largura da imagem, em pixels.
                largura2 = largura
                altura2 = float(altura) + 100#almentamos a altura em 100 pixels
                r = altura2 / altura
                largura2 = largura * r#aumentamos a largura proporcionalmente a altura
                dim  = (int (largura2), int(altura2))#dim recebe a altura e a largura
                #verifica se o tamanho máximo foi atingido
                if altura2 >= altf or largura2 >= largf:
                    tkMessageBox.showerror("Error", "Maximun size reached !")
                else:
                    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)#utilizando uma função do Opencv redimensionaos a imagem
                    ver = auxiliar.verifica_cor(image)#verifica se a imagem é preto e branco
                    #se a imagem não for preto e branco ou se não está em escala de cinza convertemos para RGB antes de mostrar na área de trabalho
                    #if ver == 0 and  flag ['gray'] == 0:
                    #    image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#utilizando uma função do Opencv convertemos para RGB
                    #else:
                    image2 = image
                    imagem.set_imgcv(image2)
                    janela.mostrar (image2)#chama o método mostrar da classe janela e passa a imagem editada como argumento
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")



     def zoomout(self):
        #os processo desse método são iguais ao do método zoom in , porem ao invés de aumentar a imagem em 100 pixels, ela é diminuida
        flag = imagem.get_flag()
        if flag['img'] == 1:
            image = imagem.get_imgcv()
            imcv = copy.deepcopy (image)
            imagem.set_imganterior(imcv)
            height, width = image.shape[:2]
            if height <= 20 or width <= 20:
                 tkMessageBox.showerror("Error", "Minimun size reached !")
            else:
                altura = image.shape[0]
                altura2 = altura
                largura = image.shape[1]
                largura2 = largura
                altura2 = float(altura) - 100
                r = altura2 / altura
                largura2 = largura * r
                dim  = (int (largura2), int(altura2))
                if altura2 <= 20 or largura2 <= 20:
                    tkMessageBox.showerror("Error", "Minimun size reached !")
                else:
                    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
                    ver = auxiliar.verifica_cor(image)
                    #if ver == 0 and  flag ['gray'] == 0:
                    #    image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    #else:
                    image2 = image
                    imagem.set_imgcv(image2)
                    janela.mostrar (image2)
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")



     def corta(self):
        def click_and_crop( event, x, y, flags, param):#( Nil )
             global refPt, cropping, fatia, a, b, c, d
             if event == cv2.EVENT_LBUTTONDOWN:
                 refPt = [(x, y)]
                 #a e b recebem as primeiras cordenadas da área de seleção
                 a = x
                 b = y
                 cropping = True
             elif event == cv2.EVENT_LBUTTONUP:
                 refPt.append((x, y))
                 #c e d recebem as outras cordenada
                 c = x 
                 d = y 
                 cropping = False
                 if flag ['gray'] == 0:#se a imagem for colorida:
                     #desenhamos um retângulo verde utilizando uma função da bibliotece Opencv com as coordenadas
                     cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)#a imagem com o retangulo é "colocada" em image, portanto quando o while reiniciar o loop a imagem com o retângulo será exibida
                 else:#se a imagem estiver em escala de cinza:
                     #desenhamos um retângulo preto utilizando uma função da bibliotece Opencv com as coordenadas definidas pelo usuário
                     cv2.rectangle(image, refPt[0], refPt[1], 0, 2)#a imagem com o retangulo é "colocada" em image, portanto quando o while reiniciar o loop a imagem com o retângulo será exibida
                     #diminuimos as coordenadas para que não aareça nenhuma borda do retângulo na imagem final
                     a = a + 2
                     b = b + 2
                     c = c - 1
                     d = d - 1
                 self.img4 = self.imgpi#self.img4 recebe a imagem no formato compativel com as funções da biblioteca Pillow
                 self.img4 = self.img4.crop ((a,b,c,d))#através de uma função da biblioteca pillow (com as coordenadas a, b, c e d), a imagem é cortada
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        #fazemos uma cópia do dicionario de flags que é recebido e utilizamos ele como flag anterior, para ser usado no método Undo
        flg = copy.deepcopy(flag)
        imagem.set_flaganterior(flg)
        image = imagem.get_imgcv()
        self.imgpi = Image.fromarray(image)#diferente do que ocorre nos outros filtros, para realizar o corte da imagem também é necessário que a imagem usada para a edição esteja no formato compativel com a biblioteca Pillow
        imagem.set_imgpil(self.imgpi)
        #fazemos uma cópia da imagem que é "recebida" pelo método e usamos ela como a imagem anterior, para, se necessário, ser usada pelo método undo da classe Janela
        imcv = copy.deepcopy (image)
        imagem.set_imganterior(imcv)
        if flag['img'] == 1:
                tkMessageBox.showinfo("Notice", "Press 'esc' to go out and 'space' to save the chage")#mensagem explicando como fazer a edição
                cv2.namedWindow('Cortar')#criamos uma janela do Opencv
                cv2.setMouseCallback('Cortar', click_and_crop)#Se o usuário relizar algum clique com o botão esquerdo, este "método auxiliar" é chamado
                while(1):
                    ver = auxiliar.verifica_cor(image)#verifica se a imagem é preto e branco
                    if ver == 0 and flag['gray'] == 0 and flag['canny']==0 and flag['roberts']==0 and flag['prewitt']==0 and flag['sobel']==0 and flag['sobelx']==0 and flag['sobely']==0:
                        exibecv = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    else:
                        exibecv = image
                    cv2.imshow('Cortar',exibecv)#exibimos a imagem em formato Opencv na janela 
                    k=cv2.waitKey(1)&0xFF#espera o usuário digitar alguma tecla. k recebe o valor desta tecla em ASCII (se nenhuma tecla for selecionada ele recebe 255, portanto se a imagem em image for alterada ele mostrará a alteração)
                    if k==27:#se  usuário pressionar "esc", a janela fecha sem que a imagem editada seja salva
                        break
                    elif k == 32:#se o usuário pressionar "space" a imagem editada é salva:
                        imgv = np.asarray(self.img4)#"imgv" recebe a imagem após ser cortada. Precisamos converter para o formato compativel com o OPencv, pois o corte é realizado através de uma função da biblioteca Pillow(veja no método clip and crop)
                        imagem.set_imgcv(imgv)
                        janela.mostrar (imgv)#chamamos o método mostrar da classe janela para exibir a imagem editada na área de trabalho
                        flag['crop'] = 1
                        imagem.set_flag(flag)
                        break
                cv2.destroyAllWindows()
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")

     def undo (self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:#verifica se há alguma imagem na área de trabalho
            if flag ['undo'] == 1:#verifica se o flag "undo" está em 1, ou seja, se é possivel realizar o processo
                #self.imag = processo.get_imganteior()#self.imag recebe a imagem anterior, ou seja o resultado da penultima alteração da imagem
                #imag = imagem.get_imganteior()#self.imag recebe a imagem anterior, ou seja o resultado da penultima alteração da imagem
                imag = auxiliar.pega_imagemanterior()
                if imag == "fim":
                    tkMessageBox.showerror("Error", "You can't make this change")
                else:
                    ver = auxiliar.verifica_cor(imag)#através do método verifica_cor da classe process é verificado se imagem anterior é preto e branco
                    if ver == 0:#se não for preto e branco:
                        try:#tenta converter a imagem para RGB e após isso mostrar a imagem(atrvés do método mostrar)
                            #image2 = cv2.cvtColor(imag, cv2.COLOR_BGR2RGB)
                            image2 = imag
                            janela.mostrar(image2)
                        except:#se não for possivel converter a imagem para RGB, ele apenas mostra a imagem(atrvés do método mostrar)
                            janela.mostrar(imag)
                    else:#se a imagem for preto e branco ele apenas mostra a imagem (atrvés do método mostrar)
                        janela.mostrar(imag)
                    imagem.set_imgcv(imag)#o atribulto self._imgcv da classe image recebe a imagem anterior
                    fg = auxiliar.pega_flaganterior()
                    imagem.set_flag(fg)
            else:#se não for possivel realizar o processo uma mensagem de erro é exibida
                tkMessageBox.showerror("Error", "You can't make this change yet")
        else:#se não houver uma imagem na area de trabalho uma mensagem de erro é exibida
            tkMessageBox.showerror("Error", "Please import an image first!")

     #este método é chamado apenas pelo método sequence, portanto ele não está associado á nenhum botão diretamente. Recomendamos que antes de ver este método, veja o método sequence
     def pega(self, ev, qual):
         #verifica por qual evento o méto foi chamado
        if ev == 1:
            #verifica qual filtro foi selecionado.
            if qual == 1:#verifica se o filtro Threshold foi selecionado
                mi = self.e1thresh1.get()#mi recebe o que foi digitado na caixa de texto self.e1thresh1(valor minimo), através de uma função do Tkinter
                mx = self.e2thresh1.get()#mx recebe o que foi digitado na caixa de texto self.e2thresh1(valor maximo), através de uma função do Tkinter
                try:#tenta converter a entrada em um inteiro
                    mi = int (mi)
                    mx = int (mx)
                    #verifica se o numero de entrada é valido, caso contraro uma mensagem de erro é exibida
                    if mi > 255 or mx > 255:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 255")
                    elif mi < 0 or mx < 0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    elif mi > mx:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:#se a entrada for válida self.k1 e sel.k12 recebem m1 e mx respectivamente
                        self.k1 = mi
                        self.k12 = mx
                                                    
                except ValueError:#se ao tentar converter para inteiro ocorrer um ValueError uma mensagem é exibida
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 2:#verifica se o filtro sobelx foi selecionado
                k = self.e1sobelx1.get()#k recebe o que foi digitado em na caixa de texto self.e1sobelx1
                try:#tenta converter o valor de k em um inteiro e tratar esse valor
                    k = int (k)
                    #verifica se o valor colocado é valido
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:#verifica se o valor de kernel selecionado é par ou impar
                            #se for par ele é incrementado e 1
                            k = k + 1
                        self.k1 = k#self.k1 recebe o valor de kernel selecionado para o filtro sobelx
                        self.k12 = 0#self.k12 recebe 0
                except ValueError:#se ao tentar converter para inteiro ocorrer um ValueError uma mensagem é exibida
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 3:#verifica se o filtro selecionado for o sobely
                #O processo e tratamento do valor de kernel selecionado é igual ao feito no sobelx
                k = self.e1sobely1.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k1 = k
                        self.k12 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 4:#verifica se o filtro selecionado é o sobel
                #O processo e tratamento do valor de kernel selecionado é igual ao feito no sobelx
                k = self.e1sobel1.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k1 = k
                        self.k12 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 5:#verifica se o filtro selecionado é o gamma
                self.k1 = int(self.s1.get())#self.k1 recebe o valor selecionado
        elif ev == 2:#verifica se o evento selecionado é o 2
            #os processos que ocorrem aqui será o mesmo que ocorr caso ev seja 1. Porém o valor de kernel é colocado em self.k2 e em self.k22
            if qual == 1:
                mi = self.e1thresh2.get()
                mx = self.e2thresh2.get()
                try:
                    mi = int (mi)
                    mx = int (mx)
                    if mi > 255 or mx > 255:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 255")
                    elif mi < 0 or mx < 0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    elif mi > mx:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        self.k2 = mi
                        self.k22 = mx
                                                    
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 2:
                k = self.e1sobelx2.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k2 = k
                        self.k22 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 3:
                k = self.e1sobely2.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k2 = k
                        self.k22 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 4:
                k = self.e1sobel2.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k2 = k
                        self.k22 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 5:
                self.k2 = int(self.s2.get())
        elif ev == 3:#verifica se o evento selecionado é o 3
            #os processos que ocorrem aqui será o mesmo que ocorr caso ev seja 1. Porém o valor de kernel é colocado em self.k3 e em self.k32
            if qual == 1:
                mi = self.e1thresh3.get()
                mx = self.e2thresh3.get()
                try:
                    mi = int (mi)
                    mx = int (mx)
                    if mi > 255 or mx > 255:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 255")
                    elif mi < 0 or mx < 0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    elif mi > mx:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        self.k2 = mi
                        self.k32 = mx
                                                    
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 2:
                k = self.e1sobelx3.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k3 = k
                        self.k32 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 3:
                k = self.e1sobely3.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k3 = k
                        self.k32 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 4:
                k = self.e1sobel3.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k3 = k
                        self.k32 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 5:
                self.k3 = int(self.s3.get())
        elif ev == 4:#verifica se o evento selecionado é o 4
            #os processos que ocorrem aqui será o mesmo que ocorr caso ev seja 1. Porém o valor de kernel é colocado em self.k4 e em self.k42
            if qual == 1:
                mi = self.e1thresh4.get()
                mx = self.e2thresh4.get()
                try:
                    mi = int (mi)
                    mx = int (mx)
                    if mi > 255 or mx > 255:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 255")
                    elif mi < 0 or mx < 0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    elif mi > mx:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        self.k4 = mi
                        self.k42 = mx
                                                    
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 2:
                k = self.e1sobelx4.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k4 = k
                        self.k42 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 3:
                k = self.e1sobely4.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k4 = k
                        self.k42 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 4:
                k = self.e1sobel4.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k4 = k
                        self.k42 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 5:
                self.k4 = int(self.s4.get())
        elif ev == 5:#verifica se o evento selecionado é o 5
            #os processos que ocorrem aqui será o mesmo que ocorre caso ev seja 1. Porém o valor de kernel é colocado em self.k5 e em self.k52
            if qual == 1:
                mi = self.e1thresh5.get()
                mx = self.e2thresh5.get()
                try:
                    mi = int (mi)
                    mx = int (mx)
                    if mi > 255 or mx > 255:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 255")
                    elif mi < 0 or mx < 0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    elif mi > mx:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        self.k5 = mi
                        self.k52 = mx
                                                    
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 2:
                k = self.e1sobelx5.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k5 = k
                        self.k52 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 3:
                k = self.e1sobely5.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k5 = k
                        self.k52 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 4:
                k = self.e1sobel5.get()
                try:
                    k = int (k)
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        a = k % 2
                        if a == 0:
                            k = k + 1
                        self.k5 = k
                        self.k52 = 0
                except ValueError:
                    tkMessageBox.showerror("Error", "Invalid entry")

            elif qual == 5:
                self.k5 = int(self.s5.get())

        
                
        

     def sequence(self):
        #cria e coloca os atributos que receberão os valores de kernel caso o filtro selecionado exija a entrada desses valores
        self.k1 = 0
        self.k12 = 0
        self.k2 = 0
        self.k22 = 0
        self.k3 = 0
        self.k32 = 0
        self.k4 = 0
        self.k42 = 0
        self.k5 = 0
        self.k52 = 0
        #função responsavel por "pegar" o filtro selecionado, e se necessário chama o método pega para receber os valores de kernel
        def ok1():
            self.func1 = op1.get()#self.func1 recebe uma string, que corresponde ao nome do filtro selecionado

            #verifica se o filtro selecionado precisa receber um valor de kernel
            
            if self.func1 == 'thresh': #verifica se foi selecionado o filtro thresh, se sim é necessário que o usuário entre com o valor maximo e mínimo
                #Cria e posiciona widgets na aba event 1 da janela process sequence, para que o usuário entre com os valores mínimo e máximo 
                l1 = Label(f1, text="Minimun: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1thresh1 = Entry(f1) #as entradas também foram nomeadas de forma à indicar o evento e o caso especial a qual pertencem, neste caso é a primeira entrada, para o caso thresh no evento 1
                self.e1thresh1.grid ( row = 1, column = 1)
                l2 = Label(f1, text="Maximun: ")
                l2.grid(row = 2, column = 0, padx = 10, pady = 10)
                self.e2thresh1 = Entry(f1)# segunda entrada, para o caso thresh no envento1
                self.e2thresh1.grid ( row = 2, column = 1)
                b1  = Button (f1, text = "OK", command = lambda: self.pega(1, 1))#ao clicar neste botão ele chamará o metodo pega, o primeiro argumento (1) significa qual é o evento e o segundo(1) qual é o caso especial
                b1.grid ( row = 3, column = 1)

            elif self.func1 == 'sobelx':#verifica se foi selecionado o filtro o sobelx, se sim é necessário que o usuário entre com o valor de kernel
                #Cria e posiciona widgets na aba event 1 da janela process sequence, para que o usuário entre com o valor de kernel
                l1 = Label(f1, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobelx1 = Entry(f1)
                self.e1sobelx1.grid ( row = 1, column = 1)
                b1 = Button (f1, text = "OK", command = lambda: self.pega(1, 2))# [...]self.pega(evento, caso especial)
                b1.grid ( row = 3, column = 1)

            elif self.func1 == 'sobely':#verifica se foi selecionado o filtro o sobely, se sim é necessário que o usuário entre com o valor de kernel
                #Cria e posiciona widgets na aba event 1 da janela process sequence, para que o usuário entre com o valor de kernel
                l1 = Label(f1, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobely1 = Entry(f1)
                self.e1sobely1.grid ( row = 1, column = 1)
                b1 = Button (f1, text = "OK", command = lambda: self.pega(1, 3))
                b1.grid ( row = 3, column = 1)

            elif self.func1 == 'sobel':#verifica se foi selecionado o filtro o sobel, se sim é necessário que o usuário entre com o valor de kernel
                #Cria e posiciona widgets na aba event 1 da janela process sequence, para que o usuário entre com o valor de kernel
                l1 = Label(f1, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobel1 = Entry(f1)
                self.e1sobel1.grid ( row = 1, column = 1)
                b1 = Button (f1, text = "OK", command = lambda: self.pega(1, 4))
                b1.grid ( row = 3, column = 1)

            elif self.func1 == 'gamma':#verifica se foi selecionado o filtro o gamma, se sim é necessário que o usuário entre com o valor de kernel
                #Cria e posiciona widgets na aba event 1 da janela process sequence, para que o usuário entre com o valor de kernel
                #Diferentemente do que ocorre nos casos anteriores, neste nós criamos uma barra de rolagem com um deslocamento de 0.5, para que o usário selecione o valor de gamma mais facilmente 
                self.s1 = Scale(f1, from_ = 0, to = 3.5, resolution = 0.5, orient = HORIZONTAL)
                self.s1.grid (row = 1 , column = 0, columnspan  = 2)
                b1 = Button (f1, text = "OK", command = lambda: self.pega(1, 5))
                b1.grid ( row = 3, column = 1)

            else:
                #caso o filtro selecionado não precise ser "personalizado", self.k1 e self.k12, os atributos responsáveis por receber os valores, recebem 0 
                self.k1 = 0
                self.k12 = 0
        def ok2():
            #os processos que ocorrem aqui são iguais aos que ocorrem na função ok1, mudando apenas os argumentos, nomes e atributos que indicam a qual evento pertence
            self.func2 = op2.get()
            
            if self.func2 == 'thresh':
                l1 = Label(f2, text="Minimun: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1thresh2 = Entry(f2)
                self.e1thresh2.grid ( row = 1, column = 1)
                l2 = Label(f2, text="Maximun: ")
                l2.grid(row = 2, column = 0, padx = 10, pady = 10)
                self.e2thresh2 = Entry(f2)
                self.e2thresh2.grid ( row = 2, column = 1)
                b1  = Button (f2, text = "OK", command = lambda: self.pega(2, 1))
                b1.grid ( row = 3, column = 1)

            elif self.func2 == 'sobelx':
                l1 = Label(f2, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobelx2 = Entry(f2)
                self.e1sobelx2.grid ( row = 1, column = 1)
                b1 = Button (f2, text = "OK", command = lambda: self.pega(2, 2))
                b1.grid ( row = 3, column = 1)

            elif self.func2 == 'sobely':
                l1 = Label(f2, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobely2 = Entry(f2)
                self.e1sobely2.grid ( row = 1, column = 1)
                b1 = Button (f2, text = "OK", command = lambda: self.pega(2, 3))
                b1.grid ( row = 3, column = 1)

            elif self.func2 == 'sobel':
                l1 = Label(f2, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobel2 = Entry(f2)
                self.e1sobel2.grid ( row = 1, column = 1)
                b1 = Button (f2, text = "OK", command = lambda: self.pega(2, 4))
                b1.grid ( row = 3, column = 1)

            elif self.func2 == 'gamma':
                self.s2 = Scale(f2, from_ = 0, to = 3.5, resolution = 0.5, orient = HORIZONTAL)
                self.s2.grid (row = 1 , column = 0, columnspan  = 2)
                b1 = Button (f2, text = "OK", command = lambda: self.pega(2, 5))
                b1.grid ( row = 3, column = 1)

            else:
                self.k2 = 0
                self.k22 = 0
        def ok3():
            #os processos que ocorrem aqui são iguais aos que ocorrem na função ok1, mudando apenas os argumentos, nomes e atributos que indicam a qual evento pertence
            self.func3 = op3.get()
            
            if self.func3 == 'thresh':
                l1 = Label(f3, text="Minimun: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1thresh3 = Entry(f3)
                self.e1thresh3.grid ( row = 1, column = 1)
                l2 = Label(f3, text="Maximun: ")
                l2.grid(row = 2, column = 0, padx = 10, pady = 10)
                self.e2thresh3 = Entry(f3)
                self.e2thresh3.grid ( row = 2, column = 1)
                b1  = Button (f3, text = "OK", command = lambda: self.pega(3, 1))
                b1.grid ( row = 3, column = 1)

            elif self.func3 == 'sobelx':
                l1 = Label(f3, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobelx3 = Entry(f3)
                self.e1sobelx3.grid ( row = 1, column = 1)
                b1 = Button (f3, text = "OK", command = lambda: self.pega(3, 2))
                b1.grid ( row = 3, column = 1)

            elif self.func3 == 'sobely':
                l1 = Label(f3, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobely3 = Entry(f3)
                self.e1sobely3.grid ( row = 1, column = 1)
                b1 = Button (f3, text = "OK", command = lambda: self.pega(3, 3))
                b1.grid ( row = 3, column = 1)

            elif self.func3 == 'sobel':
                l1 = Label(f3, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobel3 = Entry(f3)
                self.e1sobel3.grid ( row = 1, column = 1)
                b1 = Button (f3, text = "OK", command = lambda: self.pega(3, 4))
                b1.grid ( row = 3, column = 1)

            elif self.func3 == 'gamma':
                self.s3 = Scale(f3, from_ = 0, to = 3.5, resolution = 0.5, orient = HORIZONTAL)
                self.s3.grid (row = 1 , column = 0, columnspan  = 2)
                b1 = Button (f3, text = "OK", command = lambda: self.pega(3, 5))
                b1.grid ( row = 3, column = 1)

            else:
                self.k3 = 0
                self.k32 = 0
        def ok4():
            #os processos que ocorrem aqui são iguais aos que ocorrem na função ok1, mudando apenas os argumentos, nomes e atributos que indicam a qual evento pertence
            self.func4 = op4.get()
            
            if self.func4 == 'thresh':
                l1 = Label(f4, text="Minimun: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1thresh4 = Entry(f4)
                self.e1thresh4.grid ( row = 1, column = 1)
                l2 = Label(f4, text="Maximun: ")
                l2.grid(row = 2, column = 0, padx = 10, pady = 10)
                self.e2thresh4 = Entry(f4)
                self.e2thresh4.grid ( row = 2, column = 1)
                b1  = Button (f4, text = "OK", command = lambda: self.pega(4, 1))
                b1.grid ( row = 3, column = 1)

            elif self.func4 == 'sobelx':
                l1 = Label(f4, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobelx4 = Entry(f4)
                self.e1sobelx4.grid ( row = 1, column = 1)
                b1 = Button (f4, text = "OK", command = lambda: self.pega(4, 2))
                b1.grid ( row = 3, column = 1)

            elif self.func4 == 'sobely':
                l1 = Label(f4, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobely4 = Entry(f4)
                self.e1sobely4.grid ( row = 1, column = 1)
                b1 = Button (f4, text = "OK", command = lambda: self.pega(4, 3))
                b1.grid ( row = 3, column = 1)

            elif self.func4 == 'sobel':
                l1 = Label(f4, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobel4 = Entry(f4)
                self.e1sobel4.grid ( row = 1, column = 1)
                b1 = Button (f4, text = "OK", command = lambda: self.pega(4, 4))
                b1.grid ( row = 3, column = 1)

            elif self.func4 == 'gamma':
                self.s4 = Scale(f4, from_ = 0, to = 3.5, resolution = 0.5, orient = HORIZONTAL)
                self.s4.grid (row = 1 , column = 0, columnspan  = 2)
                b1 = Button (f4, text = "OK", command = lambda: self.pega(4, 5))
                b1.grid ( row = 3, column = 1)

            else:
                self.k4 = 0
                self.k42 = 0
        def ok5():
            #os processos que ocorrem aqui são iguais aos que ocorrem na função ok1, mudando apenas os argumentos, nomes e atributos que indicam a qual evento pertence
            self.func5 = op5.get()
            
            if self.func5 == 'thresh':
                l1 = Label(f5, text="Minimun: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1thresh5 = Entry(f5)
                self.e1thresh5.grid ( row = 1, column = 1)
                l2 = Label(f5, text="Maximun: ")
                l2.grid(row = 2, column = 0, padx = 10, pady = 10)
                self.e2thresh5 = Entry(f5)
                self.e2thresh5.grid ( row = 2, column = 1)
                b1  = Button (f5, text = "OK", command = lambda: self.pega(5, 1))
                b1.grid ( row = 3, column = 1)

            elif self.func5 == 'sobelx':
                l1 = Label(f5, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobelx5 = Entry(f5)
                self.e1sobelx5.grid ( row = 1, column = 1)
                b1 = Button (f5, text = "OK", command = lambda: self.pega(5, 2))
                b1.grid ( row = 3, column = 1)

            elif self.func5 == 'sobely':
                l1 = Label(f5, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobely5 = Entry(f5)
                self.e1sobely5.grid ( row = 1, column = 1)
                b1 = Button (f5, text = "OK", command = lambda: self.pega(5, 3))
                b1.grid ( row = 3, column = 1)

            elif self.func5 == 'sobel':
                l1 = Label(f4, text="Kernel size: ")
                l1.grid(row = 1, column = 0, padx = 10, pady = 10)
                self.e1sobel5 = Entry(f5)
                self.e1sobel5.grid ( row = 1, column = 1)
                b1 = Button (f5, text = "OK", command = lambda: self.pega(5, 4))
                b1.grid ( row = 3, column = 1)

            elif self.func5 == 'gamma':
                self.s5 = Scale(f5, from_ = 0, to = 3.5, resolution = 0.5, orient = HORIZONTAL)
                self.s5.grid (row = 1 , column = 0, columnspan  = 2)
                b1 = Button (f5, text = "OK", command = lambda: self.pega(5, 5))
                b1.grid ( row = 3, column = 1)

            else:
                self.k5 = 0
                self.k52 = 0
                
                
            
        #bloco principal do método sequence     
        newwin = Toplevel(self.root)# cria uma nova janela
        n = ttk.Notebook(newwin)#cria um notebook utilizando uma função da biblioteca ttk
        #cria os 5 frames, que ficarão em 5 abas do notebook n
        f1 = ttk.Frame(n)
        f2 = ttk.Frame(n)
        f3 = ttk.Frame(n)
        f4 = ttk.Frame(n)
        f5 = ttk.Frame(n)
        #adiciona os frames ao notebook n
        n.add(f1, text='Event 1')
        n.add(f2, text='Event 2')
        n.add(f3, text='Event 3')
        n.add(f4, text='Event 4')
        n.add(f5, text='Event 5')
        n.grid( row = 0, column = 0, padx = 10, pady = 10)#posiciona

        #cria uma variavel da classe StringVar para cada evento, para depois ser utilizada no menu de opções.
        #define o que será a opção inicial 
        op1 = StringVar(f1)
        op1.set('pass')
        op2= StringVar(f2)
        op2.set('pass')
        op3 = StringVar(f3)
        op3.set('pass')
        op4 = StringVar(f4)
        op4.set('pass')
        op5 = StringVar(f5)
        op5.set('pass')

        #aba 1 (event 1)
        f1l = OptionMenu(f1, op1, 'pass', 'gray', 'canny', 'roberts', 'invert', 'prewitt', 'sobelx', 'sobely', 'sobel', 'thresh', 'gamma')#cria um menu de opções e adiciona quais serão as opções nele, ou seja, os filtros  
        f1l.grid( row = 0, column = 0, padx = 10, pady = 10)#posiciona o menu de opções
        bu = Button(f1, text="Save", command=ok1)#cria um botão que chamará a função ok1, para "pegar" e salvar o filtro selecionado
        bu.grid( row = 3, column = 0)#posiciona o botão

        #aba 2 (event 2)
        f2l =  OptionMenu(f2, op2, 'pass', 'gray', 'canny', 'roberts', 'invert', 'prewitt', 'sobelx', 'sobely', 'sobel', 'thresh', 'gamma')#cria um menu de opções e adiciona quais serão as opções nele, ou seja, os filtros  
        f2l.grid( row = 0, column = 0, padx = 10, pady = 10)#posiciona o menu de opções
        bu = Button(f2, text="Save", command=ok2)#cria um botão que chamará a função ok2, para "pegar" e salvar o filtro selecionado
        bu.grid( row = 3, column = 0)#posiciona o botão

        #aba3 (event 3)
        f3l =  OptionMenu(f3, op3, 'pass', 'gray', 'canny', 'roberts', 'invert', 'prewitt', 'sobelx', 'sobely', 'sobel', 'thresh', 'gamma')#cria um menu de opções e adiciona quais serão as opções nele, ou seja, os filtros  
        f3l.grid( row = 0, column = 0, padx = 10, pady = 10)#posiciona o menu de opções
        bu = Button(f3, text="Save", command=ok3)#cria um botão que chamará a função ok3, para "pegar" e salvar o filtro selecionado
        bu.grid( row = 3, column = 0)#posiciona o botão

        #aba4 (event 4)
        f4l =  OptionMenu(f4, op4, 'pass', 'gray', 'canny', 'roberts', 'invert', 'prewitt', 'sobelx', 'sobely', 'sobel', 'thresh', 'gamma')#cria um menu de opções e adiciona quais serão as opções nele, ou seja, os filtros  
        f4l.grid( row = 0, column = 0, padx = 10, pady = 10)#posiciona o menu de opções
        bu = Button(f4, text="Save", command=ok4)#cria um botão que chamará a função ok4, para "pegar" e salvar o filtro selecionado
        bu.grid( row = 3, column = 0)#posiciona o botão

        #aba5 (event 5)
        f5l =  OptionMenu(f5, op5, 'pass', 'gray', 'canny', 'roberts', 'invert', 'prewitt', 'sobelx', 'sobely', 'sobel', 'thresh', 'gamma')#cria um menu de opções e adiciona quais serão as opções nele, ou seja, os filtros  
        f5l.grid( row = 0, column = 0, padx = 10, pady = 10)#posiciona o menu de opções
        bu = Button(f5, text="Save", command=ok5)#cria um botão que chamará a função ok5, para "pegar" e salvar o filtro selecionado
        bu.grid( row = 3, column = 0)#posiciona o botão
        
     def do (self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:
            if self.func1 == 'pass':#verifica se o usuário selecionou a opção "pass"
                pass
            else:#caso o usuário tenha escolhido alguma filtro:
                if self.k1 == 0:#caso self.k1 seja 0, segnifica que o usuário selecionou um filtro que não possui nenhum valor de kernel selecionado, ou seja não necessita de nenhum argumento para chamar a função
                    try:#tenta chamar o método responsável pelo filtro selecionado
                        ev1 = getattr (filtrosb, self.func1)()#esta função do Pytho equivala a: processo.(nome do método em self.func1)()
                    except AttributeError:#se ocorrer um erro ao tentar chamar um método da classe filtrosb(borderfilters), ele tenta chamar na classe filtrosg(generalfilters)
                        try: 
                            ev1 = getattr (filtrosg, self.func1)()
                        except TypeError:
                            tkMessageBox.showerror("Error", "Invalid entry!")
                    except TypeError:#caso ocorra um TypeError e o método não possa ser chamado uma mensagem de erro é exibida 
                        tkMessageBox.showerror("Error", "Invalid entry!")
                        
                elif self.k1 !=0 and self.k12 !=0:#se self.k1 e self.k12 sejam diferentes de zero, significa que o usuário selecionou um filtro que possui dois valores de entrada, ou seja, o thresh foi selecionado
                    try:#tenta chamar o método tresh
                        ev1 = getattr (filtrosg, self.func1)(self.k1, self.k12)#equivale à: processo.(nome do metodo)((minimo), (máximo))
                    except TypeError:#caso ocorra um TypeError e o método não possa ser chamado uma mensagem de erro é exibida 
                        tkMessageBox.showerror("Error", "Invalid entry!")   
                else:#caso nenhuma das opções acima não seja cumprida significa que o filtro selecionado possui uma opção, ou seja, um argumento; como por exemplo, o filtro Sobel
                    try:#tenta chamar o método responsável pelo filtro selecionado
                        ev1 = getattr (filtrosb, self.func1)(self.k1)#equivale à: processo.(nome do método).((valor de entrada))
                    except AttributeError:#se ocorrer um erro ao tentar chamar um método da classe filtrosb(borderfilters), ele tenta chamar na classe filtrosg(generalfilters)
                        ev1 = getattr (filtrosg, self.func1)()
                    except TypeError:#caso ocorra um TypeError e o método não possa ser chamado uma mensagem de erro é exibida 
                        tkMessageBox.showerror("Error", "Invalid entry!")
            #os processos para chamar o método do filtro selecionado pelo usuario em "event 2" são iguais ao do "event 1"      
            if self.func2 == 'pass':
                pass
            else:
                if self.k2 == 0:
                    try:
                            ev2 = getattr (filtrosb, self.func2)()
                    except AttributeError:
                        try:
                            ev2 = getattr (filtrosg, self.func2)()
                        except TypeError:
                            tkMessageBox.showerror("Error", "Invalid entry!")
                    except TypeError:
                        tkMessageBox.showerror("Error", "Invalid entry!")
                
                elif self.k2 !=0 and self.k22 !=0:
                    try:
                        ev2 = getattr (filtrosg, self.func2)(self.k2, self.k22)
                    except TypeError:
                         tkMessageBox.showerror("Error", "Invalid entry!")
                    
                else:
                    try:
                        ev2 = getattr (filtrosb, self.func2)(self.k2)
                    except AttributeError:
                            ev2 = getattr (filtrosg, self.func2)(self.k2)
                    except TypeError:
                         tkMessageBox.showerror("Error", "Invalid entry!")
            #os processos para chamar o método do filtro selecionado pelo usuario em "event 3" são iguais ao do "event 1"       
            if self.func3 == 'pass':
                pass
            else:
                if self.k3 == 0:
                    try:
                        ev1 = getattr (filtrosb, self.func3)()
                    except AttributeError:
                        try:
                            ev1 = getattr (filtrosg, self.func3)()
                        except TypeError:
                            tkMessageBox.showerror("Error", "Invalid entry!")
                    except TypeError:
                         tkMessageBox.showerror("Error", "Invalid entry!")

                elif self.k3 !=0 and self.k32 !=0:
                    try:
                        ev1 = getattr (filtrosg, self.func3)(self.k3, self.k32)
                    except TypeError:
                         tkMessageBox.showerror("Error", "Invalid entry!")
                else:
                    try:
                        ev1 = getattr (filtrosb, self.func3)(self.k3)
                    except AttributeError:
                            ev1 = getattr (filtrosg, self.func3)()
                    except TypeError:
                         tkMessageBox.showerror("Error", "Invalid entry!")
            #os processos para chamar o método do filtro selecionado pelo usuario em "event 4" são iguais ao do "event 1"        
            if self.func4 == 'pass':
                pass
            else:
                if self.k4 == 0:
                    try:
                        ev1 = getattr (filtrosb, self.func4)()
                    except AttributeError:
                        try:
                            ev1 = getattr (filtrosg, self.func4)()
                        except TypeError:
                            tkMessageBox.showerror("Error", "Invalid entry!")
                    except TypeError:
                         tkMessageBox.showerror("Error", "Invalid entry!")
                    
                elif self.k4 !=0 and self.k42 !=0:
                    try:
                        ev1 = getattr (filtrosg, self.func4)(self.k4, self.k42)
                    except TypeError:
                         tkMessageBox.showerror("Error", "Invalid entry!")
                    

                else:
                    try:
                        ev1 = getattr (filtrosb, self.func4)(self.k4)
                    except AttributeError:
                            ev1 = getattr (filtrosg, self.func4)()
                    except TypeError:
                         tkMessageBox.showerror("Error", "Invalid entry!")
            #os processos para chamar o método do filtro selecionado pelo usuario em "event 5" são iguais ao do "event 1"
            if self.func5 == 'pass':
                pass
            else:
                if self.k5 == 0:
                    try:
                        ev1 = getattr (filtrosb, self.func5)()
                    except AttributeError:
                        try:
                            ev1 = getattr (filtrosg, self.func5)()
                        except TypeError:
                            tkMessageBox.showerror("Error", "Invalid entry!")
                    except TypeError:
                         tkMessageBox.showerror("Error", "Invalid entry!")
                    
                elif self.k5 !=0 and self.k52 !=0:
                    try:
                        ev1 = getattr (filtrosg, self.func5)(self.k5, self.k52)
                    except TypeError:
                         tkMessageBox.showerror("Error", "Invalid entry!")
                    

                else:
                    try:
                        ev1 = getattr (filtrosb, self.func5)(self.k5)
                    except AttributeError:
                            ev1 = getattr (filtrosg, self.func5)()
                    except TypeError:
                         tkMessageBox.showerror("Error", "Invalid entry!")
                    
                
                                        
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")


    
class filesop(object):
    def __init__(self, root):
        self.root = root

    def videotoimage (self):
        def mostracaptura(file):
            if len(file)>0:#verifica se filename não está vazio
                image = cv2.imread(file)#carrega a imagem em image, utilizando uma função do Open cv
                height, width = image.shape[:2]#pega a altura e a largura da imagem
                altf, largf = janela.get_fundospecifi()
                if height > altf or width > largf:#verifica se a imagem  não é maior que a area de trabalho
                    #Ajuste do tamanho
                    altura = image.shape[0]# altura recebe um numero int que é a atura da imagem
                    altura2 = altura #faz uma cópia desse valor em altura2
                    largura = image.shape[1]#largura recebe um numero int que é a largura desta imagem
                    largura2 = largura#faz uma copia desse valor em largura2 
                    #enquanto a imagem for maior que a area de trabalho ele irá diminuir a altura um 100 pixels e diminuirá a largura proporcionalmente
                    while altura2 > altf or largura2 > largf:
                        altura = altura2
                        largura = largura2
                        altura2 = float(altura) - 100
                        r = altura2 / altura
                        largura2 = largura * r
                    dim  = (int (largura2), int(altura2))#dim recebe a nova altura e largura da imagem
                    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)#utilizando uma função Opencv a imagem é redimensionada 
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#converte a imagem do Open cv para o formato RGB
                    flag = {'img' :1,'gray': 0, 'f1':0, 'f2': 0, 'f3' : 0, 'canny' : 0, 'roberts': 0, 'sobelx': 0 , 'sobely': 0, 'sobel': 0, 'prewitt': 0, 'process': 0, 'draw': 0, 'undo' :0, 'crop': 0}#reseta todos os flags exceto o "img" que é colocado em 1
                    imagem.set_imgcv(image)#seta o atributo sel.imgcv da classe process com a imagem 
                    imagem.set_flag(flag)#seta self.flag da classe process
                    janela.mostrar (image)#chama o metodo mostrar e passa imagem como argumento 
                else:#se a imagem não for maior que a área de trabalho
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#converte a imagem do Open cv para o formato RGB
                    flag = {'img' :1,'gray': 0, 'f1':0, 'f2': 0, 'f3' : 0, 'canny' : 0, 'roberts': 0, 'sobelx': 0 , 'sobely': 0, 'sobel': 0, 'prewitt': 0, 'process': 0, 'draw': 0, 'undo' :0, 'crop': 0}#reseta todos os flags exceto o "img" que é colocado em 1
                    imagem.set_imgcv(image)#seta o atributo sel.imgcv da classe process com a imagem 
                    imagem.set_flag(flag)#seta self._flag da classe process
                    janela.mostrar (image)#chama o metodo mostrar e passa imagem como argumento 
        self.flagframe = 1
        ret = 1
        #tkMessageBox.showinfo("Notice", "Select the video file")#mensagem com informações sobre como operar esta ferramenta
        workdirectory = os.getcwd()
        #as proximas duas funções retornam uma string contendo o nome do arquivo e sua localização e o diretorio para as imagens que serão geradas
        filename = tkFileDialog.askopenfilename(initialdir = workdirectory,title = "Select Video",filetypes = (("Audio Video Interleave","*.avi"),("MPEG-4","*.mp4")))#através desta função o usuário pode selecionar o arquivo de video
        #tkMessageBox.showinfo("Notice", "Select the directory where the images will be save")
        directoryname = tkFileDialog.askdirectory(initialdir = workdirectory,title = "Select directory  where the images will be save")#através desta função o usuário pode selecionar o diretorio onde as imagens serão salvas
        spl = None
        slp, lim = configuracao.getframeparametros()#spl e lim recebem novos valores, caso o usuário tenha alterado eles
        tempo = 0
        #se o usuário não alterou o tempo entre a captura dos frames, o valor padrão será utilizado, ou seja 0,3s
        if slp == 0.0:
            slp = 0.0
        if len(filename) > 0 and len(directoryname) > 0:#verifica se a variavel 'filename' não esta vazia
            cap = cv2.VideoCapture(filename)#abre o arquivo de video selecionado
            ct = 0#ct será o contador que da nome a imagem, por exemplo: 1.jpg; 2.jpg... o número do arquivo é controlado pela variavel ct
            tempo = 0
            while(ret):#enquanto o arquivo estiver aberto
                start = time.time()
                ct = ct + 1#incrementa ct 
                ret, frame = cap.read()#através desta função do Opencv "lemos" o primeiro ou o próximo frame do video e ele é salvo na variavel frame
                if ret:
                    name = directoryname + '/' + str(ct) + '.jpg'#concatenamos algumas strings para dar nome ao arquivo, ex: diretorio1/diretorio2 + / + 1 + .jpg = diretorio1/diretorio2/1.jpg 
                    #mostramos o nome do arquivbo salvo na barra de informações
                    showname = 'Creating...' + name
                    janela.showinfo(showname)
                    self.root.update()
                    cv2.imwrite(name, frame)#através desta função do Opencv nós salvamos o frame lido anteriormente como uma imagem, cujo nome corresponde a string na variavel "name"
                    #mostramos a imagem criada na area de trabalho
                    mostracaptura(name)
                    end2 = time.time()
                    inter = slp - (end2 - start)
                    if inter < 0: inter = 0.0
                    time.sleep(inter)#faz o programa parar por um determinado tempo, para que seja possivel acompanhar o progresso da conversão 
                    end = time.time()
                tempo = tempo + (end - start)
                if lim != None:#se o usuario configurou um numero limite de frames
                    if ct == lim:#se o número limite de frames for atingido o loop é interrompido
                        break
                if self.flagframe == 0:#se o usuario clicou no botão "stop frame capture"
                    break
            frame_rate = round((ct/tempo), 3)#cacula o frame rate da camera
            dia = datetime.datetime.now()
            testo = ["Frame rate real { \n", str(frame_rate), "\n}\n", "Frame rate device { \n30\n}\n", "frame rate selected (seconds) {\n", str(slp), "\n}\n", "Frame { \n", str(ct), "\n}\n", "process finished in: ", str(dia)]
            end = directoryname +'/info.txt'
            arq = open ( end, 'w')
            arq.writelines(testo)
            arq.close()
            cap.release()
            cv2.destroyAllWindows()
            janela.showinfo('finished')
   

    def stopvti(self):
        self.flagframe = 0
   

    def newfile(self):
        #PRECISA SER ALTERADO
        #abre uma imagem totalmente branca
        fdirectory = (os.getcwd() + '\icones\\')
        imgf = cv2.imread(fdirectory + "box2.jpg")
        #coloca ela no tamanho do fundo
        altf, largf = janela.get_fundospecifi()
        dim = (largf, altf)
        imgf = cv2.resize(imgf, dim, interpolation = cv2.INTER_AREA)
        imgf = np.asarray(imgf)#converte para o "formato Opencv"
        janela.mostrar(imgf)#exibe esta imagem
        janela.showinfo(" ")
        #reseta a biblioteca de flags
        flag = {'img' :0,'gray': 0, 'f1':0, 'f2': 0, 'f3' : 0, 'canny' : 0, 'roberts': 0, 'sobelx': 0 , 'sobely': 0, 'sobel': 0, 'prewitt': 0, 'process': 0, 'draw': 0, 'undo' :0, 'crop': 0}
        imagem.set_flag(flag)

    def save(self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag ['img'] == 1: #verifica se a alguma imagem na área de trabalho
            image = imagem.get_imgcv()
            cv2.imwrite('imagem.png',image)#salva a imagem utlizando uma função do Opencv, com o nome "imagem.png"
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")

    def saveas(self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag ['img'] == 1:#verifica se a alguma imagem na área de trabalho
            #utlizando uma função do Tkinter permite que o usuário selecione o diretório, nome e extenção com o qual o arquivo será salvo
            workdirectory = os.getcwd()
            local = tkFileDialog.asksaveasfilename(initialdir = workdirectory,title = "Select directory",filetypes = (("jpeg files","*.jpg *.jpeg *.jpe"),("Windows bitmaps","*.bpm"),("Portable Network Graphics","*.png"),("Portable image format","*.pbm *.pgm *.ppm"), ("JPEG 2000 files","*.jp2"), ("Tagged Image File Format","*.tiff")))
            image = imagem.get_imgcv()
            try:
                cv2.imwrite(local,image)#salva a imagem utlizando uma função do Opencv no local e com o nome selecionado
            except:
                tkMessageBox.showerror("Error", "Please write the name of the file with the extension:\n name.extension")
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")

    def importar (self):
        #Utliza uma função do Tkinter para pegar o nome, extenção e diretória onde a imagem esta e coloca estas informações em filename. Neste trá uma string, da seguinte forma:" Home/diretório1/diretório2/arquivo.ext"
        workdirectory = os.getcwd()
        filename = tkFileDialog.askopenfilename(initialdir = workdirectory,title = "Select directory",filetypes = (("jpeg files","*.jpg *.jpeg *.jpe"),("Windows bitmaps","*.bpm"),("Portable Network Graphics","*.png"),("Portable image format","*.pbm *.pgm *.ppm"), ("Graphics Interchange Format","*.gif"), ("Microsoft","*.msp"), ("PiCture eXchange","*.pcx"), ("Tagged Image File Format","*.tiff"), ("X BitMap","*.xbm")))
        if len(filename)>0:#verifica se filename não está vazio
            image = cv2.imread(filename)#carrega a imagem em image, utilizando uma função do Open cv
            janela.showinfo(filename)
            height, width = image.shape[:2]#pega a altura e a largura da imagem
            altf, largf = janela.get_fundospecifi()
            if height > altf or width > largf:#verifica se a imagem selecionada não é maior que a area de trabalho
                tkMessageBox.showinfo("Notice", "Image size adjusted")#mostra uma mensagem utilizando uma função do Tkinter de que o tamanho da imagem foi ajustado
                #Ajuste do tamanho
                altura = image.shape[0]# altura recebe um numero int que é a atura da imagem
                altura2 = altura #faz uma cópia desse valor em altura2
                largura = image.shape[1]#largura recebe um numero int que é a largura desta imagem
                largura2 = largura#faz uma copia desse valor em largura2 
                #enquanto a imagem for maior que a area de trabalho ele irá diminuir a altura um 100 pixels e diminuirá a largura proporcionalmente
                while altura2 > altf or largura2 > largf:
                    altura = altura2
                    largura = largura2
                    altura2 = float(altura) - 100
                    r = altura2 / altura
                    largura2 = largura * r
                dim  = (int (largura2), int(altura2))#dim recebe a nova altura e largura da imagem
                image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)#utilizando uma função Opencv a imagem é redimensionada 
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#converte a imagem do Open cv para o formato RGB
                flag = {'img' :1,'gray': 0, 'f1':0, 'f2': 0, 'f3' : 0, 'canny' : 0, 'roberts': 0, 'sobelx': 0 , 'sobely': 0, 'sobel': 0, 'prewitt': 0, 'process': 0, 'draw': 0, 'undo' :0, 'crop': 0}#reseta todos os flags exceto o "img" que é colocado em 1
                imagem.set_imgcv(image)#seta o atributo sel.imgcv da classe process com a imagem selecionada
                imagem.set_flag(flag)#seta self.flag da classe process
                janela.mostrar (image)#chama o metodo mostrar e passa imagem selecionada como argumento 
            else:#se a imagem não for maior que a área de trabalho
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#converte a imagem do Open cv para o formato RGB
                flag = {'img' :1,'gray': 0, 'f1':0, 'f2': 0, 'f3' : 0, 'canny' : 0, 'roberts': 0, 'sobelx': 0 , 'sobely': 0, 'sobel': 0, 'prewitt': 0, 'process': 0, 'draw': 0, 'undo' :0, 'crop': 0}#reseta todos os flags exceto o "img" que é colocado em 1
                imagem.set_imgcv(image)#seta o atributo sel.imgcv da classe process com a imagem selecionada
                imagem.set_flag(flag)#seta self._flag da classe process
                janela.mostrar (image)#chama o metodo mostrar e passa imagem selecionada como argumento 
    

    def play (self, directoryname, sec):
        self.flag2 = 1#coloca o self.flag2 (utilizado para sinalizar a paradada sequencia) em 1
        cont = 1#cont é o contador que utlizado para contar as imagens
        ct = 0 #contador para o indice das listas
        flag3 = 0#flag3 é utlizado se a imagem está sendo mostrada, se sim, o dicionario de flags é alterado
        imgvetor = [0]
        img_namevetor = [0]
        #com esta função do Tkinter, directoryname recebe uma string com o nome do diretorio onde esta a imagem
        #directoryname = tkFileDialog.askdirectory(initialdir = "C:\Users\Gustavo\Documents",title = "Select directory")
        #sec recebe o valor da taxa de fps, se o usuário não tiver selecionado é selecionado 0.3 segundos
        #sec = configuracao.getplayseq()
        if sec == None:
            sec = 0.3
        #primeiramente as imagens são processadas e colocadas em um vetor
        while(1):
            janela.showinfo("processing")
            if len(directoryname)== 0:#verifica se nenhum diretorio foi selecionado, se a resposta for TRUE ele seta self.flag2 para 0
                self.flag2 = 0
                break
            #filename recebe o produto da concatenação do diretorio com o contador(corresponde ao nome da imagem) com a extenção .jpg.
            filename = directoryname + '/'+ str (cont) + '.jpg'#Exemplo:Home/diretório1/1.jpg
            #mg_namevetor[ct] = filename
            img_namevetor.append(filename)
            image = cv2.imread(filename)#image, utilizando uma função do Opencv, recebe a imagem
            try:#tenta pegar a altura e a largura da imagem
                height, width = image.shape[:2]
            except TypeError:#se ocorrem um TypeError é exibida uma mensagem de erro e o loop é encerrado
                tkMessageBox.showerror("Error", "select another directory!!")
                self.flag2 = 0
                break
            except AttributeError: #se ocorrer um AttributeError:
                break
            altf, largf = janela.get_fundospecifi() #pega a altura e a largura do fundo
            #se a imagem for maior que a área de trabalho ocorre o mesmo tratamento que ocorre no método import e ela é redimensionada
            if height > altf or width > largf:
                altura = image.shape[0]
                altura2 = altura
                largura = image.shape[1]
                largura2 = largura
                while altura2 > altf or largura2 > largf:
                    altura = altura2
                    largura = largura2
                    altura2 = float(altura) - 100
                    r = altura2 / altura
                    largura2 = largura * r
                dim  = (int (largura2), int(altura2))
                image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
                self.imag = image#self.imag recebe a imagem selecionada
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)# a imagem é convertida para RGB
                #imgvetor[ct] = image#após a imagem ser processada ela é armazenada em um vetor
                imgvetor.append(image)#após a imagem ser processada ela é armazenada em um vetor
                flag3 = 1#flag3 é "setado"
            else:#se a imagem não for maior que a área de trabalho:
                self.imag = image#self.imag recebe a imagem selecionada
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)# a imagem é convertida para RGB
                imgvetor.append(image)#após a imagem ser processada ela é armazenada em um vetor
                flag3 = 1#flag3 é "setado"
            cont = cont + 1#cont é incrementado. Para que seja exibido a próxima imagem
            ct = ct + 1
            self.root.update()#atualiza a jenela
        cont = 1
        info= "displaying images\nFrame rate (s) = " + str(sec)+"s"
        janela.showinfo(info)
        #após o processamento as imagens são exibidas
        if len(imgvetor) == 1:
            self.flag2 = 0
            tkMessageBox.showerror("Error", "select another directory!!")
        while self.flag2 !=0:#enquanto não é sinalizado para parar:
            start = time.time()
            self.root.update()#"atualiza a jenela" para verificar se algum botão foi pressionado
            if self.flag2 == 0:#se o botão pause foi pressionado (coloca self.flag2 em 0) ele para a sequencia saido do loop
                break
            self.imag = image#self.imag recebe a imagem selecionada
            try:
                image = imgvetor[cont]
            except IndexError:
                cont = 1
                image = imgvetor[cont]
            janela.mostrar (image)#o método mostrar é chamado e a imagem é passada como um argumento
            flag3 = 1#flag3 é "setado"
            cont = cont + 1#cont é incrementado. Para que seja exibido a próxima imagem
            end = time.time()
            tempo = end - start
            inter = sec - tempo
            if inter < 0:
                inter = 0.0
            time.sleep(inter)#faz o programa parar por 0.5s, para que seja possivel visualizar a imagem antes que a pŕoxima imagem seja exibida
        if flag3 == 1:#se o flag3 for 1, o diconŕio de flags é "setado" na classe Jenela e na classe process
            flag = {'img' :1,'gray': 0, 'f1':0, 'f2': 0, 'f3' : 0, 'canny' : 0, 'roberts': 0, 'sobelx': 0 , 'sobely': 0, 'sobel': 0, 'prewitt': 0, 'process': 0, 'draw': 0, 'undo' :0, 'crop': 0}
            imagem.set_imgcv(image)
            imagem.set_flag(flag)


    def pause (self):
        #se este método for chamado self.flag2 é colocado em 0, dessa forma o loop que está em andamento no método play é parado
        self.flag2 = 0



class info (object):
    def __init__(self, root):
        self.root = root
        
    def About(self):
        newwin = Toplevel(self.root)#cria uma nova janela
        #cria e configura um label com as informções
        display = Label(newwin, text="Programa feito pra te ajudar \n Imagens \n filtros e muito mais !", font = ('FreeSans', '12'))
        display.grid(row = 0, column = 0, padx = 10, pady = 10)

    def helpi(self):
        newwin = Toplevel(self.root)#cria uma nova janela
        n = ttk.Notebook(newwin)#cria um "Notebook", utilizando a biblioteca ttk
        #cria dois frames9f1 e f2)
        f1 = ttk.Frame(n)   
        f2 = ttk.Frame(n)
        #adiciona os frame ao notebook com os titulos de "widgets function", para f1, e "More", para f2
        n.add(f1, text='Widgets function')
        n.add(f2, text='More')
        n.grid( row = 0, column = 0, padx = 10, pady = 10)#posiciona os frames
        #cria no frame f1 um label f1l, adiciona as informações e posiciona ele  
        f1l = Label(f1, text="button 1 - process an image\n button 2- import an image\n button 3 - draw\n button 4 - crop\n button 5 - filter one (gray)\n button 6 - filter two (gamma adjust)\n button 7 - filter three (edge)\n button 8 - zoom in \n button 9 - zoom out\n \n*left, up to dow")
        f1l.grid( row = 0, column = 0, padx = 10, pady = 10)
        #cria no frame f1 um label f1l, adiciona as informações e posiciona ele
        f2l = Label(f2, text="If you want know more about \nthis amazing programm, send\n an email to:\n legal@utfpr.edu.br ")
        f2l.grid( row = 0, column = 0, padx = 10, pady = 10)



class aux (ediction):
    def __init__(self, root):
        self.root = root
        self.sec = None #sera u8sado na função auxplay
        self.imagensant = ["fim"]
        self.flagsant = [{ 'img': 1, 'gray': 0, 'f1':0, 'f2': 0, 'f3' : 0, 'canny' : 0, 'roberts': 0, 'sobelx': 0 , 'sobely': 0, 'sobel': 0, 'prewitt': 0, 'process': 0, 'draw': 0, 'undo' :1, 'crop': 0}]
        self.contflags = 0
        self.contimagens = 0
        self.contimagens_temp = 0

    def organiza_imganterior(self, imganterior):
        self.imagensant.append(imganterior)
        self.contimagens = self.contimagens + 1
        #self.organiza_flaganterior()

    def pega_imagemanterior(self):
        self.contimagens_temp = self.contimagens
        if self.contimagens >= 1:
            self.contimagens = self.contimagens - 1
            imgtemp =  self.imagensant[self.contimagens_temp]
            #self.imagensant.remove(imgtemp)
            del self.imagensant[self.contimagens_temp]
            return imgtemp
        else:
            return self.imagensant[0]

    def organiza_flaganterior(self, flaganterior):
        flaganterior = imagem.get_flaganterior()
        self.flagsant.append(flaganterior)
        self.contflags = self.contflags + 1

    def pega_flaganterior(self):
        if self.contflags != self.contimagens_temp:
            flaganterior = self.flagsant[self.contflags]
            while (self.contflags != self.contimagens_temp):
                self.flagsant.append(flaganterior)
                self.contflags = self.contflags + 1
        if self.contflags >= 1:
            cont = self.contflags
            self.contflags = self.contflags - 1
            flagtemp =  self.flagsant[cont]
            del self.flagsant[cont]
            return flagtemp
        else:
            return self.flagssant[0]

    def verifica_cor(self, imagem):
        imagem = Image.fromarray(imagem)#"imagem" recebe a imagem da qual se deseja vericar as cores, após esta ser convertida em um formato compativel com as funções da biblioteca Pillow 
        pilimage = ImageTk.PhotoImage(imagem)
        a = imagem.getcolors()#a recebe uma lista com todas as cores da imagem, sendo que se o número máximo for excedido a recebe None
        if a == None:#se "a" receber None significa que a imagem é colorida, portanto a função retorna 0
            return 0
        else:
            if len(a) == 2:#se a possuir apenas dois elementos significa que a imagem é preto e branco e a função retorna 1
                return 1
            else:#se a possuir mais que dois elementos significa que ela é colorida e a função retorna 0
                return 0


    def auxplay (self):
        def op1(diretorio, sec):
            if sec != 0:
                    self.sec = sec
            else:
                   tkMessageBox.showerror("Error", "This option is not available!")                     
        def op2(diretorio, sec):
            if sec != 0:
                    self.sec = sec
            else:
                   tkMessageBox.showerror("Error", "This option is not available!")
                                     
        def op3(diretorio, sec):
            if sec != 0 :
                    self.sec = sec
            else:
                   tkMessageBox.showerror("Error", "This option is not available!")
        def op4(diretorio, sec):
            if sec != 0 or sec == "None":
                    self.sec = sec
            else:
                   tkMessageBox.showerror("Error", "This option is not available!")

        def op5(diretorio, sec):
            #sec recebe o valor da taxa de fps, se o usuário não tiver selecionado é selecionado 0.3 segundos
            sec = configuracao.getplayseq()
            self.sec = sec

        def execute(diretorio):
            arquivo.play(diretorio, self.sec)
            newwin.destroy()

        #variaveis onde iremos armazenar os valores (em segundos) do frame rate, para ser usado na funçao play
        captura = 0
        device = 0
        real = 0
        selectedvid = 0
        selected = 0
        fpscaptura = 0
        fpsreal = 0
        fpsdevice = 0
        s_selectedvid = 0
        s_selected = 0
        #com esta função do Tkinter, directoryname recebe uma string com o nome do diretorio onde esta a imagem
        workdirectory = os.getcwd()
        directoryname = tkFileDialog.askdirectory(initialdir = workdirectory,title = "Select directory")
        texto = []#lista onde será armazenada o texto do arquivo
        arqnome = directoryname +'/info.txt'#nome do qrquivo que iremos abrir
        try:
            arq = open(arqnome, 'r')#abre o arquivo
            #coloca o texto do arquivo na lista "texto"
            for line in arq:
                texto.append(line)
            #pega o valor do frame rate real, da lista texto e coloca na variavel real
            if texto [0] == "Frame rate real { \n":
                fpsreal = texto [1]
                try:
                    fpsreal = float(fpsreal)
                    real = round((1/fpsreal), 3)
                except:
                    tkMessageBox.showerror("Error", "info.txt is corrupted or changed!")
            #pega o valor do frame rate da captura, da lista texto e coloca na variavel "captura"
            if texto [6] == "Frame rate captura{\n":
                fpscaptura = texto [7]
                try:
                    fpscaptura = float(fpscaptura)
                    captura = round((1/fpscaptura), 3)
                except:
                    tkMessageBox.showerror("Error", "info.txt is corrupted or changed!")
            #pega o valor do frame rate selecionado pelo usuario (se ele converteu de video para imagens); da lista texto e coloca na variavel "selectvid"
            if texto [6] == "frame rate selected (seconds) {\n":
                selectedvid= texto [7]
                if selectedvid == None:
                    s_selectedvid = 0
                else:
                    s_selectedvid = selectedvid
                    try:
                        selectedvid = float(selectedvid)
                    except:
                        tkMessageBox.showerror("Error", "info.txt is corrupted or changed!")
            #pega o valor do frame rate padrao do dispositivo, da lista texto e coloca na variavel "device"
            fpsdevice = texto [4]
            try:
                fpsdevice = float(fpsdevice)
                device = round((1/fpsdevice), 3)
            except:
                tkMessageBox.showerror("Error", "info.txt is corrupted or changed!")
        except:
            captura = 0
            device = 0
            real = 0
            selectedvid = 0

        selected = configuracao.getplayseq()
        if selected == None: 
            s_selected = 0.3
        else:
            s_selected = selected


        newwin = Toplevel(self.root)#cria uma nova janela
        #cria e configura um label com as informções
        display = Label(newwin, text="Select the frame rate: ")
        display.grid(row = 0, column = 0, padx = 10, pady = 10)
        op = Menubutton(newwin, text = "options")
        #op.grid()
        menu = Menu(op, tearoff = 0)
        op["menu"] = menu
        op.grid(row = 0, column = 1, padx = 10)

        nome1 = "capture - (" + str(fpscaptura) + "fps)"
        nome2 = "device specification - (" + str(fpsdevice) + "fps)"
        nome3 = "real - (" + str(fpsreal) + "fps)"
        nome4 = "selected (video capture) - (" + str(s_selectedvid) + "s)"
        nome5 = "selected - (" + str(s_selected) + "s)"

        menu.add_command(label = nome1, command = lambda: op1(directoryname, captura))
        menu.add_command(label = nome2, command = lambda: op2(directoryname, device))
        menu.add_command(label = nome3, command = lambda: op3(directoryname, real))
        menu.add_command(label = nome4, command = lambda: op4(directoryname, selectedvid))
        menu.add_command(label = nome5, command = lambda: op5(directoryname, selected))

        botao = Button(newwin, text = "Execute", command = lambda: execute(directoryname))
        botao.grid(row = 1, column = 0)


    def auxsobelx (self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:#verifica se a alguma imagem na área de trabalho
            #Antes de chamar o método para que seja realizada a edição, é necessário que o usuário defina o valor do kernel:
            newwin = Toplevel(self.root)#cria uma nova janela
            #cria e posiciona os widgets dessa janela
            l1 = Label(newwin, text="Kernel size: ")
            l1.grid(row = 0, column = 0, padx = 10, pady = 10)
            self.e1 = Entry(newwin)
            self.e1.grid ( row = 0, column = 1)
            #após o usuário digitar o valor de kernel, ele deve clicar neste botão, que chamaráo método responável por "pegar" o valor digitado e chamar o método sobelx
            b1  = Button (newwin, text = "OK", command = lambda: self.get_entry(1))#o número 1 é passado como argumento, pois ele será usado para "avisar" o método get_entry que ele precisa pegar o valor de kernel de sobelx  
            b1.grid ( row = 1, column = 0, columnspan = 2)
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")
            

    def auxsobely (self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:#verifica se a alguma imagem na área de trabalho
            #Antes de chamar o método para que seja realizada a edição, é necessário que o usuário defina o valor do kernel:
            newwin = Toplevel(self.root)#cria uma nova janela
            #cria e posiciona os widgets dessa janela
            l1 = Label(newwin, text="Kernel size: ")
            l1.grid(row = 0, column = 0, padx = 10, pady = 10)
            self.e1 = Entry(newwin)
            self.e1.grid ( row = 0, column = 1)
            #após o usuário digitar o valor de kernel, ele deve clicar neste botão, que chamaráo método responável por "pegar" o valor digitado e chamar o método sobely
            b1  = Button (newwin, text = "OK", command = lambda: self.get_entry(2))#o número 2 é passado como argumento, pois ele será usado para "avisar" o método get_entry que ele precisa pegar o valor de kernel de sobely
            b1.grid ( row = 1, column = 0, columnspan = 2)                            
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")
            

    def auxsobel (self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:#verifica se a alguma imagem na área de trabalho
            #Antes de chamar o método para que seja realizada a edição, é necessário que o usuário defina o valor do kernel:
            newwin = Toplevel(self.root)#cria uma nova janela
            #cria e posiciona os widgets dessa janela
            l1 = Label(newwin, text="Kernel size: ")
            l1.grid(row = 0, column = 0, padx = 10, pady = 10)
            self.e1 = Entry(newwin)
            self.e1.grid ( row = 0, column = 1)
            #após o usuário digitar o valor de kernel, ele deve clicar neste botão, que chamaráo método responável por "pegar" o valor digitado e chamar o método sobely
            b1  = Button (newwin, text = "OK", command = lambda: self.get_entry(3))#o número 3 é passado como argumento, pois ele será usado para "avisar" o método get_entry que ele precisa pegar o valor de kernel de sobel
            b1.grid ( row = 1, column = 0, columnspan = 2)
                                        
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")

    def auxthresh (self):
        flag = imagem.get_flag()#"flag" recebe os flags da imagem para a verificação do estado da imagem
        if flag['img'] == 1:#verifica se a alguma imagem na área de trabalho
            #Antes de chamar o método para que seja realizada a edição, é necessário que o usuário defina o valor mínimo e máximo:
            newwin = Toplevel(self.root)#cria uma nova janela
            #cria e posiciona os widgets dessa janela
            l1 = Label(newwin, text="Minimun: ")
            l1.grid(row = 0, column = 0, padx = 10, pady = 10)
            self.e1 = Entry(newwin)
            self.e1.grid ( row = 0, column = 1)
            l2 = Label(newwin, text="Maximun: ")
            l2.grid(row = 1, column = 0, padx = 10, pady = 10)
            self.e2 = Entry(newwin)
            self.e2.grid ( row = 1, column = 1)
            #após o usuário digitar o valor mínimo e máximo, ele deve clicar neste botão, que chamaráo método responável por "pegar" o valor digitado e chamar o método thresh
            b1  = Button (newwin, text = "OK", command = lambda: self.get_entry2())
            b1.grid ( row = 2, column = 0, columnspan = 2)                            
        else:
            tkMessageBox.showerror("Error", "Please import an image first!")

    def get_entry(self, onde):
                global k
                k = self.e1.get()#k recebe o valor de kernel definido
                try:#tenta converter o valor de k em um inteiro e trata esse valor
                    k = int (k)
                    #verifica se o valor selecionado esta dentro dos parametros esperados
                    if k > 31:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 31")
                    elif k<0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        #verifica se o numero é par ou ímpar
                        a = k % 2
                        if a == 0:#se for par ele é incrementado em 1
                            k = k + 1
                        else:
                            k = k
                        self.e1.delete(0,END)
                        if onde ==1:#se o argumento passado ao chamar essa função for 1 significa que ele foi chamado para pegar o valor de kernel do sobelx 
                            filtrosb.sobelx(k)#portanto ele irá chamar o método da classe process responsável por esse filtro e passará o velor de kernel como um argumento
                        elif onde == 2:#se o argumento passado ao chamar essa função for 2 significa que ele foi chamado para pegar o valor de kernel do sobely
                            filtrosb.sobely(k)#portanto ele irá chamar o método da classe process responsável por esse filtro e passará o velor de kernel como um argumento
                        elif onde == 3:#se o argumento passado ao chamar essa função for 3 significa que ele foi chamado para pegar o valor de kernel do sobel
                            filtrosb.sobel(k)#portanto ele irá chamar o método da classe process responsável por esse filtro e passará o velor de kernel como um argumento
                except ValueError:#se ocorrer um TypeError significa que o usuário não digitou apenas números, portanto uma mensagem de erro é exibida
                    tkMessageBox.showerror("Error", "Invalid entry")
                    
    def get_entry2(self):
                global k
                #mi e mx recebem o valor mínimo e máxio respectivamente
                mi = self.e1.get()
                mx = self.e2.get()
                try:#tenta converter o valor de mi e mx para inteiro e tratar esses valores
                    mi = int (mi)
                    mx = int (mx)
                    #verifica se o valor selecionado esta dentro dos parametros esperados
                    if mi > 255 or mx > 255:
                        tkMessageBox.showerror("Error", "Maximun kernel size = 255")
                    elif mi < 0 or mx < 0:
                        tkMessageBox.showerror("Error", "Invalid entry")
                    else:
                        filtrosg.thresh(mi, mx)#chama o método thresh da calle process e passa o valor mínimo e máximo como argumento
                                                    
                except ValueError:#se ocorrer um TypeError significa que o usuário não digitou apenas números, portanto uma mensagem de erro é exibida
                    tkMessageBox.showerror("Error", "Invalid entry")




class setings(object):
    """docstring for setings"""
    def __init__(self, root):
         self.root = root
         self.sleept = 0.0
         self.framelim = None

         self.micro_intervalo = None
         self.micro_quantframe = None
         self.diretorio = None

         self.sec = None
    def conf(self):
        newwin = Toplevel(self.root)#cria uma nova janela
        n = ttk.Notebook(newwin)#cria um "Notebook", utilizando a biblioteca ttk
        #cria os frames que serão as basers para as abas
        f1 = ttk.Frame(n)   
        f2 = ttk.Frame(n)
        f3 = ttk.Frame(n)
        #adiciona os frame ao notebook com os titulos de "widgets function", para f1, e "More", para f2
        n.add(f1, text='Frame capture')
        n.add(f2, text='Microscope capture')
        n.add(f3, text = 'Play')
        n.grid( row = 0, column = 0, padx = 10, pady = 10)#posiciona os frames

        #Na primeira aba o usuário poderá configurar o tempo entre a captura dos frames e o um numero limite de frames
        #cria no frame f1 dois label, adiciona as informações e posiciona ele  
        f1l1 = Label(f1, text="Frame Rate(seconds)")
        f1l1.grid( row = 0, column = 0, padx = 10, pady = 10)
        f1l2 = Label(f1, text="frame limit")
        f1l2.grid( row = 1, column = 0, padx = 10, pady = 10)
        #cria dus caixas de entrada
        self.f1e1 = Entry (f1)#nesta o usuário deverá colocar o tempo entre a captura dos frames
        self.f1e1.grid(row = 0, column = 1, padx = 5)
        self.f1e2 = Entry (f1)#nesta o usuário deverá colocar o limite de frames
        self.f1e2.grid(row = 1, column = 1, padx = 5)
        b1 = Button(f1, text = "Save", command = self.framecap)
        b1.grid(row = 2, column = 0, columnspan = 2)

        #Na segunda aba o usuário poderá configurar se ele deseja que o programa capture automaticamente os frames do microscopio e a quantidade de frames capturados
        #cria no frame f2 dois label, onde sera informado qual o valor que o usuário deve colocar, e posiciona eles
        f2l1 = Label(f2, text = "Capture interval (frame)")
        f2l1.grid( row = 0, column = 0, padx = 10, pady = 10)
        f2l2 = Label(f2, text="frame limit")
        f2l2.grid( row = 1, column = 0, padx = 10, pady = 10)
        #cria dus caixas de entrada
        self.f2e1 = Entry (f2)#nesta o usuário deverá colocar o intervalo entre a captura dos frames
        self.f2e1.grid(row = 0, column = 1, padx = 5)
        self.f2e2 = Entry (f2)#nesta o usuário deverá colocar o limite de frames
        self.f2e2.grid(row = 1, column = 1, padx = 5)
        b2 = Button(f2, text = "Save", command = self.microcap)
        b2.grid(row = 2, column = 0, columnspan = 2)

        #Na terceira aba o usuário poderá selecionar a texa de exibição, em fps, que ele deseja para a função Play
        #cria no frame f3 um label e posiciona ele
        f3l1 = Label(f3, text = "Frame Rate")
        f3l1.grid(row =0, column = 0, padx = 10, pady = 10)
        #cria uma caixa de entrada
        self.f3e1 = Entry (f3)
        self.f3e1.grid(row = 0, column = 1, padx = 5)
        #cria botão que ativa a função que pega io valor selecionado
        b3 = Button(f3, text = "Save", command = self.playseq)
        b3.grid(row = 1, column = 0, columnspan = 2) 


    #Configura a função frame capture
    def framecap (self):
        sleept = self.f1e1.get()
        framelim = self.f1e2.get()
        try:#tenta converter o valor de sleept e framelim para inteiro e tratar esses valores
            self.sleept = float(sleept)
            self.framelim = int(framelim)
            if self.sleept < 0.0:
                tkMessageBox.showerror("Error", "Invalid entry1")  
            if self.framelim == 0:
                self.framelim = None
            if self.framelim < 0 :
                tkMessageBox.showerror("Error", "Invalid entry1")          
        except ValueError:#se ocorrer um TypeError significa que o usuário não digitou apenas números, portanto uma mensagem de erro é exibida
            tkMessageBox.showerror("Error", "Invalid entry")
    def getframeparametros(self):
        return (self.sleept, self.framelim)

    #configura a função microscope
    def microcap (self):
        intervalo = self.f2e1.get()
        quantframe = self.f2e2.get()
        try:#tenta converter o valor de intervalo e quantframe para inteiro e tratar esses valores
            self.micro_intervalo = int(intervalo)
            self.micro_quantframe = int(quantframe)
            if self.micro_intervalo < 1:
                tkMessageBox.showerror("Error", "Invalid entry1")  
            if self.micro_quantframe < 1 :
                tkMessageBox.showerror("Error", "Invalid entry1")
            if self.micro_intervalo >= 1:
                workdirectory = os.getcwd()
                directoryname = tkFileDialog.askdirectory(initialdir = workdirectory,title = "Select directory  where the images will be save")#através desta função o usuário pode selecionar o diretorio onde as imagens serão salvas
                if len(directoryname) > 0:
                    self.diretorio = directoryname
                else:
                    self.micro_intervalo = None
                    self.micro_quantframe = None
                    tkMessageBox.showerror("Error", "Please select a directory")
        except ValueError:#se ocorrer um TypeError significa que o usuário não digitou apenas números, portanto uma mensagem de erro é exibida
            tkMessageBox.showerror("Error", "Invalid entry")
    def getmicroparametros(self):
        return (self.micro_intervalo, self.micro_quantframe, self.diretorio)

    #configura função play
    def playseq(self):
        fps = self.f3e1.get()
        try:#tenta converter o valor de intervalo e quantframe para inteiro e tratar esses valores
            fps = float(fps)
            if fps < 0:
                tkMessageBox.showerror("Error", "Invalid entry")
            else:
                self.sec = round((1/fps), 3)
        except ValueError:#se ocorrer um TypeError significa que o usuário não digitou apenas números, portanto uma mensagem de erro é exibida
            tkMessageBox.showerror("Error", "Invalid entry")
    def getplayseq(self):
        return self.sec




class vid(object):
    """docstring for setings"""
    def __init__(self, root):
         self.root = root

    def micro(self):
        def mostracaptura(file):
            if len(file)>0:#verifica se filename não está vazio
                image = cv2.imread(file)#carrega a imagem em image, utilizando uma função do Open cv
                height, width = image.shape[:2]#pega a altura e a largura da imagem
                if height > 950 or width > 1740:#verifica se a imagem  não é maior que a area de trabalho
                    #Ajuste do tamanho
                    altura = image.shape[0]# altura recebe um numero int que é a atura da imagem
                    altura2 = altura #faz uma cópia desse valor em altura2
                    largura = image.shape[1]#largura recebe um numero int que é a largura desta imagem
                    largura2 = largura#faz uma copia desse valor em largura2 
                    #enquanto a imagem for maior que a area de trabalho ele irá diminuir a altura um 100 pixels e diminuirá a largura proporcionalmente
                    while altura2 > 950 or largura2 > 1740:
                        altura = altura2
                        largura = largura2
                        altura2 = float(altura) - 100
                        r = altura2 / altura
                        largura2 = largura * r
                    dim  = (int (largura2), int(altura2))#dim recebe a nova altura e largura da imagem
                    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)#utilizando uma função Opencv a imagem é redimensionada 
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#converte a imagem do Open cv para o formato RGB
                    flag = {'img' :1,'gray': 0, 'f1':0, 'f2': 0, 'f3' : 0, 'canny' : 0, 'roberts': 0, 'sobelx': 0 , 'sobely': 0, 'sobel': 0, 'prewitt': 0, 'process': 0, 'draw': 0, 'undo' :0, 'crop': 0}#reseta todos os flags exceto o "img" que é colocado em 1
                    imagem.set_imgcv(image)#seta o atributo sel.imgcv da classe process com a imagem 
                    imagem.set_flag(flag)#seta self.flag da classe process
                    janela.mostrar (image)#chama o metodo mostrar e passa imagem como argumento 
                else:#se a imagem não for maior que a área de trabalho
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#converte a imagem do Open cv para o formato RGB
                    flag = {'img' :1,'gray': 0, 'f1':0, 'f2': 0, 'f3' : 0, 'canny' : 0, 'roberts': 0, 'sobelx': 0 , 'sobely': 0, 'sobel': 0, 'prewitt': 0, 'process': 0, 'draw': 0, 'undo' :0, 'crop': 0}#reseta todos os flags exceto o "img" que é colocado em 1
                    imagem.set_imgcv(image)#seta o atributo sel.imgcv da classe process com a imagem 
                    imagem.set_flag(flag)#seta self._flag da classe process
                    janela.mostrar (image)#chama o metodo mostrar e passa imagem como argumento 
        cont = 0#conta quantos frames foram exibidos- usado para a função frame capture
        cont2 =0##conta quantos frames foram exibidos- usado para calculo do frame rate
        ct = 1 #conta quantos frames foram capturados
        tempo = 0
        tempo2 = 0
        tempocap = 0
        captura = cv2.VideoCapture(1)#através desta função da biblioteca Open cv nós temos acesso a camera externa
        intervalo, quant, diretorio = configuracao.getmicroparametros()#se o usuário configurou um intervalo para captura de imagens, é pego esses valores
        tkMessageBox.showinfo("Notice", "Press 'esc' to go out and 'space' capture an image")
        start = time.time()
        captura.set(3, 480)
        captura.set(4, 640)
        while 1:
            start2 = time.time()#comeca a contagem de tempo
            ret, frame = captura.read()#lemos um frame que vem da camêra externa
            try:
                cv2.imshow("Video", frame)#exibimos essa imagem em uma janela do Opencv
            except:
                tkMessageBox.showerror("Error", "Please check if the microscope is conected")#se não houver nenhuma camera conectada
                break
            cont = cont + 1#incrementamos o contador de frames exibidos
            if intervalo != None:#se o usuario configurou algum valor de intervalo
                if intervalo == cont:#se o valor do intervalor for igual ao valor do contador de frames
                    if ct <= quant:#se o numero de frames capturados for inferior ao limite de frames capturados
                        if ct == 1:
                            startcap = time.time()#comeca a contagem de tempo da captura de frames
                        #se todas as condições acima foram obedecidas é executado a captura do frame que esta sendo exibida: 
                        name = diretorio + '/' + str(ct) + '.jpg'#concatenamos algumas strings para dar nome ao arquivo, ex: diretorio1/diretorio2 + / + 1 + .jpg = diretorio1/diretorio2/1.jpg 
                        #mostramos o nome do arquivbo salvo na barra de informações
                        showname = 'Creating...' + name
                        janela.showinfo(showname)
                        self.root.update()#atualizamos a janela para que este seja exibida
                        cv2.imwrite(name, frame)#através desta função do Opencv nós salvamos o frame lido anteriormente como uma imagem, cujo nome corresponde a string na variavel "name"
                        #mostramos a imagem criada na area de trabalho
                        mostracaptura(name)#acionamos a função que mostara a imagem salva na area de trabalho do programa
                        self.root.update()#atualizamos a janela para que a imagem seja exibida
                        cont = 0#zera o contador, para recomeçar a contagem do inervalo
                        ct = ct + 1#incrementamos em 1 o contador de imagens
                        if ct == (quant + 1):#se for o ultimo frame a contagem de tempo para
                            endcap = time.time()
                            tempocap = endcap - startcap#tempocap recebe o valor do intervalo de tempo de captura 
                            intervalo = None
            k = cv2.waitKey(1) & 0xff
            if k == 27:#se o usuario pressionar a tecla 'esc' o loop é encerrado
                break
            if k == 32:#se o usuário precionar 'space' é feita a captura do frame que esta sendo exibido:
                if diretorio == None:#se o usuario ainda não tiver selecionado um diretorio onde a imagem sera salva
                    workdirectory = os.getcwd()#pega o directorio em que o programa esta
                    diretorio = tkFileDialog.askdirectory(initialdir = workdirectory,title = "Select directory  where the images will be save")#através desta função o usuário pode selecionar o diretorio onde as imagens serão salvas
                name = diretorio + '/' + str(ct) + '.jpg'#concatenamos algumas strings para dar nome ao arquivo, ex: diretorio1/diretorio2 + / + 1 + .jpg = diretorio1/diretorio2/1.jpg 
                #mostramos o nome do arquivbo salvo na barra de informações
                showname = 'Creating...' + name
                janela.showinfo(showname)
                self.root.update()
                cv2.imwrite(name, frame)#através desta função do Opencv nós salvamos o frame lido anteriormente como uma imagem, cujo nome corresponde a string na variavel "name"
                #mostramos a imagem criada na area de trabalho
                mostracaptura(name)#acionamos a função que mostara a imagem salva na area de trabalho do programa
                self.root.update()#atualizamos a janela para que a imagem seja exibida
                ct = ct + 1#incrementamos em 1 o contador de imagens
                continue
            cont2 = cont2 + 1
            end2 = time.time()#paramos a contagem de tempo do ciclo
            if cont2 <= 100:
                tempo2 = tempo2 + (end2 - start2)#tempo2 recebe o valor acumulado do tempo de execução do loop
        if cont != 0:
            frame_rate2 = round((100/tempo2), 3)#cacula o frame rate da camera
        if tempocap != 0:
            frame_ratecap = round((quant/tempocap), 3)#calcula o frame rate da captura
            #cria um arquivo .txt com as informações de execução
            dia = datetime.datetime.now()
            testo = ["Frame rate real { \n", str(frame_rate2), "\n}\n", "Frame rate device { \n30\n}\n", "Frame rate captura{\n", str(frame_ratecap),"\n}\n" , "Frame { \n", str(cont2), "\n}\n", "process finished in: ", str(dia) ]
            end = diretorio+'/info.txt'
            arq = open ( end, 'w')
            arq.writelines(testo)
            arq.close()
        elif tempocap == 0 and ct != 1:
            #se o usário apenas realizou algumas capturas manualmente será criado um arquivo .txt, porém sem o frame rate da captura
            dia = datetime.datetime.now()
            testo = ["Frame rate real { \n", str(frame_rate2), "\n}\n", "Frame rate device { \n30\n}\n", "Frame { \n", str(cont2), "\n}\n", "process finished in: ", str(dia) ]
            end = diretorio +'/info.txt'
            arq = open ( end, 'w')
            arq.writelines(testo)
            arq.close()
        captura.release()
        cv2.destroyAllWindows()



        
drawing=False
mode=True 

#instanciando as classes
raiz = Tk()
janela = Janela(raiz)
filtrosg = generalfilters()
filtrosb = borderfilters()
ferramentas = tools(raiz)
imagem = image()
arquivo = filesop(raiz)
informacao = info(raiz)
auxiliar = aux(raiz)
video = vid(raiz)
configuracao = setings(raiz)

#fullscreen 
w, h = raiz.winfo_screenwidth()-3, raiz.winfo_screenheight()-3
raiz.geometry("%dx%d+0+0" %(w, h))
#titulo da janela
raiz.title("Modelo 01")
#icone do programa
imgicon =  ImageTk.PhotoImage(file='icone6.ico')
raiz.tk.call('wm', 'iconphoto', raiz._w, imgicon)
#cor do backgraund da janela
raiz["bg"] = 'gray'
raiz.mainloop()


#############################################
'''
Se o comentário estiver acima de uma linha de código, enmtão ele explicará o trecho do código abaixo dele
Se o comentário estiver ao lado de uma linha de código, então ele explicará apenas aquela linha em espefico
'''
