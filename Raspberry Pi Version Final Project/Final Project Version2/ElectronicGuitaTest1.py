'''
This is the work Of Jihang Xie and Dajr Alfred

Our work is the Electronic Guitar based on Karplus-Strong Algorithms.

The hardware consists of a guitar shape made in Makerspace, a Raspberry PI,
4 MPR121s(Capacitive Touched Sensors), a dispaly screen, keyboard and lots of
jumper wires.

The sortware is based on python, pyaudio and numpy. The core algorithm, as I
mentioned, is Karplus-Strong Algorithms. Due to the fact that the notes (or
pitch) always make the delay, N, not a integer. So, I also use the fractional
delay here, just like the interpolation of Chorus algorithm.


'''

# import necessary libraries in python
import simpleaudio as sa
import sounddevice as sd
import tkinter as Tk
import struct
import numpy as np
import wave
import time
import board
import busio
import adafruit_mpr121
#from matplotlib import pyplot
from my_Karplus_Strong_Alg import my_Karplus_Strong_Alg as KS
from my_vibrato_func import my_vibrato_func

# Using tkinker to design a GUI which can quit the program

CONTINUE = True

def my_quit():
    global CONTINUE
    global root
    root.quit()
    CONTINUE = False


root = Tk.Tk()

# the button of 'Quit'
B1 = Tk.Button(root,text = 'QUIT', command = my_quit)
S1 = Tk.Label(root, text = 'There is no input')
S2 = Tk.Label(root, text = 'Vibrato Disabled')

B1.pack(side=Tk.BOTTOM , fill = Tk.X)
S1.pack(fill = Tk.X)
S2.pack(fill = Tk.X)



# Read the data from MPR121s through I2C communication
i2c = busio.I2C(board.SCL,board.SDA)

# We use 4 MPR121 to recognize 48 notes (each MPR121 has 12 input pins)...
# ... corresponding 4 different address
mpr121_1 = adafruit_mpr121.MPR121(i2c,address=0x5a)
#mpr121_2 = adafruit_mpr121.MPR121(i2c,address=0x5b)
#mpr121_3 = adafruit_mpr121.MPR121(i2c,address=0x5c)
#mpr121_4 = adafruit_mpr121.MPR121(i2c,address=0x5d)


wf = wave.open('sGuitarSoundOutput.wav', 'w')		# wf : wave file
wf.setnchannels(1)			# one channel (mono)
wf.setsampwidth(2)			# two bytes per sample (16 bits per sample)
wf.setframerate(48000)			# samples per second

# Thd main loop
# In this loop, the program will communicate with the sensors for inputs.
# When getting the inputs, the program will output the corresponding sounds with
# the corresponding main frequencies.
while CONTINUE:
    root.update()
    audio = np.zeros(24000)
    PinNum = []

    for i in range(11):    # Traversing the 12 pins of each MPR121

        # Processing the input from the 1st Mpr121
         if mpr121_1[i].value:
              #print('mpr121_1 Pin {} is touched\n'.format(i))
              
              Note_Freq , output = KS('mpr121_1',i)  # K-S Alg and get output
              audio += output[0:24000]


              PinNum.append(str(i)+'('+str(Note_Freq)+'Hz'+')'+' ')


              if mpr121_1[11].value:
                  LabelString2 = 'Vibrato Enabled'
                  S2.config(text = LabelString2)

                  audio = my_vibrato_func(audio)
              else :
                  LabelString2 = 'Vibrato Disabled'
                  S2.config(text = LabelString2)
                  

              

    LabelString = 'Pin '+ str(PinNum) + ' is/are touched'

    S1.config(text = LabelString)#audio =np.array(audio)
    # normalize to 16-bit range
    audio *= 32767 / np.max(np.abs(audio))
    # convert to 16-bbit data
    audio = audio.astype(np.int16)

    # start playback
    play_obj = sa.play_buffer(audio, 1, 2, 48000)

    # wait for playback to finish before exiting
    play_obj.wait_done()



              # Play the output through pyaudio
              #for index in range(x_len):
              #    output_bytes = struct.pack('h',output[index])
              #    wf.writeframes(output_bytes)




              

print("* Finished *")

wf.close()
'''
pyplot.ioff()
pyplot.show()
pyplot.close()
'''
    
