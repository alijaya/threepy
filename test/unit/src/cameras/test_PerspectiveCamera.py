from __future__ import division

import unittest

import THREE

"""
 * @author simonThiele / https:#github.com/simonThiele
 """

class TestPerspectiveCamera( unittest.TestCase ):

    def setUp( self ):

        self.addTypeEqualityFunc( THREE.Matrix4, self.assertMatrix4AlmostEqual )

    def assertMatrix4AlmostEqual( self, first, second, msg = None ):

        self.assertEqual( len( first.elements ), len( second.elements ) )

        for i in xrange( len( first.elements ) ):

            self.assertAlmostEqual( first.elements[ i ], second.elements[ i ] )

    def test_updateProjectionMatrix( self ):

        cam = THREE.PerspectiveCamera( 75, 16 / 9, 0.1, 300.0 )

        # updateProjectionMatrix is called in contructor
        m = cam.projectionMatrix

        # perspective projection is given my the 4x4 Matrix
        # 2n/r-l        0            l+r/r-l                 0
        #   0        2n/t-b    t+b/t-b                 0
        #   0            0        -(f+n/f-n)    -(2fn/f-n)
        #   0            0                -1                     0

        # self matrix was calculated by hand via glMatrix.perspective(75, 16 / 9, 0.1, 300.0, pMatrix)
        # to get a reference matrix from plain WebGL
        reference = THREE.Matrix4().set(
            0.7330642938613892, 0, 0, 0,
            0, 1.3032253980636597, 0, 0,
            0, 0, -1.000666856765747, -0.2000666856765747,
            0, 0, -1, 0
        )

        self.assertEqual( reference, m )

    def test_clone( self ):

        near = 1
        far = 3
        bottom = -1
        top = 1
        aspect = 16 / 9
        fov = 90

        cam = THREE.PerspectiveCamera( fov, aspect, near, far )

        clonedCam = cam.clone()

        self.assertEqual( cam.fov, clonedCam.fov  ) # fov is equal
        self.assertEqual( cam.aspect, clonedCam.aspect  ) # aspect is equal
        self.assertEqual( cam.near, clonedCam.near  ) # near is equal
        self.assertEqual( cam.far, clonedCam.far  ) # far is equal
        self.assertEqual( cam.zoom, clonedCam.zoom  ) # zoom is equal
        self.assertTrue( cam.projectionMatrix.equals(clonedCam.projectionMatrix)  ) # projectionMatrix is equal
