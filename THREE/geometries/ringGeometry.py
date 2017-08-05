from __future__ import division
import math

from ..core import geometry
from ..core import bufferGeometry
from ..core import bufferAttribute
from ..math import vector2
from ..math import vector3
from ..utils import Expando

"""
 * @author Kaleb Murphy
 * @author Mugen87 / https://github.com/Mugen87
 """

# RingGeometry

class RingGeometry( geometry.Geometry ):

    def __init__( self, innerRadius = 20, outerRadius = 50, thetaSegments = 8, phiSegments = 1, thetaStart = 0, thetaLength = 2 * math.pi ):

        super( RingGeometry, self ).__init__()

        self.type = "RingGeometry"

        self.parameters = Expando(
            innerRadius = innerRadius,
            outerRadius = outerRadius,
            thetaSegments = thetaSegments,
            phiSegments = phiSegments,
            thetaStart = thetaStart,
            thetaLength = thetaLength
        )

        self.fromBufferGeometry( RingBufferGeometry( innerRadius, outerRadius, thetaSegments, phiSegments, thetaStart, thetaLength ) )
        self.mergeVertices()

# RingBufferGeometry

class RingBufferGeometry( bufferGeometry.BufferGeometry ):

    def __init__( self, innerRadius = 20, outerRadius = 50, thetaSegments = 8, phiSegments = 1, thetaStart = 0, thetaLength = 2 * math.pi ):

        super( RingBufferGeometry, self ).__init__()

        self.type = "RingBufferGeometry"

        self.parameters = Expando(
            innerRadius = innerRadius,
            outerRadius = outerRadius,
            thetaSegments = thetaSegments,
            phiSegments = phiSegments,
            thetaStart = thetaStart,
            thetaLength = thetaLength
        )

        thetaSegments = max( 3, thetaSegments )
        phiSegments = max( 1, phiSegments )

        # buffers

        indices = []
        vertices = []
        normals = []
        uvs = []

        # some helper variables

        radius = innerRadius
        radiusStep = ( ( outerRadius - innerRadius ) / phiSegments )
        vertex = vector3.Vector3()
        uv = vector2.Vector2()

        # generate vertices, normals and uvs

        for j in xrange( phiSegments + 1 ):

            for i in xrange( thetaSegments + 1 ):

                # values are generate from the inside of the ring to the outside

                segment = thetaStart + i / thetaSegments * thetaLength

                # vertex

                vertex.x = radius * math.cos( segment )
                vertex.y = radius * math.sin( segment )

                vertices.extend( [ vertex.x, vertex.y, vertex.z ] )

                # normal

                normals.extend( [ 0, 0, 1 ] )

                # uv

                uv.x = ( vertex.x / outerRadius + 1 ) / 2
                uv.y = ( vertex.y / outerRadius + 1 ) / 2

                uvs.extend( [ uv.x, uv.y ] )

            # increase the radius for next row of vertices

            radius += radiusStep

        # indices

        for j in xrange( phiSegments ):

            thetaSegmentLevel = j * ( thetaSegments + 1 )

            for i in xrange( thetaSegments ):

                segment = i + thetaSegmentLevel

                a = segment
                b = segment + thetaSegments + 1
                c = segment + thetaSegments + 2
                d = segment + 1

                # faces

                indices.extend( [ a, b, d ] )
                indices.extend( [ b, c, d ] )

        # build geometry

        self.setIndex( indices )
        self.addAttribute( "position", bufferAttribute.Float32BufferAttribute( vertices, 3 ) )
        self.addAttribute( "normal", bufferAttribute.Float32BufferAttribute( normals, 3 ) )
        self.addAttribute( "uv", bufferAttribute.Float32BufferAttribute( uvs, 2 ) )
