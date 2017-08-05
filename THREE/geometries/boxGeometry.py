from __future__ import division

from ..core import geometry
from ..core import bufferGeometry
from ..core import bufferAttribute
from ..math import vector3
from ..utils import Expando
"""
 * @author mrdoob / http:#mrdoob.com/
 * @author Mugen87 / https:#github.com/Mugen87
 """

# BoxGeometry

class BoxGeometry( geometry.Geometry ):

    def __init__( self, width, height, depth, widthSegments = 1, heightSegments = 1, depthSegments = 1 ):

        super( BoxGeometry, self ).__init__()

        self.type = "BoxGeometry"

        self.parameters = Expando(
            width = width,
            height = height,
            depth = depth,
            widthSegments = widthSegments,
            heightSegments = heightSegments,
            depthSegments = depthSegments
        )

        self.fromBufferGeometry( BoxBufferGeometry( width, height, depth, widthSegments, heightSegments, depthSegments ) )
        self.mergeVertices()

# BoxBufferGeometry

class BoxBufferGeometry( bufferGeometry.BufferGeometry ):

    def __init__( self, width, height, depth, widthSegments = 1, heightSegments = 1, depthSegments = 1 ):

        super( BoxBufferGeometry, self ).__init__()

        self.type = "BoxBufferGeometry"

        self.parameters = Expando(
            width = width,
            height = height,
            depth = depth,
            widthSegments = widthSegments,
            heightSegments = heightSegments,
            depthSegments = depthSegments
        )

        # segments

        # buffers

        indices = []
        vertices = []
        normals = []
        uvs = []

        # helper variables

        scope = Expando(
            numberOfVertices = 0,
            groupStart = 0
        )

        # buildPlane

        def buildPlane( u, v, w, udir, vdir, width, height, depth, gridX, gridY, materialIndex ):

            numberOfVertices = scope.numberOfVertices
            groupStart = scope.groupStart

            segmentWidth = width / gridX
            segmentHeight = height / gridY

            widthHalf = width / 2
            heightHalf = height / 2
            depthHalf = depth / 2

            gridX1 = gridX + 1
            gridY1 = gridY + 1

            vertexCounter = 0
            groupCount = 0

            vector = vector3.Vector3()

            # generate vertices, normals and uvs

            for iy in xrange( gridY1 ):

                y = iy * segmentHeight - heightHalf

                for ix in xrange( gridX1 ):

                    x = ix * segmentWidth - widthHalf

                    # set values to correct vector component

                    setattr( vector, u, x * udir )
                    setattr( vector, v, y * vdir )
                    setattr( vector, w, depthHalf )

                    # now apply vector to vertex buffer

                    vertices.extend( [ vector.x, vector.y, vector.z ] )

                    # set values to correct vector component

                    setattr( vector, u, 0 )
                    setattr( vector, v, 0 )
                    setattr( vector, w, 1 if depth > 0 else - 1 )

                    # now apply vector to normal buffer

                    normals.extend( [ vector.x, vector.y, vector.z ] )

                    # uvs

                    uvs.append( ix / gridX )
                    uvs.append( 1 - ( iy / gridY ) )

                    # counters

                    vertexCounter += 1

            # indices

            # 1. you need three indices to draw a single face
            # 2. a single segment consists of two faces
            # 3. so we need to generate six (2*3) indices per segment

            for iy in xrange( gridY ):

                for ix in xrange( gridX ):

                    a = numberOfVertices + ix + gridX1 * iy
                    b = numberOfVertices + ix + gridX1 * ( iy + 1 )
                    c = numberOfVertices + ( ix + 1 ) + gridX1 * ( iy + 1 )
                    d = numberOfVertices + ( ix + 1 ) + gridX1 * iy

                    # faces

                    indices.extend( [ a, b, d ] )
                    indices.extend( [ b, c, d ] )

                    # increase counter

                    groupCount += 6

            # add a group to the geometry. self will ensure multi material support

            self.addGroup( groupStart, groupCount, materialIndex )

            # calculate start value for groups

            groupStart += groupCount

            # update total number of vertices

            numberOfVertices += vertexCounter

            scope.numberOfVertices = numberOfVertices
            scope.groupStart = groupStart

        # end buildPlane

        # build each side of the box geometry

        buildPlane( "z", "y", "x", - 1, - 1, depth, height,   width,  depthSegments, heightSegments, 0 ) # px
        buildPlane( "z", "y", "x",   1, - 1, depth, height, - width,  depthSegments, heightSegments, 1 ) # nx
        buildPlane( "x", "z", "y",   1,   1, width, depth,    height, widthSegments, depthSegments,  2 ) # py
        buildPlane( "x", "z", "y",   1, - 1, width, depth,  - height, widthSegments, depthSegments,  3 ) # ny
        buildPlane( "x", "y", "z",   1, - 1, width, height,   depth,  widthSegments, heightSegments, 4 ) # pz
        buildPlane( "x", "y", "z", - 1, - 1, width, height, - depth,  widthSegments, heightSegments, 5 ) # nz

        # build geometry

        self.setIndex( indices )
        self.addAttribute( "position", bufferAttribute.Float32BufferAttribute( vertices, 3 ) )
        self.addAttribute( "normal", bufferAttribute.Float32BufferAttribute( normals, 3 ) )
        self.addAttribute( "uv", bufferAttribute.Float32BufferAttribute( uvs, 2 ) )
