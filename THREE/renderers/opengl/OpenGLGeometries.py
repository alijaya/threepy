import OpenGLAttributes as attributes

from ...core import bufferGeometry

from OpenGL.GL import *

geometries = {}

def get( object, geometry ):

    # if has been cached
    if geometry.id in geometries: return geometries[ geometry.id ]

    # TODO handle geometry on dispose

    buffergeometry = None

    if hasattr( geometry, "isBufferGeometry" ):

        buffergeometry = geometry

    elif hasattr( geometry, "isGeometry" ):

        # if hasn't cached
        if not hasattr( geometry, "_bufferGeometry" ):

            geometry._bufferGeometry = bufferGeometry.BufferGeometry().setFromObject( object )
        
        buffergeometry = geometry._bufferGeometry

    # set cache
    geometries[ geometry.id ] = buffergeometry

    return buffergeometry

def update( geometry ):

    index = geometry.index
    geometryAttributes = geometry.attributes

    if index:

        attributes.update( index, GL_ELEMENT_ARRAY_BUFFER )
    
    for value in geometryAttributes.itervalues():

        attributes.update( value, GL_ARRAY_BUFFER )

    # TODO morph targets