from __future__ import division

import logging

from OpenGL import GL

"""
 * @author fordacious / fordacious.github.io
 """

class WebGLProperties( object ):

    def __init__( self ):

        properties = {}

    def get( self, object ):

        uuid = object.uuid
        map = properties.get( uuid )

        if map is None :

            map = {}
            properties[ uuid ] = map

        return map

    def remove( self, object ):

        del properties[ object.uuid ]

    def clear( self ):

        properties = {}
