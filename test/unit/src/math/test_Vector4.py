from __future__ import division
import unittest
import math

from THREE import Vector4

from Constants import *

class TestVector4( unittest.TestCase ):

    def setUp( self ):

        self.addTypeEqualityFunc( Vector4, self.assertVector4Equal )

    def assertVector4Equal( self, first, second, msg = None ):

        self.assertEqual( first.x, second.x, msg )
        self.assertEqual( first.y, second.y, msg )
        self.assertEqual( first.z, second.z, msg )
        self.assertEqual( first.w, second.w, msg )

    def test_constructor( self ):

        a = Vector4()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )
        self.assertEqual( a.z, 0 )
        self.assertEqual( a.w, 1 )

        a = Vector4( x, y, z, w )
        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )
        self.assertEqual( a.z, z )
        self.assertEqual( a.w, w )

    def test_copy( self ):

        a = Vector4( x, y, z, w )
        b = Vector4().copy( a )
        self.assertEqual( b.x, x )
        self.assertEqual( b.y, y )
        self.assertEqual( b.z, z )
        self.assertEqual( b.w, w )

        # ensure that it is a true copy
        a.x = 0
        a.y = -1
        a.z = -2
        a.w = -3
        self.assertEqual( b.x, x )
        self.assertEqual( b.y, y )
        self.assertEqual( b.z, z )
        self.assertEqual( b.w, w )
    
    def test_set( self ):

        a = Vector4()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )
        self.assertEqual( a.z, 0 )
        self.assertEqual( a.w, 1 )

        a.set( x, y, z, w )
        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )
        self.assertEqual( a.z, z )
        self.assertEqual( a.w, w )
    
    def test_setX_setY_setZ_setW( self ):

        a = Vector4()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )
        self.assertEqual( a.z, 0 )
        self.assertEqual( a.w, 1 )

        a.setX( x )
        a.setY( y )
        a.setZ( z )
        a.setW( w )

        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )
        self.assertEqual( a.z, z )
        self.assertEqual( a.w, w )

    def test_setComponent_getComponent( self ):

        a = Vector4()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )
        self.assertEqual( a.z, 0 )
        self.assertEqual( a.w, 1 )

        a.setComponent( 0, 1 )
        a.setComponent( 1, 2 )
        a.setComponent( 2, 3 )
        a.setComponent( 3, 4 )
        self.assertEqual( a.getComponent( 0 ), 1 )
        self.assertEqual( a.getComponent( 1 ), 2 )
        self.assertEqual( a.getComponent( 2 ), 3 )
        self.assertEqual( a.getComponent( 3 ), 4 )

    def test_add( self ):

        a = Vector4( x, y, z, w )
        b = Vector4( -x, -y, -z, -w )

        a.add( b )
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )
        self.assertEqual( a.z, 0 )
        self.assertEqual( a.w, 0 )

        c = Vector4().addVectors( b, b )
        self.assertEqual( c.x, -2 * x )
        self.assertEqual( c.y, -2 * y )
        self.assertEqual( c.z, -2 * z )
        self.assertEqual( c.w, -2 * w )

    def test_sub( self ):

        a = Vector4( x, y, z, w )
        b = Vector4( -x, -y, -z, -w )

        a.sub( b )
        self.assertEqual( a.x, 2 * x )
        self.assertEqual( a.y, 2 * y )
        self.assertEqual( a.z, 2 * z )
        self.assertEqual( a.w, 2 * w )

        c = Vector4().subVectors( a, a )
        self.assertEqual( c.x, 0 )
        self.assertEqual( c.y, 0 )
        self.assertEqual( c.z, 0 )
        self.assertEqual( c.w, 0 )
    
    def test_multiply_divide( self ):

        a = Vector4( x, y, z, w )
        b = Vector4( -x, -y, -z, -w )

        a.multiplyScalar( -2 )
        self.assertEqual( a.x, x * -2 )
        self.assertEqual( a.y, y * -2 )
        self.assertEqual( a.z, z * -2 )
        self.assertEqual( a.w, w * -2 )

        b.multiplyScalar( -2 )
        self.assertEqual( b.x, 2 * x )
        self.assertEqual( b.y, 2 * y )
        self.assertEqual( b.z, 2 * z )
        self.assertEqual( b.w, 2 * w )

        a.divideScalar( -2 )
        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )
        self.assertEqual( a.z, z )
        self.assertEqual( a.w, w )

        b.divideScalar( -2 )
        self.assertEqual( b.x, -x )
        self.assertEqual( b.y, -y )
        self.assertEqual( b.z, -z )
        self.assertEqual( b.w, -w )

    def test_min_max_clamp( self ):

        a = Vector4( x, y, z, w )
        b = Vector4( -x, -y, -z, -w )
        c = Vector4()

        c.copy( a ).min( b )
        self.assertEqual( c.x, -x )
        self.assertEqual( c.y, -y )
        self.assertEqual( c.z, -z )
        self.assertEqual( c.w, -w )

        c.copy( a ).max( b )
        self.assertEqual( c.x, x )
        self.assertEqual( c.y, y )
        self.assertEqual( c.z, z )
        self.assertEqual( c.w, w )

        c.set( -2 * x, 2 * y, -2 * z, 2 * w )
        c.clamp( b, a )
        self.assertEqual( c.x, -x )
        self.assertEqual( c.y, y )
        self.assertEqual( c.z, -z )
        self.assertEqual( c.w, w )

    def test_negate( self ):

        a = Vector4( x, y, z, w )

        a.negate()
        self.assertEqual( a.x, -x )
        self.assertEqual( a.y, -y )
        self.assertEqual( a.z, -z )
        self.assertEqual( a.w, -w )

    def test_dot( self ):
        a = Vector4( x, y, z, w )
        b = Vector4( -x, -y, -z, -w )
        c = Vector4( 0, 0, 0, 0 )

        result = a.dot( b )
        self.assertEqual( result, - x * x - y * y - z * z - w * w )

        result = a.dot( c )
        self.assertEqual( result, 0 )
    
    def test_length_lengthSq( self ):

        a = Vector4( x, 0, 0, 0 )
        b = Vector4( 0, -y, 0, 0 )
        c = Vector4( 0, 0, z, 0 )
        d = Vector4( 0, 0, 0, w )
        e = Vector4( 0, 0, 0, 0 )

        self.assertEqual( a.length(), x )
        self.assertEqual( a.lengthSq(), x * x )
        self.assertEqual( b.length(), y )
        self.assertEqual( b.lengthSq(), y * y )
        self.assertEqual( c.length(), z )
        self.assertEqual( c.lengthSq(), z * z )
        self.assertEqual( d.length(), w )
        self.assertEqual( d.lengthSq(), w * w )
        self.assertEqual( e.length(), 0 )
        self.assertEqual( e.lengthSq(), 0 )

        a.set( x, y, z, w )
        self.assertEqual( a.length(), math.sqrt( x * x + y * y + z * z + w * w ) )
        self.assertEqual( a.lengthSq(), x * x + y * y + z * z + w * w )
    
    def test_normalize( self ):

        a = Vector4( x, 0, 0, 0 )
        b = Vector4( 0, -y, 0, 0 )
        c = Vector4( 0, 0, z, 0 )
        d = Vector4( 0, 0, 0, -w )

        a.normalize()
        self.assertEqual( a.length(), 1 )
        self.assertEqual( a.x, 1 )

        b.normalize()
        self.assertEqual( b.length(), 1 )
        self.assertEqual( b.y, -1 )

        c.normalize()
        self.assertEqual( c.length(), 1 )
        self.assertEqual( c.z, 1 )

        d.normalize()
        self.assertEqual( d.length(), 1 )
        self.assertEqual( d.w, -1 )

    # def test_distanceTo_distanceToSquared( self ):

    #     a = Vector4( x, 0, 0, 0 )
    #     b = Vector4( 0, -y, 0, 0 )
    #     c = Vector4( 0, 0, z, 0 )
    #     d = Vector4( 0, 0, 0, -w )
    #     e = Vector4()

    #     self.assertEqual( a.distanceTo( e ), x )
    #     self.assertEqual( a.distanceToSquared( e ), x * x )

    #     self.assertEqual( b.distanceTo( e ), y )
    #     self.assertEqual( b.distanceToSquared( e ), y * y )

    #     self.assertEqual( c.distanceTo( e ), z )
    #     self.assertEqual( c.distanceToSquared( e ), z * z )
        
    #     self.assertEqual( d.distanceTo( e ), w )
    #     self.assertEqual( d.distanceToSquared( e ), w * w )

    def test_setLength( self ):

        a = Vector4( x, 0, 0, 0 )

        self.assertEqual( a.length(), x )
        a.setLength( y )
        self.assertEqual( a.length(), y )

        a = Vector4( 0, 0, 0, 0 )
        self.assertEqual( a.length(), 0 )
        a.setLength( y )
        self.assertEqual( a.length(), 0 ) # no effect
    
    def test_lerp_clone( self ):

        a = Vector4( x, 0, z, 0 )
        b = Vector4( 0, -y, 0, -w )

        self.assertTrue( a.lerp( a, 0 ).equals( a.lerp( a, 0.5 ) ) )
        self.assertTrue( a.lerp( a, 0 ).equals( a.lerp( a, 1 ) ) )

        self.assertTrue( a.clone().lerp( b, 0 ).equals( a ) )

        self.assertEqual( a.clone().lerp( b, 0.5 ).x, x * 0.5 )
        self.assertEqual( a.clone().lerp( b, 0.5 ).y, -y * 0.5 )
        self.assertEqual( a.clone().lerp( b, 0.5 ).z, z * 0.5 )
        self.assertEqual( a.clone().lerp( b, 0.5 ).w, -w * 0.5 )

        self.assertTrue( a.clone().lerp( b, 1 ).equals( b ) )

    def test_equals( self ):

        a = Vector4( x, 0, z, 0 )
        b = Vector4( 0, -y, 0, -w )

        self.assertNotEqual( a.x, b.x )
        self.assertNotEqual( a.y, b.y )
        self.assertNotEqual( a.z, b.z )
        self.assertNotEqual( a.w, b.w )

        self.assertFalse( a.equals( b ) )
        self.assertFalse( b.equals( a ) )

        a.copy( b )
        self.assertEqual( a.x, b.x )
        self.assertEqual( a.y, b.y )
        self.assertEqual( a.z, b.z )
        self.assertEqual( a.w, b.w )

        self.assertTrue( a.equals( b ) )
        self.assertTrue( b.equals( a ) )
