from __future__ import division

import logging

from ..math import vector4
from ..math import vector3
from ..math import vector2
from ..math import color
from ..math import _Math
from ..utils import Expando
from ..utils import ctypesArray

"""
 * @author mrdoob / http:#mrdoob.com/
 """

class BufferAttribute( object ):

    def __init__( self, array, itemSize, normalized = False ):

        if isinstance( array, list ):

            raise ValueError( "THREE.BufferAttribute: array should be a Typed Array." )

        self.isBufferAttribute = True

        self.uuid = _Math.generateUUID()
        self.name = ""

        self.array = array
        self.itemSize = itemSize
        self.count = len( array ) // itemSize if array is not None else 0
        self.normalized = normalized

        self.dynamic = False
        self.updateRange = Expando( offset = 0, count = - 1 )
        self.onUploadCallback = lambda *args: None
        self.version = 0

    @property
    def needsUpdate( self ):

        return None

    @needsUpdate.setter
    def needsUpdate( self, value ):

        if value == True: self.version += 1

    def setArray( self, array ):

        if isinstance( array, list ):

            raise ValueError( "THREE.BufferAttribute: array should be a Typed Array." )

        self.count = len( array ) // self.itemSize if array is not None else 0
        self.array = array

    def setDynamic( self, value ):

        self.dynamic = value

        return self

    def copy( self, source ):

        self.array = type( source.array )( *source.array )
        self.itemSize = source.itemSize
        self.count = source.count
        self.normalized = source.normalized

        self.dynamic = source.dynamic

        return self

    def copyAt( self, index1, attribute, index2 ):

        index1 *= self.itemSize
        index2 *= attribute.itemSize

        for i in xrange( self.itemSize ):

            self.array[ index1 + i ] = attribute.array[ index2 + i ]

        return self

    def copyArray( self, array ):

        self.array[0:] = array

        return self

    def copyColorsArray( self, colors ):

        array = self.array
        offset = 0

        for color in colors:

            if color is None:

                logging.warning( "THREE.BufferAttribute.copyColorsArray(): color is None", i )
                color = color.Color()

            array[ offset ] = color.r
            offset += 1
            array[ offset ] = color.g
            offset += 1
            array[ offset ] = color.b
            offset += 1

        return self

    def copyIndicesArray( self, indices ):

        array = self.array
        offset = 0

        for index in indices:

            array[ offset ] = index.a
            offset += 1
            array[ offset ] = index.b
            offset += 1
            array[ offset ] = index.c
            offset += 1

        return self

    def copyVector2sArray( self, vectors ):

        array = self.array
        offset = 0

        for vector in vectors:

            if vector is None:

                logging.warning( "THREE.BufferAttribute.copyVector2sArray(): vector is None", i )
                vector = vector2.Vector2()

            array[ offset ] = vector.x
            offset += 1
            array[ offset ] = vector.y
            offset += 1

        return self

    def copyVector3sArray( self, vectors ):

        array = self.array
        offset = 0

        for vector in vectors:

            if vector is None:

                logging.warning( "THREE.BufferAttribute.copyVector3sArray(): vector is None", i )
                vector = vector3.Vector3()

            array[ offset ] = vector.x
            offset += 1
            array[ offset ] = vector.y
            offset += 1
            array[ offset ] = vector.z
            offset += 1

        return self

    def copyVector4sArray( self, vectors ):

        array = self.array
        offset = 0

        for vector in vectors:

            if vector is None:

                logging.warning( "THREE.BufferAttribute.copyVector4sArray(): vector is None", i )
                vector = vector4.Vector4()

            array[ offset ] = vector.x
            offset += 1
            array[ offset ] = vector.y
            offset += 1
            array[ offset ] = vector.z
            offset += 1
            array[ offset ] = vector.w
            offset += 1

        return self

    def set( self, value, offset = 0 ):

        size = len( value )
        mx = len( self.array )
        if offset + size <= mx: self.array[ offset : offset + size ] = value
        else: self.array[ offset : ] = value[ : mx - offset ]

        return self

    def getX( self, index ):

        return self.array[ index * self.itemSize ]

    def setX( self, index, x ):

        self.array[ index * self.itemSize ] = x

        return self

    def getY( self, index ):

        return self.array[ index * self.itemSize + 1 ]

    def setY( self, index, y ):

        self.array[ index * self.itemSize + 1 ] = y

        return self

    def getZ( self, index ):

        return self.array[ index * self.itemSize + 2 ]

    def setZ( self, index, z ):

        self.array[ index * self.itemSize + 2 ] = z

        return self

    def getW( self, index ):

        return self.array[ index * self.itemSize + 3 ]

    def setW( self, index, w ):

        self.array[ index * self.itemSize + 3 ] = w

        return self

    def setXY( self, index, x, y ):

        index *= self.itemSize

        self.array[ index + 0 ] = x
        self.array[ index + 1 ] = y

        return self

    def setXYZ( self, index, x, y, z ):

        index *= self.itemSize

        self.array[ index + 0 ] = x
        self.array[ index + 1 ] = y
        self.array[ index + 2 ] = z

        return self

    def setXYZW( self, index, x, y, z, w ):

        index *= self.itemSize

        self.array[ index + 0 ] = x
        self.array[ index + 1 ] = y
        self.array[ index + 2 ] = z
        self.array[ index + 3 ] = w

        return self

    def onUpload( self, callback ):

        self.onUploadCallback = callback

        return self

    def clone( self ):

        return BufferAttribute( self.array, self.itemSize ).copy( self )

#

class Int8BufferAttribute( BufferAttribute ):

    def __init__( self, arr, itemSize ):

        super( Int8BufferAttribute, self ).__init__( ctypesArray( "b", arr ), itemSize )

class Uint8BufferAttribute( BufferAttribute ):

    def Uint8BufferAttribute( self, arr, itemSize ):

        super( Uint8BufferAttribute, self ).__init__( ctypesArray( "B", arr ), itemSize )

class Uint8ClampedBufferAttribute( BufferAttribute ):

    def __init__( self, arr, itemSize ):

        super( Uint8ClampedBufferAttribute, self ).__init__( ctypesArray( "B", arr ), itemSize )

class Int16BufferAttribute( BufferAttribute ):

    def __init__( self, arr, itemSize ):

        super( Int16BufferAttribute, self ).__init__( ctypesArray( "h", arr ), itemSize )

class Uint16BufferAttribute( BufferAttribute ):

    def __init__( self, arr, itemSize ):

        super( Uint16BufferAttribute, self ).__init__( ctypesArray( "H", arr ), itemSize )

class Int32BufferAttribute( BufferAttribute ):

    def __init__( self, arr, itemSize ):

        super( Int32BufferAttribute, self ).__init__( ctypesArray( "l", arr ), itemSize )

class Uint32BufferAttribute( BufferAttribute ):

    def __init__( self, arr, itemSize ):

        super( Uint32BufferAttribute, self ).__init__( ctypesArray( "L", arr ), itemSize )

class Float32BufferAttribute( BufferAttribute ):

    def __init__( self, arr, itemSize ):

        super( Float32BufferAttribute, self ).__init__( ctypesArray( "f", arr ), itemSize )

class Float64BufferAttribute( BufferAttribute ):

    def __init__( self, arr, itemSize ):

        super( Float64BufferAttribute, self ).__init__( ctypesArray( "d", arr ), itemSize )
