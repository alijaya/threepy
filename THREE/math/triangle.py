from __future__ import division
import math

import vector3
import line3
import plane

"""
 * @author bhouston / http:#clara.io
 * @author mrdoob / http:#mrdoob.com/
 """

class Triangle( object ):

    def __init__( self, a = None, b = None, c = None ):

        self.a = a or vector3.Vector3()
        self.b = b or vector3.Vector3()
        self.c = c or vector3.Vector3()

    @staticmethod
    def s_normal( a, b, c, optionalTarget = None ):

        v0 = vector3.Vector3()

        result = optionalTarget or vector3.Vector3()

        result.subVectors( c, b )
        v0.subVectors( a, b )
        result.cross( v0 )

        resultLengthSq = result.lengthSq()
        if resultLengthSq > 0:

            return result.multiplyScalar( 1 / math.sqrt( resultLengthSq ) )

        return result.set( 0, 0, 0 )

    # static/instance method to calculate barycentric coordinates
    # based on: http:#www.blackpawn.com/texts/pointinpoly/default.html
    @staticmethod
    def s_barycoordFromPoint( point, a, b, c, optionalTarget = None ):

        v0 = vector3.Vector3()
        v1 = vector3.Vector3()
        v2 = vector3.Vector3()

        v0.subVectors( c, a )
        v1.subVectors( b, a )
        v2.subVectors( point, a )

        dot00 = v0.dot( v0 )
        dot01 = v0.dot( v1 )
        dot02 = v0.dot( v2 )
        dot11 = v1.dot( v1 )
        dot12 = v1.dot( v2 )

        denom = ( dot00 * dot11 - dot01 * dot01 )

        result = optionalTarget or vector3.Vector3()

        # collinear or singular triangle
        if denom == 0:

            # arbitrary location outside of triangle?
            # not sure if self is the best idea, maybe should be returning None
            return result.set( - 2, - 1, - 1 )

        invDenom = 1 / denom
        u = ( dot11 * dot02 - dot01 * dot12 ) * invDenom
        v = ( dot00 * dot12 - dot01 * dot02 ) * invDenom

        # barycentric coordinates must always sum to 1
        return result.set( 1 - u - v, v, u )

    @staticmethod
    def s_containsPoint( point, a, b, c ):

        v1 = vector3.Vector3()

        result = Triangle.s_barycoordFromPoint( point, a, b, c, v1 )

        return ( result.x >= 0 ) and ( result.y >= 0 ) and ( ( result.x + result.y ) <= 1 )

    def set( self, a, b, c ):

        self.a.copy( a )
        self.b.copy( b )
        self.c.copy( c )

        return self

    def setFromPointsAndIndices( self, points, i0, i1, i2 ):

        self.a.copy( points[ i0 ] )
        self.b.copy( points[ i1 ] )
        self.c.copy( points[ i2 ] )

        return self

    def clone( self ):

        return Triangle().copy( self )

    def copy( self, triangle ):

        self.a.copy( triangle.a )
        self.b.copy( triangle.b )
        self.c.copy( triangle.c )

        return self

    def area( self ):

        v0 = vector3.Vector3()
        v1 = vector3.Vector3()

        v0.subVectors( self.c, self.b )
        v1.subVectors( self.a, self.b )

        return v0.cross( v1 ).length() * 0.5

    def midpoint( self, optionalTarget = None ):

        result = optionalTarget or vector3.Vector3()
        return result.addVectors( self.a, self.b ).add( self.c ).multiplyScalar( 1 / 3 )

    def normal( self, optionalTarget = None ):

        return Triangle.s_normal( self.a, self.b, self.c, optionalTarget )

    def plane( self, optionalTarget = None ):

        result = optionalTarget or plane.Plane()

        return result.setFromCoplanarPoints( self.a, self.b, self.c )

    def barycoordFromPoint( self, point, optionalTarget = None ):

        return Triangle.s_barycoordFromPoint( point, self.a, self.b, self.c, optionalTarget )

    def containsPoint( self, point ):

        return Triangle.s_containsPoint( point, self.a, self.b, self.c )

    def closestPointToPoint( self, point, optionalTarget = None ):

        p = plane.Plane()
        edgeList = [ line3.Line3(), line3.Line3(), line3.Line3() ]
        projectedPoint = vector3.Vector3()
        closestPoint = vector3.Vector3()

        result = optionalTarget or vector3.Vector3()
        minDistance = float( "inf" )

        # project the point onto the plane of the triangle

        p.setFromCoplanarPoints( self.a, self.b, self.c )
        p.projectPoint( point, projectedPoint )

        # check if the projection lies within the triangle

        if self.containsPoint( projectedPoint ) == True:

            # if so, self is the closest point

            result.copy( projectedPoint )

        else:

            # if not, the point falls outside the triangle. the result is the closest point to the triangle"s edges or vertices

            edgeList[ 0 ].set( self.a, self.b )
            edgeList[ 1 ].set( self.b, self.c )
            edgeList[ 2 ].set( self.c, self.a )

            for i in xrange( len( edgeList ) ):

                edgeList[ i ].closestPointToPoint( projectedPoint, True, closestPoint )

                distance = projectedPoint.distanceToSquared( closestPoint )

                if distance < minDistance:

                    minDistance = distance

                    result.copy( closestPoint )

        return result

    def equals( self, triangle ):

        return triangle.a.equals( self.a ) and triangle.b.equals( self.b ) and triangle.c.equals( self.c )
