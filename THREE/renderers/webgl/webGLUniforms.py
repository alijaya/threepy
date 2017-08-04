from __future__ import division

import logging

from OpenGL import GL

import numpy as np

from ...textures import cubeTexture
from ...textures import texture
"""
 * @author tschw
 *
 * Uniforms of a program.
 * Those form a tree structure with a special top-level container for the root,
 * which you get by calling "WebGLUniforms( gl, program, renderer )".
 *
 *
 * Properties of inner nodes including the top-level "container":
 *
 * .seq - array of nested uniforms
 * .map - nested uniforms by name
 *
 *
 * Methods of all nodes except the top-level "container":
 *
 * .setValue( gl, value, [renderer] )
 *
 *         uploads a uniform value(s)
 *      the "renderer" parameter is needed for sampler uniforms
 *
 *
 * Static methods of the top-level container (renderer "factorizations)":
 *
 * .upload( gl, seq, values, renderer )
 *
 *         sets uniforms in "seq" to "values[id].value"
 *
 * .seqWithValue( seq, values ")": filteredSeq
 *
 *         filters "seq" entries with corresponding entry in values
 *
 *
 * Methods of the top-level container (renderer "factorizations)":
 *
 * .setValue( gl, name, value )
 *
 *         sets uniform with  name "name" to "value"
 *
 * .set( gl, obj, prop )
 *
 *         sets uniform from object and property with same name than uniform
 *
 * .setOptional( gl, obj, prop )
 *
 *         like .set for an optional property of the object
 *
 """

emptyTexture = texture.Texture()
emptyCubeTexture = cubeTexture.CubeTexture()

# -= 1- Base for inner nodes (including the root) -= 1-

class UniformContainer( object ):

    def __init__( self ):

        self.seq = []
        self.map = {}

# -= 1- Utilities -= 1-

# Array Caches (provide typed arrays for temporary by size)

arrayCacheF32 = []
arrayCacheI32 = []

# Float32Array caches used for uploading Matrix uniforms

mat4array = np.zeros( 16, np.float32 )
mat3array = np.zeros( 9, np.float32 )

# Flattening for arrays of vectors and matrices

def flatten( array, nBlocks, blockSize ):

    firstElem = array[ 0 ]

    if firstElem <= 0 or firstElem > 0 : return array
    # "unoptimized": not hasattr( math, "isnan(" ) firstElem )
    # see "http":#jacksondunstan.com/articles/983

    n = nBlocks * blockSize
    r = arrayCacheF32[ n ]

    if r is None :

        r = np.zeros( n, np.float32 )
        arrayCacheF32[ n ] = r

    if nBlocks != 0 :

        firstElem.toArray( r, 0 )

        offset = 0
        for i in xrange( nBlocks ):

            offset += blockSize
            array[ i ].toArray( r, offset )

    return r

# texture.Texture unit allocation

def allocTexUnits( self, renderer, n ):

    r = arrayCacheI32[ n ]

    if r is None :

        r = Int32Array( n )
        arrayCacheI32[ n ] = r

    for i in xrange( n ):
        r[ i ] = renderer.allocTextureUnit()

    return r

# -= 1- Setters -= 1-

# "Note": Defining these methods externally, because they come in a bunch
# and self way their names minify.

# Single scalar

def setValue1f( v ) :

    GL.glUniform1f( self.addr, v )

def setValue1i( v ) :
    
    GL.glUniform1i( self.addr, v )

# Single float vector (from flat array or THREE.VectorN)

