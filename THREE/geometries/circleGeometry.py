from __future__ import division
import math

from ..core import geometry
from ..core import bufferGeometry
from ..core import bufferAttribute
from ..math import vector3
from ..math import vector2
from ..utils import Expando

"""
 * @author benaadams / https:#twitter.com/ben_a_adams
 * @author Mugen87 / https:#github.com/Mugen87
 * @author hughes
 """

# CircleGeometry

class CircleGeometry( geometry.Geometry ):

    def __init__( self, radius = 50, segments = 8, thetaStart = 0, thetaLength = 2 * math.pi ):

        super( CircleGeometry, self ).__init__()

        self.type = "CircleGeometry"

        self.parameters = Expando(
            radius = radius,
            segments = segments,
            thetaStart = thetaStart,
            thetaLength = thetaLength
        )

        self.fromBufferGeometry( CircleBufferGeometry( radius, segments, thetaStart, thetaLength ) )
        self.mergeVertices()

# CircleBufferGeometry

class CircleBufferGeometry( bufferGeometry.BufferGeometry ):

    def __init__( self, radius = 50, segments = 8, thetaStart = 0, thetaLength = 2 * math.pi ):

        super( CircleBufferGeometry, self ).__init__()

        self.type = "CircleBufferGeometry"

        self.parameters = Expando(
            radius = radius,
            segments = segments,
            thetaStart = thetaStart,
            thetaLength = thetaLength
        )

        segments = max( 3, segments )

        # buffers

        indices = []
        vertices = []
        normals = []
        uvs = []

        # helper variables

        vertex = vector3.Vector3()
        uv = vector2.Vector2()

        # center point

        vertices.extend( [ 0, 0, 0 ] )
        normals.extend( [ 0, 0, 1 ] )
        uvs.extend( [ 0.5, 0.5 ] )

        s = 0
        i = 3
        while s <= segments:

            segment = thetaStart + s / segments * thetaLength

            # vertex

            vertex.x = radius * math.cos( segment )
            vertex.y = radius * math.sin( segment )

            vertices.extend( [ vertex.x, vertex.y, vertex.z ] )

            # normal

            normals.extend( [ 0, 0, 1 ] )

            # uvs

            uv.x = ( vertices[ i ] / radius + 1 ) / 2
            uv.y = ( vertices[ i + 1 ] / radius + 1 ) / 2

            uvs.extend( [ uv.x, uv.y ] )

            s += 1
            i += 3

        # indices

        for i in xrange( segments + 1 ):

            indices.extend( [ i, i + 1, 0 ] )

        # build geometry

        self.setIndex( indices )
        self.addAttribute( "position", bufferAttribute.Float32BufferAttribute( vertices, 3 ) )
        self.addAttribute( "normal", bufferAttribute.Float32BufferAttribute( normals, 3 ) )
        self.addAttribute( "uv", bufferAttribute.Float32BufferAttribute( uvs, 2 ) )
