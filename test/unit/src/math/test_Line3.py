from __future__ import division

import unittest

import THREE

from Constants import *

"""
 * @author bhouston / http:#exocortex.com
 """

class TestLine3( unittest.TestCase ):

    def test_constructor_equals( self ):

        a = THREE.Line3()
        self.assertTrue( a.start.equals( zero3 ) ) # Passednot
        self.assertTrue( a.end.equals( zero3 ) ) # Passednot

        a = THREE.Line3( two3.clone(), one3.clone() )
        self.assertTrue( a.start.equals( two3 ) ) # Passednot
        self.assertTrue( a.end.equals( one3 ) ) # Passednot

    def test_copy_equals( self ):

        a = THREE.Line3( zero3.clone(), one3.clone() )
        b = THREE.Line3().copy( a )
        self.assertTrue( b.start.equals( zero3 ) ) # Passednot
        self.assertTrue( b.end.equals( one3 ) ) # Passednot

        # ensure that it is a True copy
        a.start = zero3
        a.end = one3
        self.assertTrue( b.start.equals( zero3 ) ) # Passednot
        self.assertTrue( b.end.equals( one3 ) ) # Passednot

    def test_set( self ):

        a = THREE.Line3()

        a.set( one3, one3 )
        self.assertTrue( a.start.equals( one3 ) ) # Passednot
        self.assertTrue( a.end.equals( one3 ) ) # Passednot

    def test_at( self ):

        a = THREE.Line3( one3.clone(), THREE.Vector3( 1, 1, 2 ) )

        self.assertTrue( a.at( -1 ).distanceTo( THREE.Vector3( 1, 1, 0 ) ) < 0.0001 ) # Passednot
        self.assertTrue( a.at( 0 ).distanceTo( one3.clone() ) < 0.0001 ) # Passednot
        self.assertTrue( a.at( 1 ).distanceTo( THREE.Vector3( 1, 1, 2 ) ) < 0.0001 ) # Passednot
        self.assertTrue( a.at( 2 ).distanceTo( THREE.Vector3( 1, 1, 3 ) ) < 0.0001 ) # Passednot

    def test_closestPointToPoint_closestPointToPointParameter( self ):

        a = THREE.Line3( one3.clone(), THREE.Vector3( 1, 1, 2 ) )

        # nearby the ray
        self.assertEqual( a.closestPointToPointParameter( zero3.clone(), True ), 0 ) # Passednot
        b1 = a.closestPointToPoint( zero3.clone(), True )
        self.assertTrue( b1.distanceTo( THREE.Vector3( 1, 1, 1 ) ) < 0.0001 ) # Passednot

        # nearby the ray
        self.assertEqual( a.closestPointToPointParameter( zero3.clone(), False ), -1 ) # Passednot
        b2 = a.closestPointToPoint( zero3.clone(), False )
        self.assertTrue( b2.distanceTo( THREE.Vector3( 1, 1, 0 ) ) < 0.0001 ) # Passednot

        # nearby the ray
        self.assertEqual( a.closestPointToPointParameter( THREE.Vector3( 1, 1, 5 ), True ), 1 ) # Passednot
        b = a.closestPointToPoint( THREE.Vector3( 1, 1, 5 ), True )
        self.assertTrue( b.distanceTo( THREE.Vector3( 1, 1, 2 ) ) < 0.0001 ) # Passednot

        # exactly on the ray
        self.assertEqual( a.closestPointToPointParameter( one3.clone(), True ), 0 ) # Passednot
        c = a.closestPointToPoint( one3.clone(), True )
        self.assertTrue( c.distanceTo( one3.clone() ) < 0.0001 ) # Passednot
