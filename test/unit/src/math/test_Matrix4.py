from __future__ import division
import unittest
import math

from THREE import Euler
from THREE import Matrix4
from THREE import Quaternion
from THREE import Vector3

from Constants import *

class TestMatrix4( unittest.TestCase ):

    def setUp( self ):

        self.addTypeEqualityFunc( Matrix4, self.assertMatrix4AlmostEqual )

    def assertMatrix4AlmostEqual( self, first, second, msg = None ):

        self.assertEqual( len( first.elements ), len( second.elements ) )

        for i in range( len( first.elements ) ):

            self.assertAlmostEqual( first.elements[ i ], second.elements[ i ] )

    def test_constructor( self ):

        a = Matrix4()
        self.assertEqual( a.determinant(), 1 )

        b = Matrix4().set( 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 )
        self.assertEqual( b.elements[0], 0 )
        self.assertEqual( b.elements[1], 4 )
        self.assertEqual( b.elements[2], 8 )
        self.assertEqual( b.elements[3], 12 )
        self.assertEqual( b.elements[4], 1 )
        self.assertEqual( b.elements[5], 5 )
        self.assertEqual( b.elements[6], 9 )
        self.assertEqual( b.elements[7], 13 )
        self.assertEqual( b.elements[8], 2 )
        self.assertEqual( b.elements[9], 6 )
        self.assertEqual( b.elements[10], 10 )
        self.assertEqual( b.elements[11], 14 )
        self.assertEqual( b.elements[12], 3 )
        self.assertEqual( b.elements[13], 7 )
        self.assertEqual( b.elements[14], 11 )
        self.assertEqual( b.elements[15], 15 )

        self.assertNotEqual( a, b )

    def test_copy( self ):

        a = Matrix4().set( 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 )
        b = Matrix4().copy( a )

        self.assertEqual( a, b )

        # ensure that it is a True copy
        a.elements[0] = 2
        self.assertNotEqual( a, b )

    def test_set( self ):

        b = Matrix4()
        self.assertEqual( b.determinant(), 1 )

        b.set( 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 )
        self.assertEqual( b.elements[0], 0 )
        self.assertEqual( b.elements[1], 4 )
        self.assertEqual( b.elements[2], 8 )
        self.assertEqual( b.elements[3], 12 )
        self.assertEqual( b.elements[4], 1 )
        self.assertEqual( b.elements[5], 5 )
        self.assertEqual( b.elements[6], 9 )
        self.assertEqual( b.elements[7], 13 )
        self.assertEqual( b.elements[8], 2 )
        self.assertEqual( b.elements[9], 6 )
        self.assertEqual( b.elements[10], 10 )
        self.assertEqual( b.elements[11], 14 )
        self.assertEqual( b.elements[12], 3 )
        self.assertEqual( b.elements[13], 7 )
        self.assertEqual( b.elements[14], 11 )
        self.assertEqual( b.elements[15], 15 )

    def test_identity( self ):

        b = Matrix4().set( 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 )
        self.assertEqual( b.elements[0], 0 )
        self.assertEqual( b.elements[1], 4 )
        self.assertEqual( b.elements[2], 8 )
        self.assertEqual( b.elements[3], 12 )
        self.assertEqual( b.elements[4], 1 )
        self.assertEqual( b.elements[5], 5 )
        self.assertEqual( b.elements[6], 9 )
        self.assertEqual( b.elements[7], 13 )
        self.assertEqual( b.elements[8], 2 )
        self.assertEqual( b.elements[9], 6 )
        self.assertEqual( b.elements[10], 10 )
        self.assertEqual( b.elements[11], 14 )
        self.assertEqual( b.elements[12], 3 )
        self.assertEqual( b.elements[13], 7 )
        self.assertEqual( b.elements[14], 11 )
        self.assertEqual( b.elements[15], 15 )

        a = Matrix4()
        self.assertNotEqual( a, b )

        b.identity()
        self.assertEqual( a, b )

    def test_multiplyMatrices( self ):

        # Reference:
        #
        # #!/usr/bin/env python
        # from __future__ import print_function
        # import numpy as np
        # print(
        #     np.dot(
        #         np.reshape([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53], (4, 4)),
        #         np.reshape([59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131], (4, 4))
        #     )
        # )
        #
        # [[ 1585  1655  1787  1861]
        #  [ 5318  5562  5980  6246]
        #  [10514 11006 11840 12378]
        #  [15894 16634 17888 18710]]
        lhs = Matrix4().set( 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53 )
        rhs = Matrix4().set( 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131 )
        ans = Matrix4()

        ans.multiplyMatrices( lhs, rhs )

        self.assertEqual( ans.elements[0], 1585 )
        self.assertEqual( ans.elements[1], 5318 )
        self.assertEqual( ans.elements[2], 10514 )
        self.assertEqual( ans.elements[3], 15894 )
        self.assertEqual( ans.elements[4], 1655 )
        self.assertEqual( ans.elements[5], 5562 )
        self.assertEqual( ans.elements[6], 11006 )
        self.assertEqual( ans.elements[7], 16634 )
        self.assertEqual( ans.elements[8], 1787 )
        self.assertEqual( ans.elements[9], 5980 )
        self.assertEqual( ans.elements[10], 11840 )
        self.assertEqual( ans.elements[11], 17888 )
        self.assertEqual( ans.elements[12], 1861 )
        self.assertEqual( ans.elements[13], 6246 )
        self.assertEqual( ans.elements[14], 12378 )
        self.assertEqual( ans.elements[15], 18710 )

    def test_multiplyScalar( self ):

        b = Matrix4().set( 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 )
        self.assertEqual( b.elements[0], 0 )
        self.assertEqual( b.elements[1], 4 )
        self.assertEqual( b.elements[2], 8 )
        self.assertEqual( b.elements[3], 12 )
        self.assertEqual( b.elements[4], 1 )
        self.assertEqual( b.elements[5], 5 )
        self.assertEqual( b.elements[6], 9 )
        self.assertEqual( b.elements[7], 13 )
        self.assertEqual( b.elements[8], 2 )
        self.assertEqual( b.elements[9], 6 )
        self.assertEqual( b.elements[10], 10 )
        self.assertEqual( b.elements[11], 14 )
        self.assertEqual( b.elements[12], 3 )
        self.assertEqual( b.elements[13], 7 )
        self.assertEqual( b.elements[14], 11 )
        self.assertEqual( b.elements[15], 15 )

        b.multiplyScalar( 2 )
        self.assertEqual( b.elements[0], 0*2 )
        self.assertEqual( b.elements[1], 4*2 )
        self.assertEqual( b.elements[2], 8*2 )
        self.assertEqual( b.elements[3], 12*2 )
        self.assertEqual( b.elements[4], 1*2 )
        self.assertEqual( b.elements[5], 5*2 )
        self.assertEqual( b.elements[6], 9*2 )
        self.assertEqual( b.elements[7], 13*2 )
        self.assertEqual( b.elements[8], 2*2 )
        self.assertEqual( b.elements[9], 6*2 )
        self.assertEqual( b.elements[10], 10*2 )
        self.assertEqual( b.elements[11], 14*2 )
        self.assertEqual( b.elements[12], 3*2 )
        self.assertEqual( b.elements[13], 7*2 )
        self.assertEqual( b.elements[14], 11*2 )
        self.assertEqual( b.elements[15], 15*2 )

    def test_determinant( self ):

        a = Matrix4()
        self.assertEqual( a.determinant(), 1 )

        a.elements[0] = 2
        self.assertEqual( a.determinant(), 2 )

        a.elements[0] = 0
        self.assertEqual( a.determinant(), 0 )

        # calculated via http:#www.euclideanspace.com/maths/algebra/matrix/functions/determinant/fourD/index.htm
        a.set( 2, 3, 4, 5, -1, -21, -3, -4, 6, 7, 8, 10, -8, -9, -10, -12 )
        self.assertEqual( a.determinant(), 76 )

    def test_getInverse( self ):

        identity = Matrix4()

        a = Matrix4()
        b = Matrix4().set( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 )
        c = Matrix4().set( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 )

        self.assertNotEqual( a, b )
        b.getInverse( a, False )
        self.assertEqual( b, Matrix4() )

        self.assertRaises( ValueError, b.getInverse, c, True )

        testMatrices = [
            Matrix4().makeRotationX( 0.3 ),
            Matrix4().makeRotationX( -0.3 ),
            Matrix4().makeRotationY( 0.3 ),
            Matrix4().makeRotationY( -0.3 ),
            Matrix4().makeRotationZ( 0.3 ),
            Matrix4().makeRotationZ( -0.3 ),
            Matrix4().makeScale( 1, 2, 3 ),
            Matrix4().makeScale( 1/8, 1/2, 1/3 ),
            Matrix4().makePerspective( -1, 1, 1, -1, 1, 1000 ),
            Matrix4().makePerspective( -16, 16, 9, -9, 0.1, 10000 ),
            Matrix4().makeTranslation( 1, 2, 3 )
            ]

        for m in testMatrices:

            mInverse = Matrix4().getInverse( m )
            mSelfInverse = m.clone()
            mSelfInverse.getInverse( mSelfInverse )


            # self-inverse should the same as inverse
            self.assertEqual( mSelfInverse, mInverse )

            # the determinant of the inverse should be the reciprocal
            self.assertAlmostEqual( m.determinant() * mInverse.determinant(), 1 )

            mProduct = Matrix4().multiplyMatrices( m, mInverse )

            # the determinant of the identity matrix is 1
            self.assertAlmostEqual( mProduct.determinant(), 1 )
            self.assertEqual( mProduct, identity )

    def test_makeBasis_extractBasis( self ):

        identityBasis = [ Vector3( 1, 0, 0 ), Vector3( 0, 1, 0 ), Vector3( 0, 0, 1 ) ]
        a = Matrix4().makeBasis( identityBasis[0], identityBasis[1], identityBasis[2] )
        identity = Matrix4()
        self.assertEqual( a, identity )

        testBases = [ [ Vector3( 0, 1, 0 ), Vector3( -1, 0, 0 ), Vector3( 0, 0, 1 ) ] ]
        for testBasis in testBases:

            b = Matrix4().makeBasis( testBasis[0], testBasis[1], testBasis[2] )
            outBasis = [ Vector3(), Vector3(), Vector3() ]
            b.extractBasis( outBasis[0], outBasis[1], outBasis[2] )
            # check what goes in, is what comes out.
            for j in range( len( outBasis ) ):
                self.assertTrue( outBasis[j].equals( testBasis[j] ) )

            # get the basis out the hard war
            for j in range( len( identityBasis ) ):
                outBasis[j].copy( identityBasis[j] )
                outBasis[j].applyMatrix4( b )

            # did the multiply method of basis extraction work?
            for j in range( len( outBasis ) ):
                self.assertTrue( outBasis[j].equals( testBasis[j] ) )

    def test_transpose( self ):

        a = Matrix4()
        b = a.clone().transpose()
        self.assertEqual( a, b )

        b = Matrix4().set( 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 )
        c = b.clone().transpose()
        self.assertNotEqual( b, c )
        c.transpose()
        self.assertEqual( b, c )

    def test_clone( self ):

        a = Matrix4().set( 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 )
        b = a.clone()

        self.assertEqual( a, b )

        # ensure that it is a True copy
        a.elements[0] = 2
        self.assertNotEqual( a, b )

    def test_compose_decompose( self ):
        tValues = [
            Vector3(),
            Vector3( 3, 0, 0 ),
            Vector3( 0, 4, 0 ),
            Vector3( 0, 0, 5 ),
            Vector3( -6, 0, 0 ),
            Vector3( 0, -7, 0 ),
            Vector3( 0, 0, -8 ),
            Vector3( -2, 5, -9 ),
            Vector3( -2, -5, -9 )
        ]

        sValues = [
            Vector3( 1, 1, 1 ),
            Vector3( 2, 2, 2 ),
            Vector3( 1, -1, 1 ),
            Vector3( -1, 1, 1 ),
            Vector3( 1, 1, -1 ),
            Vector3( 2, -2, 1 ),
            Vector3( -1, 2, -2 ),
            Vector3( -1, -1, -1 ),
            Vector3( -2, -2, -2 )
        ]

        rValues = [
            Quaternion(),
            Quaternion().setFromEuler( Euler( 1, 1, 0 ) ),
            Quaternion().setFromEuler( Euler( 1, -1, 1 ) ),
            Quaternion( 0, 0.9238795292366128, 0, 0.38268342717215614 )
        ]


        for t in tValues:
            for s in sValues:
                for r in rValues:

                    m = Matrix4().compose( t, r, s )
                    t2 = Vector3()
                    r2 = Quaternion()
                    s2 = Vector3()

                    m.decompose( t2, r2, s2 )

                    m2 = Matrix4().compose( t2, r2, s2 )

                    self.assertEqual( m, m2 )