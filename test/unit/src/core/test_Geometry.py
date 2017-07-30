from __future__ import division
import sys
import math

import unittest

import THREE

"""
 * @author simonThiele / https:#github.com/simonThiele
 """

def getGeometryByParams( x1, y1, z1, x2, y2, z2, x3, y3, z3  ):

    geometry = THREE.Geometry()

    # a triangle
    geometry.vertices = [
        THREE.Vector3( x1, y1, z1 ),
        THREE.Vector3( x2, y2, z2 ),
        THREE.Vector3( x3, y3, z3 )
    ]

    return geometry

def getGeometry():

    return getGeometryByParams( -0.5, 0, 0, 0.5, 0, 0, 0, 1, 0 )

class TestGeometry( unittest.TestCase ):

    def test_rotateX( self ):

        geometry = getGeometry()

        matrix = THREE.Matrix4()
        matrix.makeRotationX( math.pi / 2 ) # 90 degree

        geometry.applyMatrix( matrix )

        v0 = geometry.vertices[0]
        v1 = geometry.vertices[1]
        v2 = geometry.vertices[2]
        self.assertTrue( v0.x == -0.5 and v0.y == 0 and v0.z == 0 ) # first vertex was rotated
        self.assertTrue( v1.x == 0.5 and v1.y == 0 and v1.z == 0 ) # second vertex was rotated
        self.assertTrue( v2.x == 0 and v2.y < sys.float_info.epsilon and v2.z == 1 ) # third vertex was rotated

    def test_rotateY( self ):

        geometry = getGeometry()

        matrix = THREE.Matrix4()
        matrix.makeRotationY( math.pi ) # 180 degrees

        geometry.applyMatrix( matrix )

        v0 = geometry.vertices[0]
        v1 = geometry.vertices[1]
        v2 = geometry.vertices[2]

        self.assertTrue( v0.x == 0.5 and v0.y == 0 and v0.z < sys.float_info.epsilon ) # first vertex was rotated
        self.assertTrue( v1.x == -0.5 and v1.y == 0 and v1.z < sys.float_info.epsilon ) # second vertex was rotated
        self.assertTrue( v2.x == 0 and v2.y == 1 and v2.z == 0 ) # third vertex was rotated

    def test_rotateZ( self ):

        geometry = getGeometry()

        matrix = THREE.Matrix4()
        matrix.makeRotationZ( math.pi / 2 * 3 ) # 270 degrees

        geometry.applyMatrix( matrix )

        v0 = geometry.vertices[0]
        v1 = geometry.vertices[1]
        v2 = geometry.vertices[2]

        self.assertTrue( v0.x < sys.float_info.epsilon and v0.y == 0.5 and v0.z == 0 ) # first vertex was rotated
        self.assertTrue( v1.x < sys.float_info.epsilon and v1.y == -0.5 and v1.z == 0 ) # second vertex was rotated
        self.assertTrue( v2.x == 1 and v2.y < sys.float_info.epsilon and v2.z == 0 ) # third vertex was rotated

    # def test_fromBufferGeometry( self ):

    #     bufferGeometry = THREE.BufferGeometry()
    #     bufferGeometry.addAttribute("position", THREE.BufferAttribute(array( "f", [1, 2, 3, 4, 5, 6, 7, 8, 9] ), 3 ) )
    #     bufferGeometry.addAttribute("color", THREE.BufferAttribute(array( "f", [0, 0, 0, 0.5, 0.5, 0.5, 1, 1, 1] ), 3 ) )
    #     bufferGeometry.addAttribute("normal", THREE.BufferAttribute(array( "f", [0, 1, 0, 1, 0, 1, 1, 1, 0] ), 3 ) )
    #     bufferGeometry.addAttribute("uv", THREE.BufferAttribute(array( "f", [0, 0, 0, 1, 1, 1] ), 2 ) )
    #     bufferGeometry.addAttribute("uv2", THREE.BufferAttribute(array( "f", [0, 0, 0, 1, 1, 1] ), 2 ) )

    #     geometry = THREE.Geometry().fromBufferGeometry( bufferGeometry )

    #     colors = geometry.colors
    #     self.assertTrue(
    #         colors[0].r == 0 and colors[0].g == 0 and colors[0].b == 0 and \
    #         colors[1].r == 0.5 and colors[1].g == 0.5 and colors[1].b == 0.5 and \
    #         colors[2].r == 1 and colors[2].g == 1 and colors[2].b == 1
    #         ) # colors were created well

    #     vertices = geometry.vertices
    #     self.assertTrue(
    #         vertices[0].x == 1 and vertices[0].y == 2 and vertices[0].z == 3 and \
    #         vertices[1].x == 4 and vertices[1].y == 5 and vertices[1].z == 6 and \
    #         vertices[2].x == 7 and vertices[2].y == 8 and vertices[2].z == 9
    #         ) # vertices were created well

    #     vNormals = geometry.faces[0].vertexNormals
    #     self.assertTrue(
    #         vNormals[0].x == 0 and vNormals[0].y == 1 and vNormals[0].z == 0 and \
    #         vNormals[1].x == 1 and vNormals[1].y == 0 and vNormals[1].z == 1 and \
    #         vNormals[2].x == 1 and vNormals[2].y == 1 and vNormals[2].z == 0
    #         ) # vertex normals were created well

    def test_normalize( self ):

        geometry = getGeometry()
        geometry.computeLineDistances()

        distances = geometry.lineDistances
        self.assertEqual( distances[0], 0 ) # distance to the 1st point is 0
        self.assertEqual( distances[1], 1 + distances[0] ) # distance from the 1st to the 2nd is sqrt(2nd - 1st) + distance - 1
        self.assertEqual( distances[2], math.sqrt( 0.5 * 0.5 + 1 ) + distances[1] ) # distance from the 1st to the 3nd is sqrt(3rd - 2nd) + distance - 1

