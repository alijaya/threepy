from __future__ import division
import unittest
import math
import sys

import THREE

from Constants import *


orders = [ 'XYZ', 'YXZ', 'ZXY', 'ZYX', 'YZX', 'XZY' ]
eulerAngles = THREE.Euler( 0.1, -0.3, 0.25 )

def qSub ( a, b ):

	result = THREE.Quaternion()
	result.copy( a )

	result.x -= b.x
	result.y -= b.y
	result.z -= b.z
	result.w -= b.w

	return result

def doSlerpObject( aArr, bArr, t ):

    a = THREE.Quaternion().fromArray( aArr )
    b = THREE.Quaternion().fromArray( bArr )
    c = THREE.Quaternion().fromArray( aArr )

    c.slerp( b, t )

    def equals( x, y, z, w, maxError = sys.float_info.epsilon ):

        return 	abs( x - c.x ) <= maxError and \
                abs( y - c.y ) <= maxError and \
                abs( z - c.z ) <= maxError and \
                abs( w - c.w ) <= maxError

    return {

        "equals": equals,

        "length": c.length(),

        "dotA": c.dot( a ),
        "dotB": c.dot( b )

    }

def doSlerpArray( a, b, t ):

    result = [ 0, 0, 0, 0 ]

    THREE.Quaternion.slerpFlat( result, 0, a, 0, b, 0, t )

    def arrDot( a, b ):

        return 	a[ 0 ] * b[ 0 ] + a[ 1 ] * b[ 1 ] + \
                a[ 2 ] * b[ 2 ] + a[ 3 ] * b[ 3 ]

    def equals( x, y, z, w, maxError = sys.float_info.epsilon ):

        return 	abs( x - result[ 0 ] ) <= maxError and \
                abs( y - result[ 1 ] ) <= maxError and \
                abs( z - result[ 2 ] ) <= maxError and \
                abs( w - result[ 3 ] ) <= maxError

    return {

        "equals": equals,

        "length": math.sqrt( arrDot( result, result ) ),

        "dotA": arrDot( result, a ),
        "dotB": arrDot( result, b )

    }

