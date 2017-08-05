from __future__ import division
import math

from ..core import geometry
from ..core import bufferGeometry
from ..core import bufferAttribute
from ..math import vector3
from ..math import vector2
from ..utils import Expando

"""
 * @author mrdoob / http:#mrdoob.com/
 * @author Mugen87 / https:#github.com/Mugen87
 """

# CylinderGeometry

class CylinderGeometry( geometry.Geometry ):

    def __init__( self, radiusTop = 20, radiusBottom = 20, height = 100, radialSegments = 8, heightSegments = 1, openEnded = False, thetaStart = 0.0, thetaLength = 2.0 * math.pi ):

        super( CylinderGeometry, self ).__init__()

        self.type = "CylinderGeometry"

        self.parameters = Expando(
            radiusTop = radiusTop,
            radiusBottom = radiusBottom,
            height = height,
            radialSegments = radialSegments,
            heightSegments = heightSegments,
            openEnded = openEnded,
            thetaStart = thetaStart,
            thetaLength = thetaLength
        )

        self.fromBufferGeometry( CylinderBufferGeometry( radiusTop, radiusBottom, height, radialSegments, heightSegments, openEnded, thetaStart, thetaLength ) )
        self.mergeVertices()

# CylinderBufferGeometry

class CylinderBufferGeometry( bufferGeometry.BufferGeometry ):

    def __init__( self, radiusTop = 20, radiusBottom = 20, height = 100, radialSegments = 8, heightSegments = 1, openEnded = False, thetaStart = 0.0, thetaLength = 2.0 * math.pi ):

        super( CylinderBufferGeometry, self ).__init__()

        self.type = "CylinderBufferGeometry"

        self.parameters = Expando(
            radiusTop = radiusTop,
            radiusBottom = radiusBottom,
            height = height,
            radialSegments = radialSegments,
            heightSegments = heightSegments,
            openEnded = openEnded,
            thetaStart = thetaStart,
            thetaLength = thetaLength
        )

        # buffers

        indices = []
        vertices = []
        normals = []
        uvs = []

        # helper variables

        scope = Expando(
            index = 0,
            groupStart = 0
        )
        indexArray = []
        halfHeight = height / 2

        # helper function

        def generateTorso():

            index = scope.index
            groupStart = scope.groupStart

            normal = vector3.Vector3()
            vertex = vector3.Vector3()

            groupCount = 0

            # self will be used to calculate the normal
            slope = ( radiusBottom - radiusTop ) / height

            # generate vertices, normals and uvs

            for y in xrange( heightSegments + 1 ):

                indexRow = []

                v = y / heightSegments

                # calculate the radius of the current row

                radius = v * ( radiusBottom - radiusTop ) + radiusTop

                for x in xrange( radialSegments + 1 ):

                    u = x / radialSegments

                    theta = u * thetaLength + thetaStart

                    sinTheta = math.sin( theta )
                    cosTheta = math.cos( theta )

                    # vertex

                    vertex.x = radius * sinTheta
                    vertex.y = - v * height + halfHeight
                    vertex.z = radius * cosTheta
                    vertices.extend( [ vertex.x, vertex.y, vertex.z ] )

                    # normal

                    normal.set( sinTheta, slope, cosTheta ).normalize()
                    normals.extend( [ normal.x, normal.y, normal.z ] )

                    # uv

                    uvs.extend( [ u, 1 - v ] )

                    # save index of vertex in respective row

                    indexRow.append( index )
                    index += 1

                # now save vertices of the row in our index array

                indexArray.append( indexRow )

            # generate indices

            for x in xrange( radialSegments ):

                for y in xrange( heightSegments ):

                    # we use the index array to access the correct indices

                    a = indexArray[ y ][ x ]
                    b = indexArray[ y + 1 ][ x ]
                    c = indexArray[ y + 1 ][ x + 1 ]
                    d = indexArray[ y ][ x + 1 ]

                    # faces

                    indices.extend( [ a, b, d ] )
                    indices.extend( [ b, c, d ] )

                    # update group counter

                    groupCount += 6

            # add a group to the geometry. self will ensure multi material support

            self.addGroup( groupStart, groupCount, 0 )

            # calculate start value for groups

            groupStart += groupCount


            scope.index = index
            scope.groupStart = groupStart

        def generateCap( top ):

            index = scope.index
            groupStart = scope.groupStart

            uv = vector2.Vector2()
            vertex = vector3.Vector3()

            groupCount = 0

            radius = radiusTop if top == True else radiusBottom
            sign = 1 if top == True else - 1

            # save the index of the first center vertex
            centerIndexStart = index

            # first we generate the center vertex data of the cap.
            # because the geometry needs one set of uvs per face,
            # we must generate a center vertex per face/segment

            for x in xrange( 1, radialSegments + 1 ):

                # vertex

                vertices.extend( [ 0, halfHeight * sign, 0 ] )

                # normal

                normals.extend( [ 0, sign, 0 ] )

                # uv

                uvs.extend( [ 0.5, 0.5 ] )

                # increase index

                index += 1

            # save the index of the last center vertex

            centerIndexEnd = index

            # now we generate the surrounding vertices, normals and uvs

            for x in xrange( radialSegments + 1 ):

                u = x / radialSegments
                theta = u * thetaLength + thetaStart

                cosTheta = math.cos( theta )
                sinTheta = math.sin( theta )

                # vertex

                vertex.x = radius * sinTheta
                vertex.y = halfHeight * sign
                vertex.z = radius * cosTheta
                vertices.extend( [ vertex.x, vertex.y, vertex.z ] )

                # normal

                normals.extend( [ 0, sign, 0 ] )

                # uv

                uv.x = ( cosTheta * 0.5 ) + 0.5
                uv.y = ( sinTheta * 0.5 * sign ) + 0.5
                uvs.extend( [ uv.x, uv.y ] )

                # increase index

                index += 1

            # generate indices

            for x in xrange( radialSegments ):

                c = centerIndexStart + x
                i = centerIndexEnd + x

                if top == True :

                    # face top

                    indices.extend( [ i, i + 1, c ] )

                else:

                    # face bottom

                    indices.extend( [ i + 1, i, c ] )

                groupCount += 3

            # add a group to the geometry. self will ensure multi material support

            self.addGroup( groupStart, groupCount, 1 if top == True else 2 )

            # calculate start value for groups

            groupStart += groupCount

            scope.index = index
            scope.groupStart = groupStart

        # end helper

        # generate geometry

        generateTorso()

        if openEnded == False :

            if radiusTop > 0 : generateCap( True )
            if radiusBottom > 0 : generateCap( False )

        # build geometry

        self.setIndex( indices )
        self.addAttribute( "position", bufferAttribute.Float32BufferAttribute( vertices, 3 ) )
        self.addAttribute( "normal", bufferAttribute.Float32BufferAttribute( normals, 3 ) )
        self.addAttribute( "uv", bufferAttribute.Float32BufferAttribute( uvs, 2 ) )
