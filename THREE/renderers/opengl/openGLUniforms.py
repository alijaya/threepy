from OpenGL.GL import *

import re
import numbers

import logging

from ...textures import texture
from ...utils import Expando
from ...utils import ctypesArray

emptyTexture = texture.Texture()
# emptyCubeTexture = CubeTexture()

class UniformContainer( object ):

    def __init__( self ):

        self.seq = []
        self.map = {}

# Flattening for arrays of vectors and matrices

def flatten( array, nBlocks, blockSize ):

    firstElem = array[ 0 ]

    if isinstance( firstElem, numbers.Number ): return array

    n = nBlocks * blockSize
    r = ctypesArray( "f", n )

    if nBlocks != 0:

        offset = 0

        for i in xrange( nBlocks ):

            offset += blockSize
            array[ i ].toArray( r, offset )
    
    return r

# --- Uniform Classes ---

class SingleUniform( object ):

    def __init__( self, id, activeInfo, addr ):

        self.id = id
        self.addr = addr

        # def setValue( value ):

        #     print( id, value )
        #     self.getSingularSetter( activeInfo.type )( value )

        # self.setValue = setValue
        self.setValue = self.getSingularSetter( activeInfo.type )

    # Single scalar

    def setValue1f( self, v ): glUniform1f( self.addr, v )
    def setValue1i( self, v ): glUniform1i( self.addr, v )

    # Single float vector (from flat array or THREE.VectorN)

    def setValue2fv( self, v ):
        
        if hasattr( v, "x" ): glUniform2f( self.addr, v.x, v.y )
        else: glUniform2fv( self.addr, 1, v )

    def setValue3fv( self, v ):

        if hasattr( v, "x" ): glUniform3f( self.addr, v.x, v.y, v.z )
        elif hasattr( v, "r" ): glUniform3f( self.addr, v.r, v.g, v.b )
        else: glUniform3fv( self.addr, 1, v )

    def setValue4fv( self, v ):

        if hasattr( v, "x" ): glUniform4f( self.addr, v.x, v.y, v.z, v.w )
        else: glUniform4fv( self.addr, 1, v )

    # Single matrix (from flat array or MatrixN)

    def setValue2fm( self, v ):

        if hasattr( v, "elements" ): glUniformMatrix2fv( self.addr, 1, False, v.elements )
        else: glUniformMatrix2fv( self.addr, 1, False, v )

    def setValue3fm( self, v ):

        if hasattr( v, "elements" ): glUniformMatrix3fv( self.addr, 1, False, v.elements )
        else: glUniformMatrix3fv( self.addr, 1, False, v )

    def setValue4fm( self, v ):

        if hasattr( v, "elements" ): glUniformMatrix4fv( self.addr, 1, False, v.elements )
        else: glUniformMatrix4fv( self.addr, 1, False, v )

    # Single texture (2D / Cube)

    def setValueT1( self, v ):

        from .. import OpenGLRenderer as renderer

        unit = renderer.allocTextureUnit()

        glUniform1i( self.addr, unit )

        renderer.setTexture2D( v or emptyTexture, unit )

    # def setValueT6( self, v ):

    #     from .. import OpenGLRenderer as renderer

    #     unit = renderer.allocTextureUnit()

    #     glUniform1i( self.addr, unit )

    #     renderer.setTextureCube( v or emptyCubeTexture, unit )

    # Helper to pick the right setter for the singular case

    def getSingularSetter( self, type ):

        if   type == 0x1406: return self.setValue1f # FLOAT
        elif type == 0x8b50: return self.setValue2fv # _VEC2
        elif type == 0x8b51: return self.setValue3fv # _VEC3
        elif type == 0x8b52: return self.setValue4fv # _VEC4

        elif type == 0x8b5a: return self.setValue2fm # _MAT2
        elif type == 0x8b5b: return self.setValue3fm # _MAT3
        elif type == 0x8b5c: return self.setValue4fm # _MAT4

        elif type == 0x8b5e or 0x8d66: return self.setValueT1 # SAMPLER_2D, SAMPLER_EXTERNAL_OES
        # elif type == 0x8b60: return setValueT6 # SAMPLER_CUBE

        elif type == 0x1404 or type == 0x8b56: return self.setValue1i # INT, BOOL
        elif type == 0x8b53 or type == 0x8b57: return self.setValue2iv # _VEC2
        elif type == 0x8b54 or type == 0x8b58: return self.setValue3iv # _VEC3
        elif type == 0x8b55 or type == 0x8b59: return self.setValue4iv # _VEC4

