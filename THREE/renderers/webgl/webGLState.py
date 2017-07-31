from __future__ import division

from array import array
import re

import logging

from OpenGL import GL

from ...constants import NotEqualDepth, GreaterDepth, GreaterEqualDepth, EqualDepth, LessEqualDepth, LessDepth, AlwaysDepth, NeverDepth, CullFaceFront, CullFaceBack, CullFaceNone, CustomBlending, MultiplyBlending, SubtractiveBlending, AdditiveBlending, NoBlending, NormalBlending, DoubleSide, BackSide
from ...math import vector4
"""
 * @author mrdoob / "http":#mrdoob.com/
 """

class WebGLState( object ):

    def WebGLState( self, extensions, utils ):

        self.extensions = extensions
        self.utils = utils

        self.colorBuffer = ColorBuffer()
        self.depthBuffer = DepthBuffer()
        self.stencilBuffer = StencilBuffer()

        self.buffers = {
            "color": self.colorBuffer,
            "depth": self.depthBuffer,
            "stencil": self.stencilBuffer
        }

        self.maxVertexAttributes = GL.glGetIntegerv( GL.GL_MAX_VERTEX_ATTRIBS )
        self.newAttributes = array( "B", self.maxVertexAttributes )
        self.enabledAttributes = array( "B", self.maxVertexAttributes )
        self.attributeDivisors = array( "B", self.maxVertexAttributes )

        self.capabilities = {}
        self.compressedTextureFormats = None

        self.currentProgram = None

        self.currentBlending = None
        self.currentBlendEquation = None
        self.currentBlendSrc = None
        self.currentBlendDst = None
        self.currentBlendEquationAlpha = None
        self.currentBlendSrcAlpha = None
        self.currentBlendDstAlpha = None
        self.currentPremultipledAlpha = False

        self.currentFlipSided = None
        self.currentCullFace = None

        self.currentLineWidth = None

        self.currentPolygonOffsetFactor = None
        self.currentPolygonOffsetUnits = None

        self.currentScissorTest = None

        self.maxTextures = GL.glGetParameter( GL.GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS )

        self.version = float( re.match( "WebGL\ ([0-9])", GL.glGetString( GL.GL_VERSION ) ).groups( 1 ) )
        self.lineWidthAvailable = float( self.version ) >= 1.0

        self.currentTextureSlot = None
        self.currentBoundTextures = {}
        self.currentScissor = vector4.Vector4()
        self.currentViewport = vector4.Vector4()

        self.emptyTextures = {}
        self.emptyTextures[ GL.GL_TEXTURE_2D ] = self.createTexture( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_2D, 1 )
        self.emptyTextures[ GL.GL_TEXTURE_CUBE_MAP ] = self.createTexture( GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X, 6 )

        # init

        self.colorBuffer.setClear( 0, 0, 0, 1 )
        self.depthBuffer.setClear( 1 )
        self.stencilBuffer.setClear( 0 )

        self.enable( GL.GL_DEPTH_TEST )
        self.depthBuffer.setFunc( LessEqualDepth )

        self.setFlipSided( False )
        self.setCullFace( CullFaceBack )
        self.enable( GL.GL_CULL_FACE )

        self.enable( GL.GL_BLEND )
        self.setBlending( NormalBlending )

    #

    def createTexture( self, type, target, count ):

        data = array( "B", [0] * 4 ) # 4 is required to match default unpack alignment of 4.
        texture = GL.glCreateTexture()

        GL.glBindTexture( type, texture )
        GL.glTexParameteri( type, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST )
        GL.glTexParameteri( type, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST )

        for i in range( count ):

            GL.glTexImage2D( target + i, 0, GL.GL_RGBA, 1, 1, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, data )

        return texture

    def initAttributes( self ):

        for i in range( len( self.newAttributes ) ) :

            self.newAttributes[ i ] = 0

    def enableAttribute( self, attribute ):

        self.newAttributes[ attribute ] = 1

        if self.enabledAttributes[ attribute ] == 0 :

            GL.glEnableVertexAttribArray( attribute )
            self.enabledAttributes[ attribute ] = 1

        if self.attributeDivisors[ attribute ] != 0 :

            extension = self.extensions.get( "ANGLE_instanced_arrays" )

            extension.vertexAttribDivisorANGLE( attribute, 0 )
            self.attributeDivisors[ attribute ] = 0

    def enableAttributeAndDivisor( self, attribute, meshPerAttribute ):

        self.newAttributes[ attribute ] = 1

        if self.enabledAttributes[ attribute ] == 0 :

            GL.glEnableVertexAttribArray( attribute )
            self.enabledAttributes[ attribute ] = 1

        if self.attributeDivisors[ attribute ] != meshPerAttribute :

            extension = extensions.get( "ANGLE_instanced_arrays" )

            extension.vertexAttribDivisorANGLE( attribute, meshPerAttribute )
            self.attributeDivisors[ attribute ] = meshPerAttribute

    def disableUnusedAttributes( self ):

        for i in range( len( self.enabledAttributes ) ) :

            if self.enabledAttributes[ i ] != self.newAttributes[ i ] :

                GL.glDisableVertexAttribArray( i )
                self.enabledAttributes[ i ] = 0

    def enable( self, id ):

        if self.capabilities[ id ] != True :

            GL.glEnable( id )
            self.capabilities[ id ] = True

    def disable( self, id ):

        if self.capabilities[ id ] != False :

            GL.glDisable( id )
            self.capabilities[ id ] = False

    def getCompressedTextureFormats( self ):

        if self.compressedTextureFormats is None :

            self.compressedTextureFormats = []

            if extensions.get( "WEBGL_compressed_texture_pvrtc" ) or \
                 extensions.get( "WEBGL_compressed_texture_s3tc" ) or \
                 extensions.get( "WEBGL_compressed_texture_etc1" ) :

                formats = GL.glGetParameter( GL.GL_COMPRESSED_TEXTURE_FORMATS )

                for format in formats:

                    self.compressedTextureFormats.append( format )

        return self.compressedTextureFormats

    def useProgram( self, program ):

        if self.currentProgram != program :

            GL.glUseProgram( program )

            self.currentProgram = program

            return True

        return False

    def setBlending( self, blending, blendEquation, blendSrc, blendDst, blendEquationAlpha, blendSrcAlpha, blendDstAlpha, premultipliedAlpha ):

        if blending != NoBlending :

            self.enable( GL.GL_BLEND )

        else:

            self.disable( GL.GL_BLEND )

        if blending != CustomBlending :

            if blending != self.currentBlending or premultipliedAlpha != self.currentPremultipledAlpha :

                if blending == AdditiveBlending:

                    if premultipliedAlpha :

                        GL.glBlendEquationSeparate( GL.GL_FUNC_ADD, GL.GL_FUNC_ADD )
                        GL.glBlendFuncSeparate( GL.GL_ONE, GL.GL_ONE, GL.GL_ONE, GL.GL_ONE )

                    else:

                        GL.glBlendEquation( GL.GL_FUNC_ADD )
                        GL.glBlendFunc( GL.GL_SRC_ALPHA, GL.GL_ONE )

                elif blending == SubtractiveBlending:

                    if premultipliedAlpha :

                        GL.glBlendEquationSeparate( GL.GL_FUNC_ADD, GL.GL_FUNC_ADD )
                        GL.glBlendFuncSeparate( GL.GL_ZERO, GL.GL_ZERO, GL.GL_ONE_MINUS_SRC_COLOR, GL.GL_ONE_MINUS_SRC_ALPHA )

                    else:

                        GL.glBlendEquation( GL.GL_FUNC_ADD )
                        GL.glBlendFunc( GL.GL_ZERO, GL.GL_ONE_MINUS_SRC_COLOR )

                elif blending == MultiplyBlending:

                    if premultipliedAlpha :

                        GL.glBlendEquationSeparate( GL.GL_FUNC_ADD, GL.GL_FUNC_ADD )
                        GL.glBlendFuncSeparate( GL.GL_ZERO, GL.GL_SRC_COLOR, GL.GL_ZERO, GL.GL_SRC_ALPHA )

                    else:

                        GL.glBlendEquation( GL.GL_FUNC_ADD )
                        GL.glBlendFunc( GL.GL_ZERO, GL.GL_SRC_COLOR )

                else:

                    if premultipliedAlpha :

                        GL.glBlendEquationSeparate( GL.GL_FUNC_ADD, GL.GL_FUNC_ADD )
                        GL.glBlendFuncSeparate( GL.GL_ONE, GL.GL_ONE_MINUS_SRC_ALPHA, GL.GL_ONE, GL.GL_ONE_MINUS_SRC_ALPHA )

                    else:

                        GL.glBlendEquationSeparate( GL.GL_FUNC_ADD, GL.GL_FUNC_ADD )
                        GL.glBlendFuncSeparate( GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA, GL.GL_ONE, GL.GL_ONE_MINUS_SRC_ALPHA )

            self.currentBlendEquation = None
            self.currentBlendSrc = None
            self.currentBlendDst = None
            self.currentBlendEquationAlpha = None
            self.currentBlendSrcAlpha = None
            self.currentBlendDstAlpha = None

        else:

            blendEquationAlpha = blendEquationAlpha or blendEquation
            blendSrcAlpha = blendSrcAlpha or blendSrc
            blendDstAlpha = blendDstAlpha or blendDst

            if blendEquation != self.currentBlendEquation or blendEquationAlpha != self.currentBlendEquationAlpha :

                GL.glBlendEquationSeparate( utils.convert( blendEquation ), utils.convert( blendEquationAlpha ) )

                self.currentBlendEquation = blendEquation
                self.currentBlendEquationAlpha = blendEquationAlpha

            if blendSrc != self.currentBlendSrc or blendDst != self.currentBlendDst or blendSrcAlpha != self.currentBlendSrcAlpha or blendDstAlpha != self.currentBlendDstAlpha :

                GL.glBlendFuncSeparate( utils.convert( blendSrc ), utils.convert( blendDst ), utils.convert( blendSrcAlpha ), utils.convert( blendDstAlpha ) )

                self.currentBlendSrc = blendSrc
                self.currentBlendDst = blendDst
                self.currentBlendSrcAlpha = blendSrcAlpha
                self.currentBlendDstAlpha = blendDstAlpha

        self.currentBlending = blending
        self.currentPremultipledAlpha = premultipliedAlpha

    def setMaterial( self, material ):

        if material.side == DoubleSide:

            self.disable( GL.GL_CULL_FACE )

        else:

            self.enable( GL.GL_CULL_FACE )

        self.setFlipSided( material.side == BackSide )

        if material.transparent == True:

            self.setBlending( material.blending, material.blendEquation, material.blendSrc, material.blendDst, material.blendEquationAlpha, material.blendSrcAlpha, material.blendDstAlpha, material.premultipliedAlpha )
        
        else:

            self.setBlending( NoBlending )

        self.depthBuffer.setFunc( material.depthFunc )
        self.depthBuffer.setTest( material.depthTest )
        self.depthBuffer.setMask( material.depthWrite )
        self.colorBuffer.setMask( material.colorWrite )

        self.setPolygonOffset( material.polygonOffset, material.polygonOffsetFactor, material.polygonOffsetUnits )

    #

    def setFlipSided( self, flipSided ):

        if self.currentFlipSided != flipSided :

            if flipSided :

                GL.glFrontFace( GL.GL_CW )

            else:

                GL.glFrontFace( GL.GL_CCW )

            self.currentFlipSided = flipSided

    def setCullFace( self, cullFace ):

        if cullFace != CullFaceNone :

            self.enable( GL.GL_CULL_FACE )

            if cullFace != self.currentCullFace :

                if cullFace == CullFaceBack :

                    GL.glCullFace( GL.GL_BACK )

                elif cullFace == CullFaceFront :

                    GL.glCullFace( GL.GL_FRONT )

                else:

                    GL.glCullFace( GL.GL_FRONT_AND_BACK )

        else:

            self.disable( GL.GL_CULL_FACE )

        self.currentCullFace = cullFace

    def setLineWidth( self, width ):

        if width != self.currentLineWidth :

            if self.lineWidthAvailable : GL.glLineWidth( width )

            self.currentLineWidth = width

    def setPolygonOffset( self, polygonOffset, factor, units ):

        if polygonOffset :

            self.enable( GL.GL_POLYGON_OFFSET_FILL )

            if self.currentPolygonOffsetFactor != factor or self.currentPolygonOffsetUnits != units :

                GL.glPolygonOffset( factor, units )

                self.currentPolygonOffsetFactor = factor
                self.currentPolygonOffsetUnits = units

        else:

            self.disable( GL.GL_POLYGON_OFFSET_FILL )

    def getScissorTest( self ):

        return self.currentScissorTest

    def setScissorTest( self, scissorTest ):

        self.currentScissorTest = scissorTest

        if scissorTest :

            self.enable( GL.GL_SCISSOR_TEST )

        else:

            self.disable( GL.GL_SCISSOR_TEST )

    # texture

    def activeTexture( self, webglSlot ):

        if webglSlot is None : webglSlot = GL.GL_TEXTURE0 + self.maxTextures - 1

        if self.currentTextureSlot != webglSlot :

            GL.glActiveTexture( webglSlot )
            self.currentTextureSlot = webglSlot

    def bindTexture( self, webglType, webglTexture ):

        if self.currentTextureSlot is None :

            self.activeTexture()

        boundTexture = self.currentBoundTextures[ self.currentTextureSlot ]

        if boundTexture is None :

            boundTexture = { "type": None, "texture": None }
            self.currentBoundTextures[ self.currentTextureSlot ] = boundTexture

        if boundTexture.type != webglType or boundTexture.texture != webglTexture :

            GL.glBindTexture( webglType, webglTexture or self.emptyTextures[ webglType ] )

            boundTexture.type = webglType
            boundTexture.texture = webglTexture

    def compressedTexImage2D( self, *args ):

        try:

            GL.glCompressedTexImage2D( *args )

        except Exception as error:

            logging.error( "THREE.WebGLState: %s" % error )

    def texImage2D( self, *args ):

        try:

            GL.glTexImage2D( *args )

        except Exception as error:

            logging.error( "THREE.WebGLState: %s" % error )

    #

    def scissor( self, scissor ):

        if self.currentScissor.equals( scissor ) == False :

            GL.glScissor( scissor.x, scissor.y, scissor.z, scissor.w )
            self.currentScissor.copy( scissor )

    def viewport( self, viewport ):

        if self.currentViewport.equals( viewport ) == False :

            GL.glViewport( viewport.x, viewport.y, viewport.z, viewport.w )
            self.currentViewport.copy( viewport )

    #

    def reset( self ):

        for i in range( len( self.enabledAttributes ) ) :

            if self.enabledAttributes[ i ] == 1 :

                GL.glDisableVertexAttribArray( i )
                self.enabledAttributes[ i ] = 0

        self.capabilities = {}
        self.compressedTextureFormats = None

        self.currentTextureSlot = None
        self.currentBoundTextures = {}
        self.currentProgram = None

        self.currentBlending = None

        self.currentFlipSided = None
        self.currentCullFace = None

        self.colorBuffer.reset()
        self.depthBuffer.reset()
        self.stencilBuffer.reset()

