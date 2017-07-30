from __future__ import division

import logging

from OpenGL import GL

"""
 * @author mrdoob / "http":#mrdoob.com/
 """

class WebGLExtensions( object ):

    def __init__( self ):

        self.extensions = {}

    def get( self, name ):

        if name in self.extensions[ name ] :

            return self.extensions[ name ]

        extension = None

        # if name == "WEBGL_depth_texture":
        #     extension = GL.glGetExtension( "WEBGL_depth_texture" ) or GL.glGetExtension( "MOZ_WEBGL_depth_texture" ) or GL.glGetExtension( "WEBKIT_WEBGL_depth_texture" )

        # elif name == "EXT_texture_filter_anisotropic":
        #     extension = GL.glGetExtension( "EXT_texture_filter_anisotropic" ) or GL.glGetExtension( "MOZ_EXT_texture_filter_anisotropic" ) or GL.glGetExtension( "WEBKIT_EXT_texture_filter_anisotropic" )

        # elif name == "WEBGL_compressed_texture_s3tc":
        #     extension = GL.glGetExtension( "WEBGL_compressed_texture_s3tc" ) or GL.glGetExtension( "MOZ_WEBGL_compressed_texture_s3tc" ) or GL.glGetExtension( "WEBKIT_WEBGL_compressed_texture_s3tc" )

        # elif name == "WEBGL_compressed_texture_pvrtc":
        #     extension = GL.glGetExtension( "WEBGL_compressed_texture_pvrtc" ) or GL.glGetExtension( "WEBKIT_WEBGL_compressed_texture_pvrtc" )

        # elif name == "WEBGL_compressed_texture_etc1":
        #     extension = GL.glGetExtension( "WEBGL_compressed_texture_etc1" )

        # else:
        #     extension = GL.glGetExtension( name )

        if extension is None :

            logging.warning( "THREE.WebGLRenderer: %s extension not supported." % name )

        self.extensions[ name ] = extension

        return extension