class TestQuaternion( unittest.TestCase ):

    def test_constructor( self ):

        a = THREE.Quaternion()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )
        self.assertEqual( a.z, 0 )
        self.assertEqual( a.w, 1 )

        a = THREE.Quaternion( x, y, z, w )
        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )
        self.assertEqual( a.z, z )
        self.assertEqual( a.w, w )

    def test_copy( self ):

        a = THREE.Quaternion( x, y, z, w )
        b = THREE.Quaternion().copy( a )
        self.assertEqual( b.x, x )
        self.assertEqual( b.y, y )
        self.assertEqual( b.z, z )
        self.assertEqual( b.w, w )

        # ensure that it is a true copy
        a.x = 0
        a.y = -1
        a.z = 0
        a.w = -1
        self.assertEqual( b.x, x )
        self.assertEqual( b.y, y )

    def test_set( self ):

        a = THREE.Quaternion()
        self.assertEqual( a.x, 0 )
        self.assertEqual( a.y, 0 )
        self.assertEqual( a.z, 0 )
        self.assertEqual( a.w, 1 )

        a.set( x, y, z, w )
        self.assertEqual( a.x, x )
        self.assertEqual( a.y, y )
        self.assertEqual( a.z, z )
        self.assertEqual( a.w, w )

    def test_setFromAxisAngle( self ):

        # TODO: find cases to validate.
        self.assertTrue( True )

        zero = THREE.Quaternion()

        a = THREE.Quaternion().setFromAxisAngle( THREE.Vector3( 1, 0, 0 ), 0 )
        self.assertTrue( a.equals( zero ) )
        a = THREE.Quaternion().setFromAxisAngle( THREE.Vector3( 0, 1, 0 ), 0 )
        self.assertTrue( a.equals( zero ) )
        a = THREE.Quaternion().setFromAxisAngle( THREE.Vector3( 0, 0, 1 ), 0 )
        self.assertTrue( a.equals( zero ) )

        b1 = THREE.Quaternion().setFromAxisAngle( THREE.Vector3( 1, 0, 0 ), math.pi )
        self.assertFalse( a.equals( b1 ) )
        b2 = THREE.Quaternion().setFromAxisAngle( THREE.Vector3( 1, 0, 0 ), -math.pi )
        self.assertFalse( a.equals( b2 ) )

        b1.multiply( b2 )
        self.assertTrue( a.equals( b1 ) )

    def test_setFromEuler_setFromQuaternion( self ):

        angles = [ THREE.Vector3( 1, 0, 0 ), THREE.Vector3( 0, 1, 0 ), THREE.Vector3( 0, 0, 1 ) ]

        # ensure euler conversion to/from THREE.Quaternion matches.
        for order in orders:
            for angle in angles:
                eulers2 = THREE.Euler().setFromQuaternion( THREE.Quaternion().setFromEuler( THREE.Euler( angle.x, angle.y, angle.z, order ) ), order )
                newAngle = THREE.Vector3( eulers2.x, eulers2.y, eulers2.z )
                self.assertAlmostEqual( newAngle.distanceTo( angle ), 0 )

    def test_setFromEuler_setFromRotationMatrix( self ):

        # ensure euler conversion for THREE.Quaternion matches that of THREE.Matrix4
        for order in orders:
            orderAngles = eulerAngles.clone()
            orderAngles.order = order
            q = THREE.Quaternion().setFromEuler( orderAngles )
            m = THREE.Matrix4().makeRotationFromEuler( orderAngles )
            q2 = THREE.Quaternion().setFromRotationMatrix( m )

            self.assertAlmostEqual( qSub( q, q2 ).length(), 0 )

    def test_normalize_length_lengthSq( self ):

        a = THREE.Quaternion( x, y, z, w )
        b = THREE.Quaternion( -x, -y, -z, -w )

        self.assertNotEqual( a.length(), 1)
        self.assertNotEqual( a.lengthSq(), 1)
        a.normalize()
        self.assertEqual( a.length(), 1)
        self.assertEqual( a.lengthSq(), 1)

        a.set( 0, 0, 0, 0 )
        self.assertEqual( a.lengthSq(), 0)
        self.assertEqual( a.length(), 0)
        a.normalize()
        self.assertEqual( a.lengthSq(), 1)
        self.assertEqual( a.length(), 1)

    def test_inverse_conjugate( self ):

        a = THREE.Quaternion( x, y, z, w )

        # TODO: add better validation here.

        b = a.clone().conjugate()

        self.assertEqual( a.x, -b.x )
        self.assertEqual( a.y, -b.y )
        self.assertEqual( a.z, -b.z )
        self.assertEqual( a.w, b.w )


    def test_multiplyQuaternions_multiply( self ):

        angles = [ THREE.Euler( 1, 0, 0 ), THREE.Euler( 0, 1, 0 ), THREE.Euler( 0, 0, 1 ) ]

        q1 = THREE.Quaternion().setFromEuler( angles[0] )
        q2 = THREE.Quaternion().setFromEuler( angles[1] )
        q3 = THREE.Quaternion().setFromEuler( angles[2] )

        q = THREE.Quaternion().multiplyQuaternions( q1, q2 ).multiply( q3 )

        m1 = THREE.Matrix4().makeRotationFromEuler( angles[0] )
        m2 = THREE.Matrix4().makeRotationFromEuler( angles[1] )
        m3 = THREE.Matrix4().makeRotationFromEuler( angles[2] )

        m = THREE.Matrix4().multiplyMatrices( m1, m2 ).multiply( m3 )

        qFromM = THREE.Quaternion().setFromRotationMatrix( m )

        self.assertAlmostEqual( qSub( q, qFromM ).length(), 0 )

    def test_multiplyVector3( self ):

        angles = [ THREE.Euler( 1, 0, 0 ), THREE.Euler( 0, 1, 0 ), THREE.Euler( 0, 0, 1 ) ]

        # ensure euler conversion for THREE.Quaternion matches that of THREE.Matrix4
        for order in orders:
            for angle in angles:
                orderAngle = angle.clone()
                orderAngle.order = order
                q = THREE.Quaternion().setFromEuler( orderAngle )
                m = THREE.Matrix4().makeRotationFromEuler( orderAngle )

                v0 = THREE.Vector3(1, 0, 0)
                qv = v0.clone().applyQuaternion( q )
                mv = v0.clone().applyMatrix4( m )

                self.assertAlmostEqual( qv.distanceTo( mv ), 0 )

    def test_equals( self ):

        a = THREE.Quaternion( x, y, z, w )
        b = THREE.Quaternion( -x, -y, -z, -w )

        self.assertNotEqual( a.x, b.x )
        self.assertNotEqual( a.y, b.y )

        self.assertFalse( a.equals( b ) )
        self.assertFalse( b.equals( a ) )

        a.copy( b )
        self.assertEqual( a.x, b.x )
        self.assertEqual( a.y, b.y )

        self.assertTrue( a.equals( b ) )
        self.assertTrue( b.equals( a ) )

    def slerpTestSkeleton( self, doSlerp, maxError ):

        a = [
            0.6753410084407496,
            0.4087830051091744,
            0.32856700410659473,
            0.5185120064806223
        ]

        b = [
            0.6602792107657797,
            0.43647413932562285,
            0.35119011210236006,
            0.5001871596632682
        ]

        def isNormal( result ):

            normError = abs( 1 - result[ "length" ] )
            return normError <= maxError

        result = doSlerp( a, b, 0 )
        self.assertTrue( result[ "equals" ](
                a[ 0 ], a[ 1 ], a[ 2 ], a[ 3 ], 0 ) ) # Exactly A @ t = 0

        result = doSlerp( a, b, 1 )
        self.assertTrue( result[ "equals" ](
                b[ 0 ], b[ 1 ], b[ 2 ], b[ 3 ], 0 ) ) # Exactly B @ t = 1

        result = doSlerp( a, b, 0.5 )
        self.assertTrue( abs( result[ "dotA" ] - result[ "dotB" ] ) <= sys.float_info.epsilon ) # Symmetry at 0.5
        self.assertTrue( isNormal( result ) ) # Approximately normal (at 0.5)

        result = doSlerp( a, b, 0.25 )
        self.assertTrue( result[ "dotA" ] > result[ "dotB" ] ) # Interpolating at 0.25
        self.assertTrue( isNormal( result ) ) # Approximately normal (at 0.25)

        result = doSlerp( a, b, 0.75 )
        self.assertTrue( result[ "dotA" ] < result[ "dotB" ] ) # Interpolating at 0.75
        self.assertTrue( isNormal( result ) ) # Approximately normal (at 0.75)

        D = math.sqrt( 0.5 )

        result = doSlerp( [ 1, 0, 0, 0 ], [ 0, 0, 1, 0 ], 0.5 )
        self.assertTrue( result[ "equals" ]( D, 0, D, 0 ) ) # X/Z diagonal from axes
        self.assertTrue( isNormal( result ) ) # Approximately normal (X/Z diagonal)

        result = doSlerp( [ 0, D, 0, D ], [ 0, -D, 0, D ], 0.5 )
        self.assertTrue( result[ "equals" ]( 0, 0, 0, 1 ) ) # W-Unit from diagonals
        self.assertTrue( isNormal( result ) ) # Approximately normal (W-Unit)

    def test_slerp( self ):

        self.slerpTestSkeleton( doSlerpObject, sys.float_info.epsilon )


    def test_slerpFlat( self ):

        self.slerpTestSkeleton( doSlerpArray, sys.float_info.epsilon )
