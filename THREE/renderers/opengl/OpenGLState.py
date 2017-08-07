
from OpenGL.GL import *

import re

from ...constants import NotEqualDepth, GreaterDepth, GreaterEqualDepth, EqualDepth, LessEqualDepth, LessDepth, AlwaysDepth, NeverDepth, CullFaceFront, CullFaceBack, CullFaceNone, CustomBlending, MultiplyBlending, SubtractiveBlending, AdditiveBlending, NoBlending, NormalBlending, DoubleSide, BackSide
from ...math.vector4 import Vector4
from ...utils import Expando
from ...utils import ctypesArray
from ctypes import *

class ColorBuffer( object ):

    def __init__( self ):

        self.locked = False
        self.currentColorMask = None
        self.currentColorClear = Vector4()

    def setMask( self, colorMask ):

        if self.currentColorMask != colorMask and not self.locked:

            glColorMask( colorMask, colorMask, colorMask, colorMask )
            currentColorMask = colorMask

    def setLocked( self, lock ):

        self.locked = lock

    def setClear( self, r, g, b, a, premultipliedAlpha = False ):

        if premultipliedAlpha:

            r *= a
            g *= a
            b *= a
        
        color = Vector4( r, g, b, a )

        if not self.currentColorClear.equals( color ):

            glClearColor( r, g, b, a )
            self.currentColorClear.copy( color )

    def reset( self ):

        self.locked = False

        self.currentColorMask = None
        self.currentColorClear.set( -1, 0, 0, 0 )

class DepthBuffer( object ):

    def __init__( self ):

        self.locked = False
        self.currentDepthMask = None
        self.currentDepthFunc = None
        self.currentDepthClear = None

    def setTest( self, depthTest ):

        if depthTest: enable( GL_DEPTH_TEST )
        else: disable( GL_DEPTH_TEST )

    def setMask( self, depthMask ):

        if self.currentDepthMask != depthMask and not self.locked:

            glDepthMask( depthMask )
            self.currentDepthMask = depthMask
    
    def setFunc( self, depthFunc = LessEqualDepth ):

        if self.currentDepthFunc != depthFunc:

            if depthFunc == NeverDepth: glDepthFunc( GL_NEVER )
            elif depthFunc == AlwaysDepth: glDepthFunc( GL_ALWAYS )
            elif depthFunc == LessDepth: glDepthFunc( GL_LESS )
            elif depthFunc == LessEqualDepth: glDepthFunc( GL_LEQUAL )
            elif depthFunc == EqualDepth: glDepthFunc( GL_EQUAL )
            elif depthFunc == GreaterEqualDepth: glDepthFunc( GL_GEQUAL )
            elif depthFunc == GreaterDepth: glDepthFunc( GL_GREATER )
            elif depthFunc == NotEqualDepth: glDepthFunc( GL_NOTEQUAL )
            else: glDepthFunc( GL_LEQUAL )

            self.currentDepthFunc = depthFunc

    def setLocked( self, lock ):

        self.locked = lock

    def setClear( self, depth ):

        if self.currentDepthClear != depth:

            glClearDepth( depth )
            self.currentDepthClear = depth

    def reset( self ):

        self.locked = False

        self.currentDepthMask = None
        self.currentDepthFunc = None
        self.currentDepthClear = None

###

def initAttributes():

    memset( newAttributes, 0, sizeof( newAttributes ) )

def enableAttribute( attribute ):

    newAttributes[ attribute ] = 1

    if enabledAttributes[ attribute ] == 0:

        glEnableVertexAttribArray( attribute )
        enabledAttributes[ attribute ] = 1

    # TODO extension
    # if attributeDivisors[ attribute] != 0:

# TODO enableAttributeAndDivisor

def disableUnusedAttributes():

    for i in xrange( len( enabledAttributes ) ):

        if enabledAttributes[ i ] != newAttributes[ i ]:

            glDisableVertexAttribArray( i )
            enabledAttributes[ i ] = 0

def enable( id ):

    if not capabilities.get( id, False ):

        glEnable( id )
        capabilities[ id ] = True

def disable( id ):

    if capabilities.get( id, True ):

        glDisable( id )
        capabilities[ id ] = False

def viewport( viewport ):

    if not currentViewport.equals( viewport ):

        glViewport( viewport.x, viewport.y, viewport.z, viewport.w )
        currentViewport.copy( viewport )

def getScissorTest():

    return currentScissorTest

def setScissorTest( scissorTest ):

    global currentScissorTest

    currentScissorTest = scissorTest

    if scissorTest: enable( GL_SCISSOR_TEST )
    else: disable( GL_SCISSOR_TEST )
    

def scissor( scissor ):

    if not currentScissor.equals( scissor ):

        glScissor( scissor.x, scissor.y, scissor.z, scissor.w )
        currentScissor.copy( scissor )

# texture

def createTexture( type, target, count ):

    data = ctypesArray( "B", 4 )
    texture = glGenTextures( 1 )

    glBindTexture( type, texture )
    # glTexParameteri( type, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
    # glTexParamateri( type, GL_TEXTURE_MAX_FILTER, GL_NEAREST )

    for i in xrange( count ):

        glTexImage2D( target + i, 0, GL_RGBA, 1, 1, 0, GL_RGBA, GL_UNSIGNED_BYTE, data )
    
    return texture

