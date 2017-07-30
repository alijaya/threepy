from __future__ import division
import math
import numbers

import re
import logging

import _Math

"""
 * @author mrdoob / http:#mrdoob.com/
 """

ColorKeywords = { "aliceblue": 0xF0F8FF, "antiquewhite": 0xFAEBD7, "aqua": 0x00FFFF, "aquamarine": 0x7FFFD4, "azure": 0xF0FFFF,
    "beige": 0xF5F5DC, "bisque": 0xFFE4C4, "black": 0x000000, "blanchedalmond": 0xFFEBCD, "blue": 0x0000FF, "blueviolet": 0x8A2BE2,
    "brown": 0xA52A2A, "burlywood": 0xDEB887, "cadetblue": 0x5F9EA0, "chartreuse": 0x7FFF00, "chocolate": 0xD2691E, "coral": 0xFF7F50,
    "cornflowerblue": 0x6495ED, "cornsilk": 0xFFF8DC, "crimson": 0xDC143C, "cyan": 0x00FFFF, "darkblue": 0x00008B, "darkcyan": 0x008B8B,
    "darkgoldenrod": 0xB8860B, "darkgray": 0xA9A9A9, "darkgreen": 0x006400, "darkgrey": 0xA9A9A9, "darkkhaki": 0xBDB76B, "darkmagenta": 0x8B008B,
    "darkolivegreen": 0x556B2F, "darkorange": 0xFF8C00, "darkorchid": 0x9932CC, "darkred": 0x8B0000, "darksalmon": 0xE9967A, "darkseagreen": 0x8FBC8F,
    "darkslateblue": 0x483D8B, "darkslategray": 0x2F4F4F, "darkslategrey": 0x2F4F4F, "darkturquoise": 0x00CED1, "darkviolet": 0x9400D3,
    "deeppink": 0xFF1493, "deepskyblue": 0x00BFFF, "dimgray": 0x696969, "dimgrey": 0x696969, "dodgerblue": 0x1E90FF, "firebrick": 0xB22222,
    "floralwhite": 0xFFFAF0, "forestgreen": 0x228B22, "fuchsia": 0xFF00FF, "gainsboro": 0xDCDCDC, "ghostwhite": 0xF8F8FF, "gold": 0xFFD700,
    "goldenrod": 0xDAA520, "gray": 0x808080, "green": 0x008000, "greenyellow": 0xADFF2F, "grey": 0x808080, "honeydew": 0xF0FFF0, "hotpink": 0xFF69B4,
    "indianred": 0xCD5C5C, "indigo": 0x4B0082, "ivory": 0xFFFFF0, "khaki": 0xF0E68C, "lavender": 0xE6E6FA, "lavenderblush": 0xFFF0F5, "lawngreen": 0x7CFC00,
    "lemonchiffon": 0xFFFACD, "lightblue": 0xADD8E6, "lightcoral": 0xF08080, "lightcyan": 0xE0FFFF, "lightgoldenrodyellow": 0xFAFAD2, "lightgray": 0xD3D3D3,
    "lightgreen": 0x90EE90, "lightgrey": 0xD3D3D3, "lightpink": 0xFFB6C1, "lightsalmon": 0xFFA07A, "lightseagreen": 0x20B2AA, "lightskyblue": 0x87CEFA,
    "lightslategray": 0x778899, "lightslategrey": 0x778899, "lightsteelblue": 0xB0C4DE, "lightyellow": 0xFFFFE0, "lime": 0x00FF00, "limegreen": 0x32CD32,
    "linen": 0xFAF0E6, "magenta": 0xFF00FF, "maroon": 0x800000, "mediumaquamarine": 0x66CDAA, "mediumblue": 0x0000CD, "mediumorchid": 0xBA55D3,
    "mediumpurple": 0x9370DB, "mediumseagreen": 0x3CB371, "mediumslateblue": 0x7B68EE, "mediumspringgreen": 0x00FA9A, "mediumturquoise": 0x48D1CC,
    "mediumvioletred": 0xC71585, "midnightblue": 0x191970, "mintcream": 0xF5FFFA, "mistyrose": 0xFFE4E1, "moccasin": 0xFFE4B5, "navajowhite": 0xFFDEAD,
    "navy": 0x000080, "oldlace": 0xFDF5E6, "olive": 0x808000, "olivedrab": 0x6B8E23, "orange": 0xFFA500, "orangered": 0xFF4500, "orchid": 0xDA70D6,
    "palegoldenrod": 0xEEE8AA, "palegreen": 0x98FB98, "paleturquoise": 0xAFEEEE, "palevioletred": 0xDB7093, "papayawhip": 0xFFEFD5, "peachpuff": 0xFFDAB9,
    "peru": 0xCD853F, "pink": 0xFFC0CB, "plum": 0xDDA0DD, "powderblue": 0xB0E0E6, "purple": 0x800080, "red": 0xFF0000, "rosybrown": 0xBC8F8F,
    "royalblue": 0x4169E1, "saddlebrown": 0x8B4513, "salmon": 0xFA8072, "sandybrown": 0xF4A460, "seagreen": 0x2E8B57, "seashell": 0xFFF5EE,
    "sienna": 0xA0522D, "silver": 0xC0C0C0, "skyblue": 0x87CEEB, "slateblue": 0x6A5ACD, "slategray": 0x708090, "slategrey": 0x708090, "snow": 0xFFFAFA,
    "springgreen": 0x00FF7F, "steelblue": 0x4682B4, "tan": 0xD2B48C, "teal": 0x008080, "selftle": 0xD8BFD8, "tomato": 0xFF6347, "turquoise": 0x40E0D0,
    "violet": 0xEE82EE, "wheat": 0xF5DEB3, "white": 0xFFFFFF, "whitesmoke": 0xF5F5F5, "yellow": 0xFFFF00, "yellowgreen": 0x9ACD32
}

