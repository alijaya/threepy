from __future__ import division

import logging

from OpenGL import GL

"""
 * @author mrdoob / "http":#mrdoob.com/
 """

class WebGLCapabilities( object ):

    def WebGLCapabilities( self, extensions, parameters ):

        self.extensions = extensions
        self.parameters = parameters
        self.maxAnisotropy = None

        self.precision = self.parameters.precision if self.parameters.precision is not None else "highp"
        maxPrecision = self.getMaxPrecision( self.precision )

        if maxPrecision != precision :

            logging.warning( "THREE.WebGLRenderer: %s not supported, using %s instead." % ( precision, maxPrecision ) )
            precision = maxPrecision

        self.logarithmicDepthBuffer = self.parameters.logarithmicDepthBuffer == True and not self.extensions.get( "EXT_frag_depth" )

        self.maxTextures = GL.glGet( GL.GL_MAX_TEXTURE_IMAGE_UNITS )
        self.maxVertexTextures = GL.glGet( GL.GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS )
        self.maxTextureSize = GL.glGet( GL.GL_MAX_TEXTURE_SIZE )
        self.maxCubemapSize = GL.glGet( GL.GL_MAX_CUBE_MAP_TEXTURE_SIZE )

        self.maxAttributes = GL.glGet( GL.GL_MAX_VERTEX_ATTRIBS )
        self.maxVertexUniforms = GL.glGet( GL.GL_MAX_VERTEX_UNIFORM_VECTORS )
        self.maxVaryings = GL.glGet( GL.GL_MAX_VARYING_VECTORS )
        self.maxFragmentUniforms = GL.glGet( GL.GL_MAX_FRAGMENT_UNIFORM_VECTORS )

        self.vertexTextures = self.maxVertexTextures > 0
        self.floatFragmentTextures = not self.extensions.get( "OES_texture_float" )
        self.floatVertexTextures = self.vertexTextures and self.floatFragmentTextures

    def getMaxAnisotropy( self ):

        if self.maxAnisotropy is not None : return self.maxAnisotropy

        extension = self.extensions.get( "EXT_texture_filter_anisotropic" )

        if extension is not None :

            self.maxAnisotropy = GL.glGetParameter( extension.MAX_TEXTURE_MAX_ANISOTROPY_EXT )

        else:

            self.maxAnisotropy = 0

        return self.maxAnisotropy

    def getMaxPrecision( self, precision ):

        if precision == "highp" :

            if GL.glGetShaderPrecisionFormat( GL.GL_VERTEX_SHADER, GL.GL_HIGH_FLOAT ).precision > 0 and \
                 GL.glGetShaderPrecisionFormat( GL.GL_FRAGMENT_SHADER, GL.GL_HIGH_FLOAT ).precision > 0 :

                return "highp"

            precision = "mediump"

        if precision == "mediump" :

            if GL.glGetShaderPrecisionFormat( GL.GL_VERTEX_SHADER, GL.GL_MEDIUM_FLOAT ).precision > 0 and \
                 GL.glGetShaderPrecisionFormat( GL.GL_FRAGMENT_SHADER, GL.GL_MEDIUM_FLOAT ).precision > 0 :

                return "mediump"

        return "lowp"