def activeTexture( openglSlot = None ):

    global currentTextureSlot

    if openglSlot is None: openglSlot = GL_TEXTURE0 + maxTextures - 1

    if currentTextureSlot != openglSlot:

        glActiveTexture( openglSlot )
        currentTextureSlot = openglSlot

def bindTexture( openglType, openglTexture ):

    if currentTextureSlot is None: activeTexture()

    boundTexture = currentBoundTextures.get( currentTextureSlot )

    if not boundTexture:

        boundTexture = Expando( type = None, texture = None )
        currentBoundTextures[ currentTextureSlot ] = boundTexture

    if boundTexture.type != openglType or boundTexture.texture != openglTexture:

        glBindTexture( openglType, openglTexture or emptyTextures[ openglType ] )

        boundTexture.type = openglType
        boundTexture.texture = openglTexture

def texImage2D( *args ):

    glTexImage2D( *args )

def setBlending( blending, blendEquation = None, blendSrc = None, blendDst = None, 
    blendEquationAlpha = None, blendSrcAlpha = None, blendDstAlpha = None, premultipliedAlpha = False ):

    global currentBlending, currentBlendEquation, currentBlendSrc, currentBlendDst, \
        currentBlendEquationAlpha, currentBlendSrcAlpha, currentBlendDstAlpha, currentPremultipliedAlpha

    if blending != NoBlending: enable( GL_BLEND )
    else: disable( GL_BLEND )

    if blending != CustomBlending:

        if blending != currentBlending or premultipliedAlpha != currentPremultipliedAlpha:

            if   blending == AdditiveBlending:

                if premultipliedAlpha:
                    
                    glBlendEquationSeparate( GL_FUNC_ADD, GL_FUNC_ADD )
                    glBlendFuncSeparate( GL_ONE, GL_ONE, GL_ONE, GL_ONE )

                else:

                    glBlendEquation( GL_FUNC_ADD )
                    glBlendFunc( GL_SRC_ALPHA, GL_ONE )

            elif blending == SubtractiveBlending:

                if premultipliedAlpha:
                    
                    glBlendEquationSeparate( GL_FUNC_ADD, GL_FUNC_ADD )
                    glBlendFuncSeparate( GL_ZERO, GL_ZERO, GL_ONE_MINUS_SRC_COLOR, GL_ONE_MINUS_SRC_ALPHA )

                else:

                    glBlendEquation( GL_FUNC_ADD )
                    glBlendFunc( GL_ZERO, GL_ONE_MINUS_SRC_COLOR )

            elif blending == MultiplyBlending:

                if premultipliedAlpha:
                    
                    glBlendEquationSeparate( GL_FUNC_ADD, GL_FUNC_ADD )
                    glBlendFuncSeparate( GL_ZERO, GL_SRC_COLOR, GL_ZERO, GL_SRC_ALPHA )

                else:

                    glBlendEquation( GL_FUNC_ADD )
                    glBlendFunc( GL_ZERO, GL_SRC_COLOR )

            else:

                if premultipliedAlpha:
                    
                    glBlendEquationSeparate( GL_FUNC_ADD, GL_FUNC_ADD )
                    glBlendFuncSeparate( GL_ONE, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA )

                else:

                    glBlendEquationSeparate( GL_FUNC_ADD, GL_FUNC_ADD )
                    glBlendFuncSeparate( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA )
            
            currentBlendEquation = None
            currentBlendSrc = None
            currentBlendDst = None
            currentBlendEquationAlpha = None
            currentBlendSrcAlpha = None
            currentBlendDstAlpha = None

        else:

            blendEquationAlpha = blendEquationAlpha or blendEquation
            blendSrcAlpha = blendSrcAlpha or blendSrc
            blendDstAlpha = blendDstAlpha or blendDst

            if blendEquation != currentBlendEquation or blendEquationAlpha != currentBlendEquationAlpha:

                glBlendEquationSeparate( utils.convert( blendEquation ), utils.convert( blendEquationAlpha ) )

                currentBlendEquation = blendEquation
                currentBlendEquationAlpha = blendEquationAlpha

            if blendSrc != currentBlendSrc or blendDst != currentBlendDst or \
                blendSrcAlpha != currentBlendSrcAlpha or blendDstAlpha != currentDstAlpha:

                glBlendFuncSeparate( utils.convert( blendSrc ), utils.convert( blendDst ), utils.convert( blendSrcAlpha ), utils.convert( blendDstAlpha ) )

                currentBlendSrc = blendSrc
                currentBlendDst = blendDst
                currentBlendSrcAlpha = blendSrcAlpha
                currentBlendDstAlpha = blendDstAlpha

            currentBlending = blending
            currentPremultipliedAlpha = premultipliedAlpha

def setLineWidth( width ):

    global currentLineWidth

    if width != currentLineWidth:

        if lineWidthAvailable: glLineWidth( width )

        currentLineWidth = width