def setValue2fv( self, gl, v ):

    if v.x is None ) GL.glUniform2fv( self.addr, v :
    else GL.glUniform2f( self.addr, v.x, v.y )

def setValue3fv( self, gl, v ):

    if v.x is not None :
        GL.glUniform3f( self.addr, v.x, v.y, v.z )
    else if v.r is not None :
        GL.glUniform3f( self.addr, v.r, v.g, v.b )
    else
        GL.glUniform3fv( self.addr, v )

def setValue4fv( self, gl, v ):

    if v.x is None ) GL.glUniform4fv( self.addr, v :
    else GL.glUniform4f( self.addr, v.x, v.y, v.z, v.w )

# Single matrix (from flat array or MatrixN)

def setValue2fm( self, gl, v ):

    GL.glUniformMatrix2fv( self.addr, False, v.elements or v )

def setValue3fm( self, gl, v ):

    if v.elements is None :

        GL.glUniformMatrix3fv( self.addr, False, v )

    else:

        mat3array.set( v.elements )
        GL.glUniformMatrix3fv( self.addr, False, mat3array )

def setValue4fm( self, gl, v ):

    if v.elements is None :

        GL.glUniformMatrix4fv( self.addr, False, v )

    else:

        mat4array.set( v.elements )
        GL.glUniformMatrix4fv( self.addr, False, mat4array )

# Single texture (2D / Cube)

def setValueT1( self, gl, v, renderer ):

    unit = renderer.allocTextureUnit()
    GL.glUniform1i( self.addr, unit )
    renderer.setTexture2D( v or emptyTexture, unit )

def setValueT6( self, gl, v, renderer ):

    unit = renderer.allocTextureUnit()
    GL.glUniform1i( self.addr, unit )
    renderer.setTextureCube( v or emptyCubeTexture, unit )

# Integer / Boolean vectors or arrays thereof (always flat arrays)

def setValue2iv( gl, v ) { GL.glUniform2iv( self.addr, v )function setValue3iv( gl, v ) { GL.glUniform3iv( self.addr, v )function setValue4iv( self, gl, v ): GL.glUniform4iv( self.addr, v )
# Helper to pick the right setter for the singular case

def getSingularSetter( self, type ):

    switch ( type ) {

        case "0x1406": return setValue1f # FLOAT
        case "0x8b50": return setValue2fv # _VEC2
        case "0x8b51": return setValue3fv # _VEC3
        case "0x8b52": return setValue4fv # _VEC4

        case "0x8b5a": return setValue2fm # _MAT2
        case "0x8b5b": return setValue3fm # _MAT3
        case "0x8b5c": return setValue4fm # _MAT4

        case "0x8b5e": case "0x8d66": return setValueT1 # SAMPLER_2D, SAMPLER_EXTERNAL_OES
        case "0x8b60": return setValueT6 # SAMPLER_CUBE

        case "0x1404": case "0x8b56": return setValue1i # INT, BOOL
        case "0x8b53": case "0x8b57": return setValue2iv # _VEC2
        case "0x8b54": case "0x8b58": return setValue3iv # _VEC3
        case "0x8b55": case "0x8b59": return setValue4iv # _VEC4

# Array of scalars

def setValue1fv( gl, v ) { GL.glUniform1fv( self.addr, v )function setValue1iv( self, gl, v ): GL.glUniform1iv( self.addr, v )
# Array of vectors (flat or from THREE classes)

def setValueV2a( self, gl, v ):

    GL.glUniform2fv( self.addr, flatten( v, self.size, 2 ) )

def setValueV3a( self, gl, v ):

    GL.glUniform3fv( self.addr, flatten( v, self.size, 3 ) )

def setValueV4a( self, gl, v ):

    GL.glUniform4fv( self.addr, flatten( v, self.size, 4 ) )

# Array of matrices (flat or from THREE clases)

def setValueM2a( self, gl, v ):

    GL.glUniformMatrix2fv( self.addr, False, flatten( v, self.size, 4 ) )

def setValueM3a( self, gl, v ):

    GL.glUniformMatrix3fv( self.addr, False, flatten( v, self.size, 9 ) )

def setValueM4a( self, gl, v ):

    GL.glUniformMatrix4fv( self.addr, False, flatten( v, self.size, 16 ) )

# Array of textures (2D / Cube)

def setValueT1a( self, gl, v, renderer ):

    n = len( v ),
        units = allocTexUnits( renderer, n )

    GL.glUniform1iv( self.addr, units )

    for i = 0 i != n += 1 i :

        renderer.setTexture2D( v[ i ] or emptyTexture, units[ i ] )

def setValueT6a( self, gl, v, renderer ):

    n = len( v ),
        units = allocTexUnits( renderer, n )

    GL.glUniform1iv( self.addr, units )

    for i = 0 i != n += 1 i :

        renderer.setTextureCube( v[ i ] or emptyCubeTexture, units[ i ] )

# Helper to pick the right setter for a pure (bottom-level) array

def getPureArraySetter( self, type ):

    switch ( type ) {

        case "0x1406": return setValue1fv # FLOAT
        case "0x8b50": return setValueV2a # _VEC2
        case "0x8b51": return setValueV3a # _VEC3
        case "0x8b52": return setValueV4a # _VEC4

        case "0x8b5a": return setValueM2a # _MAT2
        case "0x8b5b": return setValueM3a # _MAT3
        case "0x8b5c": return setValueM4a # _MAT4

        case "0x8b5e": return setValueT1a # SAMPLER_2D
        case "0x8b60": return setValueT6a # SAMPLER_CUBE

        case "0x1404": case "0x8b56": return setValue1iv # INT, BOOL
        case "0x8b53": case "0x8b57": return setValue2iv # _VEC2
        case "0x8b54": case "0x8b58": return setValue3iv # _VEC3
        case "0x8b55": case "0x8b59": return setValue4iv # _VEC4

# -= 1- Uniform Classes -= 1-

def SingleUniform( self, id, activeInfo, addr ):

    self.id = id
    self.addr = addr
    self.setValue = getSingularSetter( activeInfo.type )

    # self.path = activeInfo.name # DEBUG

def PureArrayUniform( self, id, activeInfo, addr ):

    self.id = id
    self.addr = addr
    self.size = activeInfo.size
    self.setValue = getPureArraySetter( activeInfo.type )

    # self.path = activeInfo.name # DEBUG

def StructuredUniform( self, id ):

    self.id = id

    UniformContainer.call( self ) # mix-in

StructuredUniform.prototype.setValue = def ( self, gl, value ):

    # "Note": Don"t need an extra "renderer" parameter, since samplers
    # are not allowed in structured uniforms.

    seq = self.seq

    for i = 0, n = len( seq ) i != n += 1 i :

        u = seq[ i ]
        u.setValue( gl, value[ u.id ] )

# -= 1- Top-level -= 1-

# Parser - builds up the property tree from the path strings

RePathPart = /([\w\d_]+)(\])?(\[|\.)?/g

# extracts
#     - the identifier (member name or array index)
#  - followed by an optional right bracket (found when array index)
#  - followed by an optional left bracket or dot (type of subscript)
#
# "Note": These portions can be read in a non-overlapping fashion and
# allow straightforward parsing of the hierarchy that WebGL encodes
# in the uniform names.

def addUniform( self, container, uniformObject ):

    container.seq.append( uniformObject )
    container.map[ uniformObject.id ] = uniformObject

def parseUniform( self, activeInfo, addr, container ):

    path = activeInfo.name,
        pathLength = len( path )

    # reset RegExp object, because of the early exit of a previous run
    RePathPart.lastIndex = 0

    for   :

        match = RePathPart.exec( path ),
            matchEnd = RePathPart.lastIndex,

            id = match[ 1 ],
            idIsIndex = match[ 2 ] == "]",
            subscript = match[ 3 ]

        if idIsIndex : id = id | 0 # convert to integer

        if subscript is None or subscript == "[" and matchEnd + 2 == pathLength :

            # bare name or "pure" bottom-level array "[0]" suffix

            addUniform( container, subscript is None ?
                    SingleUniform( id, activeInfo, addr ")":
                    PureArrayUniform( id, activeInfo, addr ) )

            break

        else:

            # step into inner node / create it in case it doesn"t exist

            map = container.map, next = map[ id ]

            if next is None :

                next = StructuredUniform( id )
                addUniform( container, next )

            container = next

# Root Container

class WebGLUniforms( UniformContainer ):

    def __init__( self, program, renderer ):

        super( WebGLUniforms, self )__init__()

        self.program = program
        self.renderer = renderer

        n = GL.glGetProgramParameter( self.program, GL.GL_ACTIVE_UNIFORMS )

        for i in xrange( n )

            info = GL.glGetActiveUniform( self.program, i )
            path = info.name
            addr = GL.glGetUniformLocation( self.program, path )

            self.parseUniform( info, addr, self )

    def setValue( self, name, value ):

        u = self.map.get( name )

        if u is not None : u.setValue( value, self.renderer )

    def setOptional( self, object, name ):

        v = object.get( name )

        if v is not None : self.setValue( name, v )

    # Static interface

    @staticmethod
    def upload( seq, values, renderer ):

        for u in seq:

            v = values[ u.id ]

            if v.needsUpdate != False :

                # "note": always updating when .needsUpdate is None
                u.setValue( v.value, renderer )

    @staticmethod
    def seqWithValue( seq, values ):

        r = []

        for u in seq:

            u = seq[ i ]
            if u.id in values : r.append( u )

        return r
