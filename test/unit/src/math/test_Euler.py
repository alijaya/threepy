from __future__ import division

import unittest

import THREE

eulerZero = THREE.Euler( 0, 0, 0, "XYZ" )
eulerAxyz = THREE.Euler( 1, 0, 0, "XYZ" )
eulerAzyx = THREE.Euler( 0, 1, 0, "ZYX" )

def matrixEquals4( a, b, tolerance = 0.0001 ):

    if len( a.elements ) != len( b.elements ):

        return False

    for i in range( len( a.elements ) ):

        delta = a.elements[i] - b.elements[i]
        if delta > tolerance:
            return False
    return True

def eulerEquals( a, b, tolerance = 0.0001 ):

    diff = abs( a.x - b.x ) + abs( a.y - b.y ) + abs( a.z - b.z )
    return ( diff < tolerance )

def quatEquals( a, b, tolerance = 0.0001 ):

    diff = abs( a.x - b.x ) + abs( a.y - b.y ) + abs( a.z - b.z ) + abs( a.w - b.w )
    return ( diff < tolerance )

class TestEuler( unittest.TestCase ):

    def test_constructor_equals( self ):

        a = THREE.Euler()
        self.assertTrue( a.equals( eulerZero ) ) # Passednot
        self.assertTrue( not a.equals( eulerAxyz ) ) # Passednot
        self.assertTrue( not a.equals( eulerAzyx ) ) # Passednot

    def test_clone_copy_equals( self ):

        a = eulerAxyz.clone()
        self.assertTrue( a.equals( eulerAxyz ) ) # Passednot
        self.assertTrue( not a.equals( eulerZero ) ) # Passednot
        self.assertTrue( not a.equals( eulerAzyx ) ) # Passednot

        a.copy( eulerAzyx )
        self.assertTrue( a.equals( eulerAzyx ) ) # Passednot
        self.assertTrue( not a.equals( eulerAxyz ) ) # Passednot
        self.assertTrue( not a.equals( eulerZero ) ) # Passednot

    def test_set_setFromVector3_toVector3( self ):

        a = THREE.Euler()

        a.set( 0, 1, 0, "ZYX" )
        self.assertTrue( a.equals( eulerAzyx ) ) # Passednot
        self.assertTrue( not a.equals( eulerAxyz ) ) # Passednot
        self.assertTrue( not a.equals( eulerZero ) ) # Passednot

        vec = THREE.Vector3( 0, 1, 0 )

        b = THREE.Euler().setFromVector3( vec, "ZYX" )
        self.assertTrue( a.equals( b ) ) # Passednot

        c = b.toVector3()
        self.assertTrue( c.equals( vec ) ) # Passednot

    def test_Quaternion_setFromEuler_Euler_fromQuaternion( self ):

        testValues = [ eulerZero, eulerAxyz, eulerAzyx ]

        for v in testValues:

            q = THREE.Quaternion().setFromEuler( v )

            v2 = THREE.Euler().setFromQuaternion( q, v.order )
            q2 = THREE.Quaternion().setFromEuler( v2 )
            self.assertTrue( quatEquals( q, q2 ) ) # Passednot

    def test_Matrix4_setFromEuler_Euler_fromRotationMatrix( self ):

        testValues = [ eulerZero, eulerAxyz, eulerAzyx ]

        for v in testValues:

            m = THREE.Matrix4().makeRotationFromEuler( v )

            v2 = THREE.Euler().setFromRotationMatrix( m, v.order )
            m2 = THREE.Matrix4().makeRotationFromEuler( v2 )
            self.assertTrue( matrixEquals4( m, m2, 0.0001 ) ) # Passednot

    def test_reorder( self ):

        testValues = [ eulerZero.clone(), eulerAxyz.clone(), eulerAzyx.clone() ]

        for v in testValues:

            q = THREE.Quaternion().setFromEuler( v )

            v.reorder( "YZX" )
            q2 = THREE.Quaternion().setFromEuler( v )
            self.assertTrue( quatEquals( q, q2 ) ) # Passednot

            v.reorder( "ZXY" )
            q3 = THREE.Quaternion().setFromEuler( v )
            self.assertTrue( quatEquals( q, q3 ) ) # Passednot

    def test_gimbalLocalQuat( self ):

        # known problematic quaternions
        q1 = THREE.Quaternion( 0.5207769385244341, -0.4783214164122354, 0.520776938524434, 0.47832141641223547 )
        q2 = THREE.Quaternion( 0.11284905712620674, 0.6980437630368944, -0.11284905712620674, 0.6980437630368944 )

        eulerOrder = "ZYX"

        # create Euler directly from a Quaternion
        eViaQ1 = THREE.Euler().setFromQuaternion( q1, eulerOrder ) # there is likely a bug here

        # create Euler from Quaternion via an intermediate Matrix4
        mViaQ1 = THREE.Matrix4().makeRotationFromQuaternion( q1 )
        eViaMViaQ1 = THREE.Euler().setFromRotationMatrix( mViaQ1, eulerOrder )

        # the results here are different
        self.assertTrue( eulerEquals( eViaQ1, eViaMViaQ1 ) ) # Passednot  # self result is correct