def setPolygonOffset( polygonOffset, factor = None, units = None ):

    global currentPolygonOffsetFactor, currentPolygonOffsetUnits

    if polygonOffset:

        enable( GL_POLYGON_OFFSET_FILL )

        if currentPolygonOffsetFactor != factor or currentPolygonOffsetUnits != units:

            glPolygonOffset( factor, units )

            currentPolygonOffsetFactor = factor
            currentPolygonOffsetUnits = units
    
    else:

        disable( GL_POLYGON_OFFSET_FILL )

def setMaterial( material ):

    if material.side == DoubleSide: disable( GL_CULL_FACE )
    else: enable( GL_CULL_FACE )

    setFlipSided( material.side == BackSide )

    if material.transparent == True:
        
        setBlending( material.blending, material.blendEquation, material.blendSrc, material.blendDst, 
            material.blendEquationAlpha, material.blendSrcAlpha, material.blendDstAlpha, material.premultipliedAlpha )
    
    else:

        setBlending( NoBlending )

    depthBuffer.setFunc( material.depthFunc )
    depthBuffer.setTest( material.depthTest )
    depthBuffer.setMask( material.depthWrite )
    colorBuffer.setMask( material.colorWrite )

    setPolygonOffset( material.polygonOffset, material.polygonOffsetFactor, material.polygonOffsetUnits )

def setFlipSided( flipSided ):

    global currentFlipSided

    if currentFlipSided != flipSided:

        if flipSided: glFrontFace( GL_CW )
        else: glFrontFace( GL_CCW )

        currentFlipSided = flipSided

def setCullFace( cullFace ):

    global currentCullFace

    if cullFace != CullFaceNone:

        enable( GL_CULL_FACE )

        if cullFace != currentCullFace:

            if cullFace == CullFaceBack: glCullFace( GL_BACK )
            elif cullFace == CullFaceFront: glCullFace( GL_FRONT )
            else: glCullFace( GL_FRONT_AND_BACK )
        
    else:

        disable( GL_CULL_FACE )
    
    currentCullFace = cullFace

def useProgram( program ):

    global currentProgram

    if currentProgram != program:

        glUseProgram( program )

        currentProgram = program

        return True

    return False

colorBuffer = ColorBuffer()
depthBuffer = DepthBuffer()

buffers = Expando(
    color = colorBuffer,
    depth = depthBuffer
)

maxVertexAttributes = None
newAttributes = None
enabledAttributes = None
attributeDivisors = None

capabilities = {}

compressedTextureFormats = None

currentProgram = None

currentBlending = None
currentBlendEquation = None
currentBlendSrc = None
currentBlendDst = None
currentBlendEquationAlpha = None
currentBlendSrcAlpha = None
currentBlendDstAlpha = None
currentPremultipliedAlpha = None

currentFlipSided = None
currentCullFace = None

currentLineWidth = None

currentPolygonOffsetFactor = None
currentPolygonOffsetUnits = None

currentScissorTest = None

maxTextures = None

version = None
lineWidthAvailable = None

currentTextureSlot = None
currentBoundTextures = {}

currentViewport = Vector4()
currentScissor = Vector4()

def init():

    global emptyTextures, maxVertexAttributes, newAttributes, enabledAttributes, maxTextures

    colorBuffer.setClear( 0, 0, 0, 1 )
    depthBuffer.setClear( 1 )

    enable( GL_DEPTH_TEST )
    depthBuffer.setFunc( LessEqualDepth )

    setFlipSided( False )
    setCullFace( CullFaceBack )
    enable( GL_CULL_FACE )

    enable( GL_BLEND )
    setBlending( NormalBlending )

    emptyTextures = {}
    emptyTextures[ GL_TEXTURE_2D ] = createTexture( GL_TEXTURE_2D, GL_TEXTURE_2D, 1 )
    emptyTextures[ GL_TEXTURE_CUBE_MAP ] = createTexture( GL_TEXTURE_CUBE_MAP, GL_TEXTURE_CUBE_MAP_POSITIVE_X, 6 )

    maxVertexAttributes = glGetIntegerv( GL_MAX_VERTEX_ATTRIBS )
    newAttributes = ctypesArray( "B", maxVertexAttributes )
    enabledAttributes = ctypesArray( "B", maxVertexAttributes )

    maxTextures = glGetIntegerv( GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS )

    version = re.match( "([0-9]\.[0-9])", glGetString( GL_VERSION ) ).group( 1 )
    lineWidthAvailable = float( version ) >= 1.0

def reset():

    global capabilities, currentTextureSlot, currentBoundTextures, \
        currentProgram, currentBlending, currentFlipSided, currentCullFace

    for i in xrange( len( enabledAttributes ) ):

        if enabledAttributes[ i ] == 1:

            glDisableVertexAttribArray( i )
            enabledAttributes[ i ] = 0
    
    capabilities = {}

    # compressedTextureFormats = None
    
    currentTextureSlot = None
    currentBoundTextures = None

    currentProgram = None

    currentBlending = None

    currentFlipSided = None
    currentCullFace = None

    colorBuffer.reset()
    depthBuffer.reset()
    # stencilBuffer.reset()
