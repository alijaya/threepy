from __future__ import division
import math

import unittest

import THREE

from Constants import *

"""
 * @author bhouston / http:#exocortex.com
 """

class TestTriangle( unittest.TestCase ):

    def test_constructor( self ):

        a = THREE.Triangle()
        self.assertTrue( a.a.equals( zero3 ) ) # Passednot
        self.assertTrue( a.b.equals( zero3 ) ) # Passednot
        self.assertTrue( a.c.equals( zero3 ) ) # Passednot

        a = THREE.Triangle( one3.clone().negate(), one3.clone(), two3.clone() )
        self.assertTrue( a.a.equals( one3.clone().negate() ) ) # Passednot
        self.assertTrue( a.b.equals( one3 ) ) # Passednot
        self.assertTrue( a.c.equals( two3 ) ) # Passednot

    def test_copy( self ):

        a = THREE.Triangle( one3.clone().negate(), one3.clone(), two3.clone() )
        b = THREE.Triangle().copy( a )
        self.assertTrue( b.a.equals( one3.clone().negate() ) ) # Passednot
        self.assertTrue( b.b.equals( one3 ) ) # Passednot
        self.assertTrue( b.c.equals( two3 ) ) # Passednot

        # ensure that it is a True copy
        a.a = one3
        a.b = zero3
        a.c = zero3
        self.assertTrue( b.a.equals( one3.clone().negate() ) ) # Passednot
        self.assertTrue( b.b.equals( one3 ) ) # Passednot
        self.assertTrue( b.c.equals( two3 ) ) # Passednot

    def test_setFromPointsAndIndices( self ):

        a = THREE.Triangle()

        points = [ one3, one3.clone().negate(), two3 ]
        a.setFromPointsAndIndices( points, 1, 0, 2 )
        self.assertTrue( a.a.equals( one3.clone().negate() ) ) # Passednot
        self.assertTrue( a.b.equals( one3 ) ) # Passednot
        self.assertTrue( a.c.equals( two3 ) ) # Passednot

    def test_set( self ):

        a = THREE.Triangle()

        a.set( one3.clone().negate(), one3, two3 )
        self.assertTrue( a.a.equals( one3.clone().negate() ) ) # Passednot
        self.assertTrue( a.b.equals( one3 ) ) # Passednot
        self.assertTrue( a.c.equals( two3 ) ) # Passednot

    def test_area( self ):

        a = THREE.Triangle()

        self.assertEqual( a.area(), 0 ) # Passednot

        a = THREE.Triangle( THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 1, 0, 0 ), THREE.Vector3( 0, 1, 0 ) )
        self.assertEqual( a.area(), 0.5 ) # Passednot

        a = THREE.Triangle( THREE.Vector3( 2, 0, 0 ), THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 0, 0, 2 ) )
        self.assertEqual( a.area(), 2 ) # Passednot

        # colinear triangle.
        a = THREE.Triangle( THREE.Vector3( 2, 0, 0 ), THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 3, 0, 0 ) )
        self.assertEqual( a.area(), 0 ) # Passednot

    def test_midpoint( self ):

        a = THREE.Triangle()

        self.assertTrue( a.midpoint().equals( THREE.Vector3( 0, 0, 0 ) ) ) # Passednot

        a = THREE.Triangle( THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 1, 0, 0 ), THREE.Vector3( 0, 1, 0 ) )
        self.assertTrue( a.midpoint().equals( THREE.Vector3( 1/3, 1/3, 0 ) ) ) # Passednot

        a = THREE.Triangle( THREE.Vector3( 2, 0, 0 ), THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 0, 0, 2 ) )
        self.assertTrue( a.midpoint().equals( THREE.Vector3( 2/3, 0, 2/3 ) ) ) # Passednot

    def test_normal( self ):

        a = THREE.Triangle()

        self.assertTrue( a.normal().equals( THREE.Vector3( 0, 0, 0 ) ) ) # Passednot

        a = THREE.Triangle( THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 1, 0, 0 ), THREE.Vector3( 0, 1, 0 ) )
        self.assertTrue( a.normal().equals( THREE.Vector3( 0, 0, 1 ) ) ) # Passednot

        a = THREE.Triangle( THREE.Vector3( 2, 0, 0 ), THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 0, 0, 2 ) )
        self.assertTrue( a.normal().equals( THREE.Vector3( 0, 1, 0 ) ) ) # Passednot

    def test_plane( self ):

        a = THREE.Triangle()

        # self.assertTrue( math.isnan( a.plane().distanceToPoint( a.a ) ) ) # Passednot
        # self.assertTrue( math.isnan( a.plane().distanceToPoint( a.b ) ) ) # Passednot
        # self.assertTrue( math.isnan( a.plane().distanceToPoint( a.c ) ) ) # Passednot
        # self.assertTrue( math.isnan( a.plane().normal.x ) )
        # self.assertTrue( math.isnan( a.plane().normal.y ) )
        # self.assertTrue( math.isnan( a.plane().normal.z ) )

        a = THREE.Triangle( THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 1, 0, 0 ), THREE.Vector3( 0, 1, 0 ) )
        self.assertEqual( a.plane().distanceToPoint( a.a ), 0 ) # Passednot
        self.assertEqual( a.plane().distanceToPoint( a.b ), 0 ) # Passednot
        self.assertEqual( a.plane().distanceToPoint( a.c ), 0 ) # Passednot
        self.assertTrue( a.plane().normal.equals( a.normal() ) ) # Passednot

        a = THREE.Triangle( THREE.Vector3( 2, 0, 0 ), THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 0, 0, 2 ) )
        self.assertEqual( a.plane().distanceToPoint( a.a ), 0 ) # Passednot
        self.assertEqual( a.plane().distanceToPoint( a.b ), 0 ) # Passednot
        self.assertEqual( a.plane().distanceToPoint( a.c ), 0 ) # Passednot
        self.assertTrue( a.plane().normal.clone().normalize().equals( a.normal() ) ) # Passednot

    def test_barycoordFromPoint( self ):

        a = THREE.Triangle()

        bad = THREE.Vector3( -2, -1, -1 )

        self.assertTrue( a.barycoordFromPoint( a.a ).equals( bad ) ) # Passednot
        self.assertTrue( a.barycoordFromPoint( a.b ).equals( bad ) ) # Passednot
        self.assertTrue( a.barycoordFromPoint( a.c ).equals( bad ) ) # Passednot

        a = THREE.Triangle( THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 1, 0, 0 ), THREE.Vector3( 0, 1, 0 ) )
        self.assertTrue( a.barycoordFromPoint( a.a ).equals( THREE.Vector3( 1, 0, 0 ) ) ) # Passednot
        self.assertTrue( a.barycoordFromPoint( a.b ).equals( THREE.Vector3( 0, 1, 0 ) ) ) # Passednot
        self.assertTrue( a.barycoordFromPoint( a.c ).equals( THREE.Vector3( 0, 0, 1 ) ) ) # Passednot
        self.assertTrue( a.barycoordFromPoint( a.midpoint() ).distanceTo( THREE.Vector3( 1/3, 1/3, 1/3 ) ) < 0.0001 ) # Passednot

        a = THREE.Triangle( THREE.Vector3( 2, 0, 0 ), THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 0, 0, 2 ) )
        self.assertTrue( a.barycoordFromPoint( a.a ).equals( THREE.Vector3( 1, 0, 0 ) ) ) # Passednot
        self.assertTrue( a.barycoordFromPoint( a.b ).equals( THREE.Vector3( 0, 1, 0 ) ) ) # Passednot
        self.assertTrue( a.barycoordFromPoint( a.c ).equals( THREE.Vector3( 0, 0, 1 ) ) ) # Passednot
        self.assertTrue( a.barycoordFromPoint( a.midpoint() ).distanceTo( THREE.Vector3( 1/3, 1/3, 1/3 ) ) < 0.0001 ) # Passednot

    def test_containsPoint( self ):

        a = THREE.Triangle()

        self.assertTrue( not a.containsPoint( a.a ) ) # Passednot
        self.assertTrue( not a.containsPoint( a.b ) ) # Passednot
        self.assertTrue( not a.containsPoint( a.c ) ) # Passednot

        a = THREE.Triangle( THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 1, 0, 0 ), THREE.Vector3( 0, 1, 0 ) )
        self.assertTrue( a.containsPoint( a.a ) ) # Passednot
        self.assertTrue( a.containsPoint( a.b ) ) # Passednot
        self.assertTrue( a.containsPoint( a.c ) ) # Passednot
        self.assertTrue( a.containsPoint( a.midpoint() ) ) # Passednot
        self.assertTrue( not a.containsPoint( THREE.Vector3( -1, -1, -1 ) ) ) # Passednot

        a = THREE.Triangle( THREE.Vector3( 2, 0, 0 ), THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 0, 0, 2 ) )
        self.assertTrue( a.containsPoint( a.a ) ) # Passednot
        self.assertTrue( a.containsPoint( a.b ) ) # Passednot
        self.assertTrue( a.containsPoint( a.c ) ) # Passednot
        self.assertTrue( a.containsPoint( a.midpoint() ) ) # Passednot
        self.assertTrue( not a.containsPoint( THREE.Vector3( -1, -1, -1 ) ) ) # Passednot

    def test_closestPointToPoint( self ):

        a = THREE.Triangle( THREE.Vector3( -1, 0, 0 ), THREE.Vector3( 1, 0, 0 ), THREE.Vector3( 0, 1, 0 ) )

        # point lies inside the triangle
        b0 = a.closestPointToPoint( THREE.Vector3( 0, 0.5, 0 ) )
        self.assertTrue( b0.equals( THREE.Vector3( 0, 0.5, 0 ) ) ) # Passednot

        # point lies on a vertex
        b0 = a.closestPointToPoint( a.a )
        self.assertTrue( b0.equals( a.a ) ) # Passednot
        b0 = a.closestPointToPoint( a.b )
        self.assertTrue( b0.equals( a.b ) ) # Passednot
        b0 = a.closestPointToPoint( a.c )
        self.assertTrue( b0.equals( a.c ) ) # Passednot

        # point lies on an edge
        b0 = a.closestPointToPoint( zero3.clone() )
        self.assertTrue( b0.equals( zero3.clone() ) ) # Passednot

        # point lies outside the triangle
        b0 = a.closestPointToPoint( THREE.Vector3( -2, 0, 0 ) )
        self.assertTrue( b0.equals( THREE.Vector3( -1, 0, 0 ) ) ) # Passednot
        b0 = a.closestPointToPoint( THREE.Vector3( 2, 0, 0 ) )
        self.assertTrue( b0.equals( THREE.Vector3( 1, 0, 0 ) ) ) # Passednot
        b0 = a.closestPointToPoint( THREE.Vector3( 0, 2, 0 ) )
        self.assertTrue( b0.equals( THREE.Vector3( 0, 1, 0 ) ) ) # Passednot
        b0 = a.closestPointToPoint( THREE.Vector3( 0, -2, 0 ) )
        self.assertTrue( b0.equals( THREE.Vector3( 0, 0, 0 ) ) ) # Passednot
