import OpenGLAttributes as attributes

from ...core import bufferGeometry
import OpenGLAttributes as attributes

from OpenGL.GL import *

geometries = {}

def onGeometryDispose( event ):

    from ..OpenGLRenderer import _infoMemory as infoMemory

    geometry = event.target
    buffergeometry = geometries[ geometry.id ]

    if buffergeometry.index:

        attributes.remove( buffergeometry.index )

    for name in buffergeometry.attributes:

        attributes.remove( buffergeometry.attributes[ name ] )

    geometry.removeEventListener( "dispose", onGeometryDispose )

    del geometries[ geometry.id ]

    # TODO Remove duplicate code

    # TODO wireframeAttribute

    infoMemory.geometries -= 1

def get( object, geometry ):

    from ..OpenGLRenderer import _infoMemory as infoMemory

    # if has been cached
    if geometry.id in geometries: return geometries[ geometry.id ]

    geometry.addEventListener( "dispose", onGeometryDispose )

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

    infoMemory.geometries += 1

    return buffergeometry

def update( geometry ):

    index = geometry.index
    geometryAttributes = geometry.attributes

    if index:

        attributes.update( index, GL_ELEMENT_ARRAY_BUFFER )
    
    for value in geometryAttributes.itervalues():

        attributes.update( value, GL_ARRAY_BUFFER )

    # TODO morph targets