from __future__ import division
import math

import unittest

import THREE

class TestColor( unittest.TestCase ):

    def test_constructor( self ):

        c = THREE.Color()
        self.assertTrue( c.r ) # "Red: " + c.r
        self.assertTrue( c.g ) # "Green: " + c.g
        self.assertTrue( c.b ) # "Blue: " + c.b

    def test_rgb_constructor( self ):

        c = THREE.Color( 1, 1, 1 )
        self.assertEqual( c.r, 1 ) # Passed
        self.assertEqual( c.g, 1 ) # Passed
        self.assertEqual( c.b, 1 ) # Passed

    def test_copyHex( self ):

        c = THREE.Color()
        c2 = THREE.Color(0xF5FFFA)
        c.copy(c2)
        self.assertEqual( c.getHex(), c2.getHex() ) # "Hex c: " + c.getHex() + " Hex c2: " + c2.getHex()

    def test_copyColorString( self ):

        c = THREE.Color()
        c2 = THREE.Color("ivory")
        c.copy(c2)
        self.assertEqual( c.getHex(), c2.getHex() ) # "Hex c: " + c.getHex() + " Hex c2: " + c2.getHex()

    def test_setRGB( self ):

        c = THREE.Color()
        c.setRGB(1, 0.2, 0.1)
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0.2 ) # "Green: " + c.g
        self.assertEqual( c.b, 0.1 ) # "Blue: " + c.b

    def test_copyGammaToLinear( self ):

        c = THREE.Color()
        c2 = THREE.Color()
        c2.setRGB(0.3, 0.5, 0.9)
        c.copyGammaToLinear(c2)
        self.assertEqual( c.r, 0.09 ) # "Red c: " + c.r + " Red c2: " + c2.r
        self.assertEqual( c.g, 0.25 ) # "Green c: " + c.g + " Green c2: " + c2.g
        self.assertEqual( c.b, 0.81 ) # "Blue c: " + c.b + " Blue c2: " + c2.b

    def test_copyLinearToGamma( self ):

        c = THREE.Color()
        c2 = THREE.Color()
        c2.setRGB(0.09, 0.25, 0.81)
        c.copyLinearToGamma(c2)
        self.assertEqual( c.r, 0.3 ) # "Red c: " + c.r + " Red c2: " + c2.r
        self.assertEqual( c.g, 0.5 ) # "Green c: " + c.g + " Green c2: " + c2.g
        self.assertEqual( c.b, 0.9 ) # "Blue c: " + c.b + " Blue c2: " + c2.b

    def test_convertGammaToLinear( self ):

        c = THREE.Color()
        c.setRGB(0.3, 0.5, 0.9)
        c.convertGammaToLinear()
        self.assertEqual( c.r, 0.09 ) # "Red: " + c.r
        self.assertEqual( c.g, 0.25 ) # "Green: " + c.g
        self.assertEqual( c.b, 0.81 ) # "Blue: " + c.b

    def test_convertLinearToGamma( self ):

        c = THREE.Color()
        c.setRGB(4, 9, 16)
        c.convertLinearToGamma()
        self.assertEqual( c.r, 2 ) # "Red: " + c.r
        self.assertEqual( c.g, 3 ) # "Green: " + c.g
        self.assertEqual( c.b, 4 ) # "Blue: " + c.b

    def test_setWithNum( self ):

        c = THREE.Color()
        c.set(0xFF0000)
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0 ) # "Green: " + c.g
        self.assertEqual( c.b, 0 ) # "Blue: " + c.b

    def test_setWithString( self ):

        c = THREE.Color()
        c.set("silver")
        self.assertEqual( c.getHex(), 0xC0C0C0 ) # "Hex c: " + c.getHex()

    def test_clone( self ):

        c = THREE.Color("teal")
        c2 = c.clone()
        self.assertEqual( c2.getHex(), 0x008080 ) # "Hex c2: " + c2.getHex()

    def test_lerp( self ):

        c = THREE.Color()
        c2 = THREE.Color()
        c.setRGB(0, 0, 0)
        c.lerp(c2, 0.2)
        self.assertEqual( c.r, 0.2 ) # "Red: " + c.r
        self.assertEqual( c.g, 0.2 ) # "Green: " + c.g
        self.assertEqual( c.b, 0.2 ) # "Blue: " + c.b

    def test_setStyleRGBRed( self ):

        c = THREE.Color()
        c.setStyle("rgb(255,0,0)")
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0 ) # "Green: " + c.g
        self.assertEqual( c.b, 0 ) # "Blue: " + c.b

    def test_setStyleRGBARed( self ):

        c = THREE.Color()
        c.setStyle("rgba(255,0,0,0.5)")
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0 ) # "Green: " + c.g
        self.assertEqual( c.b, 0 ) # "Blue: " + c.b

    def test_setStyleRGBRedWithSpaces( self ):

        c = THREE.Color()
        c.setStyle("rgb( 255 , 0,   0 )")
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0 ) # "Green: " + c.g
        self.assertEqual( c.b, 0 ) # "Blue: " + c.b

    def test_setStyleRGBARedWithSpaces( self ):

        c = THREE.Color()
        c.setStyle("rgba( 255,  0,  0  , 1 )")
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0 ) # "Green: " + c.g
        self.assertEqual( c.b, 0 ) # "Blue: " + c.b

    def test_setStyleRGBPercent( self ):

        c = THREE.Color()
        c.setStyle("rgb(100%,50%,10%)")
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0.5 ) # "Green: " + c.g
        self.assertEqual( c.b, 0.1 ) # "Blue: " + c.b

    def test_setStyleRGBAPercent( self ):

        c = THREE.Color()
        c.setStyle("rgba(100%,50%,10%, 0.5)")
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0.5 ) # "Green: " + c.g
        self.assertEqual( c.b, 0.1 ) # "Blue: " + c.b

    def test_setStyleRGBPercentWithSpaces( self ):

        c = THREE.Color()
        c.setStyle("rgb( 100% ,50%  , 10% )")
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0.5 ) # "Green: " + c.g
        self.assertEqual( c.b, 0.1 ) # "Blue: " + c.b

    def test_setStyleRGBAPercentWithSpaces( self ):

        c = THREE.Color()
        c.setStyle("rgba( 100% ,50%  ,  10%, 0.5 )")
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0.5 ) # "Green: " + c.g
        self.assertEqual( c.b, 0.1 ) # "Blue: " + c.b

    def test_setStyleHSLRed( self ):

        c = THREE.Color()
        c.setStyle("hsl(360,100%,50%)")
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0 ) # "Green: " + c.g
        self.assertEqual( c.b, 0 ) # "Blue: " + c.b

    def test_setStyleHSLARed( self ):

        c = THREE.Color()
        c.setStyle("hsla(360,100%,50%,0.5)")
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0 ) # "Green: " + c.g
        self.assertEqual( c.b, 0 ) # "Blue: " + c.b

    def test_setStyleHSLRedWithSpaces( self ):

        c = THREE.Color()
        c.setStyle("hsl(360,  100% , 50% )")
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0 ) # "Green: " + c.g
        self.assertEqual( c.b, 0 ) # "Blue: " + c.b

    def test_setStyleHSLARedWithSpaces( self ):

        c = THREE.Color()
        c.setStyle("hsla( 360,  100% , 50%,  0.5 )")
        self.assertEqual( c.r, 1 ) # "Red: " + c.r
        self.assertEqual( c.g, 0 ) # "Green: " + c.g
        self.assertEqual( c.b, 0 ) # "Blue: " + c.b

    def test_setStyleHexSkyBlue( self ):

        c = THREE.Color()
        c.setStyle("#87CEEB")
        self.assertEqual( c.getHex(), 0x87CEEB ) # "Hex c: " + c.getHex()

    def test_setStyleHexSkyBlueMixed( self ):

        c = THREE.Color()
        c.setStyle("#87cEeB")
        self.assertEqual( c.getHex(), 0x87CEEB ) # "Hex c: " + c.getHex()

    def test_setStyleHex2Olive( self ):

        c = THREE.Color()
        c.setStyle("#F00")
        self.assertEqual( c.getHex(), 0xFF0000 ) # "Hex c: " + c.getHex()

    def test_setStyleHex2OliveMixed( self ):

        c = THREE.Color()
        c.setStyle("#f00")
        self.assertEqual( c.getHex(), 0xFF0000 ) # "Hex c: " + c.getHex()

    def test_setStyleColorName( self ):

        c = THREE.Color()
        c.setStyle("powderblue")
        self.assertEqual( c.getHex(), 0xB0E0E6 ) # "Hex c: " + c.getHex()

    def test_getHex( self ):

        c = THREE.Color("red")
        res = c.getHex()
        self.assertEqual( res, 0xFF0000 ) # "Hex: " + res

    def test_setHex( self ):

        c = THREE.Color()
        c.setHex(0xFA8072)
        self.assertEqual( c.getHex(), 0xFA8072 ) # "Hex: " + c.getHex()

    def test_getHexString( self ):

        c = THREE.Color("tomato")
        res = c.getHexString()
        self.assertEqual( res, "ff6347" ) # "Hex: " + res

    def test_getStyle( self ):

        c = THREE.Color("plum")
        res = c.getStyle()
        self.assertEqual( res, "rgb(221,160,221)" ) # "style: " + res

    def test_getHSL( self ):

        c = THREE.Color( 0x80ffff )
        hsl = c.getHSL()

        self.assertEqual( hsl[ "h" ], 0.5 ) # "hue: " + hsl.h
        self.assertEqual( hsl[ "s" ], 1.0 ) # "saturation: " + hsl.s
        self.assertEqual( ( round( float( hsl[ "l" ] ) * 100 ) / 100 ), 0.75 ) # "lightness: " + hsl.l

    def test_setHSL( self ):

        c = THREE.Color()
        c.setHSL(0.75, 1.0, 0.25)
        hsl = c.getHSL()

        self.assertEqual( hsl[ "h" ], 0.75 ) # "hue: " + hsl.h
        self.assertEqual( hsl[ "s" ], 1.00 ) # "saturation: " + hsl.s
        self.assertEqual( hsl[ "l" ], 0.25 ) # "lightness: " + hsl.l
