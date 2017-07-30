from __future__ import division
import math

import unittest

import THREE

from Constants import *

"""
 * @author bhouston / http:#exocortex.com
 """

def compareBox( a, b, threshold = 0.0001 ):

    return ( a.min.distanceTo( b.min ) < threshold and \
            a.max.distanceTo( b.max ) < threshold )

class TestBox3( unittest.TestCase ):

    def test_constructor( self ):

        a = THREE.Box3()
        self.assertTrue( a.min.equals( posInf3 ) ) # Passednot
        self.assertTrue( a.max.equals( negInf3 ) ) # Passednot

        a = THREE.Box3( zero3.clone(), zero3.clone() )
        self.assertTrue( a.min.equals( zero3 ) ) # Passednot
        self.assertTrue( a.max.equals( zero3 ) ) # Passednot

        a = THREE.Box3( zero3.clone(), one3.clone() )
        self.assertTrue( a.min.equals( zero3 ) ) # Passednot
        self.assertTrue( a.max.equals( one3 ) ) # Passednot

    def test_copy( self ):

        a = THREE.Box3( zero3.clone(), one3.clone() )
        b = THREE.Box3().copy( a )
        self.assertTrue( b.min.equals( zero3 ) ) # Passednot
        self.assertTrue( b.max.equals( one3 ) ) # Passednot

        # ensure that it is a True copy
        a.min = zero3
        a.max = one3
        self.assertTrue( b.min.equals( zero3 ) ) # Passednot
        self.assertTrue( b.max.equals( one3 ) ) # Passednot

    def test_set( self ):

        a = THREE.Box3()

        a.set( zero3, one3 )
        self.assertTrue( a.min.equals( zero3 ) ) # Passednot
        self.assertTrue( a.max.equals( one3 ) ) # Passednot

    def test_setFromPoints( self ):

        a = THREE.Box3()

        a.setFromPoints( [ zero3, one3, two3 ] )
        self.assertTrue( a.min.equals( zero3 ) ) # Passednot
        self.assertTrue( a.max.equals( two3 ) ) # Passednot

        a.setFromPoints( [ one3 ] )
        self.assertTrue( a.min.equals( one3 ) ) # Passednot
        self.assertTrue( a.max.equals( one3 ) ) # Passednot

        a.setFromPoints( [] )
        self.assertTrue( a.isEmpty() ) # Passednot

    def test_empty_makeEmpty( self ):

        a = THREE.Box3()

        self.assertTrue( a.isEmpty() ) # Passednot

        a = THREE.Box3( zero3.clone(), one3.clone() )
        self.assertTrue( not a.isEmpty() ) # Passednot

        a.makeEmpty()
        self.assertTrue( a.isEmpty() ) # Passednot

    def test_getCenter( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )

        self.assertTrue( a.getCenter().equals( zero3 ) ) # Passednot

        a = THREE.Box3( zero3.clone(), one3.clone() )
        midpoint = one3.clone().multiplyScalar( 0.5 )
        self.assertTrue( a.getCenter().equals( midpoint ) ) # Passednot

    def test_getSize( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )

        self.assertTrue( a.getSize().equals( zero3 ) ) # Passednot

        a = THREE.Box3( zero3.clone(), one3.clone() )
        self.assertTrue( a.getSize().equals( one3 ) ) # Passednot

    def test_expandByPoint( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )

        a.expandByPoint( zero3 )
        self.assertTrue( a.getSize().equals( zero3 ) ) # Passednot

        a.expandByPoint( one3 )
        self.assertTrue( a.getSize().equals( one3 ) ) # Passednot

        a.expandByPoint( one3.clone().negate() )
        self.assertTrue( a.getSize().equals( one3.clone().multiplyScalar( 2 ) ) ) # Passednot
        self.assertTrue( a.getCenter().equals( zero3 ) ) # Passednot

    def test_expandByVector( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )

        a.expandByVector( zero3 )
        self.assertTrue( a.getSize().equals( zero3 ) ) # Passednot

        a.expandByVector( one3 )
        self.assertTrue( a.getSize().equals( one3.clone().multiplyScalar( 2 ) ) ) # Passednot
        self.assertTrue( a.getCenter().equals( zero3 ) ) # Passednot

    def test_expandByScalar( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )

        a.expandByScalar( 0 )
        self.assertTrue( a.getSize().equals( zero3 ) ) # Passednot

        a.expandByScalar( 1 )
        self.assertTrue( a.getSize().equals( one3.clone().multiplyScalar( 2 ) ) ) # Passednot
        self.assertTrue( a.getCenter().equals( zero3 ) ) # Passednot

    def test_containsPoint( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )

        self.assertTrue( a.containsPoint( zero3 ) ) # Passednot
        self.assertTrue( not a.containsPoint( one3 ) ) # Passednot

        a.expandByScalar( 1 )
        self.assertTrue( a.containsPoint( zero3 ) ) # Passednot
        self.assertTrue( a.containsPoint( one3 ) ) # Passednot
        self.assertTrue( a.containsPoint( one3.clone().negate() ) ) # Passednot

    def test_containsBox( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )
        b = THREE.Box3( zero3.clone(), one3.clone() )
        c = THREE.Box3( one3.clone().negate(), one3.clone() )

        self.assertTrue( a.containsBox( a ) ) # Passednot
        self.assertTrue( not a.containsBox( b ) ) # Passednot
        self.assertTrue( not a.containsBox( c ) ) # Passednot

        self.assertTrue( b.containsBox( a ) ) # Passednot
        self.assertTrue( c.containsBox( a ) ) # Passednot
        self.assertTrue( not b.containsBox( c ) ) # Passednot

    def test_getParameter( self ):

        a = THREE.Box3( zero3.clone(), one3.clone() )
        b = THREE.Box3( one3.clone().negate(), one3.clone() )

        self.assertTrue( a.getParameter( THREE.Vector3( 0, 0, 0 ) ).equals( THREE.Vector3( 0, 0, 0 ) ) ) # Passednot
        self.assertTrue( a.getParameter( THREE.Vector3( 1, 1, 1 ) ).equals( THREE.Vector3( 1, 1, 1 ) ) ) # Passednot

        self.assertTrue( b.getParameter( THREE.Vector3( -1, -1, -1 ) ).equals( THREE.Vector3( 0, 0, 0 ) ) ) # Passednot
        self.assertTrue( b.getParameter( THREE.Vector3( 0, 0, 0 ) ).equals( THREE.Vector3( 0.5, 0.5, 0.5 ) ) ) # Passednot
        self.assertTrue( b.getParameter( THREE.Vector3( 1, 1, 1 ) ).equals( THREE.Vector3( 1, 1, 1 ) ) ) # Passednot

    def test_clampPoint( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )
        b = THREE.Box3( one3.clone().negate(), one3.clone() )

        self.assertTrue( a.clampPoint( THREE.Vector3( 0, 0, 0 ) ).equals( THREE.Vector3( 0, 0, 0 ) ) ) # Passednot
        self.assertTrue( a.clampPoint( THREE.Vector3( 1, 1, 1 ) ).equals( THREE.Vector3( 0, 0, 0 ) ) ) # Passednot
        self.assertTrue( a.clampPoint( THREE.Vector3( -1, -1, -1 ) ).equals( THREE.Vector3( 0, 0, 0 ) ) ) # Passednot

        self.assertTrue( b.clampPoint( THREE.Vector3( 2, 2, 2 ) ).equals( THREE.Vector3( 1, 1, 1 ) ) ) # Passednot
        self.assertTrue( b.clampPoint( THREE.Vector3( 1, 1, 1 ) ).equals( THREE.Vector3( 1, 1, 1 ) ) ) # Passednot
        self.assertTrue( b.clampPoint( THREE.Vector3( 0, 0, 0 ) ).equals( THREE.Vector3( 0, 0, 0 ) ) ) # Passednot
        self.assertTrue( b.clampPoint( THREE.Vector3( -1, -1, -1 ) ).equals( THREE.Vector3( -1, -1, -1 ) ) ) # Passednot
        self.assertTrue( b.clampPoint( THREE.Vector3( -2, -2, -2 ) ).equals( THREE.Vector3( -1, -1, -1 ) ) ) # Passednot

    def test_distanceToPoint( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )
        b = THREE.Box3( one3.clone().negate(), one3.clone() )

        self.assertEqual( a.distanceToPoint( THREE.Vector3( 0, 0, 0 ) ), 0 ) # Passednot
        self.assertEqual( a.distanceToPoint( THREE.Vector3( 1, 1, 1 ) ), math.sqrt( 3 ) ) # Passednot
        self.assertEqual( a.distanceToPoint( THREE.Vector3( -1, -1, -1 ) ), math.sqrt( 3 ) ) # Passednot

        self.assertEqual( b.distanceToPoint( THREE.Vector3( 2, 2, 2 ) ), math.sqrt( 3 ) ) # Passednot
        self.assertEqual( b.distanceToPoint( THREE.Vector3( 1, 1, 1 ) ), 0 ) # Passednot
        self.assertEqual( b.distanceToPoint( THREE.Vector3( 0, 0, 0 ) ), 0 ) # Passednot
        self.assertEqual( b.distanceToPoint( THREE.Vector3( -1, -1, -1 ) ), 0 ) # Passednot
        self.assertEqual( b.distanceToPoint( THREE.Vector3( -2, -2, -2 ) ), math.sqrt( 3 ) ) # Passednot

    def test_distanceToPoint( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )
        b = THREE.Box3( one3.clone().negate(), one3.clone() )

        self.assertEqual( a.distanceToPoint( THREE.Vector3( 0, 0, 0 ) ), 0 ) # Passednot
        self.assertEqual( a.distanceToPoint( THREE.Vector3( 1, 1, 1 ) ), math.sqrt( 3 ) ) # Passednot
        self.assertEqual( a.distanceToPoint( THREE.Vector3( -1, -1, -1 ) ), math.sqrt( 3 ) ) # Passednot

        self.assertEqual( b.distanceToPoint( THREE.Vector3( 2, 2, 2 ) ), math.sqrt( 3 ) ) # Passednot
        self.assertEqual( b.distanceToPoint( THREE.Vector3( 1, 1, 1 ) ), 0 ) # Passednot
        self.assertEqual( b.distanceToPoint( THREE.Vector3( 0, 0, 0 ) ), 0 ) # Passednot
        self.assertEqual( b.distanceToPoint( THREE.Vector3( -1, -1, -1 ) ), 0 ) # Passednot
        self.assertEqual( b.distanceToPoint( THREE.Vector3( -2, -2, -2 ) ), math.sqrt( 3 ) ) # Passednot

    def test_intersectsBox( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )
        b = THREE.Box3( zero3.clone(), one3.clone() )
        c = THREE.Box3( one3.clone().negate(), one3.clone() )

        self.assertTrue( a.intersectsBox( a ) ) # Passednot
        self.assertTrue( a.intersectsBox( b ) ) # Passednot
        self.assertTrue( a.intersectsBox( c ) ) # Passednot

        self.assertTrue( b.intersectsBox( a ) ) # Passednot
        self.assertTrue( c.intersectsBox( a ) ) # Passednot
        self.assertTrue( b.intersectsBox( c ) ) # Passednot

        b.translate( THREE.Vector3( 2, 2, 2 ) )
        self.assertTrue( not a.intersectsBox( b ) ) # Passednot
        self.assertTrue( not b.intersectsBox( a ) ) # Passednot
        self.assertTrue( not b.intersectsBox( c ) ) # Passednot

    def test_intersectsSphere( self ):

        a = THREE.Box3( zero3.clone(), one3.clone() )
        b = THREE.Sphere( zero3.clone(), 1 )

        self.assertTrue( a.intersectsSphere( b )  ) # Passednot

        b.translate( THREE.Vector3( 2, 2, 2 ) )
        self.assertTrue( not a.intersectsSphere( b )  ) # Passednot

    def test_intersectsPlane( self ):

        a = THREE.Box3( zero3.clone(), one3.clone() )
        b = THREE.Plane( THREE.Vector3( 0, 1, 0 ), 1 )
        c = THREE.Plane( THREE.Vector3( 0, 1, 0 ), 1.25 )
        d = THREE.Plane( THREE.Vector3( 0, -1, 0 ), 1.25 )

        self.assertTrue( a.intersectsPlane( b )  ) # Passednot
        self.assertTrue( not a.intersectsPlane( c )  ) # Passednot
        self.assertTrue( not a.intersectsPlane( d )  ) # Passednot

    def test_getBoundingSphere( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )
        b = THREE.Box3( zero3.clone(), one3.clone() )
        c = THREE.Box3( one3.clone().negate(), one3.clone() )

        self.assertTrue( a.getBoundingSphere().equals( THREE.Sphere( zero3, 0 ) ) ) # Passednot
        self.assertTrue( b.getBoundingSphere().equals( THREE.Sphere( one3.clone().multiplyScalar( 0.5 ), math.sqrt( 3 ) * 0.5 ) ) ) # Passednot
        self.assertTrue( c.getBoundingSphere().equals( THREE.Sphere( zero3, math.sqrt( 12 ) * 0.5 ) ) ) # Passednot

    def test_intersect( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )
        b = THREE.Box3( zero3.clone(), one3.clone() )
        c = THREE.Box3( one3.clone().negate(), one3.clone() )

        self.assertTrue( a.clone().intersect( a ).equals( a ) ) # Passednot
        self.assertTrue( a.clone().intersect( b ).equals( a ) ) # Passednot
        self.assertTrue( b.clone().intersect( b ).equals( b ) ) # Passednot
        self.assertTrue( a.clone().intersect( c ).equals( a ) ) # Passednot
        self.assertTrue( b.clone().intersect( c ).equals( b ) ) # Passednot
        self.assertTrue( c.clone().intersect( c ).equals( c ) ) # Passednot

    def test_union( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )
        b = THREE.Box3( zero3.clone(), one3.clone() )
        c = THREE.Box3( one3.clone().negate(), one3.clone() )

        self.assertTrue( a.clone().union( a ).equals( a ) ) # Passednot
        self.assertTrue( a.clone().union( b ).equals( b ) ) # Passednot
        self.assertTrue( a.clone().union( c ).equals( c ) ) # Passednot
        self.assertTrue( b.clone().union( c ).equals( c ) ) # Passednot

    def test_applyMatrix4( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )
        b = THREE.Box3( zero3.clone(), one3.clone() )
        c = THREE.Box3( one3.clone().negate(), one3.clone() )
        d = THREE.Box3( one3.clone().negate(), zero3.clone() )

        m = THREE.Matrix4().makeTranslation( 1, -2, 1 )
        t1 = THREE.Vector3( 1, -2, 1 )

        self.assertTrue( compareBox( a.clone().applyMatrix4( m ), a.clone().translate( t1 ) ) ) # Passednot
        self.assertTrue( compareBox( b.clone().applyMatrix4( m ), b.clone().translate( t1 ) ) ) # Passednot
        self.assertTrue( compareBox( c.clone().applyMatrix4( m ), c.clone().translate( t1 ) ) ) # Passednot
        self.assertTrue( compareBox( d.clone().applyMatrix4( m ), d.clone().translate( t1 ) ) ) # Passednot

    def test_translate( self ):

        a = THREE.Box3( zero3.clone(), zero3.clone() )
        b = THREE.Box3( zero3.clone(), one3.clone() )
        c = THREE.Box3( one3.clone().negate(), one3.clone() )
        d = THREE.Box3( one3.clone().negate(), zero3.clone() )

        self.assertTrue( a.clone().translate( one3 ).equals( THREE.Box3( one3, one3 ) ) ) # Passednot
        self.assertTrue( a.clone().translate( one3 ).translate( one3.clone().negate() ).equals( a ) ) # Passednot
        self.assertTrue( d.clone().translate( one3 ).equals( b ) ) # Passednot
        self.assertTrue( b.clone().translate( one3.clone().negate() ).equals( d ) ) # Passednot
