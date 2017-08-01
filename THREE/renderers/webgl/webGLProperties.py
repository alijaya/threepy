from __future__ import division

import logging

from OpenGL import GL

"""
 * @author fordacious / fordacious.github.io
 """

class WebGLProperties( object ):

    def __init__( self ):

        self.properties = {}

    def get( self, object ):

        uuid = object.uuid
        map = self.properties.get( uuid )

        if map is None :

            map = {}
            self.properties[ uuid ] = map

        return map

    def remove( self, object ):

        del self.properties[ object.uuid ]

    def clear( self ):

        self.properties = {}
