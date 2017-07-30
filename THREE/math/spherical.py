from __future__ import division
import math

import _Math

"""
 * @author bhouston / http:#clara.io
 * @author WestLangley / http:#github.com/WestLangley
 *
 * Ref: https:#en.wikipedia.org/wiki/Spherical_coordinate_system
 *
 * The poles (phi) are at the positive and negative y axis.
 * The equator starts at positive z.
 """

class Spherical( object ):

    def __init__( self, radius = 1.0, phi = 0, theta = 0 ):

        self.radius = radius 
        self.phi = phi # up / down towards top and bottom pole
        self.theta = theta # around the equator of the sphere

    def set( self, radius, phi, theta ):

        self.radius = radius
        self.phi = phi
        self.theta = theta

        return self

    def clone( self ):

        return Spherical().copy( self )

    def copy( self, other ):

        self.radius = other.radius
        self.phi = other.phi
        self.theta = other.theta

        return self

    # restrict phi to be betwee EPS and PI-EPS
    def makeSafe( self ):

        EPS = 0.000001
        self.phi = max( EPS, min( math.pi - EPS, self.phi ) )

        return self

    def setFromVector3( self, vec3 ):

        self.radius = vec3.length()

        if self.radius == 0:

            self.theta = 0
            self.phi = 0

        else:

            self.theta = math.atan2( vec3.x, vec3.z ) # equator angle around y-up axis
            self.phi = math.acos( _Math.clamp( vec3.y / self.radius, - 1, 1 ) ) # polar angle

        return self