class ColorBuffer( object ):

    def __init__( self ):

        self.locked = False

        self.color = vector4.Vector4()
        self.currentColorMask = None
        self.currentColorClear = vector4.Vector4( 0, 0, 0, 0 )

    def setMask( self, colorMask ):

        if self.currentColorMask != colorMask and not self.locked :

            GL.glColorMask( colorMask, colorMask, colorMask, colorMask )
            self.currentColorMask = colorMask

    def setLocked( self, lock ):

        self.locked = lock

    def setClear( self, r, g, b, a, premultipliedAlpha ):

        if premultipliedAlpha == True :

            r *= a
            g *= a
            b *= a

        self.color.set( r, g, b, a )

        if self.currentColorClear.equals( self.color ) == False :

            GL.glClearColor( r, g, b, a )
            self.currentColorClear.copy( self.color )

    def reset( self ):

        self.locked = False

        self.currentColorMask = None
        self.currentColorClear.set( - 1, 0, 0, 0 ) # set to invalid state

class DepthBuffer( object ):

    def __init__( self ):

        self.locked = False

        self.currentDepthMask = None
        self.currentDepthFunc = None
        self.currentDepthClear = None

    def setTest( self, depthTest ):

        if depthTest :

            self.enable( GL.GL_DEPTH_TEST )

        else:

            self.disable( GL.GL_DEPTH_TEST )

    def setMask( self, depthMask ):

        if self.currentDepthMask != depthMask and not self.locked :

            GL.glDepthMask( depthMask )
            self.currentDepthMask = depthMask

    def setFunc( self, depthFunc ):

        if self.currentDepthFunc != depthFunc :

            if depthFunc :

                if depthFunc == NeverDepth:

                    GL.glDepthFunc( GL.GL_NEVER )

                elif depthFunc == AlwaysDepth:

                    GL.glDepthFunc( GL.GL_ALWAYS )

                elif depthFunc == LessDepth:

                    GL.glDepthFunc( GL.GL_LESS )

                elif depthFunc == LessEqualDepth:

                    GL.glDepthFunc( GL.GL_LEQUAL )

                elif depthFunc == EqualDepth:

                    GL.glDepthFunc( GL.GL_EQUAL )

                elif depthFunc == GreaterEqualDepth:

                    GL.glDepthFunc( GL.GL_GEQUAL )

                elif depthFunc == GreaterDepth:

                    GL.glDepthFunc( GL.GL_GREATER )

                elif depthFunc == NotEqualDepth:

                    GL.glDepthFunc( GL.GL_NOTEQUAL )

                else:

                    GL.glDepthFunc( GL.GL_LEQUAL )

            else:

                GL.glDepthFunc( GL.GL_LEQUAL )

            self.currentDepthFunc = depthFunc

    def setLocked( self, lock ):

        self.locked = lock

    def setClear( self, depth ):

        if self.currentDepthClear != depth :

            GL.glClearDepth( depth )
            self.currentDepthClear = depth

    def reset( self ):

        self.locked = False

        self.currentDepthMask = None
        self.currentDepthFunc = None
        self.currentDepthClear = None

