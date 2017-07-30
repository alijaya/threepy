from __future__ import division

import matrix3
import vector3

"""
 * @author bhouston / http:#clara.io
 """

class Plane( object ):

    def __init__( self, normal = None, constant = 0 ):

        # normal is assumed to be normalized

        self.normal = normal or vector3.Vector3( 1, 0, 0 )
        self.constant = constant

    def set( self, normal, constant ):

        self.normal.copy( normal )
        self.constant = constant

        return self

    def setComponents( self, x, y, z, w ):

        self.normal.set( x, y, z )
        self.constant = w

        return self

    def setFromNormalAndCoplanarPoint( self, normal, point ):

        self.normal.copy( normal )
        self.constant = - point.dot( self.normal )

        return self

    def setFromCoplanarPoints( self, a, b, c ):

        v1 = vector3.Vector3()
        v2 = vector3.Vector3()

        normal = v1.subVectors( c, b ).cross( v2.subVectors( a, b ) ).normalize()

        # Q: should an error be thrown if normal is zero (e.g. degenerate plane)?

        self.setFromNormalAndCoplanarPoint( normal, a )

        return self

    def clone( self ):

        return Plane().copy( self )

    def copy( self, plane ):

        self.normal.copy( plane.normal )
        self.constant = plane.constant

        return self

    def normalize( self ):

        # Note: will lead to a divide by zero if the plane is invalid.

        inverseNormalLength = 1.0 / self.normal.length()
        self.normal.multiplyScalar( inverseNormalLength )
        self.constant *= inverseNormalLength

        return self

    def negate( self ):

        self.constant *= - 1
        self.normal.negate()

        return self

    def distanceToPoint( self, point ):

        return self.normal.dot( point ) + self.constant

    def distanceToSphere( self, sphere ):

        return self.distanceToPoint( sphere.center ) - sphere.radius

    def projectPoint( self, point, optionalTarget = None ):

        result = optionalTarget or vector3.Vector3()

        return result.copy( self.normal ).multiplyScalar( - self.distanceToPoint( point ) ).add( point )

    def intersectLine( self, line, optionalTarget = None ):

        v1 = vector3.Vector3()

        result = optionalTarget or vector3.Vector3()

        direction = line.delta( v1 )

        denominator = self.normal.dot( direction )

        if denominator == 0:

            # line is coplanar, return origin
            if self.distanceToPoint( line.start == 0 ):

                return result.copy( line.start )

            # Unsure if self is the correct method to handle self case.
            return None

        t = - ( line.start.dot( self.normal ) + self.constant ) / denominator

        if t < 0 or t > 1:

            return None

        return result.copy( direction ).multiplyScalar( t ).add( line.start )

    def intersectsLine( self, line ):

        # Note: self tests if a line intersects the plane, not whether it (or its end-points) are coplanar with it.

        startSign = self.distanceToPoint( line.start )
        endSign = self.distanceToPoint( line.end )

        return ( startSign < 0 and endSign > 0 ) or ( endSign < 0 and startSign > 0 )

    def intersectsBox( self, box ):

        return box.intersectsPlane( self )

    def intersectsSphere( self, sphere ):

        return sphere.intersectsPlane( self )

    def coplanarPoint( self, optionalTarget = None ):

        result = optionalTarget or vector3.Vector3()

        return result.copy( self.normal ).multiplyScalar( - self.constant )

    def applyMatrix4( self, matrix, optionalNormalMatrix = None ):

        v1 = vector3.Vector3()
        m1 = matrix3.Matrix3()

        normalMatrix = optionalNormalMatrix or m1.getNormalMatrix( matrix )

        referencePoint = self.coplanarPoint( v1 ).applyMatrix4( matrix )

        normal = self.normal.applyMatrix3( normalMatrix ).normalize()

        self.constant = - referencePoint.dot( normal )

        return self

    def translate( self, offset ):

        self.constant -= offset.dot( self.normal )

        return self

    def equals( self, plane ):

        return plane.normal.equals( self.normal ) and ( plane.constant == self.constant )
