from __future__ import division
import math

from ..core import geometry
from ..core import bufferGeometry
from ..core import bufferAttribute
from ..math import vector3
from ..utils import Expando

"""
 * @author oosmoxiecode
 * @author Mugen87 / https://github.com/Mugen87
 *
 * based on http://www.blackpawn.com/texts/pqtorus/
 """

# TorusKnotGeometry

class TorusKnotGeometry( geometry.Geometry ):

    def __init__( self, radius = 100, tube = 40, tubularSegments = 64, radialSegments = 8, p = 2, q = 3 ):

        super( TorusKnotGeometry, self ).__init__()

        self.type = "TorusKnotGeometry"

        self.parameters = Expando(
            radius = radius,
            tube = tube,
            tubularSegments = tubularSegments,
            radialSegments = radialSegments,
            p = p,
            q = q
        )

        self.fromBufferGeometry( TorusKnotBufferGeometry( radius, tube, tubularSegments, radialSegments, p, q ) )
        self.mergeVertices()

# TorusKnotBufferGeometry

class TorusKnotBufferGeometry( bufferGeometry.BufferGeometry ):

    def __init__( self, radius = 100, tube = 40, tubularSegments = 64, radialSegments = 8, p = 2, q = 3 ):

        super( TorusKnotBufferGeometry, self ).__init__()

        self.type = "TorusKnotBufferGeometry"

        self.parameters = Expando(
            radius = radius,
            tube = tube,
            tubularSegments = tubularSegments,
            radialSegments = radialSegments,
            p = p,
            q = q
        )

        # buffers

        indices = []
        vertices = []
        normals = []
        uvs = []

        # helper variables

        vertex = vector3.Vector3()
        normal = vector3.Vector3()

        P1 = vector3.Vector3()
        P2 = vector3.Vector3()

        B = vector3.Vector3()
        T = vector3.Vector3()
        N = vector3.Vector3()

        # this function calculates the current position on the torus curve

        def calculatePositionOnCurve( u, p, q, radius, position ):

            cu = math.cos( u )
            su = math.sin( u )
            quOverP = q / p * u
            cs = math.cos( quOverP )

            position.x = radius * ( 2 + cs ) * 0.5 * cu
            position.y = radius * ( 2 + cs ) * su * 0.5
            position.z = radius * math.sin( quOverP ) * 0.5

        # generate vertices, normals and uvs

        for i in xrange( tubularSegments + 1 ):

            # the radian "u" is used to calculate the position on the torus curve of the current tubular segement

            u = i / tubularSegments * p * math.pi * 2

            # now we calculate two points. P1 is our current position on the curve, P2 is a little farther ahead.
            # these points are used to create a special "coordinate space", which is necessary to calculate the correct vertex positions

            calculatePositionOnCurve( u, p, q, radius, P1 )
            calculatePositionOnCurve( u + 0.01, p, q, radius, P2 )

            # calculate orthonormal basis

            T.subVectors( P2, P1 )
            N.addVectors( P2, P1 )
            B.crossVectors( T, N )
            N.crossVectors( B, T )

            # normalize B, N. T can be ignored, we don"t use it

            B.normalize()
            N.normalize()

            for j in xrange( radialSegments + 1 ):

                # now calculate the vertices. they are nothing more than an extrusion of the torus curve.
                # because we extrude a shape in the xy-plane, there is no need to calculate a z-value.

                v = j / radialSegments * math.pi * 2
                cx = - tube * math.cos( v )
                cy = tube * math.sin( v )

                # now calculate the final vertex position.
                # first we orient the extrusion with our basis vectos, then we add it to the current position on the curve

                vertex.x = P1.x + ( cx * N.x + cy * B.x )
                vertex.y = P1.y + ( cx * N.y + cy * B.y )
                vertex.z = P1.z + ( cx * N.z + cy * B.z )

                vertices.extend( [ vertex.x, vertex.y, vertex.z ] )

                # normal (P1 is always the center/origin of the extrusion, thus we can use it to calculate the normal)

                normal.subVectors( vertex, P1 ).normalize()

                normals.extend( [ normal.x, normal.y, normal.z ] )

                # uv

                uvs.append( i / tubularSegments )
                uvs.append( j / radialSegments )

        # generate indices
        for j in xrange( 1, tubularSegments + 1 ):

            for i in xrange( 1, radialSegments + 1 ):

                # indices

                a = ( radialSegments + 1 ) * ( j - 1 ) + ( i - 1 )
                b = ( radialSegments + 1 ) * j + ( i - 1 )
                c = ( radialSegments + 1 ) * j + i
                d = ( radialSegments + 1 ) * ( j - 1 ) + i

                # faces

                indices.extend( [ a, b, d ] )
                indices.extend( [ b, c, d ] )

        # build geometry

        self.setIndex( indices )
        self.addAttribute( "position", bufferAttribute.Float32BufferAttribute( vertices, 3 ) )
        self.addAttribute( "normal", bufferAttribute.Float32BufferAttribute( normals, 3 ) )
        self.addAttribute( "uv", bufferAttribute.Float32BufferAttribute( uvs, 2 ) )
