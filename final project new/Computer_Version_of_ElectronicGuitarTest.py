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
import pyaudio, struct
import tkinter as Tk
import struct
import numpy as np
import wave
import time
from Modified_my_Karplus_Strong_Alg import my_Karplus_Strong_Alg as KS
from Modified_my_Karplus_Strong_Alg import inds_init 
from my_vibrato_func import my_vibrato_func

# Using tkinker to design a GUI which can quit the program

CONTINUE = True
KEYPRESS = False
VIB = False
key_index = np.array([0])

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
      key_index = np.array([0])
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

Note_Freqs = np.array([[130.81,138.59,146.83,155.56,164.81,174.62,185.00,196.00,207.65,220.00,233.08,246.94],
                       [261.63,277.18,293.66,311.12,329.63,349.23,369.99,392.00,415.30,440.00,466.16,493.88],
                       [523.25,554.37,587.33,622.25,659.26,698.46,739.99,783.99,830.61,880.00,932.33,987.77],
                       [1046.5,1108.7,1174.7,1244.5,1318.5,1396.9,1480.0,1568.0,1661.2,1760.0,1864.7,1975.5]])


Fs = 48000 
BLOCKLEN   = 512       # Number of frames per block.***** This is selected to be greater than the longest N which corresponds to the lowest freq in Note_Freqs
eps=1e-16


num_MPR = Note_Freqs.shape[0]
KS_buffers = np.zeros((num_MPR,num_inputs,BLOCKLEN))
KS_inds = np.zeros((num_MPR,num_inputs,2))
KS_inds = inds_init(KS_inds,Note_Freqs,Fs, BLOCKLEN)
vib_buffer = np.zeros((BLOCKLEN,))
vib_inds = np.zeros((2,))
vib_inds[0] = int(0.5*BLOCKLEN)
vib_inds[1] = int(0)

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
frames_per_buffer = 512
stream = p.open(
        format      = PA_FORMAT,
        channels    = 1,
        rate        = Fs,
        input       = False,
        output      = True,
        frames_per_buffer = frames_per_buffer)
# specify low frames_per_buffer to reduce latency

# Read the data from MPR121s through I2C communication
#i2c = busio.I2C(board.SCL,board.SDA)

# We use 4 MPR121 to recognize 48 notes (each MPR121 has 12 input pins)...
# ... corresponding 4 different address
#mpr121_1 = adafruit_mpr121.MPR121(i2c,address=0x5a)
#mpr121_2 = adafruit_mpr121.MPR121(i2c,address=0x5b)
#mpr121_3 = adafruit_mpr121.MPR121(i2c,address=0x5c)
#mpr121_4 = adafruit_mpr121.MPR121(i2c,address=0x5d)


wf = wave.open('StrumGuitarSoundOutput_FPB_{}.wav'.format(frames_per_buffer), 'w')		# wf : wave file
wf.setnchannels(1)			# one channel (mono)
wf.setsampwidth(2)			# two bytes per sample (16 bits per sample)
wf.setframerate(48000)			# samples per second

# Thd main loop
# In this loop, the program will communicate with the sensors for inputs.
# When getting the inputs, the program will output the corresponding sounds with
# the corresponding main frequencies.
while CONTINUE:
    root.update()

#for i in range(11):    # Traversing the 12 pins of each MPR121
    audio_in = np.zeros((num_MPR,num_inputs,BLOCKLEN))
	# Processing the inputs
     

    audio,KS_buffers, KS_inds = KS(audio_in,0,key_index, buffer = KS_buffers, inds = KS_inds, KS_EN = KEYPRESS)  # K-S Alg and get output
    if VIB:
        audio, vib_buffer, vib_inds = my_vibrato_func(audio, vib_buffer, vib_inds)
        
    KEYPRESS = False
    # normalize to 16-bit range
    audio *= (32767/4.0) #/ (np.max(np.abs(audio))+eps)
    # convert to 16-bbit data
    audio = audio.astype(np.int16)
    outs = np.trim_zeros(audio,'b') 
    if len(outs)>0:
        outdata = outs
    else:
        outdata = audio

    # start playback
    binary_data = struct.pack('h' * len(outdata), *outdata);    # Convert to binary binary data
    stream.write(outdata, len(outdata))               # Write binary binary data to audio output


    # Play the output through pyaudio
    #for index in range(x_len):
    #    output_bytes = struct.pack('h',output[index])
    wf.writeframes(binary_data)


		  

print("* Finished *")

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()

wf.close()

    
