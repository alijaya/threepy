from __future__ import division

import vector2

"""
 * @author bhouston / http:#clara.io
 """

class Box2( object ):

    def __init__( self, min = None, max = None ):

        self.min = min or vector2.Vector2( + float( "inf" ), + float( "inf" ) )
        self.max = max or vector2.Vector2( - float( "inf" ), - float( "inf" ) )

    def set( self, min, max ):

        self.min.copy( min )
        self.max.copy( max )

        return self

    def setFromPoints( self, points ):

        self.makeEmpty()

        for i in xrange( len( points ) ):

            self.expandByPoint( points[ i ] )

        return self

    def setFromCenterAndSize( self, center, size ):

        v1 = vector2.Vector2()

        halfSize = v1.copy( size ).multiplyScalar( 0.5 )
        self.min.copy( center ).sub( halfSize )
        self.max.copy( center ).add( halfSize )

        return self

    def clone( self ):

        return Box2().copy( self )

    def copy( self, box ):

        self.min.copy( box.min )
        self.max.copy( box.max )

        return self

    def makeEmpty( self ):

        self.min.x = self.min.y = + float( "inf" )
        self.max.x = self.max.y = - float( "inf" )

        return self

    def isEmpty( self ):

        # self is a more robust check for empty than ( volume <= 0 ) because volume can get positive with two negative axes

        return ( self.max.x < self.min.x ) or ( self.max.y < self.min.y )

    def getCenter( self, optionalTarget = None ):

        result = optionalTarget or vector2.Vector2()
        return result.set( 0, 0 ) if self.isEmpty() else result.addVectors( self.min, self.max ).multiplyScalar( 0.5 )

    def getSize( self, optionalTarget = None ):

        result = optionalTarget or vector2.Vector2()
        return result.set( 0, 0 ) if self.isEmpty() else result.subVectors( self.max, self.min )

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

    def containsPoint( self, point ):

        return not ( point.x < self.min.x or point.x > self.max.x or \
                     point.y < self.min.y or point.y > self.max.y )

    def containsBox( self, box ):

        return  self.min.x <= box.min.x and box.max.x <= self.max.x and \
                self.min.y <= box.min.y and box.max.y <= self.max.y

    def getParameter( self, point, optionalTarget = None ):

        # This can potentially have a divide by zero if the box
        # has a size dimension of 0.

        result = optionalTarget or vector2.Vector2()

        return result.set(
            ( point.x - self.min.x ) / ( self.max.x - self.min.x ),
            ( point.y - self.min.y ) / ( self.max.y - self.min.y )
        )

    def intersectsBox( self, box ):

        # using 4 splitting planes to rule out intersections

        return not ( box.max.x < self.min.x or box.min.x > self.max.x or \
                     box.max.y < self.min.y or box.min.y > self.max.y )

    def clampPoint( self, point, optionalTarget = None ):

        result = optionalTarget or vector2.Vector2()
        return result.copy( point ).clamp( self.min, self.max )

    def distanceToPoint( self, point ):

        v1 = vector2.Vector2()

        clampedPoint = v1.copy( point ).clamp( self.min, self.max )
        return clampedPoint.sub( point ).length()

    def intersect( self, box ):

        self.min.max( box.min )
        self.max.min( box.max )

        return self

    def union( self, box ):

        self.min.min( box.min )
        self.max.max( box.max )

        return self

    def translate( self, offset ):

        self.min.add( offset )
        self.max.add( offset )

        return self

    def equals( self, box ):

        return box.min.equals( self.min ) and box.max.equals( self.max )
