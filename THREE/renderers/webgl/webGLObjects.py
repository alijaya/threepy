from __future__ import division

import logging

from OpenGL import GL

"""
 * @author mrdoob / "http":#mrdoob.com/
 """

class WebGLObjects( object ):

    def __init__( self, geometries, infoRender ):

        self.geometries = geometries
        self.infoRender = infoRender
        self.updateList = {}

    def update( self, object ):

        frame = self.infoRender[ "frame" ]

        geometry = object.geometry
        buffergeometry = self.geometries.get( object, geometry )

        # Update once per frame

        if self.updateList.get( buffergeometry.id ) != frame :

            if hasattr( geometry, "isGeometry" ) :

                buffergeometry.updateFromObject( object )

            self.geometries.update( buffergeometry )

            self.updateList[ buffergeometry.id ] = frame

        return buffergeometry

    def clear( self ):

        self.updateList = {}