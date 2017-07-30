from __future__ import division
import math

"""
 * @author Mugen87 / https:#github.com/Mugen87
 *
 * Ref: https:#en.wikipedia.org/wiki/Cylindrical_coordinate_system
 *
 """

class Cylindrical( object ):

    def __init__( self, radius = 1.0, theta = 0, y = 0 ):

        self.radius = radius # distance from the origin to a point in the x-z plane
        self.theta = theta # counterclockwise angle in the x-z plane measured in radians from the positive z-axis
        self.y = y # height above the x-z plane

    def set( self, radius, theta, y ):

        self.radius = radius
        self.theta = theta
        self.y = y

        return self

    def clone( self ):

        return Cylindrical().copy( self )

    def copy( self, other ):

        self.radius = other.radius
        self.theta = other.theta
        self.y = other.y

        return self

    def setFromVector3( self, vec3 ):

        self.radius = math.sqrt( vec3.x * vec3.x + vec3.z * vec3.z )
        self.theta = math.atan2( vec3.x, vec3.z )
        self.y = vec3.y

        return self
