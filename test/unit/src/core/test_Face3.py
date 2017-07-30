from __future__ import division
import math

import unittest

import THREE

"""
 * @author simonThiele / https:#github.com/simonThiele
 """

class TestFace3( unittest.TestCase ):

    def test_copy( self ):

        instance = THREE.Face3(0, 1, 2, THREE.Vector3(0, 1, 0), THREE.Color(0.25, 0.5, 0.75), 2)
        copiedInstance = instance.copy(instance)

        self.checkCopy(copiedInstance)
        self.checkVertexAndColors(copiedInstance)

    def test_copy( self ):

        instance = THREE.Face3(0, 1, 2,
            [THREE.Vector3(0, 1, 0), THREE.Vector3(1, 0, 1)],
            [THREE.Color(0.25, 0.5, 0.75), THREE.Color(1, 0, 0.4)],
            2)
        copiedInstance = instance.copy(instance)

        self.checkCopy(copiedInstance)
        self.checkVertexAndColorArrays(copiedInstance)

    def test_clone( self ):

        instance = THREE.Face3(0, 1, 2, THREE.Vector3(0, 1, 0), THREE.Color(0.25, 0.5, 0.75), 2)
        copiedInstance = instance.clone()

        self.checkCopy(copiedInstance)
        self.checkVertexAndColors(copiedInstance)


    def checkCopy( self, copiedInstance ):

        self.assertTrue( isinstance( copiedInstance, THREE.Face3 ) ) # copy created the correct type
        self.assertTrue(
            copiedInstance.a == 0 and \
            copiedInstance.b == 1 and \
            copiedInstance.c == 2 and \
            copiedInstance.materialIndex == 2 ) # properties where copied

    def checkVertexAndColors( self, copiedInstance, ):

        self.assertTrue(
            copiedInstance.normal.x == 0 and copiedInstance.normal.y == 1 and copiedInstance.normal.z == 0 and \
            copiedInstance.color.r == 0.25 and copiedInstance.color.g == 0.5 and copiedInstance.color.b == 0.75 ) # properties where copied

    def checkVertexAndColorArrays( self, copiedInstance ):

        self.assertTrue(
            copiedInstance.vertexNormals[0].x == 0 and copiedInstance.vertexNormals[0].y == 1 and copiedInstance.vertexNormals[0].z == 0 and \
            copiedInstance.vertexNormals[1].x == 1 and copiedInstance.vertexNormals[1].y == 0 and copiedInstance.vertexNormals[1].z == 1 and \
            copiedInstance.vertexColors[0].r == 0.25 and copiedInstance.vertexColors[0].g == 0.5 and copiedInstance.vertexColors[0].b == 0.75 and \
            copiedInstance.vertexColors[1].r == 1 and copiedInstance.vertexColors[1].g == 0 and copiedInstance.vertexColors[1].b == 0.4 ) # properties where copied
