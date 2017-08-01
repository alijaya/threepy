import openGLShader
from ..shaders import ShaderChunk

from OpenGL.GL import *

import re

def parseIncludes( string ):

    pattern = "^[ \t]*#include +<([\w\d.]+)>"

    def replace( match ):

        include = match.group( 1 )

        replace = getattr( ShaderChunk, include )

        if replace is None :

            raise ValueError( "Can not resolve #include <%s>" % include )

        return parseIncludes( replace )

    return re.sub( pattern, replace, string, flags = re.MULTILINE )

def unrollLoops( string ):

    pattern = "for \( int i \= (\d+)\ i < (\d+)\ i \+\+ \) \{([\s\S]+?)(?=\})\}"

    def replace( match ):

        start = match.group( 1 )
        end = match.group( 2 )
        snipper = match.group( 3 )

        unroll = ""

        for i in range( int( start ), int( end ) ) :

            unroll += re.sub( "\[ i \]", "[ %s ]" % i, snippet )

        return unroll

    return re.sub( pattern, replace, string )

class OpenGLProgram( object ):

    def __init__( self, code, material, shader, parameters ):

        defines = getattr( material, "defines", None )
        
        vertexShader = shader["vertexShader"]
        fragmentShader = shader["fragmentShader"]

        # TODO shadowMap

        # TODO envMap

        # TODO customDefines

        self.program = glCreateProgram()

        def text( arr ):

            return "\n".join( filter( lambda v: v != "", arr ) )

        def opt( str, f ):

            return str if f else ""

        prefixVertex = None
        prefixFragment = None

        if hasattr( material, "isRawShaderMaterial" ):

            prefixVertex = text( [
                # customDefines,
                "\n"
            ] )

            prefixFragment = text( [
                # customExtensions,
                # customDefines,
                "\n"
            ] )
        
        else:

            prefixVertex = text( [

                # precision

                "#define SHADER_NAME %s" % shader["name"],
                
                # customDefines

                opt( "#define USE_MAP", parameters[ "map" ] ),

                opt( "#define FLAT_SHADED", parameters[ "flatShading" ] ),

                # etc

                "uniform mat4 modelMatrix;",
                "uniform mat4 modelViewMatrix;",
                "uniform mat4 projectionMatrix;",
                "uniform mat4 viewMatrix;",
                "uniform mat3 normalMatrix;",
                "uniform vec3 cameraPosition;",

                "attribute vec3 position;",
                "attribute vec3 normal;",
                "attribute vec2 uv;",

                "#ifdef USE_COLOR",

                "    attribute vec3 color;",

                "#endif",

                "#ifdef USE_MORPHTARGETS",

                "    attribute vec3 morphTarget0;",
                "    attribute vec3 morphTarget1;",
                "    attribute vec3 morphTarget2;",
                "    attribute vec3 morphTarget3;",

                "    #ifdef USE_MORPHNORMALS",

                "        attribute vec3 morphNormal0;",
                "        attribute vec3 morphNormal1;",
                "        attribute vec3 morphNormal2;",
                "        attribute vec3 morphNormal3;",

                "    #else",

                "        attribute vec3 morphTarget4;",
                "        attribute vec3 morphTarget5;",
                "        attribute vec3 morphTarget6;",
                "        attribute vec3 morphTarget7;",

                "    #endif",

                "#endif",

                "#ifdef USE_SKINNING",

                "    attribute vec4 skinIndex;",
                "    attribute vec4 skinWeight;",

                "#endif",

                "\n"

            ] )

            prefixFragment = text( [

                # customExtensions,

                # precision

                "#define SHADER_NAME %s" % shader["name"],

                # customDefines

                opt( "#define USE_MAP", parameters[ "map" ] ),

                opt( "#define FLAT_SHADED", parameters[ "flatShading" ] ),

                # etc

                "uniform mat4 viewMatrix;",
                "uniform vec3 cameraPosition;",

                "\n"
            ] )

        vertexShader = parseIncludes( vertexShader )
        # vertexShader = replaceLightNums( vertexShader, parameters )

        fragmentShader = parseIncludes( fragmentShader )
        # fragmentShader = replaceLightNums( fragmentShader, parameters )

        if hasattr( material, "isShaderMaterial" ):

            vertexShader = unrollLoops( vertexShader )
            fragmentShader = unrollLoops( fragmentShader )
        
        vertexGlsl = prefixVertex + vertexShader
        fragmentGlsl = prefixFragment + fragmentShader

        print( "*VERTEX*", vertexGlsl )
        print( "*FRAGMENT*", fragmentGlsl )

        glVertexShader = openGLShader.OpenGLShader( GL_VERTEX_SHADER, vertexGlsl )
        glFragmentShader = openGLShader.OpenGLShader( GL_FRAGMENT_SHADER, fragmentGlsl )

        glAttachShader( self.program, glVertexShader )
        glAttachShader( self.program, glFragmentShader )

        # Force a particular attribute to index 0

        # if material.index0AttributeName:

        #     glBindAttribLocation( self.program, 0, "position" )
        
        # TODO morph Target

        glLinkProgram( self.program )

        programLog = glGetProgramInfoLog( self.program )
        vertexLog = glGetShaderInfoLog( glVertexShader )
        fragmentLog = glGetShaderInfoLog( glFragmentShader )

        runnable = True
        haveDiagnostics = True

        # TODO debug code

        # clean up

        glDeleteShader( glVertexShader )
        glDeleteShader( glFragmentShader )

        # TODO caching action

        self.cachedUniforms = None
        self.cachedAttributes = None
    
    def getUniforms( self ):

        if not self.cachedUniforms:

            self.cachedUniforms = OpenGLUniforms( self.program )
        
        return self.cachedUniforms

    def getAttributes( self ):

        if not self.cachedAttributes:

            self.cachedAttributes = self.fetchAttributeLocations( self.program )

        return self.cachedAttributes

    def fetchAttributeLocations( self, program ):

        attributes = {}

        n = glGetProgramiv( program, GL_ACTIVE_ATTRIBUTES )

        for i in range( n ):

            info = glGetActiveAttrib( program, i )
            name = info.name

            attributes[ name ] = glGetAttribLocation( program, name )

        return attributes

    def destroy( self ):

        glDeleteProgram( self.program )