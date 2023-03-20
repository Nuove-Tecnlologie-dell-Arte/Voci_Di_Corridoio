import RPi.GPIO as GPIO
import time
import os
import re
import pygame
from Sensore import *
from PIL import Image
from os import path
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import subprocess

#Inizializzazione della finestra in cui viene visualizzato il calligramma
pygame.init()
WINDOW_WIDTH = 1360
WINDOW_HEIGHT = 768
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))#,pygame.FULLSCREEN,0, 32
screen.fill((255, 255, 255))
pygame.display.set_caption("Voci Di Corridoio")
pygame.mouse.set_visible(False)
immagine = pygame.image.load("grafico.png")
labelDisplayC= immagine.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
screen.blit(immagine, labelDisplayC)
subprocess.Popen(["python", "/home/raspy/Desktop/vdc/audioPlay.py"])
args = ["-t", "7"]
running = True
if __name__ == '__main__':
	while running==True:

		#Printa la distanza del sensore ad Ultrasuoni dalla superfice
		dist = distance()
		print ("Measured Distance = %.1f cm" % dist)

		#if che si attiva quando la distanza è inferiore agli 80cm
		if dist < 1200:
			
			#Comando che avvia il sottoprogramma che registra l'audio e lo trasforma in testo
			subprocess.Popen(["python", "/home/raspy/Desktop/vdc/registraAudio.py"]+args)#os.system("python /home/raspy/Desktop/vdc/registraAudio.py -t 7") #Per cambiare il tempo di registrazione cambiare il numero dopo -t (l'unità di tempo sono i secondi)
			
			#Apertura del file scritto dal sottoprogramma ed inserimento del testo completo nella variabile text
			with open("testo.txt", "r") as file: 
				df = file.read()
			text = str(df)

			#Generazione del Calligramma tramite la libreria WordCloud e MatPlotLib (documentazione per altre impostazioni https://amueller.github.io/word_cloud/index.html)
			maschera = np.array(Image.open("/home/raspy/Desktop/vdc/orecchia.png"))
			wordcloud = WordCloud(
				contour_width=1,
				contour_color = 'steelblue',
				width = 1920,
				height = 1080,
				background_color ='white',
				stopwords = STOPWORDS,
				min_font_size = 5,
				#mask = maschera
			).generate(text) 
			#Il codice è scritto così per essere più leggibile, potrebbe essere scritto tutto sulla stessa riga
			plt.figure(figsize = (13.6, 7.68), facecolor = None)
			#plt.figure(figsize = (13.6, 7.68), facecolor = None) #Cercare il modo di crearla 1920*1080 
			plt.imshow(wordcloud)
			plt.axis("off")
			plt.tight_layout(pad = 0)

			#Salvataggio del Calligramma come PNG
			plt.savefig("grafico.png")

			#Visualizzazione dell'immagine su interfaccia (non viene usata quella di MatPlotLib perché blocca l'esecuziode del loop del programma fino alla sua chiusura)
			immagine = pygame.image.load("grafico.png")
			labelDisplayC= immagine.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
			screen.blit(immagine, labelDisplayC)
			#screen.blit(immagine,(0, 0))#commentate questo e provate il codice di sopra per centrare l'immagine se viene decentrata
			pygame.display.update()
			time.sleep(0.1)

		#Chiudi il programma con ESC
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running= False
	pygame.quit()

