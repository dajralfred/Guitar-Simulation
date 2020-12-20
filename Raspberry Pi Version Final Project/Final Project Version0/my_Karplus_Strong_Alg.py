'''
This is the Karplus-Strong Algorithms made by Jihang Xie and Dajr Alfred

We write this algorithm based on week7's note and we also refer to the fractional
delay mentioned in vibtato of week4


'''
# This is the clip16 function provided by Prof. Ivan
# and I just directly use it
def clip16(y):
    if y > 32767:
        y=32767
    elif y < -32768:
        y=-32768

    return y

# K-S Alg
def my_Karplus_Strong_Alg(MPR121_Addr,pin):

    import numpy as np  # Guassian random data and some other functions will use it

# In "Karplus-Strong note.pdf", F0=Fs/(N+d), where Fs is the sample rate...
# ...N is the delay length, d is the delay of the low pass filter and Fo...
# ... is the fundamental frequecy of the output sound produced by the system.
# ... The two-point averager has d = 0.5
    
    d = 0.5 # The delay of two-point averager
    Fs = 48000  # The default sample rate of the system

    # According MPR121's address and its pin to determine which note we want to play
    if MPR121_Addr == 'mpr121_1':
        if pin == 0:
            F_out = 130.81
        elif pin == 1:
            F_out = 138.59
        elif pin == 2:
            F_out = 146.83
        elif pin == 3:
            F_out = 155.56
        elif pin == 4:
            F_out = 164.81
        elif pin == 5:
            F_out = 174.62
        elif pin == 6:
            F_out = 185.00
        elif pin == 7:
            F_out = 196.00
        elif pin == 8:
            F_out = 207.65
        elif pin == 9:
            F_out = 220.00
        elif pin == 10:
            F_out = 233.08
        elif pin == 11:
            F_out = 246.94

            
    if MPR121_Addr == 'mpr121_2':
        if pin == 0:
            F_out = 261.63
        elif pin == 1:
            F_out = 277.18
        elif pin == 2:
            F_out = 293.66
        elif pin == 3:
            F_out = 311.12
        elif pin == 4:
            F_out = 329.63
        elif pin == 5:
            F_out = 349.23
        elif pin == 6:
            F_out = 369.99
        elif pin == 7:
            F_out = 392.00
        elif pin == 8:
            F_out = 415.30
        elif pin == 9:
            F_out = 440.00
        elif pin == 10:
            F_out = 466.16
        elif pin == 11:
            F_out = 493.88

    if MPR121_Addr == 'mpr121_3':
        if pin == 0:
            F_out = 523.25
        elif pin == 1:
            F_out = 554.37
        elif pin == 2:
            F_out = 587.33
        elif pin == 3:
            F_out = 622.25
        elif pin == 4:
            F_out = 659.26
        elif pin == 5:
            F_out = 698.46
        elif pin == 6:
            F_out = 739.99
        elif pin == 7:
            F_out = 783.99
        elif pin == 8:
            F_out = 830.61
        elif pin == 9:
            F_out = 880.00
        elif pin == 10:
            F_out = 932.33
        elif pin == 11:
            F_out = 987.77

    if MPR121_Addr == 'mpr121_4':
        if pin == 0:
            F_out = 1046.5
        elif pin == 1:
            F_out = 1108.7
        elif pin == 2:
            F_out = 1174.7
        elif pin == 3:
            F_out = 1244.5
        elif pin == 4:
            F_out = 1318.5
        elif pin == 5:
            F_out = 1396.9
        elif pin == 6:
            F_out = 1480.0
        elif pin == 7:
            F_out = 1568.0
        elif pin == 8:
            F_out = 1661.2
        elif pin == 9:
            F_out = 1760.0
        elif pin == 10:
            F_out = 1864.7
        elif pin == 11:
            F_out = 1975.5


    # Compute Delay Length through Fo
    # F0= Fs / (N+d)
    N = Fs/F_out - d
    print("The delay length N is" , round(N,2))
    print('\n')

    # Initializing the papameters of Fractional delay
    # For example y(8.3) = y(8+0.3) = (1-0.3)*y(8) + 0.3*y(9)
    kr_frac = 1.0 - round(N-np.floor(N),2)
    kr1 = 0
    kr2 = 1
    kw = 0

    # Initializeing the buffer
    # According to K-S Alg., y[n] = x[n] + (G/2)*y[n-N]+(G/2)*y[n-N+1]
    # Therofore, the buffer's length should be round(N) because N always is not...
    # ...a integer 
    buffer_len = int(round(N))
    buffer =[0]*buffer_len

    G = 0.93  # Gain and it's to nake sure about the convergence
    N = buffer_len

    #Time duration
    T=0.5

    #set parameters of input
    ZeroArray = np.zeros(int(T*Fs))
    ZeroList = ZeroArray.tolist()
    RandomArray = 8000 * np.random.randn(N)
    RandomList = RandomArray.tolist()

    x = RandomList+ZeroList

    x_len=len(x)
    print(x_len)
    y=[0]*x_len


    for i in range(x_len):
        x0 = x[i]   # read the input

        # The fractional delay: y(n+frac)  = (1-frac)*y(n) + frac*y(n+1)
        # According to K-S Alg., y[n] = x[n] + (G/2)*y[n-N]+(G/2)*y[n-N+1]
        # so we need to use kr1 and kr2 to interate the y[n-N] and y[n-N+1]
        # respectively.
        kr1_prev = kr1
        kr1_next = kr1+1
        if kr1_next == buffer_len:
            kr1_next = 0


        kr2_prev = kr2
        kr2_next = kr2+1
        if kr2_next == buffer_len:
            kr2_next = 0
       


        # Compute the output value using interpolation
        y0 = x0 +(G/2.0)*((1-kr_frac)*buffer[kr1_prev]+kr_frac*buffer[kr1_next]) + (G/2.0)*((1-kr_frac)*buffer[kr2_prev]+kr_frac*buffer[kr2_next])

        # Update buffer
        buffer[kw] = y0

        # Increase kr1 and kr2
        kr1 = kr1 + 1
        kr2 = kr2 + 1

        # Increase km
        kw = kw + 1

        # If kr1,kr2 or km is no less than buffer_len, let them begin at 0
        if kr1 >= buffer_len:
            kr1 = 0

        if kr2 >= buffer_len:
            kr2 = 0

        if kw >=buffer_len:
            kw = 0






        y0_clip = int(clip16(y0))
        
        y[i] = y0_clip
        

    # output_bytes = struct.pack('h'*x_len,*y)

        

    return x_len , y
   
   

    
                
