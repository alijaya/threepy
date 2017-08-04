from __future__ import division
import math

import numpy as np

import unittest

import THREE

"""
 * @author simonThiele / https:#github.com/simonThiele
 """

class TestBufferAttribute( unittest.TestCase ):

    def test_count( self ):

        self.assertEqual( THREE.BufferAttribute( np.array( [1, 2, 3, 4, 5, 6], np.float32 ), 3 ).count, 2 ) # count is equal to the number of chunks

    def test_copy( self ):

        attr = THREE.BufferAttribute( np.array( [1, 2, 3, 4, 5, 6], np.float32 ), 3 )
        attr.setDynamic( True )
        attr.needsUpdate = True

        attrCopy = THREE.BufferAttribute( None, None ).copy( attr )

        self.assertEqual( attr.count, attrCopy.count ) # count is equal
        self.assertEqual( attr.itemSize, attrCopy.itemSize ) # itemSize is equal
        self.assertEqual( attr.dynamic, attrCopy.dynamic ) # dynamic is equal
        self.assertEqual( attr.array.size, attrCopy.array.size ) # array length is equal
        self.assertEqual( attr.version, 1 ) # version is not copied which is good
        self.assertEqual( attrCopy.version, 0 ) # version is not copied which is good

    def test_copyAt( self ):

        attr = THREE.BufferAttribute( np.array( [1, 2, 3, 4, 5, 6, 7, 8, 9], np.float32 ), 3 )
        attr2 = THREE.BufferAttribute( np.zeros( 9, np.float32 ), 3 )

        attr2.copyAt( 1, attr, 2 )
        attr2.copyAt( 0, attr, 1 )
        attr2.copyAt( 2, attr, 0 )

        i = attr.array
        i2 = attr2.array # should be [4, 5, 6, 7, 8, 9, 1, 2, 3]

        self.assertTrue( i2[0] == i[3] and i2[1] == i[4] and i2[2] == i[5] ) # chunck copied to correct place
        self.assertTrue( i2[3] == i[6] and i2[4] == i[7] and i2[5] == i[8] ) # chunck copied to correct place
        self.assertTrue( i2[6] == i[0] and i2[7] == i[1] and i2[8] == i[2] ) # chunck copied to correct place

    def test_copyColorsArray( self ):

        attr = THREE.BufferAttribute( np.zeros( 6, np.float32 ), 3 )

        attr.copyColorsArray( [
            THREE.Color( 0, 0.5, 1 ),
            THREE.Color( 0.25, 1, 0 )
        ])

        i = attr.array
        self.assertTrue( i[0] == 0 and i[1] == 0.5 and i[2] == 1 ) # first color was copied correctly
        self.assertTrue( i[3] == 0.25 and i[4] == 1 and i[5] == 0 ) # second color was copied correctly

    def test_copyIndicesArray( self ):

        attr = THREE.BufferAttribute( np.zeros( 6, np.float32 ), 3 )

        attr.copyIndicesArray( [
            {"a": 1, "b": 2, "c": 3 },
            {"a": 4, "b": 5, "c": 6 }
        ] )

        i = attr.array
        self.assertTrue( i[0] == 1 and i[1] == 2 and i[2] == 3 ) # first indices were copied correctly
        self.assertTrue( i[3] == 4 and i[4] == 5 and i[5] == 6 ) # second indices were copied correctly

    def test_copyVector2sArray( self ):

        attr = THREE.BufferAttribute( np.zeros( 4, np.float32 ), 2 )

        attr.copyVector2sArray( [
            THREE.Vector2(1, 2),
            THREE.Vector2(4, 5)
        ])

        i = attr.array
        self.assertTrue( i[0] == 1 and i[1] == 2 ) # first vector was copied correctly
        self.assertTrue( i[2] == 4 and i[3] == 5 ) # second vector was copied correctly

    def test_copyVector3sArray( self ):

        attr = THREE.BufferAttribute( np.zeros( 6, np.float32 ), 2 )

        attr.copyVector3sArray( [
            THREE.Vector3(1, 2, 3),
            THREE.Vector3(10, 20, 30)
        ])

        i = attr.array
        self.assertTrue( i[0] == 1 and i[1] == 2 and i[2] == 3 ) # first vector was copied correctly
        self.assertTrue( i[3] == 10 and i[4] == 20 and i[5] == 30 ) # second vector was copied correctly

    def test_copyVector4sArray( self ):

        attr = THREE.BufferAttribute( np.zeros( 8, np.float32 ), 2 )

        attr.copyVector4sArray( [
            THREE.Vector4(1, 2, 3, 4),
            THREE.Vector4(10, 20, 30, 40)
        ])

        i = attr.array
        self.assertTrue( i[0] == 1 and i[1] == 2 and i[2] == 3 and i[3] == 4 ) # first vector was copied correctly
        self.assertTrue( i[4] == 10 and i[5] == 20 and i[6] == 30 and i[7] == 40 ) # second vector was copied correctly

    def test_clone( self ):

        attr = THREE.BufferAttribute( np.array( [1, 2, 3, 4, 0.12, -12], np.float32 ), 2 )
        attrCopy = attr.clone()

        self.assertEqual( attr.array.size, attrCopy.array.size ) # attribute was cloned
        for i in xrange( attr.array.size ):
            self.assertEqual( attr.array[i], attrCopy.array[i] ) # array item is equal
