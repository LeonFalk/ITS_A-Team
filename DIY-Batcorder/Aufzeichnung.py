import pyaudio
import wave
import time
import os
from datetime import datetime as DateTime
from scipy.fft import fft
import numpy as np
from array import array


#PyAudio Processing
SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
swidth = 2

#Abfrage Posttrigger 
posttrigger = input("Set posttrigger in ms:  ")
posttrigger = int(posttrigger)
post_sek = posttrigger * 0.001
length = 1
TIMEOUT_LENGTH = length + post_sek

#Abfrage minimale Lautstärke
vol = input("Set audio threshold:   ")
vol = int(vol)
Threshold = vol

#Abfrage minimale Frequenz 
freq = input("Set lower cut off frequency in Hz: ") 
freq =  int(freq)

#dateispeicherung
f_name_directory = r'/home/pi/Documents/DYI-Badcorder/Audioaufnahmen'



class Alexa:
    
    def fourier(self, samples2):
        data_chunk = array('h' , samples2)
        Y = fft(data_chunk)
        #halbierung des Datensatzes für Leistungsoptimierung
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

    def record(self):
        print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:

            data = self.stream.read(chunk)
            #2. Audiogate zur automatischen Verlängerung des Timers
            if max(self.fourier(data)) >= Threshold: 
                end = time.time() + TIMEOUT_LENGTH
            
            current = time.time()
            rec.append(data)
        self.write(b''.join(rec))

    def write(self, recording):

        now = DateTime.now()
        #Implementation Timestamp, Formatierung hier nach Belieben ändern
        date_time = now.strftime("%d-%m-%Y, %H-%M-%S")
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
        #1. Audiogate
        while True:
            audioin = self.stream.read(chunk)
            fftfreq = self.fourier(audioin)
            if max(fftfreq) >= Threshold:
                self.record()

a = Recorder()

a.listen()

