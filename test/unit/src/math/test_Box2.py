from __future__ import division
import math

import unittest

import THREE

from Constants import *

"""
 * @author bhouston / http:#exocortex.com
 """

class TestBox2( unittest.TestCase ):

    def test_constructor( self ):

        a = THREE.Box2()
        self.assertTrue( a.min.equals( posInf2 ) ) # Passednot
        self.assertTrue( a.max.equals( negInf2 ) ) # Passednot

        a = THREE.Box2( zero2.clone(), zero2.clone() )
        self.assertTrue( a.min.equals( zero2 ) ) # Passednot
        self.assertTrue( a.max.equals( zero2 ) ) # Passednot

        a = THREE.Box2( zero2.clone(), one2.clone() )
        self.assertTrue( a.min.equals( zero2 ) ) # Passednot
        self.assertTrue( a.max.equals( one2 ) ) # Passednot

    def test_copy( self ):

        a = THREE.Box2( zero2.clone(), one2.clone() )
        b = THREE.Box2().copy( a )
        self.assertTrue( b.min.equals( zero2 ) ) # Passednot
        self.assertTrue( b.max.equals( one2 ) ) # Passednot

        # ensure that it is a True copy
        a.min = zero2
        a.max = one2
        self.assertTrue( b.min.equals( zero2 ) ) # Passednot
        self.assertTrue( b.max.equals( one2 ) ) # Passednot

    def test_set( self ):

        a = THREE.Box2()

        a.set( zero2, one2 )
        self.assertTrue( a.min.equals( zero2 ) ) # Passednot
        self.assertTrue( a.max.equals( one2 ) ) # Passednot

    def test_setFromPoints( self ):

        a = THREE.Box2()

        a.setFromPoints( [ zero2, one2, two2 ] )
        self.assertTrue( a.min.equals( zero2 ) ) # Passednot
        self.assertTrue( a.max.equals( two2 ) ) # Passednot

        a.setFromPoints( [ one2 ] )
        self.assertTrue( a.min.equals( one2 ) ) # Passednot
        self.assertTrue( a.max.equals( one2 ) ) # Passednot

        a.setFromPoints( [] )
        self.assertTrue( a.isEmpty() ) # Passednot

    def test_empty_makeEmpty( self ):

        a = THREE.Box2()

        self.assertTrue( a.isEmpty() ) # Passednot

        a = THREE.Box2( zero2.clone(), one2.clone() )
        self.assertTrue( not a.isEmpty() ) # Passednot

        a.makeEmpty()
        self.assertTrue( a.isEmpty() ) # Passednot

    def test_getCenter( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )

        self.assertTrue( a.getCenter().equals( zero2 ) ) # Passednot

        a = THREE.Box2( zero2, one2 )
        midpoint = one2.clone().multiplyScalar( 0.5 )
        self.assertTrue( a.getCenter().equals( midpoint ) ) # Passednot

    def test_getSize( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )

        self.assertTrue( a.getSize().equals( zero2 ) ) # Passednot

        a = THREE.Box2( zero2.clone(), one2.clone() )
        self.assertTrue( a.getSize().equals( one2 ) ) # Passednot

    def test_expandByPoint( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )

        a.expandByPoint( zero2 )
        self.assertTrue( a.getSize().equals( zero2 ) ) # Passednot

        a.expandByPoint( one2 )
        self.assertTrue( a.getSize().equals( one2 ) ) # Passednot

        a.expandByPoint( one2.clone().negate() )
        self.assertTrue( a.getSize().equals( one2.clone().multiplyScalar( 2 ) ) ) # Passednot
        self.assertTrue( a.getCenter().equals( zero2 ) ) # Passednot

    def test_expandByVector( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )

        a.expandByVector( zero2 )
        self.assertTrue( a.getSize().equals( zero2 ) ) # Passednot

        a.expandByVector( one2 )
        self.assertTrue( a.getSize().equals( one2.clone().multiplyScalar( 2 ) ) ) # Passednot
        self.assertTrue( a.getCenter().equals( zero2 ) ) # Passednot

    def test_expandByScalar( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )

        a.expandByScalar( 0 )
        self.assertTrue( a.getSize().equals( zero2 ) ) # Passednot

        a.expandByScalar( 1 )
        self.assertTrue( a.getSize().equals( one2.clone().multiplyScalar( 2 ) ) ) # Passednot
        self.assertTrue( a.getCenter().equals( zero2 ) ) # Passednot

    def test_containsPoint( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )

        self.assertTrue( a.containsPoint( zero2 ) ) # Passednot
        self.assertTrue( not a.containsPoint( one2 ) ) # Passednot

        a.expandByScalar( 1 )
        self.assertTrue( a.containsPoint( zero2 ) ) # Passednot
        self.assertTrue( a.containsPoint( one2 ) ) # Passednot
        self.assertTrue( a.containsPoint( one2.clone().negate() ) ) # Passednot

    def test_containsBox( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )
        b = THREE.Box2( zero2.clone(), one2.clone() )
        c = THREE.Box2( one2.clone().negate(), one2.clone() )

        self.assertTrue( a.containsBox( a ) ) # Passednot
        self.assertTrue( not a.containsBox( b ) ) # Passednot
        self.assertTrue( not a.containsBox( c ) ) # Passednot

        self.assertTrue( b.containsBox( a ) ) # Passednot
        self.assertTrue( c.containsBox( a ) ) # Passednot
        self.assertTrue( not b.containsBox( c ) ) # Passednot

    def test_getParameter( self ):

        a = THREE.Box2( zero2.clone(), one2.clone() )
        b = THREE.Box2( one2.clone().negate(), one2.clone() )

        self.assertTrue( a.getParameter( THREE.Vector2( 0, 0 ) ).equals( THREE.Vector2( 0, 0 ) ) ) # Passednot
        self.assertTrue( a.getParameter( THREE.Vector2( 1, 1 ) ).equals( THREE.Vector2( 1, 1 ) ) ) # Passednot

        self.assertTrue( b.getParameter( THREE.Vector2( -1, -1 ) ).equals( THREE.Vector2( 0, 0 ) ) ) # Passednot
        self.assertTrue( b.getParameter( THREE.Vector2( 0, 0 ) ).equals( THREE.Vector2( 0.5, 0.5 ) ) ) # Passednot
        self.assertTrue( b.getParameter( THREE.Vector2( 1, 1 ) ).equals( THREE.Vector2( 1, 1 ) ) ) # Passednot

    def test_clampPoint( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )
        b = THREE.Box2( one2.clone().negate(), one2.clone() )

        self.assertTrue( a.clampPoint( THREE.Vector2( 0, 0 ) ).equals( THREE.Vector2( 0, 0 ) ) ) # Passednot
        self.assertTrue( a.clampPoint( THREE.Vector2( 1, 1 ) ).equals( THREE.Vector2( 0, 0 ) ) ) # Passednot
        self.assertTrue( a.clampPoint( THREE.Vector2( -1, -1 ) ).equals( THREE.Vector2( 0, 0 ) ) ) # Passednot

        self.assertTrue( b.clampPoint( THREE.Vector2( 2, 2 ) ).equals( THREE.Vector2( 1, 1 ) ) ) # Passednot
        self.assertTrue( b.clampPoint( THREE.Vector2( 1, 1 ) ).equals( THREE.Vector2( 1, 1 ) ) ) # Passednot
        self.assertTrue( b.clampPoint( THREE.Vector2( 0, 0 ) ).equals( THREE.Vector2( 0, 0 ) ) ) # Passednot
        self.assertTrue( b.clampPoint( THREE.Vector2( -1, -1 ) ).equals( THREE.Vector2( -1, -1 ) ) ) # Passednot
        self.assertTrue( b.clampPoint( THREE.Vector2( -2, -2 ) ).equals( THREE.Vector2( -1, -1 ) ) ) # Passednot

    def test_distanceToPoint( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )
        b = THREE.Box2( one2.clone().negate(), one2.clone() )

        self.assertEqual( a.distanceToPoint( THREE.Vector2( 0, 0 ) ), 0 ) # Passednot
        self.assertEqual( a.distanceToPoint( THREE.Vector2( 1, 1 ) ), math.sqrt( 2 ) ) # Passednot
        self.assertEqual( a.distanceToPoint( THREE.Vector2( -1, -1 ) ), math.sqrt( 2 ) ) # Passednot

        self.assertEqual( b.distanceToPoint( THREE.Vector2( 2, 2 ) ), math.sqrt( 2 ) ) # Passednot
        self.assertEqual( b.distanceToPoint( THREE.Vector2( 1, 1 ) ), 0 ) # Passednot
        self.assertEqual( b.distanceToPoint( THREE.Vector2( 0, 0 ) ), 0 ) # Passednot
        self.assertEqual( b.distanceToPoint( THREE.Vector2( -1, -1 ) ), 0 ) # Passednot
        self.assertEqual( b.distanceToPoint( THREE.Vector2( -2, -2 ) ), math.sqrt( 2 ) ) # Passednot

    def test_intersectsBox( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )
        b = THREE.Box2( zero2.clone(), one2.clone() )
        c = THREE.Box2( one2.clone().negate(), one2.clone() )

        self.assertTrue( a.intersectsBox( a ) ) # Passednot
        self.assertTrue( a.intersectsBox( b ) ) # Passednot
        self.assertTrue( a.intersectsBox( c ) ) # Passednot

        self.assertTrue( b.intersectsBox( a ) ) # Passednot
        self.assertTrue( c.intersectsBox( a ) ) # Passednot
        self.assertTrue( b.intersectsBox( c ) ) # Passednot

        b.translate( THREE.Vector2( 2, 2 ) )
        self.assertTrue( not a.intersectsBox( b ) ) # Passednot
        self.assertTrue( not b.intersectsBox( a ) ) # Passednot
        self.assertTrue( not b.intersectsBox( c ) ) # Passednot

    def test_intersect( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )
        b = THREE.Box2( zero2.clone(), one2.clone() )
        c = THREE.Box2( one2.clone().negate(), one2.clone() )

        self.assertTrue( a.clone().intersect( a ).equals( a ) ) # Passednot
        self.assertTrue( a.clone().intersect( b ).equals( a ) ) # Passednot
        self.assertTrue( b.clone().intersect( b ).equals( b ) ) # Passednot
        self.assertTrue( a.clone().intersect( c ).equals( a ) ) # Passednot
        self.assertTrue( b.clone().intersect( c ).equals( b ) ) # Passednot
        self.assertTrue( c.clone().intersect( c ).equals( c ) ) # Passednot

    def test_union( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )
        b = THREE.Box2( zero2.clone(), one2.clone() )
        c = THREE.Box2( one2.clone().negate(), one2.clone() )

        self.assertTrue( a.clone().union( a ).equals( a ) ) # Passednot
        self.assertTrue( a.clone().union( b ).equals( b ) ) # Passednot
        self.assertTrue( a.clone().union( c ).equals( c ) ) # Passednot
        self.assertTrue( b.clone().union( c ).equals( c ) ) # Passednot

    def test_translate( self ):

        a = THREE.Box2( zero2.clone(), zero2.clone() )
        b = THREE.Box2( zero2.clone(), one2.clone() )
        c = THREE.Box2( one2.clone().negate(), one2.clone() )
        d = THREE.Box2( one2.clone().negate(), zero2.clone() )

        self.assertTrue( a.clone().translate( one2 ).equals( THREE.Box2( one2, one2 ) ) ) # Passednot
        self.assertTrue( a.clone().translate( one2 ).translate( one2.clone().negate() ).equals( a ) ) # Passednot
        self.assertTrue( d.clone().translate( one2 ).equals( b ) ) # Passednot
        self.assertTrue( b.clone().translate( one2.clone().negate() ).equals( d ) ) # Passednot