class StencilBuffer( object ):

    def __init__( self ):

        self.locked = False

        self.currentStencilMask = None
        self.currentStencilFunc = None
        self.currentStencilRef = None
        self.currentStencilFuncMask = None
        self.currentStencilFail = None
        self.currentStencilZFail = None
        self.currentStencilZPass = None
        self.currentStencilClear = None

    def setTest( self, stencilTest ):

        if stencilTest :

            self.enable( GL.GL_STENCIL_TEST )

        else:

            self.disable( GL.GL_STENCIL_TEST )

    def setMask( self, stencilMask ):

        if self.currentStencilMask != stencilMask and not self.locked :

            GL.glStencilMask( stencilMask )
            self.currentStencilMask = stencilMask

    def setFunc( self, stencilFunc, stencilRef, stencilMask ):

        if  self.currentStencilFunc != stencilFunc or \
            self.currentStencilRef != stencilRef or \
            self.currentStencilFuncMask != stencilMask :

            GL.glStencilFunc( stencilFunc, stencilRef, stencilMask )

            self.currentStencilFunc = stencilFunc
            self.currentStencilRef = stencilRef
            self.currentStencilFuncMask = stencilMask

    def setOp( self, stencilFail, stencilZFail, stencilZPass ):

        if  self.currentStencilFail != stencilFail or \
            self.currentStencilZFail != stencilZFail or \
            self.currentStencilZPass != stencilZPass :

            GL.glStencilOp( stencilFail, stencilZFail, stencilZPass )

            self.currentStencilFail = stencilFail
            self.currentStencilZFail = stencilZFail
            self.currentStencilZPass = stencilZPass

    def setLocked( self, lock ):

        self.locked = lock

    def setClear( self, stencil ):

        if self.currentStencilClear != stencil :

            GL.glClearStencil( stencil )
            self.currentStencilClear = stencil

    def reset( self ):

        self.locked = False

        self.currentStencilMask = None
        self.currentStencilFunc = None
        self.currentStencilRef = None
        self.currentStencilFuncMask = None
        self.currentStencilFail = None
        self.currentStencilZFail = None
        self.currentStencilZPass = None
        self.currentStencilClear = None

#
