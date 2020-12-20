'''
This is the work Of Jihang Xie and Dajr Alfred

Our work is the Electronic Guitar based on Karplus-Strong Algorithms.

The hardware consists of a guitar shape made in Makerspace, a Raspberry Pi,
4 MPR121s(Capacitive Touched Sensors), a dispaly screen, keyboard and lots of
jumper wires.

The sortware is based on python, simpleaudio and numpy. The core algorithm, as I
mentioned, is Karplus-Strong Algorithms. Due to the fact that the notes (or
pitch) always make the delay, N, not a integer. So, I also use the fractional
delay here, just like the interpolation of Chorus algorithm.


'''

# import necessary libraries in python
import simpleaudio as sa
import tkinter as Tk
import struct
import numpy as np
import wave
import time
from matplotlib import pyplot
from Modified_my_Karplus_Strong_Alg import my_Karplus_Strong_Alg as KS
from my_vibrato_func import my_vibrato_func

# Using tkinker to design a GUI which can quit the program

CONTINUE = True
KEYPRESS = False
VIB = False
key_index = []

inputkeys = np.array(['a','s','d','f','g','h','j','k','l','z','x','v'])
num_inputs = inputkeys.shape[0]


root = Tk.Tk()

LabelString = Tk.StringVar()
LabelString2 = Tk.StringVar()

LabelString.set('Press an Input')
LabelString2.set('Vibrato Disabled')

def my_function(event):
    global CONTINUE
    global KEYPRESS
    global key_index 
    global VIB
    LabelString.set('You pressed ' + event.char)
    key_index = np.where(inputkeys == event.char)[0]
    if event.char == 'q':
      print('Good bye')
      CONTINUE = False
    if key_index.size > 0 and CONTINUE:
      KEYPRESS = True
      if key_index == 11:
        KEYPRESS = False
        if VIB:
          VIB = False
          LabelString2.set('Vibrato Disabled')
        else:
          VIB = True
          LabelString2.set('Vibrato Enabled')
    elif key_index.size == 0 and CONTINUE:
      print('This is not an accepted key.')
      print('Please use one of the following keys for sound: {}'.format(inputkeys))

def my_quit():
    global CONTINUE
    global root
    print('Good bye')
    root.quit()
    CONTINUE = False

root.bind("<Key>", my_function)

# the button of 'Quit'
B1 = Tk.Button(root,text = 'QUIT', command = my_quit)
S1 = Tk.Label(root, textvariable = LabelString)
S2 = Tk.Label(root, textvariable = LabelString2)

B1.pack(side=Tk.BOTTOM , fill = Tk.X)
S1.pack()
S2.pack()


# Read the data from MPR121s through I2C communication
#i2c = busio.I2C(board.SCL,board.SDA)

# We use 4 MPR121 to recognize 48 notes (each MPR121 has 12 input pins)...
# ... corresponding 4 different address
#mpr121_1 = adafruit_mpr121.MPR121(i2c,address=0x5a)
#mpr121_2 = adafruit_mpr121.MPR121(i2c,address=0x5b)
#mpr121_3 = adafruit_mpr121.MPR121(i2c,address=0x5c)
#mpr121_4 = adafruit_mpr121.MPR121(i2c,address=0x5d)


#wf = wave.open('sGuitarSoundOutput.wav', 'w')		# wf : wave file
#wf.setnchannels(1)			# one channel (mono)
#wf.setsampwidth(2)			# two bytes per sample (16 bits per sample)
#wf.setframerate(48000)			# samples per second

# Thd main loop
# In this loop, the program will communicate with the sensors for inputs.
# When getting the inputs, the program will output the corresponding sounds with
# the corresponding main frequencies.
while CONTINUE:
    root.update()

    for i in range(11):    # Traversing the 12 pins of each MPR121

        # Processing the input from the 1st Mpr121
         if KEYPRESS:
              #print('mpr121_1 Pin {} is touched\n'.format(i))
              
              x_len , audio = KS(0,key_index)  # K-S Alg and get output
              '''pyplot.figure(1)
              [g1] = pyplot.plot([],[],'blue')
              n=range(0,x_len)
              g1.set_xdata(n)
              g1.set_ydata(audio)
              pyplot.xlim(0,x_len)
              pyplot.ylim(-20000,20000)
              pyplot.pause(0.001)
              pyplot.clf()'''
              audio =np.array(audio)

              PinNum = i
              KEYPRESS = False

              #LabelString = 'Pin '+ str(PinNum) + ' is touched'

              #S1.config(text = LabelString)

              #if mpr121_1[11].value:
              if VIB:
                  #LabelString2 = 'Add Vibrato'
                  #S2.config(text = LabelString2)

                  audio = my_vibrato_func(audio)
              '''else :
                  LabelString2 = 'There is no vibrato'
                  S2.config(text = LabelString2)'''
                  

              

              # normalize to 16-bit range
              audio *= 32767 / np.max(np.abs(audio))
              # convert to 16-bbit data
              audio = audio.astype(np.int16)

              # start playback
              play_obj = sa.play_buffer(audio, 1, 2, 48000)

              # wait for playback to finish before exiting
              #play_obj.wait_done()



              # Play the output through pyaudio
              #for index in range(x_len):
              #    output_bytes = struct.pack('h',output[index])
              #    wf.writeframes(output_bytes)
'''
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
              for index in range(x_len):
                  output_bytes = struct.pack('h',output[index])
                  # stream.write(output_bytes)
                  
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

#wf.close()
pyplot.ioff()
pyplot.show()
pyplot.close()

    
