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

#Threshold = 10

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
swidth = 2

#Länge der Aufzeichnung
TIMEOUT_LENGTH = 2

print('Welcome, I`m Siri, your calibration tool for your PiPi Badcorder.')


#Abfrage minimale Frequenz 
freq = input("Input target minimum Frequency for ALEXA on PiPi: ") 
freq =  int(freq)


class Siri:

    
    
    def fourier(self, samples2):
        data_chunk = array('h' , samples2)
        Y = fft(data_chunk)
        Y = Y[0:round(len(Y)/2)]
        YMag = np.abs(Y)
        YMag = YMag.astype(int)
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

    def record(self):
        
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
       
        for i in rec:   
            rec_max.append(max(i))
            rec_min.append(min(i))
            rec_avg.append(sum(i) / len(i))
            
        rec_max = max(rec_max)
        #rec_min = min(rec_min)
        rec_min = int(sum(rec_min) / len(rec_min))
        rec_avg = int(sum(rec_avg) / len(rec_avg))
        #print('Your average input level:', rec_avg, '. With max:', rec_max, 'and min:', rec_min)
        
        return rec_max, rec_min, rec_avg
    
    def countdown(self):
        
        current = 5
        
        while current > 0:
            
            print(current)
            time.sleep(1)
            current = current - 1
        



    def runner(self):
        
        #noise-evaliuation
        print('First: Base noise! Be quiet and get everyone to shut up! Starting in')
        self.countdown()
        print('ready or not, starting now!')
        noise_max, noise_min, noise_avg = self.record()
        print('Your average noise level:', noise_avg, '. With max:', noise_max, 'and min:', noise_min)
        
        #signal evaliuation
        print('And now: get ready to make some Noise! Starting in')
        self.countdown()
        print('Go!')
        sig_max, sig_min, sig_avg = self.record()
        print('Your average input level:', sig_avg, '. With max:', sig_max, 'and min:', sig_min)    
        print('All done! We advise to set your Gate to a value between', noise_max, 'and', sig_min)
            

a = Siri()

a.runner()

#data_chunk = array('h' , input)
#Y = fft(data_chunk)
#Y = Y[0:round(len(Y)/2)]
#YMag = np.abs(Y)
