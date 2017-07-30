from __future__ import division

import unittest

import THREE

from Constants import *

"""
 * @author bhouston / http:#exocortex.com
 """

class TestSphere( unittest.TestCase ):

    def test_constructor( self ):

        a = THREE.Sphere()
        self.assertTrue( a.center.equals( zero3 ) ) # Passednot
        self.assertEqual( a.radius, 0 ) # Passednot

        a = THREE.Sphere( one3.clone(), 1 )
        self.assertTrue( a.center.equals( one3 ) ) # Passednot
        self.assertEqual( a.radius, 1 ) # Passednot

    def test_copy( self ):

        a = THREE.Sphere( one3.clone(), 1 )
        b = THREE.Sphere().copy( a )

        self.assertTrue( b.center.equals( one3 ) ) # Passednot
        self.assertEqual( b.radius, 1 ) # Passednot

        # ensure that it is a True copy
        a.center = zero3
        a.radius = 0
        self.assertTrue( b.center.equals( one3 ) ) # Passednot
        self.assertEqual( b.radius, 1 ) # Passednot

    def test_set( self ):

        a = THREE.Sphere()
        self.assertTrue( a.center.equals( zero3 ) ) # Passednot
        self.assertEqual( a.radius, 0 ) # Passednot

        a.set( one3, 1 )
        self.assertTrue( a.center.equals( one3 ) ) # Passednot
        self.assertEqual( a.radius, 1 ) # Passednot

    def test_empty( self ):

        a = THREE.Sphere()
        self.assertTrue( a.empty() ) # Passednot

        a.set( one3, 1 )
        self.assertTrue( not a.empty() ) # Passednot

    def test_containsPoint( self ):

        a = THREE.Sphere( one3.clone(), 1 )

        self.assertTrue( not a.containsPoint( zero3 ) ) # Passednot
        self.assertTrue( a.containsPoint( one3 ) ) # Passednot

    def test_distanceToPoint( self ):

        a = THREE.Sphere( one3.clone(), 1 )

        self.assertTrue( ( a.distanceToPoint( zero3 ) - 0.7320 ) < 0.001 ) # Passednot
        self.assertEqual( a.distanceToPoint( one3 ), -1 ) # Passednot

    def test_intersectsSphere( self ):

        a = THREE.Sphere( one3.clone(), 1 )
        b = THREE.Sphere( zero3.clone(), 1 )
        c = THREE.Sphere( zero3.clone(), 0.25 )

        self.assertTrue( a.intersectsSphere( b )  ) # Passednot
        self.assertTrue( not a.intersectsSphere( c )  ) # Passednot

    def test_intersectsPlane( self ):

        a = THREE.Sphere( zero3.clone(), 1 )
        b = THREE.Plane( THREE.Vector3( 0, 1, 0 ), 1 )
        c = THREE.Plane( THREE.Vector3( 0, 1, 0 ), 1.25 )
        d = THREE.Plane( THREE.Vector3( 0, -1, 0 ), 1.25 )

        self.assertTrue( a.intersectsPlane( b )  ) # Passednot
        self.assertTrue( not a.intersectsPlane( c )  ) # Passednot
        self.assertTrue( not a.intersectsPlane( d )  ) # Passednot

    def test_clampPoint( self ):

        a = THREE.Sphere( one3.clone(), 1 )

        self.assertTrue( a.clampPoint( THREE.Vector3( 1, 1, 3 ) ).equals( THREE.Vector3( 1, 1, 2 ) ) ) # Passednot
        self.assertTrue( a.clampPoint( THREE.Vector3( 1, 1, -3 ) ).equals( THREE.Vector3( 1, 1, 0 ) ) ) # Passednot

    def test_getBoundingBox( self ):

        a = THREE.Sphere( one3.clone(), 1 )

        self.assertTrue( a.getBoundingBox().equals( THREE.Box3( zero3, two3 ) ) ) # Passednot

        a.set( zero3, 0 )
        self.assertTrue( a.getBoundingBox().equals( THREE.Box3( zero3, zero3 ) ) ) # Passednot

    def test_applyMatrix4( self ):

        a = THREE.Sphere( one3.clone(), 1 )

        m = THREE.Matrix4().makeTranslation( 1, -2, 1 )

        self.assertTrue( a.clone().applyMatrix4( m ).getBoundingBox().equals( a.getBoundingBox().applyMatrix4( m ) ) ) # Passednot

    def test_translate( self ):

        a = THREE.Sphere( one3.clone(), 1 )

        a.translate( one3.clone().negate() )
        self.assertTrue( a.center.equals( zero3 ) ) # Passednot
