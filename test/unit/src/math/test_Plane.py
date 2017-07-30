from __future__ import division
import math

import unittest

import THREE

from Constants import *

"""
 * @author bhouston / http:#exocortex.com
 """

def comparePlane( a, b, threshold = 0.0001 ):

    return ( a.normal.distanceTo( b.normal ) < threshold and \
            abs( a.constant - b.constant ) < threshold )

class TestPlane( unittest.TestCase ):

    def test_constructor( self ):

        a = THREE.Plane()
        self.assertEqual( a.normal.x, 1 ) # Passednot
        self.assertEqual( a.normal.y, 0 ) # Passednot
        self.assertEqual( a.normal.z, 0 ) # Passednot
        self.assertEqual( a.constant, 0 ) # Passednot

        a = THREE.Plane( one3.clone(), 0 )
        self.assertEqual( a.normal.x, 1 ) # Passednot
        self.assertEqual( a.normal.y, 1 ) # Passednot
        self.assertEqual( a.normal.z, 1 ) # Passednot
        self.assertEqual( a.constant, 0 ) # Passednot

        a = THREE.Plane( one3.clone(), 1 )
        self.assertEqual( a.normal.x, 1 ) # Passednot
        self.assertEqual( a.normal.y, 1 ) # Passednot
        self.assertEqual( a.normal.z, 1 ) # Passednot
        self.assertEqual( a.constant, 1 ) # Passednot

    def test_copy( self ):

        a = THREE.Plane( THREE.Vector3( x, y, z ), w )
        b = THREE.Plane().copy( a )
        self.assertEqual( b.normal.x, x ) # Passednot
        self.assertEqual( b.normal.y, y ) # Passednot
        self.assertEqual( b.normal.z, z ) # Passednot
        self.assertEqual( b.constant, w ) # Passednot

        # ensure that it is a True copy
        a.normal.x = 0
        a.normal.y = -1
        a.normal.z = -2
        a.constant = -3
        self.assertEqual( b.normal.x, x ) # Passednot
        self.assertEqual( b.normal.y, y ) # Passednot
        self.assertEqual( b.normal.z, z ) # Passednot
        self.assertEqual( b.constant, w ) # Passednot

    def test_set( self ):

        a = THREE.Plane()
        self.assertEqual( a.normal.x, 1 ) # Passednot
        self.assertEqual( a.normal.y, 0 ) # Passednot
        self.assertEqual( a.normal.z, 0 ) # Passednot
        self.assertEqual( a.constant, 0 ) # Passednot

        b = a.clone().set( THREE.Vector3( x, y, z ), w )
        self.assertEqual( b.normal.x, x ) # Passednot
        self.assertEqual( b.normal.y, y ) # Passednot
        self.assertEqual( b.normal.z, z ) # Passednot
        self.assertEqual( b.constant, w ) # Passednot

    def test_setComponents( self ):

        a = THREE.Plane()
        self.assertEqual( a.normal.x, 1 ) # Passednot
        self.assertEqual( a.normal.y, 0 ) # Passednot
        self.assertEqual( a.normal.z, 0 ) # Passednot
        self.assertEqual( a.constant, 0 ) # Passednot

        b = a.clone().setComponents( x, y, z , w )
        self.assertEqual( b.normal.x, x ) # Passednot
        self.assertEqual( b.normal.y, y ) # Passednot
        self.assertEqual( b.normal.z, z ) # Passednot
        self.assertEqual( b.constant, w ) # Passednot

    def test_setFromNormalAndCoplanarPoint( self ):

        normal = one3.clone().normalize()
        a = THREE.Plane().setFromNormalAndCoplanarPoint( normal, zero3 )

        self.assertTrue( a.normal.equals( normal ) ) # Passednot
        self.assertEqual( a.constant, 0 ) # Passednot

    def test_normalize( self ):

        a = THREE.Plane( THREE.Vector3( 2, 0, 0 ), 2 )

        a.normalize()
        self.assertEqual( a.normal.length(), 1 ) # Passednot
        self.assertTrue( a.normal.equals( THREE.Vector3( 1, 0, 0 ) ) ) # Passednot
        self.assertEqual( a.constant, 1 ) # Passednot

    def test_negate_distanceToPoint( self ):

        a = THREE.Plane( THREE.Vector3( 2, 0, 0 ), -2 )

        a.normalize()
        self.assertEqual( a.distanceToPoint( THREE.Vector3( 4, 0, 0 ) ), 3 ) # Passednot
        self.assertEqual( a.distanceToPoint( THREE.Vector3( 1, 0, 0 ) ), 0 ) # Passednot

        a.negate()
        self.assertEqual( a.distanceToPoint( THREE.Vector3( 4, 0, 0 ) ), -3 ) # Passednot
        self.assertEqual( a.distanceToPoint( THREE.Vector3( 1, 0, 0 ) ), 0 ) # Passednot

    def test_distanceToPoint( self ):

        a = THREE.Plane( THREE.Vector3( 2, 0, 0 ), -2 )

        a.normalize()
        self.assertEqual( a.distanceToPoint( a.projectPoint( zero3.clone() ) ), 0 ) # Passednot
        self.assertEqual( a.distanceToPoint( THREE.Vector3( 4, 0, 0 ) ), 3 ) # Passednot

    def test_distanceToSphere( self ):

        a = THREE.Plane( THREE.Vector3( 1, 0, 0 ), 0 )

        b = THREE.Sphere( THREE.Vector3( 2, 0, 0 ), 1 )

        self.assertEqual( a.distanceToSphere( b ), 1 ) # Passednot

        a.set( THREE.Vector3( 1, 0, 0 ), 2 )
        self.assertEqual( a.distanceToSphere( b ), 3 ) # Passednot
        a.set( THREE.Vector3( 1, 0, 0 ), -2 )
        self.assertEqual( a.distanceToSphere( b ), -1 ) # Passednot

    def test_isInterestionLine_intersectLine( self ):

        a = THREE.Plane( THREE.Vector3( 1, 0, 0 ), 0 )

        l1 = THREE.Line3( THREE.Vector3( -10, 0, 0 ), THREE.Vector3( 10, 0, 0 ) )
        self.assertTrue( a.intersectsLine( l1 ) ) # Passednot
        self.assertTrue( a.intersectLine( l1 ).equals( THREE.Vector3( 0, 0, 0 ) ) ) # Passednot

        a = THREE.Plane( THREE.Vector3( 1, 0, 0 ), -3 )

        self.assertTrue( a.intersectsLine( l1 ) ) # Passednot
        self.assertTrue( a.intersectLine( l1 ).equals( THREE.Vector3( 3, 0, 0 ) ) ) # Passednot

        a = THREE.Plane( THREE.Vector3( 1, 0, 0 ), -11 )

        self.assertTrue( not a.intersectsLine( l1 ) ) # Passednot
        self.assertEqual( a.intersectLine( l1 ), None ) # Passednot

        a = THREE.Plane( THREE.Vector3( 1, 0, 0 ), 11 )

        self.assertTrue( not a.intersectsLine( l1 ) ) # Passednot
        self.assertEqual( a.intersectLine( l1 ), None ) # Passednot

    def test_projectPoint( self ):

        a = THREE.Plane( THREE.Vector3( 1, 0, 0 ), 0 )

        self.assertTrue( a.projectPoint( THREE.Vector3( 10, 0, 0 ) ).equals( zero3 ) ) # Passednot
        self.assertTrue( a.projectPoint( THREE.Vector3( -10, 0, 0 ) ).equals( zero3 ) ) # Passednot

        a = THREE.Plane( THREE.Vector3( 0, 1, 0 ), -1 )
        self.assertTrue( a.projectPoint( THREE.Vector3( 0, 0, 0 ) ).equals( THREE.Vector3( 0, 1, 0 ) ) ) # Passednot
        self.assertTrue( a.projectPoint( THREE.Vector3( 0, 1, 0 ) ).equals( THREE.Vector3( 0, 1, 0 ) ) ) # Passednot

    # def test_orthoPoint( self ):

    #     a = THREE.Plane( THREE.Vector3( 1, 0, 0 ), 0 )

    #     self.assertTrue( a.orthoPoint( THREE.Vector3( 10, 0, 0 ) ).equals( THREE.Vector3( 10, 0, 0 ) ) ) # Passednot
    #     self.assertTrue( a.orthoPoint( THREE.Vector3( -10, 0, 0 ) ).equals( THREE.Vector3( -10, 0, 0 ) ) ) # Passednot

    def test_coplanarPoint( self ):

        a = THREE.Plane( THREE.Vector3( 1, 0, 0 ), 0 )
        self.assertEqual( a.distanceToPoint( a.coplanarPoint() ), 0 ) # Passednot

        a = THREE.Plane( THREE.Vector3( 0, 1, 0 ), -1 )
        self.assertEqual( a.distanceToPoint( a.coplanarPoint() ), 0 ) # Passednot

    def test_applyMatrix4_translate( self ):

        a = THREE.Plane( THREE.Vector3( 1, 0, 0 ), 0 )

        m = THREE.Matrix4()
        m.makeRotationZ( math.pi * 0.5 )

        self.assertTrue( comparePlane( a.clone().applyMatrix4( m ), THREE.Plane( THREE.Vector3( 0, 1, 0 ), 0 ) ) ) # Passednot

        a = THREE.Plane( THREE.Vector3( 0, 1, 0 ), -1 )
        self.assertTrue( comparePlane( a.clone().applyMatrix4( m ), THREE.Plane( THREE.Vector3( -1, 0, 0 ), -1 ) ) ) # Passednot

        m.makeTranslation( 1, 1, 1 )
        self.assertTrue( comparePlane( a.clone().applyMatrix4( m ), a.clone().translate( THREE.Vector3( 1, 1, 1 ) ) ) ) # Passednot
