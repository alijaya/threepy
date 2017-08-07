from __future__ import division
import math

import sys
import unittest

import THREE
from THREE.utils import ctypesArray

"""
 * @author simonThiele / "https":#github.com/simonThiele
 """

DegToRad = math.pi / 180

class TestBufferGeometry( unittest.TestCase ):

    def test_add_delAttribute( self ):

        geometry = THREE.BufferGeometry()
        attributeName = "position"

        self.assertFalse( attributeName in geometry.attributes ) # no attribute defined

        geometry.addAttribute( attributeName, THREE.BufferAttribute( ctypesArray( "f", [1, 2, 3] ), 1 ) )

        self.assertTrue( attributeName in geometry.attributes ) # attribute is defined

        geometry.removeAttribute( attributeName )

        self.assertFalse( attributeName in geometry.attributes ) # no attribute defined

    def test_applyMatrix( self ):

        geometry = THREE.BufferGeometry()
        geometry.addAttribute( "position", THREE.BufferAttribute( ctypesArray( "f", 6 ), 3 ) )

        matrix = THREE.Matrix4().set(
            1, 0, 0, 1.5,
            0, 1, 0, -2,
            0, 0, 1, 3,
            0, 0, 0, 1
        )
        geometry.applyMatrix(matrix)

        position = geometry.attributes[ "position" ].array
        m = matrix.elements
        self.assertTrue( position[0] == m[12] and position[1] == m[13] and position[2] == m[14] ) # position was extracted from matrix
        self.assertTrue( position[3] == m[12] and position[4] == m[13] and position[5] == m[14] ) # position was extracted from matrix twice
        self.assertEqual( geometry.attributes[ "position" ].version, 1 ) # version was increased during update

    def test_rotateX_Y_Z( self ):

        geometry = THREE.BufferGeometry()
        geometry.addAttribute( "position", THREE.BufferAttribute( ctypesArray( "f", [1, 2, 3, 4, 5, 6] ), 3 ) )

        pos = geometry.attributes[ "position" ].array

        geometry.rotateX( 180 * DegToRad )

        # object was rotated around x so all items should be flipped but the x ones
        self.assertTrue( pos[0] == 1 and pos[1] == -2 and pos[2] == -3 and \
                         pos[3] == 4 and pos[4] == -5 and pos[5] == -6 ) # vertices were rotated around x by 180 degrees

        geometry.rotateY( 180 * DegToRad )

        # vertices were rotated around y so all items should be flipped again but the y ones
        self.assertTrue( pos[0] == -1 and pos[1] == -2 and pos[2] == 3 and \
                         pos[3] == -4 and pos[4] == -5 and pos[5] == 6 ) # vertices were rotated around y by 180 degrees

        geometry.rotateZ( 180 * DegToRad )

        # vertices were rotated around z so all items should be flipped again but the z ones
        self.assertTrue( pos[0] == 1 and pos[1] == 2 and pos[2] == 3 and \
                         pos[3] == 4 and pos[4] == 5 and pos[5] == 6 ) # vertices were rotated around z by 180 degrees

    def test_translate( self ):

        geometry = THREE.BufferGeometry()
        geometry.addAttribute( "position", THREE.BufferAttribute( ctypesArray( "f", [1, 2, 3, 4, 5, 6] ), 3 ) )

        pos = geometry.attributes[ "position" ].array

        geometry.translate( 10, 20, 30 )

        self.assertTrue( pos[0] == 11 and pos[1] == 22 and pos[2] == 33 and \
                         pos[3] == 14 and pos[4] == 25 and pos[5] == 36 ) # vertices were translated

    def test_scale( self ):

        geometry = THREE.BufferGeometry()
        geometry.addAttribute( "position", THREE.BufferAttribute( ctypesArray( "f", [-1, -1, -1, 2, 2, 2] ), 3 ) )

        pos = geometry.attributes[ "position" ].array

        geometry.scale( 1, 2, 3 )

        self.assertTrue( pos[0] == -1 and pos[1] == -2 and pos[2] == -3 and \
                         pos[3] == 2 and pos[4] == 4 and pos[5] == 6 ) # vertices were scaled

    def test_center( self ):

        geometry = THREE.BufferGeometry()
        geometry.addAttribute( "position", THREE.BufferAttribute( ctypesArray( "f", [
            -1, -1, -1,
            1, 1, 1,
            4, 4, 4
        ] ), 3 ) )

        geometry.center()

        pos = geometry.attributes[ "position" ].array
        bb = geometry.boundingBox

        # the boundingBox should go from (-1, -1, -1) to (4, 4, 4) so it has a size of (5, 5, 5)
        # after centering it the vertices should be placed between (-2.5, -2.5, -2.5) and (2.5, 2.5, 2.5)
        self.assertTrue( pos[0] == -2.5 and pos[1] == -2.5 and pos[2], -2.5 and \
                         pos[3] == -0.5 and pos[4] == -0.5 and pos[5] == -0.5 and \
                         pos[6] == 2.5 and pos[7] == 2.5 and pos[8] == 2.5 ) # vertices were replaced by boundingBox dimensions

    # def test_setFromObject( self ):

    #     lineGeo = THREE.Geometry()
    #     lineGeo.vertices.extend( [
    #         THREE.Vector3( -10, 0, 0 ),
    #         THREE.Vector3( 0, 10, 0 ),
    #         THREE.Vector3( 10, 0, 0 )
    #     ] )

    #     lineGeo.colors.extend( [
    #         THREE.Color(1, 0, 0 ),
    #         THREE.Color(0, 1, 0 ),
    #         THREE.Color(0, 0, 1 )
    #     ] )

    #     line = THREE.Line( lineGeo, None )
    #     geometry = THREE.BufferGeometry().setFromObject( line )

    #     pos = geometry.attributes.position.array
    #     col = geometry.attributes.color.array
    #     v = lineGeo.vertices
    #     c = lineGeo.colors

    #     self.assertTrue(
    #         # position exists
    #         pos is not None and \

    #         # vertex arrays have the same size
    #         len( v ) * 3 == len( pos ) and \

    #         # there are three complete vertices (each vertex contains three values)
    #         geometry.attributes.position.count == 3 and \

    #         # check if both arrays contains the same data
    #         pos[0] == v[0].x and pos[1] == v[0].y and pos[2] == v[0].z and \
    #         pos[3] == v[1].x and pos[4] == v[1].y and pos[5] == v[1].z and \
    #         pos[6] == v[2].x and pos[7] == v[2].y and pos[8] == v[2].z
    #     ) # positions are equal

    #     self.assertTrue(
    #         # color exists
    #         col is not None and \

    #         # color arrays have the same size
    #         len( c ) * 3 == len( col ) and \

    #         # there are three complete colors (each color contains three values)
    #         geometry.attributes.color.count == 3 and \

    #         # check if both arrays contains the same data
    #         col[0] == c[0].r and col[1] == c[0].g and col[2] == c[0].b and \
    #         col[3] == c[1].r and col[4] == c[1].g and col[5] == c[1].b and \
    #         col[6] == c[2].r and col[7] == c[2].g and col[8] == c[2].b
    #     ) # colors are equal

    def test_computeBoundingBox( self ):

        bb = self.getBBForVertices( [-1, -2, -3, 13, -2, -3.5, -1, -20, 0, -4, 5, 6] )

        self.assertEqual( bb.min.x == -4 and bb.min.y == -20 and bb.min.z, -3.5 ) # min values are set correctly
        self.assertEqual( bb.max.x == 13 and bb.max.y == 5 and bb.max.z, 6 ) # max values are set correctly

        bb = self.getBBForVertices( [-1, -1, -1] )

        self.assertEqual( bb.min.x == bb.max.x and bb.min.y == bb.max.y and bb.min.z, bb.max.z ) # since there is only one vertex, max and min are equal
        self.assertEqual( bb.min.x == -1 and bb.min.y == -1 and bb.min.z, -1 ) # since there is only one vertex, min and max are self vertex

    def test_computeBoundingSphere( self ):

        bs = self.getBSForVertices( [-10, 0, 0, 10, 0, 0] )

        self.assertEqual( bs.radius, (10 + 10) / 2 ) # radius is equal to deltaMinMax / 2
        self.assertTrue( bs.center.x == 0 and bs.center.y == 0 and bs.center.y == 0 ) # bounding sphere is at ( 0, 0, 0 )

        bs = self.getBSForVertices( [-5, 11, -3, 5, -11, 3] )
        radius = THREE.Vector3(5, 11, 3).length()

        self.assertEqual( bs.radius, radius ) # radius is equal to directionLength
        self.assertTrue( bs.center.x == 0 and bs.center.y == 0 and bs.center.y == 0 ) # bounding sphere is at ( 0, 0, 0 )

    def getBBForVertices( self, vertices ):

        geometry = THREE.BufferGeometry()

        geometry.addAttribute( "position", THREE.BufferAttribute( ctypesArray( "f", vertices ), 3 ) )
        geometry.computeBoundingBox()

        return geometry.boundingBox

    def getBSForVertices( self, vertices ):

        geometry = THREE.BufferGeometry()

        geometry.addAttribute( "position", THREE.BufferAttribute( ctypesArray( "f", vertices ), 3 ) )
        geometry.computeBoundingSphere()

        return geometry.boundingSphere

    def test_computeVertexNormals( self ):

        # get normals for a counter clockwise created triangle
        normals = self.getNormalsForVertices( [-1, 0, 0, 1, 0, 0, 0, 1, 0] )

        self.assertTrue( normals[0] == 0 and normals[1] == 0 and normals[2] == 1 )
            # first normal is pointing to screen since the the triangle was created counter clockwise

        self.assertTrue( normals[3] == 0 and normals[4] == 0 and normals[5] == 1 )
            # second normal is pointing to screen since the the triangle was created counter clockwise

        self.assertTrue( normals[6] == 0 and normals[7] == 0 and normals[8] == 1 )
            # third normal is pointing to screen since the the triangle was created counter clockwise

        # get normals for a clockwise created triangle
        normals = self.getNormalsForVertices( [1, 0, 0, -1, 0, 0, 0, 1, 0] )

        self.assertTrue( normals[0] == 0 and normals[1] == 0 and normals[2] == -1 )
            # first normal is pointing to screen since the the triangle was created clockwise" )

        self.assertTrue( normals[3] == 0 and normals[4] == 0 and normals[5] == -1 )
            # second normal is pointing to screen since the the triangle was created clockwise" )

        self.assertTrue( normals[6] == 0 and normals[7] == 0 and normals[8] == -1 )
            # third normal is pointing to screen since the the triangle was created clockwise" )

        normals = self.getNormalsForVertices( [0, 0, 1, 0, 0, -1, 1, 1, 0] )

        # the triangle is rotated by 45 degrees to the right so the normals of the three vertices
        # should point to (1, -1, 0).normalized(). The simplest solution is to check against a normalized
        # vector (1, -1, 0) but you will get calculation errors because of floating calculations so another
        # valid technique is to create a vector which stands in 90 degrees to the normals and calculate the
        # dot product which is the cos of the angle between them. This should be < floating calculation error
        # which can be taken from sys.float_info.epsilon
        direction = THREE.Vector3(1, 1, 0).normalize() # a vector which should have 90 degrees difference to normals
        difference = direction.dot( THREE.Vector3( normals[0], normals[1], normals[2] ) )
        self.assertTrue( difference < sys.float_info.epsilon ) # normal is equal to reference vector

        # get normals for a line should be NAN because you need min a triangle to calculate normals
        # normals = self.getNormalsForVertices( [1, 0, 0, -1, 0, 0] )
        # for i in xrange( len( normals ) ):
        #     self.assertTrue( math.isnan( normals[i] ) ) # normals can"t be calculated which is good

    def getNormalsForVertices( self, vertices ):

        geometry = THREE.BufferGeometry()

        geometry.addAttribute( "position", THREE.BufferAttribute( ctypesArray( "f", vertices ), 3 ) )

        geometry.computeVertexNormals()

        self.assertTrue( "normal" in geometry.attributes ) # normal attribute was created

        return geometry.attributes[ "normal" ].array

    def test_merge( self ):

        geometry1 = THREE.BufferGeometry()
        geometry1.addAttribute( "attrName", THREE.BufferAttribute( ctypesArray( "f", [1, 2, 3, 0, 0, 0] ), 3 ) )

        geometry2 = THREE.BufferGeometry()
        geometry2.addAttribute( "attrName", THREE.BufferAttribute( ctypesArray( "f", [4, 5, 6] ), 3 ) )

        attr = geometry1.attributes[ "attrName" ].array

        geometry1.merge(geometry2, 1)

        # merged array should be 1, 2, 3, 4, 5, 6
        for i in xrange( len( attr ) ):
            self.assertEqual( attr[i], i + 1 )

        geometry1.merge(geometry2)
        self.assertTrue( attr[0] == 4 and attr[1] == 5 and attr[2] == 6 ) # copied the 3 attributes without offset

    def test_copy( self ):

        geometry = THREE.BufferGeometry()
        geometry.addAttribute( "attrName", THREE.BufferAttribute( ctypesArray( "f", [1, 2, 3, 4, 5, 6] ), 3 ) )
        geometry.addAttribute( "attrName2", THREE.BufferAttribute( ctypesArray( "f", [0, 1, 3, 5, 6] ), 1 ) )

        copy = THREE.BufferGeometry().copy(geometry)

        self.assertTrue( copy != geometry and geometry.id != copy.id ) # object was created

        for key in geometry.attributes:
            attribute = geometry.attributes[key]
            self.assertIsNotNone( attribute ) # all attributes where copied

            for i in xrange( len( attribute.array ) ):
                self.assertEqual( attribute.array[i], copy.attributes[key].array[i] ) # values of the attribute are equal
