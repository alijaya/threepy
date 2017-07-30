from __future__ import division

import logging

from OpenGL import GL

"""
 * @author mrdoob / "http":#mrdoob.com/
 """

class WebGLAttributes( object ):

    def __init__( self ):

        self.buffers = {}

    def createBuffer( self, attribute, bufferType ):

        array = attribute.array
        usage = GL.GL_DYNAMIC_DRAW if attribute.dynamic else GL.GL_STATIC_DRAW

        buffer = GL.glGenBuffers(1)

        GL.glBindBuffer( bufferType, buffer )
        GL.glBufferData( bufferType, array, usage )

        attribute.onUploadCallback()

        type = GL.GL_FLOAT

        if array.typecode == "f" :

            type = GL.GL_FLOAT

        elif array.typecode == "d" :

            logging.warning( "THREE.WebGLAttributes: Unsupported data buffer format: Float64Array." )

        elif array.typecode == "H" :

            type = GL.GL_UNSIGNED_SHORT

        elif array.typecode == "h" :

            type = GL.GL_SHORT

        elif array.typecode == "L" :

            type = GL.GL_UNSIGNED_INT

        elif array.typecode == "l" :

            type = GL.GL_INT

        elif array.typecode == "b" :

            type = GL.GL_BYTE

        elif array.typecode == "B" :

            type = GL.GL_UNSIGNED_BYTE

        return {
            "buffer": buffer,
            "type": type,
            "bytesPerElement": array.itemsize,
            "version": attribute.version
        }

    def updateBuffer( self, buffer, attribute, bufferType ):

        array = attribute.array
        updateRange = attribute.updateRange

        GL.glBindBuffer( bufferType, buffer )

        if attribute.dynamic == False :

            GL.glBufferData( bufferType, array, GL.GL_STATIC_DRAW )

        elif updateRange.count == - 1 :

            # Not using update ranges

            GL.glBufferSubData( bufferType, 0, array )

        elif updateRange.count == 0 :

            console.error( "THREE.WebGLObjects.updateBuffer: dynamic THREE.BufferAttribute marked as needsUpdate but updateRange.count is 0, ensure you are using set methods or updating manually." )

        else:

            GL.glBufferSubData( bufferType, updateRange.offset * array.itemsize,
                array[ updateRange.offset : updateRange.offset + updateRange.count ] )

            updateRange.count = -1 # reset range

    #

    def get( self, attribute ):

        if hasattr( attribute, "isInterleavedBufferAttribute" ) : attribute = attribute.data

        return self.buffers[ attribute.uuid ]

    def remove( self, attribute ):

        if hasattr( attribute, "isInterleavedBufferAttribute" ) : attribute = attribute.data

        data = self.buffers[ attribute.uuid ]

        if data :

            GL.glDeleteBuffer( data.buffer )

            delbuffers[ attribute.uuid ]

    def update( self, attribute, bufferType ):

        if hasattr( attribute, "isInterleavedBufferAttribute" ) : attribute = attribute.data

        data = self.buffers[ attribute.uuid ]

        if data is None :

            self.buffers[ attribute.uuid ] = createBuffer( attribute, bufferType )

        elif data.version < attribute.version :

            updateBuffer( data.buffer, attribute, bufferType )

            data.version = attribute.version
