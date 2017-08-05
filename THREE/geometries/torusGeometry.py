from __future__ import division
import math

from ..core import geometry
from ..core import bufferGeometry
from ..core import bufferAttribute
from ..math import vector3
from ..utils import Expando

"""
 * @author oosmoxiecode
 * @author mrdoob / http:#mrdoob.com/
 * @author Mugen87 / https:#github.com/Mugen87
 """

# TorusGeometry

class TorusGeometry( geometry.Geometry ):

    def __init__( self, radius = 100, tube = 40, radialSegments = 8, tubularSegments = 6, arc = 2 * math.pi ):

        super( TorusGeometry, self ).__init__()

        self.type = "TorusGeometry"

        self.parameters = Expando(
            radius = radius,
            tube = tube,
            radialSegments = radialSegments,
            tubularSegments = tubularSegments,
            arc = arc
        )

        self.fromBufferGeometry( TorusBufferGeometry( radius, tube, radialSegments, tubularSegments, arc ) )
        self.mergeVertices()

# TorusBufferGeometry

class TorusBufferGeometry( bufferGeometry.BufferGeometry ):

    def __init__( self, radius = 100, tube = 40, radialSegments = 8, tubularSegments = 6, arc = 2 * math.pi ):

        super( TorusBufferGeometry, self ).__init__()

        self.type = "TorusBufferGeometry"

        self.parameters = Expando(
            radius = radius,
            tube = tube,
            radialSegments = radialSegments,
            tubularSegments = tubularSegments,
            arc = arc
        )

        # buffers

        indices = []
        vertices = []
        normals = []
        uvs = []

        # helper variables

        center = vector3.Vector3()
        vertex = vector3.Vector3()
        normal = vector3.Vector3()

        # generate vertices, normals and uvs

        for j in xrange( radialSegments + 1 ):

            for i in xrange( tubularSegments + 1 ):

                u = i / tubularSegments * arc
                v = j / radialSegments * math.pi * 2

                # vertex

                vertex.x = ( radius + tube * math.cos( v ) ) * math.cos( u )
                vertex.y = ( radius + tube * math.cos( v ) ) * math.sin( u )
                vertex.z = tube * math.sin( v )

                vertices.extend( [ vertex.x, vertex.y, vertex.z ] )

                # normal

                center.x = radius * math.cos( u )
                center.y = radius * math.sin( u )
                normal.subVectors( vertex, center ).normalize()

                normals.extend( [ normal.x, normal.y, normal.z ] )

                # uv

                uvs.append( i / tubularSegments )
                uvs.append( j / radialSegments )

        # generate indices

        for j in xrange( 1, radialSegments + 1 ):

            for i in xrange( 1, tubularSegments + 1 ):

                # indices

                a = ( tubularSegments + 1 ) * j + i - 1
                b = ( tubularSegments + 1 ) * ( j - 1 ) + i - 1
                c = ( tubularSegments + 1 ) * ( j - 1 ) + i
                d = ( tubularSegments + 1 ) * j + i

                # faces

                indices.extend( [ a, b, d ] )
                indices.extend( [ b, c, d ] )

        # build geometry

        self.setIndex( indices )
        self.addAttribute( "position", bufferAttribute.Float32BufferAttribute( vertices, 3 ) )
        self.addAttribute( "normal", bufferAttribute.Float32BufferAttribute( normals, 3 ) )
        self.addAttribute( "uv", bufferAttribute.Float32BufferAttribute( uvs, 2 ) )
