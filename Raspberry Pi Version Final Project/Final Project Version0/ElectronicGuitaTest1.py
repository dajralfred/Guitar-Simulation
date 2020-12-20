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
import tkinter as Tk
import struct
import numpy as np
import pyaudio
import time
import board
import busio
import adafruit_mpr121
from matplotlib import pyplot
from my_Karplus_Strong_Alg import my_Karplus_Strong_Alg as KS

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

B1.pack(side=Tk.BOTTOM , fill = Tk.X)

# Read the data from MPR121s through I2C communication
i2c = busio.I2C(board.SCL,board.SDA)

# We use 4 MPR121 to recognize 48 notes (each MPR121 has 12 input pins)...
# ... corresponding 4 different address
mpr121_1 = adafruit_mpr121.MPR121(i2c,address=0x5a)
mpr121_2 = adafruit_mpr121.MPR121(i2c,address=0x5b)
#mpr121_3 = adafruit_mpr121.MPR121(i2c,address=0x5c)
#mpr121_4 = adafruit_mpr121.MPR121(i2c,address=0x5d)

# Initializing the pyaudio
# The audio device of Raspberry PI can only recognize and initialize some...
# ...specific sample rate. Here I choose the default sample rate 48000 Hz
p=pyaudio.PyAudio()
print(p.get_default_output_device_info())
stream = p.open(format = pyaudio.paInt16,
               channels = 1,
               rate = 48000,
               input= False,
               output = True)

# Thd main loop
# In this loop, the program will communicate with the sensors for inputs.
# When getting the inputs, the program will output the corresponding sounds with
# the corresponding main frequencies.
while CONTINUE:
    root.update()

    for i in range(12):    # Traversing the 12 pins of each MPR121

        # Processing the input from the 1st Mpr121
         if mpr121_1[i].value:
              print('mpr121_1 Pin {} is touched\n'.format(i))
              
              x_len , output = KS('mpr121_1',i)  # K-S Alg and get output
              pyplot.figure(1)
              [g1] = pyplot.plot([],[],'blue')
              n=range(0,x_len)
              g1.set_xdata(n)
              g1.set_ydata(output)
              pyplot.xlim(0,x_len)
              pyplot.ylim(-10000,10000)
              pyplot.pause(0.001)
              pyplot.clf()

              # Play the output through pyaudio
              for index in range(200):
                  output_bytes = struct.pack('h',output[index])
                  # stream.write(output_bytes)

        # Processing the input from the 2nd Mpr121
         if mpr121_2[i].value:
              print('mpr121_2 Pin {} is touched\n'.format(i))
              
              x_len , output = KS('mpr121_2',i)   # K-S Alg and get output

              # plot the output wave
              pyplot.figure(1)
              [g1] = pyplot.plot([],[],'blue')
              n=range(0,x_len)
              g1.set_xdata(n)
              g1.set_ydata(output)
              pyplot.xlim(0,x_len)
              pyplot.ylim(-10000,10000)
              pyplot.pause(0.001)
              pyplot.clf()

              # Play the output through pyaudio
              for index in range(200):
                  output_bytes = struct.pack('h',output[index])
                  # stream.write(output_bytes)
'''                  
        # Processing the input from the 3rd Mpr121
         if mpr121_3[i].value:
              print('mpr121_3 Pin {} is touched\n'.format(i))
              
              x_len , output = KS('mpr121_3',i)  # K-S Alg and get output

              # plot the output wave
              pyplot.figure(1)
              [g1] = pyplot.plot([],[],'blue')
              n=range(0,x_len)
              g1.set_xdata(n)
              g1.set_ydata(output)
              pyplot.xlim(0,x_len)
              pyplot.ylim(-10000,10000)
              pyplot.pause(0.001)
              pyplot.clf()

              # Play the output through pyaudio
              for index in range(200):
                  output_bytes = struct.pack('h',output[index])
                  # stream.write(output_bytes)

        # Processing the input from the 4th Mpr121
         if mpr121_4[i].value:
              print('mpr121_4 Pin {} is touched\n'.format(i))
              
              x_len , output = KS('mpr121_4',i)  # K-S Alg and get output

              # plot the output wave
              pyplot.figure(1)
              [g1] = pyplot.plot([],[],'blue')
              n=range(0,x_len)
              g1.set_xdata(n)
              g1.set_ydata(output)
              pyplot.xlim(0,x_len)
              pyplot.ylim(-10000,10000)
              pyplot.pause(0.001)
              pyplot.clf()

              # Play the output through pyaudio
              for index in range(200):
                  output_bytes = struct.pack('h',output[index])
                  # stream.write(output_bytes)
'''        



              

print("* Finished *")

stream.stop_stream()
stream.close()
p.terminate()
pyplot.ioff()
pyplot.show()
pyplot.close()
    
