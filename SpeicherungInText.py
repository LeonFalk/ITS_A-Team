# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 16:05:39 2021

@author: Leon
Quelle: https://www.python-lernen.de/in-dateien-schreiben.htm
"""

###Textdatei öffnen und ausgeben
###############################################################################
#datei = open('Testdokument.txt', 'r') #-> 'r' für Read
#print (datei.read())
###############################################################################

###Textdatei öffnen und anhängen
###############################################################################
#datei = open('Testdokument.txt', 'a') #-> 'a' für Anhängen
#datei.write("\nZusatzhinweis")
###############################################################################

###Textdatei Überschreiben
###############################################################################
#datei = open('textdatei.txt','w')   #-> Überschreibt den Inhalt  
#datei.write("\rZusatzhinweis")
###############################################################################

###Textdatei öffnen und schreiben -> aufpassen. Liest schneller, als das System schreibt
###############################################################################
#datei = open('Testdokument.txt', 'r+') #-> 'r+' für Read and Write
#datei.write('neue Zeile')
#print (datei.read())
###############################################################################

import sys
from collections import namedtuple
from datetime import datetime as DateTime, timedelta as TimeDelta
from time import sleep


datei = open('Testdokument.txt', 'a') 
now = DateTime.now()
datei.write(now)
