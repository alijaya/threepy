from __future__ import division
import math
import unittest

from THREE import Object3D

from THREE import Vector3

RadToDeg = 180 / math.pi

class TestObject3D( unittest.TestCase ):

    def test_rotateX( self ):

        obj = Object3D()

        angleInRad = 1.562
        obj.rotateX( angleInRad )

        self.assertAlmostEqual( obj.rotation.x, angleInRad ) # x is equal

    def test_rotateY( self ):

        obj = Object3D()

        angleInRad = -0.346
        obj.rotateY( angleInRad )

        self.assertAlmostEqual( obj.rotation.y, angleInRad ) # y is equal

    def test_rotateZ( self ):

        obj = Object3D()

        angleInRad = 1
        obj.rotateZ( angleInRad )

        self.assertAlmostEqual( obj.rotation.z, angleInRad ) # z is equal

    def test_translateOnAxis( self ):

        obj = Object3D()

        obj.translateOnAxis( Vector3( 1, 0, 0 ), 1 )
        obj.translateOnAxis( Vector3( 0, 1, 0 ), 1.23 )
        obj.translateOnAxis( Vector3( 0, 0, 1 ), -4.56 )

        self.assertEqual( obj.position.x, 1 )
        self.assertEqual( obj.position.y, 1.23 )
        self.assertEqual( obj.position.z, -4.56 )

    def test_translateX( self ):

        obj = Object3D()
        obj.translateX(1.234)

        self.assertAlmostEqual( obj.position.x, 1.234 ) # x is equal

    def test_translateY( self ):

        obj = Object3D()
        obj.translateY(1.234)

        self.assertAlmostEqual( obj.position.y, 1.234 ) # y is equal

    def test_translateZ( self ):

        obj = Object3D()
        obj.translateZ(1.234)

        self.assertAlmostEqual( obj.position.z, 1.234 ) # z is equal

    def test_lookAt( self ):

        obj = Object3D()
        obj.lookAt(Vector3(0, -1, 1))

        self.assertAlmostEqual( obj.rotation.x * RadToDeg, 45 ) # x is equal

    def test_getWorldRotation( self ):

        obj = Object3D()

        obj.lookAt(Vector3(0, -1, 1))
        self.assertAlmostEqual( obj.getWorldRotation().x * RadToDeg, 45 ) # x is equal

        obj.lookAt(Vector3(1, 0, 0))
        self.assertAlmostEqual( obj.getWorldRotation().y * RadToDeg, 90 ) # y is equal
