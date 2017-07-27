from __future__ import division
import unittest
import math

import THREE

from Constants import *

class TestVector3( unittest.TestCase ):

    def setUp( self ):

        self.addTypeEqualityFunc( THREE.Vector3, self.assertVector3Equal )

    def assertVector3Equal( self, first, second, msg = None ):

        self.assertEqual( first.x, second.x, msg )
        self.assertEqual( first.y, second.y, msg )
        self.assertEqual( first.z, second.z, msg )

    def test_constructor( self ):

        a = THREE.Vector3()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )
        self.assertEqual( a.z, 0 )

        a = THREE.Vector3( x, y, z )
        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )
        self.assertEqual( a.z, z )

    def test_copy( self ):

        a = THREE.Vector3( x, y, z )
        b = THREE.Vector3().copy( a )
        self.assertEqual( b.x, x )
        self.assertEqual( b.y, y )
        self.assertEqual( b.z, z )

        # ensure that it is a true copy
        a.x = 0
        a.y = -1
        a.z = -2
        self.assertEqual( b.x, x )
        self.assertEqual( b.y, y )
        self.assertEqual( b.z, z )
    
    def test_set( self ):

        a = THREE.Vector3()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )
        self.assertEqual( a.z, 0 )

        a.set( x, y, z )
        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )
        self.assertEqual( a.z, z )
    
    def test_setX_setY_setZ( self ):

        a = THREE.Vector3()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )
        self.assertEqual( a.z, 0 )

        a.setX( x )
        a.setY( y )
        a.setZ( z )

        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )
        self.assertEqual( a.z, z )

    def test_setComponent_getComponent( self ):

        a = THREE.Vector3()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )
        self.assertEqual( a.z, 0 )

        a.setComponent( 0, 1 )
        a.setComponent( 1, 2 )
        a.setComponent( 2, 3 )
        self.assertEqual( a.getComponent( 0 ), 1 )
        self.assertEqual( a.getComponent( 1 ), 2 )
        self.assertEqual( a.getComponent( 2 ), 3 )

    def test_add( self ):

        a = THREE.Vector3( x, y, z )
        b = THREE.Vector3( -x, -y, -z )

        a.add( b )
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )
        self.assertEqual( a.z, 0 )

        c = THREE.Vector3().addVectors( b, b )
        self.assertEqual( c.x, -2 * x )
        self.assertEqual( c.y, -2 * y )
        self.assertEqual( c.z, -2 * z )

    def test_sub( self ):

        a = THREE.Vector3( x, y, z )
        b = THREE.Vector3( -x, -y, -z )

        a.sub( b )
        self.assertEqual( a.x, 2 * x )
        self.assertEqual( a.y, 2 * y )
        self.assertEqual( a.z, 2 * z )

        c = THREE.Vector3().subVectors( a, a )
        self.assertEqual( c.x, 0 )
        self.assertEqual( c.y, 0 )
        self.assertEqual( c.z, 0 )
    
    def test_multiply_divide( self ):

        a = THREE.Vector3( x, y, z )
        b = THREE.Vector3( -x, -y, -z )

        a.multiplyScalar( -2 )
        self.assertEqual( a.x, x * -2 )
        self.assertEqual( a.y, y * -2 )
        self.assertEqual( a.z, z * -2 )

        b.multiplyScalar( -2 )
        self.assertEqual( b.x, 2 * x )
        self.assertEqual( b.y, 2 * y )
        self.assertEqual( b.z, 2 * z )

        a.divideScalar( -2 )
        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )
        self.assertEqual( a.z, z )

        b.divideScalar( -2 )
        self.assertEqual( b.x, -x )
        self.assertEqual( b.y, -y )
        self.assertEqual( b.z, -z )

    def test_min_max_clamp( self ):

        a = THREE.Vector3( x, y, z )
        b = THREE.Vector3( -x, -y, -z )
        c = THREE.Vector3()

        c.copy( a ).min( b )
        self.assertEqual( c.x, -x )
        self.assertEqual( c.y, -y )
        self.assertEqual( c.z, -z )

        c.copy( a ).max( b )
        self.assertEqual( c.x, x )
        self.assertEqual( c.y, y )
        self.assertEqual( c.z, z )

        c.set( -2 * x, 2 * y, -2 * z )
        c.clamp( b, a )
        self.assertEqual( c.x, -x )
        self.assertEqual( c.y, y )
        self.assertEqual( c.z, -z )

    def test_negate( self ):

        a = THREE.Vector3( x, y, z )

        a.negate()
        self.assertEqual( a.x, -x )
        self.assertEqual( a.y, -y )
        self.assertEqual( a.z, -z )

    def test_dot( self ):
        a = THREE.Vector3( x, y, z )
        b = THREE.Vector3( -x, -y, -z )
        c = THREE.Vector3()

        result = a.dot( b )
        self.assertEqual( result, - x * x - y * y - z * z )

        result = a.dot( c )
        self.assertEqual( result, 0 )
    
    def test_length_lengthSq( self ):

        a = THREE.Vector3( x, 0, 0 )
        b = THREE.Vector3( 0, -y, 0 )
        c = THREE.Vector3( 0, 0, z)
        d = THREE.Vector3()

        self.assertEqual( a.length(), x )
        self.assertEqual( a.lengthSq(), x * x )
        self.assertEqual( b.length(), y )
        self.assertEqual( b.lengthSq(), y * y )
        self.assertEqual( c.length(), z )
        self.assertEqual( c.lengthSq(), z * z )
        self.assertEqual( d.length(), 0 )
        self.assertEqual( d.lengthSq(), 0 )

        a.set( x, y, z )
        self.assertEqual( a.length(), math.sqrt( x * x + y * y + z * z ) )
        self.assertEqual( a.lengthSq(), x * x + y * y + z * z )
    
    def test_normalize( self ):

        a = THREE.Vector3( x, 0, 0 )
        b = THREE.Vector3( 0, -y, 0 )
        c = THREE.Vector3( 0, 0, z)

        a.normalize()
        self.assertEqual( a.length(), 1 )
        self.assertEqual( a.x, 1 )

        b.normalize()
        self.assertEqual( b.length(), 1 )
        self.assertEqual( b.y, -1 )

        c.normalize()
        self.assertEqual( c.length(), 1 )
        self.assertEqual( c.z, 1 )

    def test_distanceTo_distanceToSquared( self ):

        a = THREE.Vector3( x, 0, 0 )
        b = THREE.Vector3( 0, -y, 0 )
        c = THREE.Vector3( 0, 0, z )
        d = THREE.Vector3()

        self.assertEqual( a.distanceTo( d ), x )
        self.assertEqual( a.distanceToSquared( d ), x * x )

        self.assertEqual( b.distanceTo( d ), y )
        self.assertEqual( b.distanceToSquared( d ), y * y )

        self.assertEqual( c.distanceTo( d ), z )
        self.assertEqual( c.distanceToSquared( d ), z * z )

    def test_setLength( self ):

        a = THREE.Vector3( x, 0, 0 )

        self.assertEqual( a.length(), x )
        a.setLength( y )
        self.assertEqual( a.length(), y )

        a = THREE.Vector3( 0, 0, 0 )
        self.assertEqual( a.length(), 0 )
        a.setLength( y )
        self.assertEqual( a.length(), 0 ) # no effect
    
    def test_projectOnVector( self ):

        a = THREE.Vector3( 1, 0, 0 )
        b = THREE.Vector3()
        normal = THREE.Vector3( 10, 0, 0 )

        self.assertEqual( b.copy( a ).projectOnVector( normal ), THREE.Vector3( 1, 0, 0 ) )
        self.assertTrue( b.copy( a ).projectOnVector( normal ).equals( THREE.Vector3( 1, 0, 0 ) ) )

        a.set( 0, 1, 0 )
        self.assertTrue( b.copy( a ).projectOnVector( normal ).equals( THREE.Vector3( 0, 0, 0 ) ) )

        a.set( 0, 0, -1 )
        self.assertTrue( b.copy( a ).projectOnVector( normal ).equals( THREE.Vector3( 0, 0, 0 ) ) )

        a.set( -1, 0, 0 )
        self.assertTrue( b.copy( a ).projectOnVector( normal ).equals( THREE.Vector3( -1, 0, 0 ) ) )

    def test_projectOnPlane( self ):

        a = THREE.Vector3( 1, 0, 0 )
        b = THREE.Vector3()
        normal = THREE.Vector3( 1, 0, 0 )

        self.assertTrue( b.copy( a ).projectOnPlane( normal ).equals( THREE.Vector3( 0, 0, 0 ) ) )

        a.set( 0, 1, 0 )
        self.assertTrue( b.copy( a ).projectOnPlane( normal ).equals( THREE.Vector3( 0, 1, 0 ) ) )

        a.set( 0, 0, -1 )
        self.assertTrue( b.copy( a ).projectOnPlane( normal ).equals( THREE.Vector3( 0, 0, -1 ) ) )

        a.set( -1, 0, 0 )
        self.assertTrue( b.copy( a ).projectOnPlane( normal ).equals( THREE.Vector3( 0, 0, 0 ) ) )

    def test_reflect( self ):

        a = THREE.Vector3()
        normal = THREE.Vector3( 0, 1, 0 )
        b = THREE.Vector3()

        a.set( 0, -1, 0 )
        self.assertTrue( b.copy( a ).reflect( normal ).equals( THREE.Vector3( 0, 1, 0 ) ) )

        a.set( 1, -1, 0 )
        self.assertTrue( b.copy( a ).reflect( normal ).equals( THREE.Vector3( 1, 1, 0 ) ) )

        a.set( 1, -1, 0 )
        normal.set( 0, -1, 0 )
        self.assertTrue( b.copy( a ).reflect( normal ).equals( THREE.Vector3( 1, 1, 0 ) ) )

    def test_angleTo( self ):

        a = THREE.Vector3( 0, -0.18851655680720186, 0.9820700116639124 )
        b = THREE.Vector3( 0, 0.18851655680720186, -0.9820700116639124 )

        self.assertEqual( a.angleTo( a ), 0 )
        self.assertEqual( a.angleTo( b ), math.pi )

        x = THREE.Vector3( 1, 0, 0 )
        y = THREE.Vector3( 0, 1, 0 )
        z = THREE.Vector3( 0, 0, 1 )

        self.assertEqual( x.angleTo( y ), math.pi / 2 )
        self.assertEqual( x.angleTo( z ), math.pi / 2 )
        self.assertEqual( z.angleTo( x ), math.pi / 2 )

    def test_lerp_clone( self ):

        a = THREE.Vector3( x, 0, z )
        b = THREE.Vector3( 0, -y, 0 )

        self.assertTrue( a.lerp( a, 0 ).equals( a.lerp( a, 0.5 ) ) )
        self.assertTrue( a.lerp( a, 0 ).equals( a.lerp( a, 1 ) ) )

        self.assertTrue( a.clone().lerp( b, 0 ).equals( a ) )

        self.assertEqual( a.clone().lerp( b, 0.5 ).x, x * 0.5 )
        self.assertEqual( a.clone().lerp( b, 0.5 ).y, -y * 0.5 )
        self.assertEqual( a.clone().lerp( b, 0.5 ).z, z * 0.5 )

        self.assertTrue( a.clone().lerp( b, 1 ).equals( b ) )

    def test_equals( self ):

        a = THREE.Vector3( x, 0, z )
        b = THREE.Vector3( 0, -y, 0 )

        self.assertNotEqual( a.x, b.x )
        self.assertNotEqual( a.y, b.y )
        self.assertNotEqual( a.z, b.z )

        self.assertFalse( a.equals( b ) )
        self.assertFalse( b.equals( a ) )

        a.copy( b )
        self.assertEqual( a.x, b.x )
        self.assertEqual( a.y, b.y )
        self.assertEqual( a.z, b.z )

        self.assertTrue( a.equals( b ) )
        self.assertTrue( b.equals( a ) )
    
    def test_applyMatrix4( self ):

        a = THREE.Vector3( x, y, z )
        b = THREE.Vector4( x, y, z, 1 )

        m = THREE.Matrix4().makeRotationX( math.pi )
        a.applyMatrix4( m )
        b.applyMatrix4( m )
        self.assertEqual( a.x, b.x / b.w )
        self.assertEqual( a.y, b.y / b.w )
        self.assertEqual( a.z, b.z / b.w )

        m = THREE.Matrix4().makeTranslation( 3, 2, 1 )
        a.applyMatrix4( m )
        b.applyMatrix4( m )
        self.assertEqual( a.x, b.x / b.w )
        self.assertEqual( a.y, b.y / b.w )
        self.assertEqual( a.z, b.z / b.w )

        m = THREE.Matrix4().set(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 1, 0
        )
        a.applyMatrix4( m )
        b.applyMatrix4( m )
        self.assertEqual( a.x, b.x / b.w )
        self.assertEqual( a.y, b.y / b.w )
        self.assertEqual( a.z, b.z / b.w )