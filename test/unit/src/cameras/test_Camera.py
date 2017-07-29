from __future__ import division
import math

import unittest

import THREE

class TestCamera( unittest.TestCase ):

    def test_lookAt( self ):

        cam = THREE.Camera()
        cam.lookAt(THREE.Vector3(0, 1, -1))

        self.assertAlmostEqual( cam.rotation.x * ( 180 / math.pi ), 45 ) # x is equal

    def test_clone( self ):

        cam = THREE.Camera()

        # fill the matrices with any nonsense values just to see if they get copied
        cam.matrixWorldInverse.set( 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 )
        cam.projectionMatrix.set( 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 )

        clonedCam = cam.clone()

        self.assertTrue( cam.matrixWorldInverse.equals(clonedCam.matrixWorldInverse)  ) # matrixWorldInverse is equal
        self.assertTrue( cam.projectionMatrix.equals(clonedCam.projectionMatrix)  ) # projectionMatrix is equal
