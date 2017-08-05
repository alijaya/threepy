from __future__ import division
import math

from ..core import geometry
from ..core import bufferAttribute
from ..core import bufferGeometry
from ..math import vector3
from ..math import vector2
from ..math import _Math
from ..utils import Expando

"""
 * @author astrodud / hasattr( http:#astrodud, "isgreat.org/" )
 * @author zz85 / https:#github.com/zz85
 * @author bhouston / http:#clara.io
 * @author Mugen87 / https:#github.com/Mugen87
 """

# LatheGeometry

class LatheGeometry( geometry.Geometry ):

    def __init__( self, points, segments = 12, phiStart = 0, phiLength = 2 * math.pi ):

        super( LatheGeometry, self ).__init__()

        self.type = "LatheGeometry"

        self.parameters = Expando(
            points = points,
            segments = segments,
            phiStart = phiStart,
            phiLength = phiLength
        )

        self.fromBufferGeometry( LatheBufferGeometry( points, segments, phiStart, phiLength ) )
        self.mergeVertices()

# LatheBufferGeometry

class LatheBufferGeometry( bufferGeometry.BufferGeometry ):

    def __init__( self, points, segments = 12, phiStart = 0, phiLength = 2 * math.pi ):

        super( LatheBufferGeometry, self ).__init__()

        self.type = "LatheBufferGeometry"

        self.parameters = Expando(
            points = points,
            segments = segments,
            phiStart = phiStart,
            phiLength = phiLength
        )

        # clamp phiLength so it"s in range of [ 0, 2PI ]

        phiLength = _Math.clamp( phiLength, 0, math.pi * 2 )

        # buffers

        indices = []
        vertices = []
        uvs = []

        # helper variables

        inverseSegments = 1.0 / segments
        vertex = vector3.Vector3()
        uv = vector2.Vector2()

        # generate vertices and uvs

        for i in xrange( segments + 1 ):

            phi = phiStart + i * inverseSegments * phiLength

            sin = math.sin( phi )
            cos = math.cos( phi )

            for j in xrange( len( points ) ):

                # vertex

                vertex.x = points[ j ].x * sin
                vertex.y = points[ j ].y
                vertex.z = points[ j ].x * cos

                vertices.extend( [ vertex.x, vertex.y, vertex.z ] )

                # uv

                uv.x = i / segments
                uv.y = j / ( len( points ) - 1 )

                uvs.extend( [ uv.x, uv.y ] )

        # indices

        for i in xrange( segments ):

            for j in xrange( len( points ) - 1 ):

                base = j + i * len( points )

                a = base
                b = base + len( points )
                c = base + len( points ) + 1
                d = base + 1

                # faces

                indices.extend( [ a, b, d ] )
                indices.extend( [ b, c, d ] )

        # build geometry

        self.setIndex( indices )
        self.addAttribute( "position", bufferAttribute.Float32BufferAttribute( vertices, 3 ) )
        self.addAttribute( "uv", bufferAttribute.Float32BufferAttribute( uvs, 2 ) )

        # generate normals

        self.computeVertexNormals()

        # if the geometry is closed, we need to average the normals along the seam.
        # because the corresponding vertices are identical (but still have different UVs).

        if phiLength == math.pi * 2 :

            normals = self.attributes[ "normal" ].array
            n1 = vector3.Vector3()
            n2 = vector3.Vector3()
            n = vector3.Vector3()

            # self is the buffer offset for the last line of vertices

            base = segments * len( points ) * 3

            i = 0
            j = 0
            while i < len( points ):

                # select the normal of the vertex in the first line

                n1.x = normals[ j + 0 ]
                n1.y = normals[ j + 1 ]
                n1.z = normals[ j + 2 ]

                # select the normal of the vertex in the last line

                n2.x = normals[ base + j + 0 ]
                n2.y = normals[ base + j + 1 ]
                n2.z = normals[ base + j + 2 ]

                # average normals

                n.addVectors( n1, n2 ).normalize()

                # assign the values to both normals

                normals[ j + 0 ] = normals[ base + j + 0 ] = n.x
                normals[ j + 1 ] = normals[ base + j + 1 ] = n.y
                normals[ j + 2 ] = normals[ base + j + 2 ] = n.z

                i += 1
                j += 3
