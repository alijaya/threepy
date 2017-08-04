from __future__ import division

import vector3
import sphere

"""
 * @author bhouston / http:#clara.io
 * @author WestLangley / http:#github.com/WestLangley
 """

class Box3( object ):

    def __init__( self, min = None, max = None ):

        self.min = min or vector3.Vector3( + float( "inf" ), + float( "inf" ), + float( "inf" ) )
        self.max = max or vector3.Vector3( - float( "inf" ), - float( "inf" ), - float( "inf" ) )

        isBox3 = True

    def set( self, min, max ):

        self.min.copy( min )
        self.max.copy( max )

        return self

    def setFromArray( self, array ):

        minX = + float( "inf" )
        minY = + float( "inf" )
        minZ = + float( "inf" )

        maxX = - float( "inf" )
        maxY = - float( "inf" )
        maxZ = - float( "inf" )

        for i in xrange( 0, len( array ), 3 ):

            x = array[ i ]
            y = array[ i + 1 ]
            z = array[ i + 2 ]

            if x < minX: minX = x
            if y < minY: minY = y
            if z < minZ: minZ = z

            if x > maxX: maxX = x
            if y > maxY: maxY = y
            if z > maxZ: maxZ = z

        self.min.set( minX, minY, minZ )
        self.max.set( maxX, maxY, maxZ )

        return self

    def setFromBufferAttribute( self, attribute ):

        minX = + float( "inf" )
        minY = + float( "inf" )
        minZ = + float( "inf" )

        maxX = - float( "inf" )
        maxY = - float( "inf" )
        maxZ = - float( "inf" )

        for i in xrange( attribute.count ):

            x = attribute.getX( i )
            y = attribute.getY( i )
            z = attribute.getZ( i )

            if x < minX: minX = x
            if y < minY: minY = y
            if z < minZ: minZ = z

            if x > maxX: maxX = x
            if y > maxY: maxY = y
            if z > maxZ: maxZ = z

        self.min.set( minX, minY, minZ )
        self.max.set( maxX, maxY, maxZ )

        return self

    def setFromPoints( self, points ):

        self.makeEmpty()

        for i in xrange( len( points ) ):

            self.expandByPoint( points[ i ] )

        return self

    def setFromCenterAndSize( self, center, size ):

        v1 = vector3.Vector3()

        halfSize = v1.copy( size ).multiplyScalar( 0.5 )

        self.min.copy( center ).sub( halfSize )
        self.max.copy( center ).add( halfSize )

        return self

    def setFromObject( self, object ):

        self.makeEmpty()

        return self.expandByObject( object )

    def clone( self ):

        return Box3().copy( self )

    def copy( self, box ):

        self.min.copy( box.min )
        self.max.copy( box.max )

        return self

    def makeEmpty( self ):

        self.min.x = self.min.y = self.min.z = + float( "inf" )
        self.max.x = self.max.y = self.max.z = - float( "inf" )

        return self

    def isEmpty( self ):

        # self is a more robust check for empty than ( volume <= 0 ) because volume can get positive with two negative axes

        return ( self.max.x < self.min.x ) or ( self.max.y < self.min.y ) or ( self.max.z < self.min.z )

    def getCenter( self, optionalTarget = None ):

        result = optionalTarget or vector3.Vector3()
        return result.set( 0, 0, 0 ) if self.isEmpty() else result.addVectors( self.min, self.max ).multiplyScalar( 0.5 )

    def getSize( self, optionalTarget = None ):

        result = optionalTarget or vector3.Vector3()
        return result.set( 0, 0, 0 ) if self.isEmpty() else result.subVectors( self.max, self.min )

    def expandByPoint( self, point ):

        self.min.min( point )
        self.max.max( point )

        return self

    def expandByVector( self, vector ):

        self.min.sub( vector )
        self.max.add( vector )

        return self

    def expandByScalar( self, scalar ):

        self.min.addScalar( - scalar )
        self.max.addScalar( scalar )

        return self

    def expandByObject( self, object ):

        # Computes the world-axis-aligned bounding box of an object (including its children),
        # accounting for both the object"s, and children"s, world transforms

        v1 = vector3.Vector3()

        scope = self

        object.updateMatrixWorld( True )

        def traverseFunction( node ):

            geometry = node.geometry

            if geometry is not None:

                if hasattr( geometry, "isGeometry" ):

                    vertices = geometry.vertices

                    for i in xrange( len( vertices ) ):

                        v1.copy( vertices[ i ] )
                        v1.applyMatrix4( node.matrixWorld )

                        scope.expandByPoint( v1 )

                elif hasattr( geometry, "isBufferGeometry" ):

                    attribute = geometry.attributes.position

                    if attribute is not None:

                        for i in xrange( attribute.count ):

                            v1.fromBufferAttribute( attribute, i ).applyMatrix4( node.matrixWorld )

                            scope.expandByPoint( v1 )
        
        object.traverse( traverseFunction )

        return self

    def containsPoint( self, point ):

        return not ( point.x < self.min.x or point.x > self.max.x or \
                     point.y < self.min.y or point.y > self.max.y or \
                     point.z < self.min.z or point.z > self.max.z )

    def containsBox( self, box ):

        return  self.min.x <= box.min.x and box.max.x <= self.max.x and \
                self.min.y <= box.min.y and box.max.y <= self.max.y and \
                self.min.z <= box.min.z and box.max.z <= self.max.z

    def getParameter( self, point, optionalTarget = None ):

        # This can potentially have a divide by zero if the box
        # has a size dimension of 0.

        result = optionalTarget or vector3.Vector3()

        return result.set(
            ( point.x - self.min.x ) / ( self.max.x - self.min.x ),
            ( point.y - self.min.y ) / ( self.max.y - self.min.y ),
            ( point.z - self.min.z ) / ( self.max.z - self.min.z )
        )

    def intersectsBox( self, box ):

        # using 6 splitting planes to rule out intersections.
        return not ( box.max.x < self.min.x or box.min.x > self.max.x or \
                     box.max.y < self.min.y or box.min.y > self.max.y or \
                     box.max.z < self.min.z or box.min.z > self.max.z )

    def intersectsSphere( self, sphere ):

        closestPoint = vector3.Vector3()

        # Find the point on the AABB closest to the sphere center.
        self.clampPoint( sphere.center, closestPoint )

        # If that point is inside the sphere, the AABB and sphere intersect.
        return closestPoint.distanceToSquared( sphere.center ) <= ( sphere.radius * sphere.radius )

    def intersectsPlane( self, plane ):

        # We compute the minimum and maximum dot product values. If those values
        # are on the same side (back or front) of the plane, then there is no intersection.

        min = None
        max = None

        if plane.normal.x > 0:

            min = plane.normal.x * self.min.x
            max = plane.normal.x * self.max.x

        else:

            min = plane.normal.x * self.max.x
            max = plane.normal.x * self.min.x

        if plane.normal.y > 0:

            min += plane.normal.y * self.min.y
            max += plane.normal.y * self.max.y

        else:

            min += plane.normal.y * self.max.y
            max += plane.normal.y * self.min.y

        if plane.normal.z > 0:

            min += plane.normal.z * self.min.z
            max += plane.normal.z * self.max.z

        else:

            min += plane.normal.z * self.max.z
            max += plane.normal.z * self.min.z

        return ( min <= plane.constant and max >= plane.constant )

    def clampPoint( self, point, optionalTarget = None ):

        result = optionalTarget or vector3.Vector3()
        return result.copy( point ).clamp( self.min, self.max )

    def distanceToPoint( self, point ):

        v1 = vector3.Vector3()

        clampedPoint = v1.copy( point ).clamp( self.min, self.max )
        return clampedPoint.sub( point ).length()

    def getBoundingSphere( self, optionalTarget = None ):

        v1 = vector3.Vector3()

        result = optionalTarget or sphere.Sphere()

        self.getCenter( result.center )

        result.radius = self.getSize( v1 ).length() * 0.5

        return result

    def intersect( self, box ):

        self.min.max( box.min )
        self.max.min( box.max )

        # ensure that if there is no overlap, the result is fully empty, not slightly empty with non-inf/+inf values that will cause subsequence intersects to erroneously return valid values.
        if self.isEmpty(): self.makeEmpty()

        return self

    def union( self, box ):

        self.min.min( box.min )
        self.max.max( box.max )

        return self

    def applyMatrix4( self, matrix ):

        points = [
            vector3.Vector3(),
            vector3.Vector3(),
            vector3.Vector3(),
            vector3.Vector3(),
            vector3.Vector3(),
            vector3.Vector3(),
            vector3.Vector3(),
            vector3.Vector3()
        ]

        # transform of empty box is an empty box.
        if self.isEmpty(): return self

        # NOTE: I am using a binary pattern to specify all 2^3 combinations below
        points[ 0 ].set( self.min.x, self.min.y, self.min.z ).applyMatrix4( matrix ) # 000
        points[ 1 ].set( self.min.x, self.min.y, self.max.z ).applyMatrix4( matrix ) # 001
        points[ 2 ].set( self.min.x, self.max.y, self.min.z ).applyMatrix4( matrix ) # 010
        points[ 3 ].set( self.min.x, self.max.y, self.max.z ).applyMatrix4( matrix ) # 011
        points[ 4 ].set( self.max.x, self.min.y, self.min.z ).applyMatrix4( matrix ) # 100
        points[ 5 ].set( self.max.x, self.min.y, self.max.z ).applyMatrix4( matrix ) # 101
        points[ 6 ].set( self.max.x, self.max.y, self.min.z ).applyMatrix4( matrix ) # 110
        points[ 7 ].set( self.max.x, self.max.y, self.max.z ).applyMatrix4( matrix )    # 111

        self.setFromPoints( points )

        return self

    def translate( self, offset ):

        self.min.add( offset )
        self.max.add( offset )

        return self

    def equals( self, box ):

        return box.min.equals( self.min ) and box.max.equals( self.max )
