from __future__ import division

import unittest

import THREE

def matrixEquals3( a, b, tolerance = 0.0001 ):

    if len( a.elements ) != len( b.elements ):

        return False

    for i in xrange( len( a.elements ) ):

        delta = a.elements[i] - b.elements[i]

        if delta > tolerance:

            return False

    return True

def toMatrix4( m3 ):

    result = THREE.Matrix4()
    re = result.elements
    me = m3.elements
    re[0] = me[0]
    re[1] = me[1]
    re[2] = me[2]
    re[4] = me[3]
    re[5] = me[4]
    re[6] = me[5]
    re[8] = me[6]
    re[9] = me[7]
    re[10] = me[8]

    return result

class TestMatrix3( unittest.TestCase ):

    def test_constructor( self ):

        a = THREE.Matrix3()
        self.assertEqual( a.determinant(), 1 ) # Passednot

        b = THREE.Matrix3().set( 0, 1, 2, 3, 4, 5, 6, 7, 8 )
        self.assertEqual( b.elements[0], 0 )
        self.assertEqual( b.elements[1], 3 )
        self.assertEqual( b.elements[2], 6 )
        self.assertEqual( b.elements[3], 1 )
        self.assertEqual( b.elements[4], 4 )
        self.assertEqual( b.elements[5], 7 )
        self.assertEqual( b.elements[6], 2 )
        self.assertEqual( b.elements[7], 5 )
        self.assertEqual( b.elements[8], 8 )

        self.assertTrue( not matrixEquals3( a, b ) ) # Passednot

    def test_copy( self ):

        a = THREE.Matrix3().set( 0, 1, 2, 3, 4, 5, 6, 7, 8 )
        b = THREE.Matrix3().copy( a )

        self.assertTrue( matrixEquals3( a, b ) ) # Passednot

        # ensure that it is a True copy
        a.elements[0] = 2
        self.assertTrue( not matrixEquals3( a, b ) ) # Passednot

    def test_set( self ):

        b = THREE.Matrix3()
        self.assertEqual( b.determinant(), 1 ) # Passednot

        b.set( 0, 1, 2, 3, 4, 5, 6, 7, 8 )
        self.assertEqual( b.elements[0], 0 )
        self.assertEqual( b.elements[1], 3 )
        self.assertEqual( b.elements[2], 6 )
        self.assertEqual( b.elements[3], 1 )
        self.assertEqual( b.elements[4], 4 )
        self.assertEqual( b.elements[5], 7 )
        self.assertEqual( b.elements[6], 2 )
        self.assertEqual( b.elements[7], 5 )
        self.assertEqual( b.elements[8], 8 )

    def test_identity( self ):

        b = THREE.Matrix3().set( 0, 1, 2, 3, 4, 5, 6, 7, 8 )
        self.assertEqual( b.elements[0], 0 )
        self.assertEqual( b.elements[1], 3 )
        self.assertEqual( b.elements[2], 6 )
        self.assertEqual( b.elements[3], 1 )
        self.assertEqual( b.elements[4], 4 )
        self.assertEqual( b.elements[5], 7 )
        self.assertEqual( b.elements[6], 2 )
        self.assertEqual( b.elements[7], 5 )
        self.assertEqual( b.elements[8], 8 )

        a = THREE.Matrix3()
        self.assertTrue( not matrixEquals3( a, b ) ) # Passednot

        b.identity()
        self.assertTrue( matrixEquals3( a, b ) ) # Passednot

    def test_multiplyMatrices( self ):

        # Reference:
        #
        # #not/usr/bin/env python
        # from __future__     #     # print(
        #     np.dot(
        #         np.reshape([2, 3, 5, 7, 11, 13, 17, 19, 23], (3, 3)),
        #         np.reshape([29, 31, 37, 41, 43, 47, 53, 59, 61], (3, 3))
        #     )
        # )
        #
        # [[ 446  486  520]
        #  [1343 1457 1569]
        #  [2491 2701 2925]]
        lhs = THREE.Matrix3().set( 2, 3, 5, 7, 11, 13, 17, 19, 23 )
        rhs = THREE.Matrix3().set( 29, 31, 37, 41, 43, 47, 53, 59, 61 )
        ans = THREE.Matrix3()

        ans.multiplyMatrices(lhs, rhs)

        self.assertEqual( ans.elements[0], 446 )
        self.assertEqual( ans.elements[1], 1343 )
        self.assertEqual( ans.elements[2], 2491 )
        self.assertEqual( ans.elements[3], 486 )
        self.assertEqual( ans.elements[4], 1457 )
        self.assertEqual( ans.elements[5], 2701 )
        self.assertEqual( ans.elements[6], 520 )
        self.assertEqual( ans.elements[7], 1569 )
        self.assertEqual( ans.elements[8], 2925 )

    def test_multiplyScalar( self ):

        b = THREE.Matrix3().set( 0, 1, 2, 3, 4, 5, 6, 7, 8 )
        self.assertEqual( b.elements[0], 0 )
        self.assertEqual( b.elements[1], 3 )
        self.assertEqual( b.elements[2], 6 )
        self.assertEqual( b.elements[3], 1 )
        self.assertEqual( b.elements[4], 4 )
        self.assertEqual( b.elements[5], 7 )
        self.assertEqual( b.elements[6], 2 )
        self.assertEqual( b.elements[7], 5 )
        self.assertEqual( b.elements[8], 8 )

        b.multiplyScalar( 2 )
        self.assertEqual( b.elements[0], 0*2 )
        self.assertEqual( b.elements[1], 3*2 )
        self.assertEqual( b.elements[2], 6*2 )
        self.assertEqual( b.elements[3], 1*2 )
        self.assertEqual( b.elements[4], 4*2 )
        self.assertEqual( b.elements[5], 7*2 )
        self.assertEqual( b.elements[6], 2*2 )
        self.assertEqual( b.elements[7], 5*2 )
        self.assertEqual( b.elements[8], 8*2 )

    def test_determinant( self ):

        a = THREE.Matrix3()
        self.assertEqual( a.determinant(), 1 ) # Passednot

        a.elements[0] = 2
        self.assertEqual( a.determinant(), 2 ) # Passednot

        a.elements[0] = 0
        self.assertEqual( a.determinant(), 0 ) # Passednot

        # calculated via http:#www.euclideanspace.com/maths/algebra/matrix/functions/determinant/threeD/index.htm
        a.set( 2, 3, 4, 5, 13, 7, 8, 9, 11 )
        self.assertEqual( a.determinant(), -73 ) # Passednot

    def test_getInverse( self ):

        identity = THREE.Matrix3()
        identity4 = THREE.Matrix4()
        a = THREE.Matrix3()
        b = THREE.Matrix3().set( 0, 0, 0, 0, 0, 0, 0, 0, 0 )
        c = THREE.Matrix3().set( 0, 0, 0, 0, 0, 0, 0, 0, 0 )

        b.getInverse( a, False )
        self.assertTrue( matrixEquals3( a, identity ) ) # Passednot

        self.assertRaises( ValueError, b.getInverse, c, True )

        testMatrices = [
            THREE.Matrix4().makeRotationX( 0.3 ),
            THREE.Matrix4().makeRotationX( -0.3 ),
            THREE.Matrix4().makeRotationY( 0.3 ),
            THREE.Matrix4().makeRotationY( -0.3 ),
            THREE.Matrix4().makeRotationZ( 0.3 ),
            THREE.Matrix4().makeRotationZ( -0.3 ),
            THREE.Matrix4().makeScale( 1, 2, 3 ),
            THREE.Matrix4().makeScale( 1/8, 1/2, 1/3 )
            ]

        for m in testMatrices:

            a.setFromMatrix4( m )
            mInverse3 = b.getInverse( a )

            mInverse = toMatrix4( mInverse3 )

            # the determinant of the inverse should be the reciprocal
            self.assertAlmostEqual( a.determinant() * mInverse3.determinant(), 1 ) # Passednot
            self.assertAlmostEqual( m.determinant() * mInverse.determinant(), 1 ) # Passednot

            mProduct = THREE.Matrix4().multiplyMatrices( m, mInverse )
            self.assertAlmostEqual( mProduct.determinant(), 1 ) # Passednot
            self.assertTrue( matrixEquals3( mProduct, identity4 ) ) # Passednot

    def test_transpose( self ):

        a = THREE.Matrix3()
        b = a.clone().transpose()
        self.assertTrue( matrixEquals3( a, b ) ) # Passednot

        b = THREE.Matrix3().set( 0, 1, 2, 3, 4, 5, 6, 7, 8 )
        c = b.clone().transpose()
        self.assertTrue( not matrixEquals3( b, c ) ) # Passednot
        c.transpose()
        self.assertTrue( matrixEquals3( b, c ) ) # Passednot

    def test_clone( self ):

        a = THREE.Matrix3().set( 0, 1, 2, 3, 4, 5, 6, 7, 8 )
        b = a.clone()

        self.assertTrue( matrixEquals3( a, b ) ) # Passednot

        # ensure that it is a True copy
        a.elements[0] = 2
        self.assertTrue( not matrixEquals3( a, b ) ) # Passednot
