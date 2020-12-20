'''
This is the Karplus-Strong Algorithms made by Jihang Xie and Dajr Alfred

We write this algorithm based on week7's note and we also refer to the fractional
delay mentioned in vibtato of week4


'''

# K-S Alg
def my_Karplus_Strong_Alg(audio,MPR121_Addr,pin, buffer, inds, KS_EN=False, Note_Freqs=None,Fs = None):

    import numpy as np  # Guassian random data and some other functions will use it

# In "Karplus-Strong note.pdf", F0=Fs/(N+d), where Fs is the sample rate...
# ...N is the delay length, d is the delay of the low pass filter and Fo...
# ... is the fundamental frequecy of the output sound produced by the system.
# ... The two-point averager has d = 0.5
    
    d = 0.5 # The delay of two-point averager
    if Fs == None:
        Fs = 48000  # The default sample rate of the system

    # According MPR121's address and its pin to determine which note we want to play
    if Note_Freqs == None:
        Note_Freqs = np.array([[130.81,138.59,146.83,155.56,164.81,174.62,185.00,196.00,207.65,220.00,233.08,246.94],
                              [261.63,277.18,293.66,311.12,329.63,349.23,369.99,392.00,415.30,440.00,466.16,493.88],
                              [523.25,554.37,587.33,622.25,659.26,698.46,739.99,783.99,830.61,880.00,932.33,987.77],
                              [1046.5,1108.7,1174.7,1244.5,1318.5,1396.9,1480.0,1568.0,1661.2,1760.0,1864.7,1975.5]])


    # Compute Delay Length through Fo
    # F0= Fs / (N+d)
    N = (Fs/Note_Freqs[MPR121_Addr,pin][0]) - d
    #print("The delay length N is" , round(N,2))
    #print('\n')

    # Initializing the papameters of Fractional delay
    # For example y(8.3) = y(8+0.3) = (1-0.3)*y(8) + 0.3*y(9)
    kr_frac = 1.0 - round(N-np.floor(N),2)
    kr1 = int(inds[MPR121_Addr,pin,0])
    kr2 = kr1-1
    kw = int(inds[MPR121_Addr,pin,1])

    # Initializeing the buffer
    # According to K-S Alg., y[n] = x[n] + (G/2)*y[n-N]+(G/2)*y[n-N+1]
    # Therofore, the buffer's length should be round(N) because N always is not...
    # ...a integer 


    G = 0.993  # Gain and it's to nake sure about the convergence

    #Time duration
    T=2.0

    #set parameters of input
    buffer_len = buffer.shape[2]
    ZeroArray = np.zeros((buffer_len-int(N),))
    if KS_EN:
        RandomArray =  np.random.random_sample((int(N),))
    else:
        RandomArray =  np.zeros((int(N),))

    x_in = np.hstack((RandomArray,ZeroArray))
    x_other = np.zeros((buffer_len,))
    
    x_len=x_in.shape[0]
    
    #print(x_len)
    y=[0]*x_len

    for m in range(Note_Freqs.shape[0]):
        for n in range(Note_Freqs.shape[1]):
            for i in range(x_len):
                if (m == MPR121_Addr) and (n == pin):
                    x = x_in
                else:
                    x = x_other
                
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
                y0 = x0 +(G/2.0)*((1-kr_frac)*buffer[m,n,kr1_prev]+kr_frac*buffer[m,n,kr1_next]) + (G/2.0)*((1-kr_frac)*buffer[m,n,kr2_prev]+kr_frac*buffer[m,n,kr2_next])

                # Update buffer
                buffer[m,n,kw] = y0

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
                
                y[i] = y0
                

            audio[m,n] = np.array(y).T
            inds[m,n,0]=kr1
            inds[m,n,1]=kw

        
    audio = np.sum(np.sum(audio,axis=1),axis=0)
    return audio, buffer, inds               
    
def inds_init(inds,Note_Freqs,Fs,BUFFERLEN):
    import numpy as np
    d = 0.5
    mpr = Note_Freqs.shape[0]
    notes = Note_Freqs.shape[1]
    for m in range(mpr):
        for n in range(notes):
            N = np.floor((Fs/Note_Freqs[m,n])-d)
            inds[m,n,0] = int(BUFFERLEN-N)
            inds[m,n,1] = int(0)
            
    return inds