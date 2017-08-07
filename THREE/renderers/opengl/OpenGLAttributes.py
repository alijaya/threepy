from OpenGL.GL import *

import logging

from ctypes import *

from ...utils import Expando

buffers = {}

def createBuffer( attribute, bufferType ):

    array = attribute.array
    usage = ( GL_STATIC_DRAW, GL_DYNAMIC_DRAW )[ attribute.dynamic ]

    buffer = glGenBuffers( 1 )

    glBindBuffer( bufferType, buffer )
    glBufferData( bufferType, array, usage )

    # attribute.onUploadCallback()

    type = GL_FLOAT

    if array._type_ == c_int8: type = GL_BYTE
    elif array._type_ == c_uint8: type = GL_UNSIGNED_BYTE
    elif array._type_ == c_int16: type = GL_SHORT
    elif array._type_ == c_uint16: type = GL_UNSIGNED_SHORT
    elif array._type_ == c_int32: type = GL_INT
    elif array._type_ == c_uint32: type = GL_UNSIGNED_INT
    elif array._type_ == c_float: type = GL_FLOAT
    elif array._type_ == c_double: logging.warning( "THREE.OpenGLAttributes: Unsupported data buffer format: float64." )

    return Expando(
        buffer = buffer,
        type = type,
        bytesPerElement = sizeof( array._type_ ),
        version = attribute.version
    )

def updateBuffer( buffer, attribute, bufferType ):

    array = attribute.array
    updateRange = attribute.updateRange

    glBindBuffer( bufferType, buffer )

    if not attribute.dynamic:

        glBufferData( bufferType, array, GL_STATIC_DRAW )

    elif updateRange.count == -1:

        # Not using update ranges

        glBufferSubData( bufferType, 0, array )

    elif updateRange.count == 0:

        logging.error( "THREE.OpenGLObjects.updateBuffer: dynamic THREE.BufferAttribute marked as needsUpdate but updateRange.count is 0, ensure you are using set methods or updating manually." )

    else:

        subArray = array[ updateRange.offset : updateRange.offset + updateRange.count ]
        glBufferSubData( bufferType, updateRange.offset * array.itemsize, subArray )

        updateRange.count = -1

#

def get( attribute ):

    if hasattr( attribute, "isInterleavedBufferAttribute" ): attribute = attribute.data

    return buffers.get( attribute.uuid )

def remove( attribute ):

    if hasattr( attribute, "isInterleavedBufferAttribute" ): attribute = attribute.data

    data = buffers.get( attribute.uuid )

    if data:

        glDeleteBuffer( data.buffer )

        del buffers[ attribute.uuid ]

def update( attribute, bufferType ):

    if hasattr( attribute, "isInterleavedBufferAttribute" ): attribute = attribute.data

    data = buffers.get( attribute.uuid )

    if data: # if already exist, update it

        updateBuffer( data.buffer, attribute, bufferType )

        data.version = attribute.version

    else: # hasn't cached, create new

        buffers[ attribute.uuid ] = createBuffer( attribute, bufferType )