class PureArrayUniform( object ):

    def __init__( self, id, activeInfo, addr ):

        self.id = id
        self.addr = addr
        self.size = activeInfo.size
        
        # def setValue( value ):

        #     print( value )
        #     self.getPureArraySetter( activeInfo.type )( value )

        # self.setValue = setValue
        self.setValue = self.getPureArraySetter( activeInfo.type )

    # Array of scalars

    def setValue1fv( self, v ): glUniform1fv( self.addr, v.size, v )
    def setValue1iv( self, v ): glUniform1iv( self.addr, v.size, v )

    # Array of vectors (flat or from THREE classes)

    def setValueV2a( self, v ):
        
        v = flatten( v, self.size, 2 )
        glUniform2fv( self.addr, v.size, v )

    def setValueV3a( self, v ):
        
        v = flatten( v, self.size, 3 )
        glUniform3fv( self.addr, v.size, v )

    def setValueV4a( self, v ):

        v = flatten( v, self.size, 4 )
        glUniform4fv( self.addr, v.size, v )

    # Array of matrices (flat or from THREE classes)

    def setValueM2a( self, v ):
        
        v = flatten( v, self.size, 4 )
        glUniformMatrix2fv( self.addr, v.size, False, v )

    def setValueM3a( self, v ):
        
        v = flatten( v, self.size, 9 )
        glUniformMatrix3fv( self.addr, v.size, False, v )

    def setValueM4a( self, v ):
        
        v = flatten( v, self.size, 16 )
        glUniformMatrix4fv( self.addr, v.size, False, v )

    # Array of textures (2D / Cube)

    def allocTexUnits( self, n ):

        from .. import OpenGLRenderer as renderer

        r = ctypesArray( "L", n )

        for i in xrange( n ):

            r[ i ] = renderer.allocTextureUnit()

    def setValueT1a( self, v ):

        from .. import OpenGLRenderer as renderer

        n = v.length
        units = allocTexUnits( n )

        glUniform1iv( self.addr, units.size, units )

        for i in xrange( n ):

            renderer.setTexture2D( v[ i ] or emptyTexture, units[ i ] )

    # def setValueT6a( self, v ):

    #     from .. import OpenGLRenderer as renderer

    #     n = v.length
    #     units = allocTexUnits( n )

    #     glUniform1iv( self.addr. units.size, units )

    #     for i in xrange( n ):

    #         renderer.setTextureCube( v[ i ] or emptyCubeTexture, units[ i ] )

    # Helper to pick the right setter for a pure (bottom-level) array

    def getPureArraySetter( self, type ):

        if   type == 0x1406: return self.setValue1fv # FLOAT
        elif type == 0x8b50: return self.setValueV2a # _VEC2
        elif type == 0x8b51: return self.setValueV3a # _VEC3
        elif type == 0x8b52: return self.setValueV4a # _VEC4

        elif type == 0x8b5a: return self.setValueM2a # _MAT2
        elif type == 0x8b5b: return self.setValueM3a # _MAT3
        elif type == 0x8b5c: return self.setValueM4a # _MAT4

        elif type == 0x8b5e: return self.setValueT1a # SAMPLER_2D
        # elif type == 0x8b60: return setValueT6a # SAMPLER_CUBE

        elif type == 0x1404 or type == 0x8b56: return self.setValue1iv # INT, BOOL
        elif type == 0x8b53 or type == 0x8b57: return self.setValue2iv # _VEC2
        elif type == 0x8b54 or type == 0x8b58: return self.setValue3iv # _VEC3
        elif type == 0x8b55 or type == 0x8b59: return self.setValue4iv # _VEC4

class StructuredUniform( UniformContainer ):

    def __init__( self, id ):

        self.id = id

        super( StructuredUniform, self ).__init__()

    def setValue( self, value ):

        # Note: Don't need an extra 'renderer' parameter, since samplers
        # are not allowed in structured uniforms.

        for u in self.seq:

            u.setValue( value[ u.id ] )

# --- Top-level ---

def addUniform( container, uniformObject ):

    container.seq.append( uniformObject )
    container.map[ uniformObject.id ] = uniformObject

def parseUniform( activeInfo, addr, container ):

    path = activeInfo.name
    pathLength = len( path )

    for match in re.finditer( "([\w\d_]+)(\])?(\[|\.)?", path ):

        matchEnd = match.end()

        id = match.group( 1 )
        idIsIndex = match.group( 2 ) == "]"
        subscript = match.group( 3 )

        if idIsIndex: id = int( id ) # convert to integer

        if not subscript or subscript == "[" and matchEnd + 2 == pathLength:

            # bare name or "pure" bottom-level array "[0]" suffix

            addUniform( container, ( PureArrayUniform if subscript else SingleUniform )( id, activeInfo, addr ) )

            break

        else:

            # step into inner node / create it in case it doesn't exist

            map = container.map
            next = map.get( id )

            if not next:

                next = StructuredUniform( id )
                addUniform( container, next )

            container = next

class OpenGLUniforms( UniformContainer ):

    def __init__( self, program ):

        super( OpenGLUniforms, self ).__init__()

        n = glGetProgramiv( program, GL_ACTIVE_UNIFORMS )

        for i in xrange( n ):

            info = glGetActiveUniform( program, i )
            info = Expando( name = info[0], size = info[1], type = info[2] )
            path = info.name
            addr = glGetUniformLocation( program, path )

            parseUniform( info, addr, self )

    def setValue( self, name, value ):

        if name in self.map: self.map[ name ].setValue( value )

    def setOptional( self, object, name ):

        if name in self.object: self.setValue( name, self.object[ name ] )

    @staticmethod
    def upload( seq, values ):

        for u in seq:

            v = values[ u.id ]

            if v.needsUpdate != False:

                u.setValue( v.value )

    @staticmethod
    def seqWithValue( seq, values ):

        r = []

        for u in seq:

            if u.id in values: r.append( u )

        return r
