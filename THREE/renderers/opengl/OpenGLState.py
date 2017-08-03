from ...constants import DoubleSide, NeverDepth, AlwaysDepth, LessDepth, LessEqualDepth, EqualDepth, GreaterEqualDepth, GreaterDepth, NotEqualDepth
from ...math.vector4 import Vector4
from ...utils import Expando

from OpenGL.GL import *

import numpy as np

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

    if newAttributes is None:

        global maxVertexAttributes
        global newAttributes
        global enabledAttributes

        maxVertexAttributes = glGetIntegerv( GL_MAX_VERTEX_ATTRIBS )
        newAttributes = np.zeros( maxVertexAttributes )
        enabledAttributes = np.zeros( maxVertexAttributes )

    newAttributes.fill( 0 )

def enableAttribute( attribute ):

    newAttributes[ attribute ] = 1

    if enabledAttributes[ attribute ] == 0:

        glEnableVertexAttribArray( attribute )
        enabledAttributes[ attribute ] = 1

    # TODO extension
    # if attributeDivisors[ attribute] != 0:

# TODO enableAttributeAndDivisor

def disableUnusedAttributes():

    for i in range( enabledAttributes.size ):

        if enabledAttributes[ i ] != newAttributes[ i ]:

            glDisableVertexAttribArray( i )
            enabledAttributes[ i ] = 0

def enable( id ):

    if capabilities.get( id, False ):

        glEnable( id )
        capabilities[ id ] = True

def disable( id ):

    if not capabilities.get( id, False ):

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

def texImage2D( *args ):

    glTexImage2D( *args )

def setMaterial( material ):

    if material.side == DoubleSide: disable( GL_CULL_FACE )
    else: enable( GL_CULL_FACE )

    # TODO setFlipSided

    # TODO material.transparent

    depthBuffer.setFunc( material.depthFunc )
    depthBuffer.setTest( material.depthTest )
    depthBuffer.setMask( material.depthWrite )
    colorBuffer.setMask( material.colorWrite )

    # TODO setPolygonOffset( material.polygonOffset, material.polygonOffsetFactor, material.polygonOffsetUnits )

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

capabilities = {}

currentViewport = Vector4()
currentScissor = Vector4()
currentScissorTest = None

currentProgram = None
