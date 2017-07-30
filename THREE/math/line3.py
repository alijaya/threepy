from __future__ import division

import vector3
import _Math

"""
 * @author bhouston / http:#clara.io
 """

class Line3( object ):

    def __init__( self, start = None, end = None ):

        self.start = start or vector3.Vector3()
        self.end = end or vector3.Vector3()

    def set( self, start, end ):

        self.start.copy( start )
        self.end.copy( end )

        return self

    def clone( self ):

        return Line3().copy( self )

    def copy( self, line ):

        self.start.copy( line.start )
        self.end.copy( line.end )

        return self

    def getCenter( self, optionalTarget = None ):

        result = optionalTarget or vector3.Vector3()
        return result.addVectors( self.start, self.end ).multiplyScalar( 0.5 )

    def delta( self, optionalTarget = None ):

        result = optionalTarget or vector3.Vector3()
        return result.subVectors( self.end, self.start )

    def distanceSq( self ):

        return self.start.distanceToSquared( self.end )

    def distance( self ):

        return self.start.distanceTo( self.end )

    def at( self, t, optionalTarget = None ):

        result = optionalTarget or vector3.Vector3()

        return self.delta( result ).multiplyScalar( t ).add( self.start )

    def closestPointToPointParameter( self, point, clampToLine ):

        startP = vector3.Vector3()
        startEnd = vector3.Vector3()

        startP.subVectors( point, self.start )
        startEnd.subVectors( self.end, self.start )

        startEnd2 = startEnd.dot( startEnd )
        startEnd_startP = startEnd.dot( startP )

        t = startEnd_startP / startEnd2

        if clampToLine:

            t = _Math.clamp( t, 0, 1 )

        return t

    def closestPointToPoint( self, point, clampToLine, optionalTarget = None ):

        t = self.closestPointToPointParameter( point, clampToLine )

        result = optionalTarget or vector3.Vector3()

        return self.delta( result ).multiplyScalar( t ).add( self.start )

    def applyMatrix4( self, matrix ):

        self.start.applyMatrix4( matrix )
        self.end.applyMatrix4( matrix )

        return self

    def equals( self, line ):

        return line.start.equals( self.start ) and line.end.equals( self.end )
