from __future__ import division
import math

from ..core import geometry
from ..core import bufferGeometry
from ..core import bufferAttribute
from ..utils import Expando

"""
 * @author mrdoob / http://mrdoob.com/
 * @author Mugen87 / https://github.com/Mugen87
 """

# PlaneGeometry

class PlaneGeometry( geometry.Geometry ):

    def __init__( self, width, height, widthSegments = 1, heightSegments = 1 ):

        super( PlaneGeometry, self ).__init__()

        self.type = "PlaneGeometry"

        self.parameters = Expando(
            width = width,
            height = height,
            widthSegments = widthSegments,
            heightSegments = heightSegments
        )

        self.fromBufferGeometry( PlaneBufferGeometry( width, height, widthSegments, heightSegments ) )
        self.mergeVertices()

# PlaneBufferGeometry

class PlaneBufferGeometry( bufferGeometry.BufferGeometry ):

    def __init__( self, width, height, widthSegments = 1, heightSegments = 1 ):

        super( PlaneBufferGeometry, self ).__init__()

        self.type = "PlaneBufferGeometry"

        self.parameters = Expando(
            width = width,
            height = height,
            widthSegments = widthSegments,
            heightSegments = heightSegments
        )

        width_half = width / 2
        height_half = height / 2

        gridX = widthSegments
        gridY = heightSegments

        gridX1 = gridX + 1
        gridY1 = gridY + 1

        segment_width = width / gridX
        segment_height = height / gridY

        # buffers

        indices = []
        vertices = []
        normals = []
        uvs = []

        # generate vertices, normals and uvs

        for iy in xrange( gridY1 ):

            y = iy * segment_height - height_half

            for ix in xrange( gridX1 ):

                x = ix * segment_width - width_half

                vertices.extend( [ x, - y, 0 ] )

                normals.extend( [ 0, 0, 1 ] )

                uvs.append( ix / gridX )
                uvs.append( 1 - ( iy / gridY ) )

        # indices

        for iy in xrange( gridY ):

            for ix in xrange( gridX ):

                a = ix + gridX1 * iy
                b = ix + gridX1 * ( iy + 1 )
                c = ( ix + 1 ) + gridX1 * ( iy + 1 )
                d = ( ix + 1 ) + gridX1 * iy

                # faces

                indices.extend( [ a, b, d ] )
                indices.extend( [ b, c, d ] )

        # build geometry

        self.setIndex( indices )
        self.addAttribute( "position", bufferAttribute.Float32BufferAttribute( vertices, 3 ) )
        self.addAttribute( "normal", bufferAttribute.Float32BufferAttribute( normals, 3 ) )
        self.addAttribute( "uv", bufferAttribute.Float32BufferAttribute( uvs, 2 ) )
