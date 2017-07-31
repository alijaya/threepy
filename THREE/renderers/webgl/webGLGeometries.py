from __future__ import division

import logging

from OpenGL import GL

from ...core import bufferAttribute
from ...core import bufferGeometry
"""
 * @author mrdoob / "http":#mrdoob.com/
 """

class WebGLGeometries( object ):

    def __init__( self, attributes, infoMemory ):

        self.attributes = attributes
        self.infoMemory = infoMemory

        self.geometries = {}
        self.wireframeAttributes = {}

    def onGeometryDispose( self, event ):

        geometry = event.target
        buffergeometry = self.geometries[ geometry.id ]

        if buffergeometry.index is not None :

            self.attributes.remove( buffergeometry.index )

        for name in buffergeometry.attributes :

            self.attributes.remove( buffergeometry.attributes[ name ] )

        geometry.removeEventListener( "dispose", onGeometryDispose )

        del geometries[ geometry.id ]

        # TODO Remove duplicate code

        attribute = self.wireframeAttributes[ geometry.id ]

        if attribute :

            self.attributes.remove( attribute )
            delwireframeAttributes[ geometry.id ]

        attribute = self.wireframeAttributes[ buffergeometry.id ]

        if attribute :

            self.attributes.remove( attribute )
            delwireframeAttributes[ buffergeometry.id ]

        #

        self.infoMemory.geometries -= 1

    def get( self, object, geometry ):

        buffergeometry = self.geometries.get( geometry.id )

        if buffergeometry : return buffergeometry

        geometry.addEventListener( "dispose", self.onGeometryDispose )

        if hasattr( geometry, "isBufferGeometry" ) :

            buffergeometry = geometry

        elif hasattr( geometry, "isGeometry" ) :

            if not hasattr( geometry, "_bufferGeometry" ) :

                geometry._bufferGeometry = bufferGeometry.BufferGeometry().setFromObject( object )

            buffergeometry = geometry._bufferGeometry

        self.geometries[ geometry.id ] = buffergeometry

        self.infoMemory[ "geometries" ] += 1

        return buffergeometry

    def update( self, geometry ):

        index = geometry.index
        geometryAttributes = geometry.attributes

        if index is not None :

            self.attributes.update( index, GL.GL_ELEMENT_ARRAY_BUFFER )

        for name in geometryAttributes :

            self.attributes.update( geometryAttributes[ name ], GL.GL_ARRAY_BUFFER )

        # morph targets

        morphAttributes = geometry.morphAttributes

        for name in morphAttributes :

            array = morphAttributes[ name ]

            for item in array:

                self.attributes.update( item, GL.GL_ARRAY_BUFFER )

    def getWireframeAttribute( self, geometry ):

        attribute = self.wireframeAttributes[ geometry.id ]

        if attribute : return attribute

        indices = []

        geometryIndex = geometry.index
        geometryAttributes = geometry.attributes

        # console.time( "wireframe" )

        if geometryIndex is not None :

            array = geometryIndex.array

            for i in range( 0, len( array ), 3 ) :

                a = array[ i + 0 ]
                b = array[ i + 1 ]
                c = array[ i + 2 ]

                indices.append( a, b, b, c, c, a )

        else:

            array = geometryAttributes.position.array

            for i in range( 0, ( len( array ) // 3 ) - 1, 3 ) :

                a = i + 0
                b = i + 1
                c = i + 2

                indices.append( a, b, b, c, c, a )

        # console.timeEnd( "wireframe" )

        attribute = ( bufferAttribute.Uint32BufferAttribute if max( indices ) > 65535 else bufferAttribute.Uint16BufferAttribute )( indices, 1 )

        self.attributes.update( attribute, GL.GL_ELEMENT_ARRAY_BUFFER )

        self.wireframeAttributes[ geometry.id ] = attribute

        return attribute
