# -*- coding: utf-8 -*-
"""
NaiNo-Kami.py.core.tseries - Module for time series 
======================================================
This module ...

.. figure:: /_images/Event.png

.. note::

    For ...

:copyright:
    The ...
:license:
    ...
"""


def correlatecomponents(a, scales=None, operation='cecm'):
    """
    correlatecomponents performs correlation between the 
    components of the same seismometers by rolling 
    operation.

    :type a: ObsPy :class:`~obspy.core.stream`
    :param a: datastream of e.g. seismogrammes.
    :type scales: vector
    :param scales: scale(s) of correlation operation.
    :type operation: string
    :param operation: type of operation.
    :rtype: array
    :return: array of root mean square time series, scale 
             in r.stats._format (samples scale unit).
    """
    # 1) Calculate moving rms and average, see moving()
    # 2) ...
    # 3) ... 

    import copy
    from obspy.core.stream import Stream
    import numpy as np
    import re

    # Initialize multiscale if undefined
    (tmax,nmax) = streamdatadim(a)
    if scales is None:
        scales = [2**i for i in range(3,999) if 2**i < (nmax - 2**i)]
        scales = np.require(scales, dtype=np.int) 
    
    # Initialize results at the minimal size
    correlations = np.zeros(( tmax, len(scales), nmax )) 

    for t, tr in enumerate(a) : # the characteristic function calculations         
            
        # Avoid clock channels 
        if not tr.stats.channel == 'YH':

            # for Z component, get E and N 
            if (tr.stats.channel[-1] == 'Z') or (tr.stats.channel == 'VERTICAL') :

                for u, ts in enumerate(a) :
                    #print ts.stats.station, ts.stats.channel

                    if (ts.stats.station == tr.stats.station) or (re.match(r'[ZVzv]', tr.stats.station[-1]) and (ts.stats.station[:-1] == tr.stats.station[:-1])) : #and (ts.stats.channel[:-1] == tr.stats.channel[:-1]):
                        #print ts.stats.station, tr.stats.station
                        #print ts.stats.channel, tr.stats.channel

                        if (ts.stats.channel[-1] == 'E') or (ts.stats.channel == 'EAST'):
                            E = ts.detrend('linear').data
                            print "E"
                        if (ts.stats.channel[-1] == 'N') or (ts.stats.channel == 'NORTH') :
                            N = ts.detrend('linear').data
                            print "N"





def moving(a, scales=None, operation='rms'):
    """
    moving (sum|average|rms) performs calculation by 
    creating series of operations of different subsets of 
    the full data set. This is also called rolling 
    operation.

    :type a: ObsPy :class:`~obspy.core.stream`
    :param a: datastream of e.g. seismogrammes.
    :type scales: vector
    :param scales: scale(s) of timeseries operation.
    :type operation: string
    :param operation: type of operation.
    :rtype: array
    :return: array of root mean square time series, scale 
             in r.stats._format (samples scale unit).
    """
    # 1) Iterate on channels
    # 2) Pre calculate the common part of all scales
    # 3) Perform channel calculation 

    import copy
    from obspy.core.stream import Stream
    import numpy as np
    
    # Initialize multiscale if undefined
    (tmax,nmax) = streamdatadim(a)
    if scales is None:
        scales = [2**i for i in range(3,999) if 2**i < (nmax - 2**i)]
        scales = np.require(scales, dtype=np.int) 

    # Initialize results at the minimal size
    timeseries = np.zeros(( tmax, len(scales), nmax )) 

    for t, tr in enumerate(a) : # the channel-wise calculations         
            
        # Avoid clock channels 
        if not tr.stats.channel == 'YH':
              
            if operation is 'rms':  
                # The cumulative sum can be exploited to calculate a moving average (the
                # cumsum function is quite efficient)
                csqr = np.cumsum(tr.detrend('linear').data ** 2)        

            if (operation is 'average') or  (operation is 'sum'):  
                # The cumulative sum can be exploited to calculate a moving average (the
                # cumsum function is quite efficient)
                csqr = np.cumsum(tr.detrend('linear').data)        

            # Convert to float
            csqr = np.require(csqr, dtype=np.float)

            for n, s in enumerate(scales) :
                
                # Avoid scales when too wide for the current channel
                if (s < (tr.stats.npts - s)) :    
                    
                    # Compute the sliding window
                    if (operation is 'rms') or (operation is 'average') or (operation is 'sum'):  
                        timeseries[t][n][s:tr.stats.npts] = csqr[s:] - csqr[:-s]

                        # for average and rms only 
                        if operation is not 'sum':
                            timeseries[t][n][:] /= s                    

                        # Pad with modified scale definitions
                        timeseries[t][n][0] = csqr[0]
                        for x in range(1, s-1):
                            timeseries[t][n][x] = (csqr[x] - csqr[0])

                            # for average and rms only
                            if operation is not 'sum':
                                timeseries[t][n][x] = timeseries[t][n][x]/(1+x)

                    # Avoid division by zero by setting zero values to tiny float
                    dtiny = np.finfo(0.0).tiny
                    idx = timeseries[t][n] < dtiny
                    timeseries[t][n][idx] = dtiny 
    
    return timeseries, scales

def streamdatadim(a):
    """
    Calculate the dimensions of all data in stream.

    Given a stream (obspy.core.stream) calculate the minimum dimensions 
    of the array that contents all data from all traces.

    This method is written in pure Python and gets slow as soon as there
    are more then ... in ...  --- normally
    this does not happen.

    :type a: ObsPy :class:`~obspy.core.stream`
    :param a: datastream of e.g. seismogrammes.
    :rtype: array
    :return: array of int corresponding to the dimensions of stream.
    """
    # 1) Does this
    # 2) Then does 
    #    that

    nmax=0
    for t, tr in enumerate(a):
        nmax = max((tr.stats.npts, nmax))

    return (t+1, nmax)
