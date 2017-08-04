from __future__ import division
import math
import random

DEG2RAD = math.pi / 180
RAD2DEG = 180 / math.pi

def generateUUID():

    chars = list( "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" )
    uuid = [ "" ] * 36
    rnd = 0
    r = None

    for i in xrange( 36 ):

        if i == 8 or i == 13 or i == 18 or i == 23:

            uuid[ i ] = "-"
        
        elif i == 14:

            uuid[ i ] = "4"
        
        else:

            if rnd <= 0x02: rnd = 0x2000000 + random.randint( 0, 0x1000000 - 1 )
            r = rnd & 0xf
            rnd = rnd >> 4
            uuid[ i ] = chars[ ( r & 0x3 ) | 0x8 if i == 19  else r ]

    return "".join( uuid )

def clamp( value, mn, mx ):

    return max( mn, min( mx, value ) )

# compute euclidian modulo of m % n
# https://en.wikipedia.org/wiki/Modulo_operation

def euclideanModulo( n, m ):

    return ( ( n % m ) + m ) % m

# Linear mapping from range <a1, a2> to range <b1, b2>

def mapLinear( x, a1, a2, b1, b2 ):

    return b1 + ( x - a1 ) * ( b2 - b1 ) / ( a2 - a1 )

# https://en.wikipedia.org/wiki/Linear_interpolation

def lerp( x, y, t ):
    
    return ( 1 - t ) * x + t * y

# http://en.wikipedia.org/wiki/Smoothstep

def smoothstep( x, mn, mx ):

    if x <= mn: return 0
    if x >= mx: return 1

    x = ( x - mn ) / ( mx - mn )

    return x * x * ( 3 - 2 * x )

def smootherstep( x, mn, mx ):

    if x <= mn: return 0
    if x >= mx: return 1

    x = ( x - mn ) / ( mx - mn )

    return x * x * x * ( x * ( x * 6 - 15 ) + 10 )

# Random integer from <low, high> interval

def randInt( low, high ):

    return random.randInt( low, high )

# Random float from <low, high> interval

def randFloat( low, high ):

    return random.uniform( low, high )

# Random float from <-range/2, range/2> interval

def randFloatSpread( range ):

    return randFloat( -range / 2, range / 2 )

def degToRad( degrees ):

    return degrees * DEG2RAD

def radToDeg( radians ):

    return radians * RAD2DEG

def isPowerOfTwo( value ):

    return ( value & ( value - 1) ) == 0 and value != 0

def nearestPowerOfTwo( value ):

    return pow( 2, round( math.log( value, 2) ) )

def nextPowerOfTwo( value ):

    value -= 1
    value |= value >> 1
    value |= value >> 2
    value |= value >> 4
    value |= value >> 8
    value |= value >> 16
    value += 1

    return value