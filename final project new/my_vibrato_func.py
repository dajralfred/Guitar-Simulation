# play_vibrato_interpolation.py
# Reads a specified wave file (mono) and plays it with a vibrato effect.
# (Sinusoidally time-varying delay)
# Uses linear interpolation
import numpy as np


def my_vibrato_func(myInput, buffer, inds,Fs=None):
    if Fs == None:
        Fs=48000
    LEN = myInput.shape[0]

    # Vibrato parameters
    f0 = 2
    W = 0.05   # W = 0 for no effect
    g=0.8     #gain
    # f0 = 2; W = 0.2

    
    # OR
    # f0 = 2
    # ratio = 2.06
    # W = (ratio - 1.0) / (2 * math.pi * f0 )
    # print(W)

    # Buffer to store past signal values. Initialize to zero.  
    BUFFER_LEN = buffer.shape[0]

    # Buffer (delay line) indices
    kr = int(inds[0])  # read index
    kw = int(inds[1])  # write index (initialize to middle of buffer)

    #print('The buffer is %d samples long.' % BUFFER_LEN)

    myOutput = np.zeros(LEN)

    # Loop through wave file 
    for n in range(0, LEN):

        # Get sample from wave file
        x0 = myInput[n]

    

        # Get previous and next buffer values (since kr is fractional)
        kr_prev = int(np.floor(kr))
        frac = kr - kr_prev    # 0 <= frac < 1
        kr_next = kr_prev + 1
        if kr_next == BUFFER_LEN:
            kr_next = 0

        # Compute output value using interpolation
        y0 = x0 + g*((1-frac) * buffer[kr_prev] + frac * buffer[kr_next])
        myOutput[n] = y0

        # Update buffer
        buffer[kw] = x0

        # Increment read index
        kr = kr + 1 + ( W / 2 )* ( 1 + np.sin( 2 * np.pi * f0 * n / Fs ) )
        # Note: kr is fractional (not integer!)
        # M[n] = M0 + (Mw / 2)*(1 + sin(2*pi*f0*n/fs))

        # Ensure that 0 <= kr < BUFFER_LEN
        if kr >= BUFFER_LEN:
            # End of buffer. Circle back to front.
            kr = kr - BUFFER_LEN

        # Increment write index    
        kw = kw + 1
        if kw == BUFFER_LEN:
            # End of buffer. Circle back to front.
            kw = 0

    inds[0]=kr
    inds[1]=kw
    return myOutput, buffer, inds