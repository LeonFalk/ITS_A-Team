# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 17:22:32 2021

@author: nhlad
"""
import pyaudio
import time
from scipy.fft import fft
import numpy as np
from array import array

#Pyaudio Parameter
SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
swidth = 2

#Länge der Aufzeichnung
TIMEOUT_LENGTH = 4
print('Welcome, I`m Siri, your calibration tool for your PiPi Badcorder.')

#Abfrage minimale Frequenz 
freq = input("Input target minimum Frequency for ALEXA on PiPi: ") 
freq =  int(freq)


class Siri:
  
    def fourier(self, samples2):
        data_chunk = array('h' , samples2)
        Y = fft(data_chunk)
        #halbierung des Datensatzes zur Leistungsoptimierung
        Y = Y[0:round(len(Y)/2)]
        YMag = np.abs(Y)
        YMag = YMag.astype(int)
        #Mit dieser Gleichung finden wir den Index der geschten Freq im Array
        n = 2 * freq * int(len(YMag))/RATE 
        n = int(n)
        fft_freq = YMag[n:]
        
        return fft_freq


    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)


    def analyze(self):
        
        rec = []
        rec_max = []
        rec_min = []
        rec_avg = [] 
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:

            data = self.stream.read(chunk)
            fftfreq = self.fourier(data)
            
            current = time.time()
            rec.append(fftfreq)
        #Da wir pro Chunk ein Array mit dem Signalspektrum haben, bilden wir die mittelwerte für jedes Array    
        for i in rec:   
            rec_max.append(max(i))
            rec_min.append(min(i))
            rec_avg.append(sum(i) / len(i))
        #Jetzt werden aus der Menge an Werten einzelne werte gezogen oder errechnet   
        rec_max = max(rec_max)
        rec_min = int(sum(rec_min) / len(rec_min))
        rec_avg = int(sum(rec_avg) / len(rec_avg))
        
        return rec_max, rec_min, rec_avg
    
    
    def countdown(self):
        
        current = 5
        while current > 0:
            
            print(current)
            time.sleep(1)
            current = current - 1
            

    def runner(self):
        
        #Rauschpegelmessung
        print('First: Base noise! Be quiet and get everyone to shut up! Starting in')
        self.countdown()
        print('ready or not, starting now!')
        noise_max, noise_min, noise_avg = self.analyze()
        print('Your average noise level:', noise_avg, '. With max:', noise_max, 'and min:', noise_min)
        
        #Signalpegelmessung
        print('And now: get ready to make some Noise! Starting in')
        self.countdown()
        print('Go!')
        sig_max, sig_min, sig_avg = self.analyze()
        print('Your average input level:', sig_avg, '. With max:', sig_max, 'and min:', sig_min)    
        print('All done! We advise to set your Gate to a value between', noise_max, 'and', sig_min)
            

a = Siri()

a.runner()