class Color( object ):

    def __init__( self, r = None, g = None, b = None ):

        self.isColor = True
        self.r = 1
        self.g = 1
        self.b = 1

        if g is None and b is None:

            # r is THREE.Color, hex or string
            self.set( r )

        else: self.setRGB( r, g, b )

    def set( self, value ):

        if value is not None and hasattr( value, "isColor" ):

            self.copy( value )

        elif isinstance( value, int ):

            self.setHex( value )

        elif isinstance( value, basestring ):

            self.setStyle( value )

        return self

    def setScalar( self, scalar ):

        self.r = scalar
        self.g = scalar
        self.b = scalar

        return self

    def setHex( self, hex ):

        hex = int( hex )

        self.r = ( hex >> 16 & 255 ) / 255
        self.g = ( hex >> 8 & 255 ) / 255
        self.b = ( hex & 255 ) / 255

        return self

    def setRGB( self, r, g, b ):

        self.r = r
        self.g = g
        self.b = b

        return self

    def setHSL( self, h, s, l ):

        def hue2rgb( p, q, t ):

            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1 / 6: return p + ( q - p ) * 6 * t
            if t < 1 / 2: return q
            if t < 2 / 3: return p + ( q - p ) * 6 * ( 2 / 3 - t )
            return p

        # h,s,l ranges are in 0.0 - 1.0
        h = _Math.euclideanModulo( h, 1 )
        s = _Math.clamp( s, 0, 1 )
        l = _Math.clamp( l, 0, 1 )

        if s == 0:

            self.r = self.g = self.b = l

        else:

            p = l * ( 1 + s ) if l <= 0.5 else l + s - ( l * s )
            q = ( 2 * l ) - p

            self.r = hue2rgb( q, p, h + 1 / 3 )
            self.g = hue2rgb( q, p, h )
            self.b = hue2rgb( q, p, h - 1 / 3 )

        return self

    def setStyle( self, style ):

        def handleAlpha( string ):

            if string == None: return

            if float( string ) < 1:

                logging.warning( "THREE.Color: Alpha component of " + style + " will be ignored." )

        m = re.match( "^((?:rgb|hsl)a?)\(\s*([^\)]*)\)" , style )

        if m:

            # rgb / hsl

            name = m.group( 1 )
            components = m.group( 2 )

            if name == "rgb" or name == "rgba":

                color = re.match( "^(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(,\s*([0-9]*\.?[0-9]+)\s*)?$", components )

                if color:

                    # rgb(255,0,0) rgba(255,0,0,0.5)
                    self.r = min( 255, int( color.group( 1 ) ) ) / 255
                    self.g = min( 255, int( color.group( 2 ) ) ) / 255
                    self.b = min( 255, int( color.group( 3 ) ) ) / 255

                    handleAlpha( color.group( 5 ) )

                    return self

                color = re.match( "^(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(,\s*([0-9]*\.?[0-9]+)\s*)?$", components )

                if color:

                    # rgb(100%,0%,0%) rgba(100%,0%,0%,0.5)
                    self.r = min( 100, int( color.group( 1 ) ) ) / 100
                    self.g = min( 100, int( color.group( 2 ) ) ) / 100
                    self.b = min( 100, int( color.group( 3 ) ) ) / 100

                    handleAlpha( color.group( 5 ) )

                    return self

            elif name == "hsl" or name == "hsla":

                color = re.match( "^([0-9]*\.?[0-9]+)\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(,\s*([0-9]*\.?[0-9]+)\s*)?$", components )

                if color:

                    # hsl(120,50%,50%) hsla(120,50%,50%,0.5)
                    h = float( color.group( 1 ) ) / 360
                    s = int( color.group( 2 ) ) / 100
                    l = int( color.group( 3 ) ) / 100

                    handleAlpha( color.group( 5 ) )

                    return self.setHSL( h, s, l )

        m = re.match( "^\#([A-Fa-f0-9]+)$", style )

        if m:

            # hex color

            hex = m.group( 1 )
            size = len( hex )

            if size == 3:

                # #ff0
                self.r = int( "0x" + hex[ 0 ] + hex[ 0 ], 16 ) / 255
                self.g = int( "0x" + hex[ 1 ] + hex[ 1 ], 16 ) / 255
                self.b = int( "0x" + hex[ 2 ] + hex[ 2 ], 16 ) / 255

                return self

            elif size == 6:

                # #ff0000
                self.r = int( "0x" + hex[ 0 ] + hex[ 1 ], 16 ) / 255
                self.g = int( "0x" + hex[ 2 ] + hex[ 3 ], 16 ) / 255
                self.b = int( "0x" + hex[ 4 ] + hex[ 5 ], 16 ) / 255

                return self

        if style and len( style ) > 0:

            if style in ColorKeywords:

                # color keywords
                hex = ColorKeywords[ style ]

                # red
                self.setHex( hex )

            else:

                # unknown color
                logging.warning( "THREE.Color: Unknown color " + style )

        return self

    def clone( self ):

        return Color( self.r, self.g, self.b )

    def copy( self, color ):

        self.r = color.r
        self.g = color.g
        self.b = color.b

        return self

    def copyGammaToLinear( self, color, gammaFactor = 2.0 ):

        self.r = pow( color.r, gammaFactor )
        self.g = pow( color.g, gammaFactor )
        self.b = pow( color.b, gammaFactor )

        return self

    def copyLinearToGamma( self, color, gammaFactor = 2.0 ):

        safeInverse = ( 1.0 / gammaFactor ) if ( gammaFactor > 0 ) else 1.0

        self.r = pow( color.r, safeInverse )
        self.g = pow( color.g, safeInverse )
        self.b = pow( color.b, safeInverse )

        return self

    def convertGammaToLinear( self ):

        r = self.r
        g = self.g
        b = self.b

        self.r = r * r
        self.g = g * g
        self.b = b * b

        return self

    def convertLinearToGamma( self ):

        self.r = math.sqrt( self.r )
        self.g = math.sqrt( self.g )
        self.b = math.sqrt( self.b )

        return self

    def getHex( self ):

        return int( self.r * 255 ) << 16 ^ int( self.g * 255 ) << 8 ^ int( self.b * 255 ) << 0

    def getHexString( self ):

        return "%06x" % self.getHex()

    def getHSL( self, optionalTarget = None ):

        # h,s,l ranges are in 0.0 - 1.0

        hsl = optionalTarget or { "h": 0, "s": 0, "l": 0 }
        r = self.r
        g = self.g
        b = self.b

        mx = max( r, g, b )
        mn = min( r, g, b )

        hue = None
        saturation = None
        lightness = ( mn + mx ) / 2.0

        if mn == mx:

            hue = 0
            saturation = 0

        else:

            delta = mx - mn

            saturation = delta / ( mx + mn ) if lightness <= 0.5 else delta / ( 2 - mx - mn )

            if mx == r: hue = ( g - b ) / delta + ( 6 if g < b else 0 )
            if mx == g: hue = ( b - r ) / delta + 2
            if mx == b: hue = ( r - g ) / delta + 4

            hue /= 6

        hsl[ "h" ] = hue
        hsl[ "s" ] = saturation
        hsl[ "l" ] = lightness

        return hsl

    def getStyle( self ):

        return "rgb(%s,%s,%s)" % ( ( int( self.r * 255 ) | 0 ), ( int( self.g * 255 ) | 0 ), ( int( self.b * 255 ) | 0 ) )

    def offsetHSL( self, h, s, l ):

        hsl = self.getHSL()

        hsl.h += h
        hsl.s += s
        hsl.l += l

        self.setHSL( hsl.h, hsl.s, hsl.l )

        return self

    def add( self, color ):

        self.r += color.r
        self.g += color.g
        self.b += color.b

        return self

    def addColors( self, color1, color2 ):

        self.r = color1.r + color2.r
        self.g = color1.g + color2.g
        self.b = color1.b + color2.b

        return self

    def addScalar( self, s ):

        self.r += s
        self.g += s
        self.b += s

        return self

    def sub( self, color ):

        self.r = max( 0, self.r - color.r )
        self.g = max( 0, self.g - color.g )
        self.b = max( 0, self.b - color.b )

        return self

    def multiply( self, color ):

        self.r *= color.r
        self.g *= color.g
        self.b *= color.b

        return self

    def multiplyScalar( self, s ):

        self.r *= s
        self.g *= s
        self.b *= s

        return self

    def lerp( self, color, alpha ):

        self.r += ( color.r - self.r ) * alpha
        self.g += ( color.g - self.g ) * alpha
        self.b += ( color.b - self.b ) * alpha

        return self

    def equals( self, c ):

        return ( c.r == self.r ) and ( c.g == self.g ) and ( c.b == self.b )

    def fromArray( self, array, offset = 0 ):

        self.r = array[ offset ]
        self.g = array[ offset + 1 ]
        self.b = array[ offset + 2 ]

        return self

    def toArray( self, array = None, offset = 0 ):

        if array is None: array = []

        array[ offset ] = self.r
        array[ offset + 1 ] = self.g
        array[ offset + 2 ] = self.b

        return array

    def toJSON( self ):

        return self.getHex()
