# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 17:22:32 2021

@author: nhlad
"""
import pyaudio
import math
import struct
import wave
import time
import os
from datetime import datetime as DateTime
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


#Abfrage Posttrigger 
posttrigger = input("Posttigger in Millisekunden eingegben:  ")
posttrigger = int(posttrigger)
post_sek = posttrigger * 0.001
length = 1


TIMEOUT_LENGTH = length + post_sek



#Abfrage minimale Lautstärke
vol = input("Minimallautstärke eingeben:   ")
vol = int(vol)
Threshold = vol



#Abfrage minimale Frequenz 
freq = input("Minimalfrequenz eingeben: ") 
freq =  int(freq)

#dateispeicherung
f_name_directory = r'C:\Users\nhlad\OneDrive - haw-hamburg.de\ITS\Niggi'



class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000
    
    def fourier(self, samples2):
        data_chunk = array('h' , samples2)
        Y = fft(data_chunk)
        Y = Y[0:round(len(Y)/2)]
        YMag = np.abs(Y)
        YMag = YMag.astype(int)
        n = 2 * freq * int(len(YMag))/RATE 
        n = int(n)
        fft_freq = YMag[n:]
        #maxfreq = np.amax(fft_freq)
        #print(max(fft_freq))
        
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
        print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:

            data = self.stream.read(chunk)
            
            if max(self.fourier(data)) >= Threshold: end = time.time() + TIMEOUT_LENGTH
            
            current = time.time()
            rec.append(data)
        self.write(b''.join(rec))

    def write(self, recording):
        #n_files = len(os.listdir(f_name_directory))
        now = DateTime.now()
        date_time = now.strftime("%d-%m-%Y, %H-%M-%S")
        #filename = os.path.join(f_name_directory, '{}.wav'.format(n_files)) #Weilistoriginal
        filename = os.path.join(f_name_directory, '{}.wav'.format(date_time))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        print('Written to file: {}'.format(filename))
        print('Returning to listening')



    def listen(self):
        print('Listening beginning')
        while True:
            audioin = self.stream.read(chunk)
            
            #data_chunk = array('h' , input)
            #Y = fft(data_chunk)
            #Y = Y[0:round(len(Y)/2)]
            #YMag = np.abs(Y)
            #print(len(YMag))
            #n = 2 * freq * int(len(YMag))/RATE 
            #n = int(n)
            #print(audioin.size)
            fftfreq = self.fourier(audioin)
            #freqmaxamp = max(fftfreq)
            #print(freqmaxamp)
            #rms_val = self.rms(fftfreq)
            if max(fftfreq) >= Threshold:
                self.record()
            #if rms_val > Threshold:
                #self.record()

a = Recorder()

a.listen()

#data_chunk = array('h' , input)
#Y = fft(data_chunk)
#Y = Y[0:round(len(Y)/2)]
#YMag = np.abs(Y)
