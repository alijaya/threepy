from __future__ import division

import unittest

import THREE

"""
 * @author bhouston / http:#exocortex.com
 """

unit3 = THREE.Vector3( 1, 0, 0 )

def planeEquals( a, b, tolerance = 0.0001 ):

    if a.normal.distanceTo( b.normal ) > tolerance: return False
    if abs( a.constant - b.constant ) > tolerance: return False

    return True

class TestFrustum( unittest.TestCase ):

    def test_constructor( self ):

        a = THREE.Frustum()

        self.assertTrue( a.planes != None ) # Passednot
        self.assertEqual( len( a.planes ), 6 ) # Passednot

        pDefault = THREE.Plane()
        for i in range( 6 ):
            self.assertTrue( a.planes[i].equals( pDefault ) ) # Passednot

        p0 = THREE.Plane( unit3, -1 )
        p1 = THREE.Plane( unit3, 1 )
        p2 = THREE.Plane( unit3, 2 )
        p3 = THREE.Plane( unit3, 3 )
        p4 = THREE.Plane( unit3, 4 )
        p5 = THREE.Plane( unit3, 5 )

        a = THREE.Frustum( p0, p1, p2, p3, p4, p5 )
        self.assertTrue( a.planes[0].equals( p0 ) ) # Passednot
        self.assertTrue( a.planes[1].equals( p1 ) ) # Passednot
        self.assertTrue( a.planes[2].equals( p2 ) ) # Passednot
        self.assertTrue( a.planes[3].equals( p3 ) ) # Passednot
        self.assertTrue( a.planes[4].equals( p4 ) ) # Passednot
        self.assertTrue( a.planes[5].equals( p5 ) ) # Passednot

    def test_copy( self ):

        p0 = THREE.Plane( unit3, -1 )
        p1 = THREE.Plane( unit3, 1 )
        p2 = THREE.Plane( unit3, 2 )
        p3 = THREE.Plane( unit3, 3 )
        p4 = THREE.Plane( unit3, 4 )
        p5 = THREE.Plane( unit3, 5 )

        b = THREE.Frustum( p0, p1, p2, p3, p4, p5 )
        a = THREE.Frustum().copy( b )
        self.assertTrue( a.planes[0].equals( p0 ) ) # Passednot
        self.assertTrue( a.planes[1].equals( p1 ) ) # Passednot
        self.assertTrue( a.planes[2].equals( p2 ) ) # Passednot
        self.assertTrue( a.planes[3].equals( p3 ) ) # Passednot
        self.assertTrue( a.planes[4].equals( p4 ) ) # Passednot
        self.assertTrue( a.planes[5].equals( p5 ) ) # Passednot

        # ensure it is a True copy by modifying source
        b.planes[0] = p1
        self.assertTrue( a.planes[0].equals( p0 ) ) # Passednot

    def test_setFromMatrix_makeOrthographic_containsPoint( self ):

        m = THREE.Matrix4().makeOrthographic( -1, 1, -1, 1, 1, 100 )
        a = THREE.Frustum().setFromMatrix( m )

        self.assertTrue( not a.containsPoint( THREE.Vector3( 0, 0, 0 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( 0, 0, -50 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( 0, 0, -1.001 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( -1, -1, -1.001 ) ) ) # Passednot
        self.assertTrue( not a.containsPoint( THREE.Vector3( -1.1, -1.1, -1.001 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( 1, 1, -1.001 ) ) ) # Passednot
        self.assertTrue( not a.containsPoint( THREE.Vector3( 1.1, 1.1, -1.001 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( 0, 0, -100 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( -1, -1, -100 ) ) ) # Passednot
        self.assertTrue( not a.containsPoint( THREE.Vector3( -1.1, -1.1, -100.1 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( 1, 1, -100 ) ) ) # Passednot
        self.assertTrue( not a.containsPoint( THREE.Vector3( 1.1, 1.1, -100.1 ) ) ) # Passednot
        self.assertTrue( not a.containsPoint( THREE.Vector3( 0, 0, -101 ) ) ) # Passednot

    def test_setFromMatrix_makePerspective_containsPoint( self ):

        m = THREE.Matrix4().makePerspective( -1, 1, 1, -1, 1, 100 )
        a = THREE.Frustum().setFromMatrix( m )

        self.assertTrue( not a.containsPoint( THREE.Vector3( 0, 0, 0 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( 0, 0, -50 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( 0, 0, -1.001 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( -1, -1, -1.001 ) ) ) # Passednot
        self.assertTrue( not a.containsPoint( THREE.Vector3( -1.1, -1.1, -1.001 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( 1, 1, -1.001 ) ) ) # Passednot
        self.assertTrue( not a.containsPoint( THREE.Vector3( 1.1, 1.1, -1.001 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( 0, 0, -99.999 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( -99.999, -99.999, -99.999 ) ) ) # Passednot
        self.assertTrue( not a.containsPoint( THREE.Vector3( -100.1, -100.1, -100.1 ) ) ) # Passednot
        self.assertTrue( a.containsPoint( THREE.Vector3( 99.999, 99.999, -99.999 ) ) ) # Passednot
        self.assertTrue( not a.containsPoint( THREE.Vector3( 100.1, 100.1, -100.1 ) ) ) # Passednot
        self.assertTrue( not a.containsPoint( THREE.Vector3( 0, 0, -101 ) ) ) # Passednot

    def test_setFromMatrix_makePerspective_intersectsSphere( self ):

        m = THREE.Matrix4().makePerspective( -1, 1, 1, -1, 1, 100 )
        a = THREE.Frustum().setFromMatrix( m )

        self.assertTrue( not a.intersectsSphere( THREE.Sphere( THREE.Vector3( 0, 0, 0 ), 0 ) ) ) # Passednot
        self.assertTrue( not a.intersectsSphere( THREE.Sphere( THREE.Vector3( 0, 0, 0 ), 0.9 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( 0, 0, 0 ), 1.1 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( 0, 0, -50 ), 0 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( 0, 0, -1.001 ), 0 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( -1, -1, -1.001 ), 0 ) ) ) # Passednot
        self.assertTrue( not a.intersectsSphere( THREE.Sphere( THREE.Vector3( -1.1, -1.1, -1.001 ), 0 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( -1.1, -1.1, -1.001 ), 0.5 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( 1, 1, -1.001 ), 0 ) ) ) # Passednot
        self.assertTrue( not a.intersectsSphere( THREE.Sphere( THREE.Vector3( 1.1, 1.1, -1.001 ), 0 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( 1.1, 1.1, -1.001 ), 0.5 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( 0, 0, -99.999 ), 0 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( -99.999, -99.999, -99.999 ), 0 ) ) ) # Passednot
        self.assertTrue( not a.intersectsSphere( THREE.Sphere( THREE.Vector3( -100.1, -100.1, -100.1 ), 0 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( -100.1, -100.1, -100.1 ), 0.5 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( 99.999, 99.999, -99.999 ), 0 ) ) ) # Passednot
        self.assertTrue( not a.intersectsSphere( THREE.Sphere( THREE.Vector3( 100.1, 100.1, -100.1 ), 0 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( 100.1, 100.1, -100.1 ), 0.2 ) ) ) # Passednot
        self.assertTrue( not a.intersectsSphere( THREE.Sphere( THREE.Vector3( 0, 0, -101 ), 0 ) ) ) # Passednot
        self.assertTrue( a.intersectsSphere( THREE.Sphere( THREE.Vector3( 0, 0, -101 ), 1.1 ) ) ) # Passednot

    def test_clone( self ):

        p0 = THREE.Plane( unit3, -1 )
        p1 = THREE.Plane( unit3, 1 )
        p2 = THREE.Plane( unit3, 2 )
        p3 = THREE.Plane( unit3, 3 )
        p4 = THREE.Plane( unit3, 4 )
        p5 = THREE.Plane( unit3, 5 )

        b = THREE.Frustum( p0, p1, p2, p3, p4, p5 )
        a = b.clone()
        self.assertTrue( a.planes[0].equals( p0 ) ) # Passednot
        self.assertTrue( a.planes[1].equals( p1 ) ) # Passednot
        self.assertTrue( a.planes[2].equals( p2 ) ) # Passednot
        self.assertTrue( a.planes[3].equals( p3 ) ) # Passednot
        self.assertTrue( a.planes[4].equals( p4 ) ) # Passednot
        self.assertTrue( a.planes[5].equals( p5 ) ) # Passednot

        # ensure it is a True copy by modifying source
        a.planes[0].copy( p1 )
        self.assertTrue( b.planes[0].equals( p0 ) ) # Passednot
