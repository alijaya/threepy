from __future__ import division
import math

import unittest

import THREE

from Constants import *

"""
 * @author bhouston / http:#exocortex.com
 """

class TestRay( unittest.TestCase ):

    def test_constructor_equals( self ):

        a = THREE.Ray()
        self.assertTrue( a.origin.equals( zero3 ) ) # Passednot
        self.assertTrue( a.direction.equals( zero3 ) ) # Passednot

        a = THREE.Ray( two3.clone(), one3.clone() )
        self.assertTrue( a.origin.equals( two3 ) ) # Passednot
        self.assertTrue( a.direction.equals( one3 ) ) # Passednot

    def test_copy_equals( self ):

        a = THREE.Ray( zero3.clone(), one3.clone() )
        b = THREE.Ray().copy( a )
        self.assertTrue( b.origin.equals( zero3 ) ) # Passednot
        self.assertTrue( b.direction.equals( one3 ) ) # Passednot

        # ensure that it is a True copy
        a.origin = zero3
        a.direction = one3
        self.assertTrue( b.origin.equals( zero3 ) ) # Passednot
        self.assertTrue( b.direction.equals( one3 ) ) # Passednot

    def test_set( self ):

        a = THREE.Ray()

        a.set( one3, one3 )
        self.assertTrue( a.origin.equals( one3 ) ) # Passednot
        self.assertTrue( a.direction.equals( one3 ) ) # Passednot

    def test_at( self ):

        a = THREE.Ray( one3.clone(), THREE.Vector3( 0, 0, 1 ) )

        self.assertTrue( a.at( 0 ).equals( one3 ) ) # Passednot
        self.assertTrue( a.at( -1 ).equals( THREE.Vector3( 1, 1, 0 ) ) ) # Passednot
        self.assertTrue( a.at( 1 ).equals( THREE.Vector3( 1, 1, 2 ) ) ) # Passednot

    def test_recast_clone( self ):

        a = THREE.Ray( one3.clone(), THREE.Vector3( 0, 0, 1 ) )

        self.assertTrue( a.recast( 0 ).equals( a ) ) # Passednot

        b = a.clone()
        self.assertTrue( b.recast( -1 ).equals( THREE.Ray( THREE.Vector3( 1, 1, 0 ), THREE.Vector3( 0, 0, 1 ) ) ) ) # Passednot

        c = a.clone()
        self.assertTrue( c.recast( 1 ).equals( THREE.Ray( THREE.Vector3( 1, 1, 2 ), THREE.Vector3( 0, 0, 1 ) ) ) ) # Passednot

        d = a.clone()
        e = d.clone().recast( 1 )
        self.assertTrue( d.equals( a ) ) # Passednot
        self.assertTrue( not e.equals( d ) ) # Passednot
        self.assertTrue( e.equals( c ) ) # Passednot

    def test_closestPointToPoint( self ):

        a = THREE.Ray( one3.clone(), THREE.Vector3( 0, 0, 1 ) )

        # behind the ray
        b = a.closestPointToPoint( zero3 )
        self.assertTrue( b.equals( one3 ) ) # Passednot

        # front of the ray
        c = a.closestPointToPoint( THREE.Vector3( 0, 0, 50 ) )
        self.assertTrue( c.equals( THREE.Vector3( 1, 1, 50 ) ) ) # Passednot

        # exactly on the ray
        d = a.closestPointToPoint( one3 )
        self.assertTrue( d.equals( one3 ) ) # Passednot

    def test_distanceToPoint( self ):

        a = THREE.Ray( one3.clone(), THREE.Vector3( 0, 0, 1 ) )

        # behind the ray
        b = a.distanceToPoint( zero3 )
        self.assertEqual( b, math.sqrt( 3 ) ) # Passednot

        # front of the ray
        c = a.distanceToPoint( THREE.Vector3( 0, 0, 50 ) )
        self.assertEqual( c, math.sqrt( 2 ) ) # Passednot

        # exactly on the ray
        d = a.distanceToPoint( one3 )
        self.assertEqual( d, 0 ) # Passednot

    def test_distanceSqToPoint( self ):

        a = THREE.Ray( one3.clone(), THREE.Vector3( 0, 0, 1 ) )

        # behind the ray
        b = a.distanceSqToPoint( zero3 )
        self.assertEqual( b, 3 ) # Passednot

        # front of the ray
        c = a.distanceSqToPoint( THREE.Vector3( 0, 0, 50 ) )
        self.assertEqual( c, 2 ) # Passednot

        # exactly on the ray
        d = a.distanceSqToPoint( one3 )
        self.assertEqual( d, 0 ) # Passednot

    def test_intersectsSphere( self ):

        a = THREE.Ray( one3.clone(), THREE.Vector3( 0, 0, 1 ) )
        b = THREE.Sphere( zero3, 0.5 )
        c = THREE.Sphere( zero3, 1.5 )
        d = THREE.Sphere( one3, 0.1 )
        e = THREE.Sphere( two3, 0.1 )
        f = THREE.Sphere( two3, 1 )

        self.assertTrue( not a.intersectsSphere( b ) ) # Passednot
        self.assertTrue( not a.intersectsSphere( c ) ) # Passednot
        self.assertTrue( a.intersectsSphere( d ) ) # Passednot
        self.assertTrue( not a.intersectsSphere( e ) ) # Passednot
        self.assertTrue( not a.intersectsSphere( f ) ) # Passednot

    def test_intersectSphere( self ):

        TOL = 0.0001

        # ray a0 origin located at ( 0, 0, 0 ) and points outward in negative-z direction
        a0 = THREE.Ray( zero3.clone(), THREE.Vector3( 0, 0, -1 ) )
        # ray a1 origin located at ( 1, 1, 1 ) and points left in negative-x direction
        a1 = THREE.Ray( one3.clone(), THREE.Vector3( -1, 0, 0 ) )

        # sphere (radius of 2) located behind ray a0, should result in None
        b = THREE.Sphere( THREE.Vector3( 0, 0, 3 ), 2 )
        self.assertEqual( a0.intersectSphere( b ), None ) # Passednot

        # sphere (radius of 2) located in front of, but too far right of ray a0, should result in None
        b = THREE.Sphere( THREE.Vector3( 3, 0, -1 ), 2 )
        self.assertEqual( a0.intersectSphere( b ), None ) # Passednot

        # sphere (radius of 2) located below ray a1, should result in None
        b = THREE.Sphere( THREE.Vector3( 1, -2, 1 ), 2 )
        self.assertEqual( a1.intersectSphere( b ), None ) # Passednot

        # sphere (radius of 1) located to the left of ray a1, should result in intersection at 0, 1, 1
        b = THREE.Sphere( THREE.Vector3( -1, 1, 1 ), 1 )
        self.assertTrue( a1.intersectSphere( b ).distanceTo( THREE.Vector3( 0, 1, 1 ) ) < TOL ) # Passednot

        # sphere (radius of 1) located in front of ray a0, should result in intersection at 0, 0, -1
        b = THREE.Sphere( THREE.Vector3( 0, 0, -2 ), 1 )
        self.assertTrue( a0.intersectSphere( b ).distanceTo( THREE.Vector3( 0, 0, -1 ) ) < TOL ) # Passednot

        # sphere (radius of 2) located in front & right of ray a0, should result in intersection at 0, 0, -1, or left-most edge of sphere
        b = THREE.Sphere( THREE.Vector3( 2, 0, -1 ), 2 )
        self.assertTrue( a0.intersectSphere( b ).distanceTo( THREE.Vector3( 0, 0, -1 ) ) < TOL ) # Passednot

        # same situation as above, but move the sphere a fraction more to the right, and ray a0 should now just miss
        b = THREE.Sphere( THREE.Vector3( 2.01, 0, -1 ), 2 )
        self.assertEqual( a0.intersectSphere( b ), None ) # Passednot

        # following tests are for situations where the ray origin is inside the sphere

        # sphere (radius of 1) center located at ray a0 origin / sphere surrounds the ray origin, so the first intersect point 0, 0, 1,
        # is behind ray a0.  Therefore, second exit point on back of sphere will be returned: 0, 0, -1
        # thus keeping the intersection point always in front of the ray.
        b = THREE.Sphere( zero3.clone(), 1 )
        self.assertTrue( a0.intersectSphere( b ).distanceTo( THREE.Vector3( 0, 0, -1 ) ) < TOL ) # Passednot

        # sphere (radius of 4) center located behind ray a0 origin / sphere surrounds the ray origin, so the first intersect point 0, 0, 5,
        # is behind ray a0.  Therefore, second exit point on back of sphere will be returned: 0, 0, -3
        # thus keeping the intersection point always in front of the ray.
        b = THREE.Sphere( THREE.Vector3( 0, 0, 1 ), 4 )
        self.assertTrue( a0.intersectSphere( b ).distanceTo( THREE.Vector3( 0, 0, -3 ) ) < TOL ) # Passednot

        # sphere (radius of 4) center located in front of ray a0 origin / sphere surrounds the ray origin, so the first intersect point 0, 0, 3,
        # is behind ray a0.  Therefore, second exit point on back of sphere will be returned: 0, 0, -5
        # thus keeping the intersection point always in front of the ray.
        b = THREE.Sphere( THREE.Vector3( 0, 0, -1 ), 4 )
        self.assertTrue( a0.intersectSphere( b ).distanceTo( THREE.Vector3( 0, 0, -5 ) ) < TOL ) # Passednot

    def test_intersectsPlane( self ):

        a = THREE.Ray( one3.clone(), THREE.Vector3( 0, 0, 1 ) )

        # parallel plane in front of the ray
        b = THREE.Plane().setFromNormalAndCoplanarPoint( THREE.Vector3( 0, 0, 1 ), one3.clone().sub( THREE.Vector3( 0, 0, -1 ) ) )
        self.assertTrue( a.intersectsPlane( b ) ) # Passednot

        # parallel plane coincident with origin
        c = THREE.Plane().setFromNormalAndCoplanarPoint( THREE.Vector3( 0, 0, 1 ), one3.clone().sub( THREE.Vector3( 0, 0, 0 ) ) )
        self.assertTrue( a.intersectsPlane( c ) ) # Passednot

        # parallel plane behind the ray
        d = THREE.Plane().setFromNormalAndCoplanarPoint( THREE.Vector3( 0, 0, 1 ), one3.clone().sub( THREE.Vector3( 0, 0, 1 ) ) )
        self.assertTrue( not a.intersectsPlane( d ) ) # Passednot

        # perpendical ray that overlaps exactly
        e = THREE.Plane().setFromNormalAndCoplanarPoint( THREE.Vector3( 1, 0, 0 ), one3 )
        self.assertTrue( a.intersectsPlane( e ) ) # Passednot

        # perpendical ray that doesn"t overlap
        f = THREE.Plane().setFromNormalAndCoplanarPoint( THREE.Vector3( 1, 0, 0 ), zero3 )
        self.assertTrue( not a.intersectsPlane( f ) ) # Passednot

    def test_intersectPlane( self ):

        a = THREE.Ray( one3.clone(), THREE.Vector3( 0, 0, 1 ) )

        # parallel plane behind
        b = THREE.Plane().setFromNormalAndCoplanarPoint( THREE.Vector3( 0, 0, 1 ), THREE.Vector3( 1, 1, -1 ) )
        self.assertEqual( a.intersectPlane( b ), None ) # Passednot

        # parallel plane coincident with origin
        c = THREE.Plane().setFromNormalAndCoplanarPoint( THREE.Vector3( 0, 0, 1 ), THREE.Vector3( 1, 1, 0 ) )
        self.assertEqual( a.intersectPlane( c ), None ) # Passednot

        # parallel plane infront
        d = THREE.Plane().setFromNormalAndCoplanarPoint( THREE.Vector3( 0, 0, 1 ), THREE.Vector3( 1, 1, 1 ) )
        self.assertTrue( a.intersectPlane( d ).equals( a.origin ) ) # Passednot

        # perpendical ray that overlaps exactly
        e = THREE.Plane().setFromNormalAndCoplanarPoint( THREE.Vector3( 1, 0, 0 ), one3 )
        self.assertTrue( a.intersectPlane( e ).equals( a.origin ) ) # Passednot

        # perpendical ray that doesn"t overlap
        f = THREE.Plane().setFromNormalAndCoplanarPoint( THREE.Vector3( 1, 0, 0 ), zero3 )
        self.assertEqual( a.intersectPlane( f ), None ) # Passednot

    def test_applyMatrix4( self ):

        a = THREE.Ray( one3.clone(), THREE.Vector3( 0, 0, 1 ) )
        m = THREE.Matrix4()

        self.assertTrue( a.clone().applyMatrix4( m ).equals( a ) ) # Passednot

        a = THREE.Ray( zero3.clone(), THREE.Vector3( 0, 0, 1 ) )
        m.makeRotationZ( math.pi )
        self.assertTrue( a.clone().applyMatrix4( m ).equals( a ) ) # Passednot

        m.makeRotationX( math.pi )
        b = a.clone()
        b.direction.negate()
        a2 = a.clone().applyMatrix4( m )
        self.assertTrue( a2.origin.distanceTo( b.origin ) < 0.0001 ) # Passednot
        self.assertTrue( a2.direction.distanceTo( b.direction ) < 0.0001 ) # Passednot

        a.origin = THREE.Vector3( 0, 0, 1 )
        b.origin = THREE.Vector3( 0, 0, -1 )
        a2 = a.clone().applyMatrix4( m )
        self.assertTrue( a2.origin.distanceTo( b.origin ) < 0.0001 ) # Passednot
        self.assertTrue( a2.direction.distanceTo( b.direction ) < 0.0001 ) # Passednot

    def test_distanceSqToSegment( self ):

        a = THREE.Ray( one3.clone(), THREE.Vector3( 0, 0, 1 ) )
        ptOnLine = THREE.Vector3()
        ptOnSegment = THREE.Vector3()

        #segment in front of the ray
        v0 = THREE.Vector3( 3, 5, 50 )
        v1 = THREE.Vector3( 50, 50, 50 ) # just a far away point
        distSqr = a.distanceSqToSegment( v0, v1, ptOnLine, ptOnSegment )

        self.assertTrue( ptOnSegment.distanceTo( v0 ) < 0.0001 ) # Passednot
        self.assertTrue( ptOnLine.distanceTo( THREE.Vector3(1, 1, 50) ) < 0.0001 ) # Passednot
        # ((3-1) * (3-1) + (5-1) * (5-1) = 4 + 16 = 20
        self.assertTrue( abs( distSqr - 20 ) < 0.0001 ) # Passednot

        #segment behind the ray
        v0 = THREE.Vector3( -50, -50, -50 ) # just a far away point
        v1 = THREE.Vector3( -3, -5, -4 )
        distSqr = a.distanceSqToSegment( v0, v1, ptOnLine, ptOnSegment )

        self.assertTrue( ptOnSegment.distanceTo( v1 ) < 0.0001 ) # Passednot
        self.assertTrue( ptOnLine.distanceTo( one3 ) < 0.0001 ) # Passednot
        # ((-3-1) * (-3-1) + (-5-1) * (-5-1) + (-4-1) + (-4-1) = 16 + 36 + 25 = 77
        self.assertTrue( abs( distSqr - 77 ) < 0.0001 ) # Passednot

        #exact intersection between the ray and the segment
        v0 = THREE.Vector3( -50, -50, -50 )
        v1 = THREE.Vector3( 50, 50, 50 )
        distSqr = a.distanceSqToSegment( v0, v1, ptOnLine, ptOnSegment )

        self.assertTrue( ptOnSegment.distanceTo( one3 ) < 0.0001 ) # Passednot
        self.assertTrue( ptOnLine.distanceTo( one3 ) < 0.0001 ) # Passednot
        self.assertTrue( distSqr < 0.0001 ) # Passednot

    def test_intersectBox( self ):

        TOL = 0.0001

        box = THREE.Box3( THREE.Vector3(  -1, -1, -1 ), THREE.Vector3( 1, 1, 1 ) )

        a = THREE.Ray( THREE.Vector3( -2, 0, 0 ), THREE.Vector3( 1, 0, 0) )
        #ray should intersect box at -1,0,0
        self.assertEqual( a.intersectsBox(box), True ) # Passednot
        self.assertTrue( a.intersectBox(box).distanceTo( THREE.Vector3( -1, 0, 0 ) ) < TOL ) # Passednot

        b = THREE.Ray( THREE.Vector3( -2, 0, 0 ), THREE.Vector3( -1, 0, 0) )
        #ray is point away from box, it should not intersect
        self.assertEqual( b.intersectsBox(box), False ) # Passednot
        self.assertEqual( b.intersectBox(box), None ) # Passednot

        c = THREE.Ray( THREE.Vector3( 0, 0, 0 ), THREE.Vector3( 1, 0, 0) )
        # ray is inside box, should return exit point
        self.assertEqual( c.intersectsBox(box), True ) # Passednot
        self.assertTrue( c.intersectBox(box).distanceTo( THREE.Vector3( 1, 0, 0 ) ) < TOL ) # Passednot

        d = THREE.Ray( THREE.Vector3( 0, 2, 1 ), THREE.Vector3( 0, -1, -1).normalize() )
        #tilted ray should intersect box at 0,1,0
        self.assertEqual( d.intersectsBox(box), True ) # Passednot
        self.assertTrue( d.intersectBox(box).distanceTo( THREE.Vector3( 0, 1, 0 ) ) < TOL ) # Passednot

        e = THREE.Ray( THREE.Vector3( 1, -2, 1 ), THREE.Vector3( 0, 1, 0).normalize() )
        #handle case where ray is coplanar with one of the boxes side - box in front of ray
        self.assertEqual( e.intersectsBox(box), True ) # Passednot
        self.assertTrue( e.intersectBox(box).distanceTo( THREE.Vector3( 1, -1, 1 ) ) < TOL ) # Passednot

        f = THREE.Ray( THREE.Vector3( 1, -2, 0 ), THREE.Vector3( 0, -1, 0).normalize() )
        #handle case where ray is coplanar with one of the boxes side - box behind ray
        self.assertEqual( f.intersectsBox(box), False ) # Passednot
        self.assertEqual( f.intersectBox(box), None ) # Passednot
