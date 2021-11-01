# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 16:28:18 2021

@author: Elvin Flores
"""
import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile 
from winsound import*
import pyaudio 
import wave
def codeRecording():
    #=============== PARAMETROS DE GRABACION ===============#
    Format = pyaudio.paInt16 # formato en cadena de 16-bits binarios
    Channel = 2 # Canales del microfono de Laptop
    Rate = 44100 # Muestras de sonido tomadas por segundo (Hz)
    Chunk = 1024 # Numero de muestras por buffer
    Tiempo = 5 # Segundos a grabar
    sound='Audios/claveA.wav' # Nombre del archivo a grabar
    Audio = pyaudio.PyAudio() # Espacio para portAudio
    #=============== INICIO DE GRABACIÓN ===============#
    # Genera un espacio para grabar o reproducir un audio 
    Sonido = Audio.open(format = Format, channels = Channel, rate = Rate,input = True, output = True, frames_per_buffer = Chunk)

    print('Inicia la grabacion')
    datos = []
    rec = []
    for i in range (0, int(Rate/Chunk*Tiempo)): # Iteraciones necesarias para guardar las muestras de la grabación del Tiempo determinado
        datos.append(Sonido.read(Chunk)) # Lectura de muestras 
        rec.append(np.frombuffer(Sonido.read(Chunk), dtype=np.int16)) # Guardado de muestras
    
    senal = np.hstack(rec) # Apila el arreglo por columnas
    
    print('Termina la grabacion')
    Sonido.stop_stream() # Para la grabación
    Sonido.close() # Cierra el espacio de grabación
    Audio.terminate() # Se cierra el espacio para portAudio
    #=============== GUARDADO EN FORMATO .WAV ===============#
    wF = wave.open(sound, 'wb')
    wF.setnchannels(Channel)
    wF.setsampwidth(Audio.get_sample_size(Format))
    wF.setframerate(Rate)
    wF.writeframes(b''.join(datos))
    wF.close()
    
    # muest,senal=wavfile.read('Audios/claveElvin.wav')
    senalN=senal/np.max(senal)
    # plt.figure(1)
    # plt.plot(senalN)
    senalBin = np.where(np.abs(senalN) >= 0.3, 1, 0) # Elimina todo valor de señal debajo de 0.1 (ruido estatico)
    # plt.figure(2)
    # plt.plot(senalBin)
    senalProm = []
    for i in range (0, len(senalBin)-440, 1):
        senalProm.append(np.mean( senalBin[i : i+440] ))
        
    for i in range(len(senalProm)):
        if(senalProm[i]!=0):
            limI=i
            break
    for i in range(len(senalProm)-1,0,-1):
        # print(i)
        if(senalProm[i]!=0):
            limD=i
            break
    senalWord=[0]
    for i in range(limI,limD):
          senalWord.append(senalProm[i])
    senalWord.append(0)
    
    return senalWord
#=============== Termina Grabaciónde señal ===============#
def signIdentify(senal):
    #=============== Prueba de identificación de elementos ===============#
    letras=[]
    # letra=[0,0]
    for i in range(0,len(senal)-1,1):
        if(senal[i]==0 and senal[i+1]!=0 ):
            letras.append([])
            letras[len(letras)-1].append(i+1)
        if(senal[i]!=0 and senal[i+1]==0 ):
          letras[len(letras)-1].append(i)  
    #=============== Calculo de distancias ===============#
    letter=[]
    
    # intDot=np.mean([2191,2483,2103,1397,1457,1292])
    # intLine=np.mean([7421,8302,8621])
    
    for i in range(0,len(letras),1):
        dif=np.abs(letras[i][0]-letras[i][1])
        print('Diferencia Interna:',dif)
        if(dif>=4000 and dif<=8000):
            letter.append('Dot')
        if(dif>=14000 and dif<=17000):
            letter.append('Line')
    intrm=[]
    
    # intSen=np.mean([5216,6744,6467,5715,4744,5537])
    # intLet=np.mean([16067,13901])
    
    for i in range(0,len(letras)-1,1):
        dif=np.abs(letras[i][1]-letras[i+1][0])
        print('Diferencia Externa:',dif)
        if(dif>=7600 and dif<=10000):
            intrm.append('Senal')
        if(dif>=23000 and dif<=28000):
            intrm.append('Letra')
    intrm.append('Letra')
    word=[]
    print(len(letter))
    print(len(intrm))
    for i in range(0,len(letras),1):
        word.append(letter[i])
        
        word.append(intrm[i])
        
    return word
    # return []
#=============== Termina Identificación de señal ===============#
def asignLetter(letra):
    crter=''
    if(letra=='o-'):
        crter=crter+'A'
    if(letra=='-ooo'):
        crter=crter+'B'
    if(letra=='-o-o'):
        crter=crter+'C'
    if(letra=='-oo'):
        crter=crter+'D'
    if(letra=='o'):
        crter=crter+'E'
    if(letra=='oo-o'):
        crter=crter+'F'
    if(letra=='--o'):
        crter=crter+'G'
    if(letra=='oooo'):
        crter=crter+'H'
    if(letra=='oo'):
        crter=crter+'I'
    if(letra=='o---'):
        crter=crter+'J'
    if(letra=='-o-'):
        crter=crter+'K'
    if(letra=='o-oo'):
        crter=crter+'L'
    if(letra=='--'):
        crter=crter+'M'
    if(letra=='-o'):
        crter=crter+'N'
    if(letra=='---'):
        crter=crter+'O'
    if(letra=='o--o'):
        crter=crter+'P'
    if(letra=='--o-'):
        crter=crter+'Q'
    if(letra=='o-o'):
        crter=crter+'R'
    if(letra=='ooo'):
        crter=crter+'S'
    if(letra=='-'):
        crter=crter+'T'
    if(letra=='oo-'):
        crter=crter+'U'
    if(letra=='ooo-'):
        crter=crter+'V'
    if(letra=='o--'):
        crter=crter+'W'
    if(letra=='-oo-'):
        crter=crter+'X'
    if(letra=='-o--'):
        crter=crter+'Y'
    if(letra=='--oo'):
        crter=crter+'Z'
    
    return crter
def formacionPalabras(morse):   
    palabra=''
    letra=''
    for i in range(0,len(morse),1):
        if(morse[i]=='Dot'):
           letra=letra+'o'    
        if(morse[i]=='Line'):
            letra=letra+'-' 
        if(morse[i]=='Letra'):
            palabra=palabra+asignLetter(letra)
            letra=''
    return palabra
    
#=============== Programa Principal ===============#
signal=codeRecording()
PlaySound('Audios/codigo.wav', SND_FILENAME|SND_ASYNC )
# plt.figure(3)
plt.plot(signal)
morse=signIdentify(signal)
#=============== Prueba formación de palabras ===============#
frase=formacionPalabras(morse)
print(frase)     
    
# 6467 5537




