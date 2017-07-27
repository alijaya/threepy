from __future__ import division
import unittest
import math

import THREE

from Constants import *

class TestVector2( unittest.TestCase ):

    def setUp( self ):

        self.addTypeEqualityFunc( THREE.Vector2, self.assertVector2Equal )

    def assertVector2Equal( self, first, second, msg = None ):

        self.assertEqual( first.x, second.x, msg )
        self.assertEqual( first.y, second.y, msg )

    def test_constructor( self ):

        a = THREE.Vector2()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )

        a = THREE.Vector2( x, y )
        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )

    def test_copy( self ):

        a = THREE.Vector2( x, y )
        b = THREE.Vector2().copy( a )
        self.assertEqual( b.x, x )
        self.assertEqual( b.y, y )

        # ensure that it is a true copy
        a.x = 0
        a.y = -1
        self.assertEqual( b.x, x )
        self.assertEqual( b.y, y )
    
    def test_set( self ):

        a = THREE.Vector2()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )

        a.set( x, y )
        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )
    
    def test_setX_setY( self ):

        a = THREE.Vector2()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )

        a.setX( x )
        a.setY( y )
        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )

    def test_setComponent_getComponent( self ):

        a = THREE.Vector2()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )

        a.setComponent( 0, 1 )
        a.setComponent( 1, 2 )
        self.assertEqual( a.getComponent( 0 ), 1 )
        self.assertEqual( a.getComponent( 1 ), 2 )

    def test_add( self ):

        a = THREE.Vector2( x, y )
        b = THREE.Vector2( -x, -y )

        a.add( b )
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )

        c = THREE.Vector2().addVectors( b, b )
        self.assertEqual( c.x, -2 * x )
        self.assertEqual( c.y, -2 * y )

    def test_sub( self ):

        a = THREE.Vector2( x, y )
        b = THREE.Vector2( -x, -y )

        a.sub( b )
        self.assertEqual( a.x, 2 * x )
        self.assertEqual( a.y, 2 * y )

        c = THREE.Vector2().subVectors( a, a )
        self.assertEqual( c.x, 0 )
        self.assertEqual( c.y, 0 )
    
    def test_multiply_divide( self ):

        a = THREE.Vector2( x, y )
        b = THREE.Vector2( -x, -y )

        a.multiplyScalar( -2 )
        self.assertEqual( a.x, x * -2 )
        self.assertEqual( a.y, y * -2 )

        b.multiplyScalar( -2 )
        self.assertEqual( b.x, 2 * x )
        self.assertEqual( b.y, 2 * y )

        a.divideScalar( -2 )
        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )

        b.divideScalar( -2 )
        self.assertEqual( b.x, -x )
        self.assertEqual( b.y, -y )

    def test_min_max_clamp( self ):

        a = THREE.Vector2( x, y )
        b = THREE.Vector2( -x, -y )
        c = THREE.Vector2()

        c.copy( a ).min( b )
        self.assertEqual( c.x, -x )
        self.assertEqual( c.y, -y )

        c.copy( a ).max( b )
        self.assertEqual( c.x, x )
        self.assertEqual( c.y, y )

        c.set( -2 * x, 2 * y )
        c.clamp( b, a )
        self.assertEqual( c.x, -x )
        self.assertEqual( c.y, y )
        
        c.set( -2 * x, 2 * x )
        c.clampScalar( -x, x )
        self.assertEqual( c.x, -x )
        self.assertEqual( c.y, x )

    def test_rounding( self ):

        self.assertEqual( THREE.Vector2( -0.1, 0.1 ).floor(), THREE.Vector2( -1, 0 ) )
        self.assertEqual( THREE.Vector2( -0.5, 0.5 ).floor(), THREE.Vector2( -1, 0 ) )
        self.assertEqual( THREE.Vector2( -0.9, 0.9 ).floor(), THREE.Vector2( -1, 0 ) )

        self.assertEqual( THREE.Vector2( -0.1, 0.1 ).ceil(), THREE.Vector2( 0, 1 ) )
        self.assertEqual( THREE.Vector2( -0.5, 0.5 ).ceil(), THREE.Vector2( 0, 1 ) )
        self.assertEqual( THREE.Vector2( -0.9, 0.9 ).ceil(), THREE.Vector2( 0, 1 ) )

        self.assertEqual( THREE.Vector2( -0.1, 0.1 ).round(), THREE.Vector2( 0, 0 ) )
        self.assertEqual( THREE.Vector2( -0.5, 0.5 ).round(), THREE.Vector2( -1, 1 ) ) # on JS, it's 0, 1, different rounding behaviour
        self.assertEqual( THREE.Vector2( -0.9, 0.9 ).round(), THREE.Vector2( -1, 1 ) )

        self.assertEqual( THREE.Vector2( -0.1, 0.1 ).roundToZero(), THREE.Vector2( 0, 0 ) )
        self.assertEqual( THREE.Vector2( -0.5, 0.5 ).roundToZero(), THREE.Vector2( 0, 0 ) )
        self.assertEqual( THREE.Vector2( -0.9, 0.9 ).roundToZero(), THREE.Vector2( 0, 0 ) )
        self.assertEqual( THREE.Vector2( -1.1, 1.1 ).roundToZero(), THREE.Vector2( -1, 1 ) )
        self.assertEqual( THREE.Vector2( -1.5, 1.5 ).roundToZero(), THREE.Vector2( -1, 1 ) )
        self.assertEqual( THREE.Vector2( -1.9, 1.9 ).roundToZero(), THREE.Vector2( -1, 1 ) )
    
    def test_negate( self ):

        a = THREE.Vector2( x, y )

        a.negate()
        self.assertEqual( a.x, -x )
        self.assertEqual( a.y, -y )

    def test_dot( self ):
        a = THREE.Vector2( x, y )
        b = THREE.Vector2( -x, -y )
        c = THREE.Vector2()

        result = a.dot( b )
        self.assertEqual( result, - x * x - y * y )

        result = a.dot( c )
        self.assertEqual( result, 0 )
    
    def test_length_lengthSq( self ):

        a = THREE.Vector2( x, 0 )
        b = THREE.Vector2( 0, -y )
        c = THREE.Vector2()

        self.assertEqual( a.length(), x )
        self.assertEqual( a.lengthSq(), x * x )
        self.assertEqual( b.length(), y )
        self.assertEqual( b.lengthSq(), y * y )
        self.assertEqual( c.length(), 0 )
        self.assertEqual( c.lengthSq(), 0 )

        a.set( x, y )
        self.assertEqual( a.length(), math.sqrt( x * x + y * y ) )
        self.assertEqual( a.lengthSq(), x * x + y * y )
    
    def test_normalize( self ):

        a = THREE.Vector2( x, 0 )
        b = THREE.Vector2( 0, -y )
        c = THREE.Vector2()

        a.normalize()
        self.assertEqual( a.length(), 1 )
        self.assertEqual( a.x, 1 )

        b.normalize()
        self.assertEqual( b.length(), 1 )
        self.assertEqual( b.y, -1 )

    def test_distanceTo_distanceToSquared( self ):

        a = THREE.Vector2( x, 0 )
        b = THREE.Vector2( 0, -y )
        c = THREE.Vector2()

        self.assertEqual( a.distanceTo( c ), x )
        self.assertEqual( a.distanceToSquared( c ), x * x )

        self.assertEqual( b.distanceTo( c ), y )
        self.assertEqual( b.distanceToSquared( c ), y * y )

    def test_setLength( self ):

        a = THREE.Vector2( x, 0 )

        self.assertEqual( a.length(), x )
        a.setLength( y )
        self.assertEqual( a.length(), y )

        a = THREE.Vector2( 0, 0 )
        self.assertEqual( a.length(), 0 )
        a.setLength( y )
        self.assertEqual( a.length(), 0 ) # no effect
    
    def test_lerp_clone( self ):

        a = THREE.Vector2( x, 0 )
        b = THREE.Vector2( 0, -y )

        self.assertTrue( a.lerp( a, 0 ).equals( a.lerp( a, 0.5 ) ) )
        self.assertTrue( a.lerp( a, 0 ).equals( a.lerp( a, 1 ) ) )

        self.assertTrue( a.clone().lerp( b, 0 ).equals( a ) )

        self.assertEqual( a.clone().lerp( b, 0.5 ).x, x * 0.5 )
        self.assertEqual( a.clone().lerp( b, 0.5 ).y, -y * 0.5 )

        self.assertTrue( a.clone().lerp( b, 1 ).equals( b ) )

    def test_equals( self ):

        a = THREE.Vector2( x, 0 )
        b = THREE.Vector2( 0, -y )

        self.assertNotEqual( a.x, b.x )
        self.assertNotEqual( a.y, b.y )

        self.assertFalse( a.equals( b ) )
        self.assertFalse( b.equals( a ) )

        a.copy( b )
        self.assertEqual( a.x, b.x )
        self.assertEqual( a.y, b.y )

        self.assertTrue( a.equals( b ) )
        self.assertTrue( b.equals( a ) )