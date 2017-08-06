import openGLShader
from ..shaders.shaderChunk import ShaderChunk
from openGLUniforms import OpenGLUniforms
from ...constants import NoToneMapping, AddOperation, MixOperation, MultiplyOperation, EquirectangularRefractionMapping, CubeRefractionMapping, SphericalReflectionMapping, EquirectangularReflectionMapping, CubeUVRefractionMapping, CubeUVReflectionMapping, CubeReflectionMapping, PCFSoftShadowMap, PCFShadowMap, CineonToneMapping, Uncharted2ToneMapping, ReinhardToneMapping, LinearToneMapping, GammaEncoding, RGBDEncoding, RGBM16Encoding, RGBM7Encoding, RGBEEncoding, sRGBEncoding, LinearEncoding
from ...utils import Expando

from OpenGL.GL import *

import re

import logging

def text( arr ):

    return "\n".join( filter( lambda v: v != "", arr ) )

def opt( str, f ):

    return str if f else ""

def getEncodingComponents( encoding ):

    if   encoding == LinearEncoding: return [ "Linear", "( value )" ]
    elif encoding == sRGBEncoding: return [ "sRGB", "( value )" ]
    elif encoding == RGBEEncoding: return [ "RGBE", "( value )" ]
    elif encoding == RGBM7Encoding: return [ "RGBM", "( value, 7.0 )" ]
    elif encoding == RGBM16Encoding: return [ "RGBM", "( value, 16.0 )" ]
    elif encoding == RGBDEncoding: return [ "RGBD", "( value, 256.0 )" ]
    elif encoding == GammaEncoding: return [ "Gamma", "( value, float( GAMMA_FACTOR ) )" ]
    else: raise ValueError( "unsupported encoding: %s" % encoding )

def getTexelDecodingFunction( functionName, encoding ):

    components = getEncodingComponents( encoding )
    return "vec4 %s( vec4 value ) { return %sToLinear%s; }" % ( functionName, components[ 0 ], components[ 1 ] )

def getTexelEncodingFunction( functionName, encoding ):

    components = getEncodingComponents( encoding )
    return "vec4 %s( vec4 value ) { return LinearTo%s%s; }" % ( functionName, components[ 0 ], components[ 1 ] )

def getToneMappingFunction( functionName, toneMapping ):

    toneMappingName = None

    if   toneMapping == LinearToneMapping: toneMappingName = "Linear"
    elif toneMapping == ReinhardToneMapping: toneMappingName = "Reinhard"
    elif toneMapping == Uncharted2ToneMapping: toneMappingName = "Uncharted2"
    elif toneMapping == CineonToneMapping: toneMappingName = "OptimizedCineon"
    else: raise ValueError( "unsupported toneMapping: %s" % toneMapping )

    return "vec3 %s( vec3 color ) { return %sToneMapping( color ); }" % ( functionName, toneMappingName )

def generateExtensions( extensions, parameters, rendererExtensions ):

    extensions = extensions or Expando()

    chunks = [
        opt( "#extension GL_OES_standard_derivatives : enable", extensions.derivatives or parameters.envMapCubeUV or parameters.bumpMap or parameters.normalMap or parameters.flatShading ),
        opt( "#extension GL_EXT_frag_depth : enable", ( extensions.fragDepth or parameters.logarithmicDepthBuffer ) and rendererExtensions.get( "EXT_frag_depth" ) ),
        opt( "#extension GL_EXT_draw_buffers : require", extensions.drawBuffers and rendererExtensions.get( "WEBGL_draw_buffers" ) ),
        opt( "#extension GL_EXT_shader_texture_lod : enable", ( extensions.shaderTextureLOD or parameters.envMap ) and rendererExtensions.get( "EXT_shader_texture_lod" ) )
    ]

    return text( chunks )

def generateDefines( defines ):

    chunks = []

    for name, value in defines:

        if value == False: continue

        chunks.append( "#define %s %s" % ( name, value ) )

    return text( chunks )

def fetchAttributeLocations( program ):

    attributes = {}

    n = glGetProgramiv( program, GL_ACTIVE_ATTRIBUTES )
    
    # because there's no wrapper for glGetActiveAttrib
    # we hack our way
    bufSize = glGetProgramiv( program, GL_ACTIVE_ATTRIBUTE_MAX_LENGTH )
    length = GLsizei()
    size = GLint()
    type = GLenum()
    name = (GLchar * bufSize)()

    for i in xrange( n ):

        glGetActiveAttrib( program, i, bufSize, length, size, type, name )
        info = Expando( name = name.value, size = size.value, type = type.value )
        nm = info.name

        attributes[ nm ] = glGetAttribLocation( program, nm )

    return attributes

def parseIncludes( string ):

    pattern = "^[ \t]*#include +<([\w\d.]+)>"

    def replace( match ):

        include = match.group( 1 )

        replace = ShaderChunk[ include ]

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

        for i in xrange( int( start ), int( end ) ) :

            unroll += re.sub( "\[ i \]", "[ %s ]" % i, snippet )

        return unroll

    return re.sub( pattern, replace, string )

def replaceLightNums( string, parameters ):

    replace = [ ( "NUM_DIR_LIGHTS", parameters.numDirLights ),
                ( "NUM_SPOT_LIGHTS", parameters.numSpotLights ),
                ( "NUM_RECT_AREA_LIGHTS", parameters.numRectAreaLights ),
                ( "NUM_POINT_LIGHTS", parameters.numPointLights ),
                ( "NUM_HEMI_LIGHTS", parameters.numHemiLights ) ]
    
    return reduce( lambda v, opt: re.sub( opt[ 0 ], str( opt[ 1 ] ), v ), replace, string )

class OpenGLProgram( object ):

    OpenGLProgramId = 0

    @staticmethod
    def getOpenGLProgramId():

        ret = OpenGLProgram.OpenGLProgramId
        OpenGLProgram.OpenGLProgramId += 1
        return ret

    def __init__( self, code, material, shader, parameters ):

        from .. import OpenGLRenderer as renderer

        self.id = OpenGLProgram.getOpenGLProgramId()
        self.code = code
        self.usedTimes = 1
        self.program = glCreateProgram()

        defines = getattr( material, "defines", None )
        
        vertexShader = shader.vertexShader
        fragmentShader = shader.fragmentShader

        # TODO shadowMap

        # TODO envMap

        gammaFactorDefine = renderer.gammaFactor if renderer.gammaFactor > 0 else 1.0

        # TODO customDefines

        prefixVertex = None
        prefixFragment = None

        if material.isRawShaderMaterial:

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

                "#version 120",
                
                "#define SHADER_NAME %s" % shader.name,
                
                # customDefines

                opt( "#define VERTEX_TEXTURES", parameters.supportsVertexTextures ),

                "#define GAMMA_FACTOR %s" % gammaFactorDefine,

                # "#define MAX_BONES %s" % parametes.maxBones,
                opt( "#define USE_FOG", parameters.useFog and parameters.fog ),
                opt( "#define FOG_EXP2", parameters.useFog and parameters.fogExp ),

                opt( "#define USE_MAP", parameters.map ),
                opt( "#define USE_ENVMAP", parameters.envMap ),
                # opt( "#define %s" % envMapTypeDefine, parameters.envMap ),
                # opt( "#define %s" % envMapModeDefine, parameters.envMap ),
                # opt( "#define %s" % envMapBlendingDefine, parameters.envMap ),
                opt( "#define USE_LIGHTMAP", parameters.lightMap ),
                opt( "#define USE_AOMAP", parameters.aoMap ),
                opt( "#define USE_EMISSIVEMAP", parameters.emissiveMap ),
                opt( "#define USE_BUMPMAP", parameters.bumpMap ),
                opt( "#define USE_NORMALMAP", parameters.normalMap ),
                opt( "#define USE_DISPLACEMENTMAP", parameters.displacementMap and parameters.supportsVertexTextures ),
                opt( "#define USE_SPECULARMAP", parameters.specularMap ),
                opt( "#define USE_ROUGHNESSMAP", parameters.roughnessMap ),
                opt( "#define USE_METALNESSMAP", parameters.metalnessMap ),
                opt( "#define USE_ALPHAMAP", parameters.alphaMap ),
                opt( "#define USE_COLOR", parameters.vertexColors ),

                opt( "#define FLAT_SHADED", parameters.flatShading ),

                # opt( "#define USE_SKINNING", parameters.skinning ),
                # opt( "#define BONE_TEXTURE", parameters.useVertexTexture ),

                # opt( "#define USE_MORPHTARGETS", parameters.morphTargets ),
                # opt( "#define USE_MORPHNORMALS", parameters.morphNormals and parameters.flatShading == False ),
                opt( "#define DOUBLE_SIDED", parameters.doubleSided ),
                opt( "#define FLIP_SIDED", parameters.flipSided ),

                "#define NUM_CLIPPING_PLANES %s" % parameters.numClippingPlanes,

                # opt( "#define USE_SHADOWMAP", parameters.shadowMapEnabled ),
                # opt( "#define %s" % shadowMapTypeDefine, parameters.shadowMapEnabled ),

                opt( "#define USE_SIZEATTENUATION", parameters.sizeAttenuation ),

                opt( "#define USE_LOGDEPTHBUF", parameters.logarithmicDepthBuffer ),
                # opt( "#define USE_LOGDEPTHBUF_EXT", parameters.logarithmicDepthBuffer and extensions.get( "EXT_frag_depth" ) ),

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

                "#version 120",
                
                "#define SHADER_NAME %s" % shader.name,

                # customDefines

                opt( "#define ALPHATEST %s" % parameters.alphaTest, parameters.alphaTest ),

                "#define GAMMA_FACTOR %s" % gammaFactorDefine,

                opt( "#define USE_FOG", parameters.useFog and parameters.fog ),
                opt( "#define FOG_EXP2", parameters.useFog and parameters.fogExp ),

                opt( "#define USE_MAP", parameters.map ),
                opt( "#define USE_ENVMAP", parameters.envMap ),
                # opt( "#define %s" % envMapTypeDefine, parameters.envMap ),
                # opt( "#define %s" % envMapModeDefine, parameters.envMap ),
                # opt( "#define %s" % envMapBlendingDefine, parameters.envMap ),
                opt( "#define USE_LIGHTMAP", parameters.lightMap ),
                opt( "#define USE_AOMAP", parameters.aoMap ),
                opt( "#define USE_EMISSIVEMAP", parameters.emissiveMap ),
                opt( "#define USE_BUMPMAP", parameters.bumpMap ),
                opt( "#define USE_NORMALMAP", parameters.normalMap ),
                opt( "#define USE_SPECULARMAP", parameters.specularMap ),
                opt( "#define USE_ROUGHNESSMAP", parameters.roughnessMap ),
                opt( "#define USE_METALNESSMAP", parameters.metalnessMap ),
                opt( "#define USE_ALPHAMAP", parameters.alphaMap ),
                opt( "#define USE_COLOR", parameters.vertexColors ),

                opt( "#define USE_GRADIENTMAP", parameters.gradientMap ),

                opt( "#define FLAT_SHADED", parameters.flatShading ),

                opt( "#define DOUBLE_SIDED", parameters.doubleSided ),
                opt( "#define FLIP_SIDED", parameters.flipSided ),

                "#define NUM_CLIPPING_PLANES %s" % parameters.numClippingPlanes,
                # "#define UNION_CLIPPING_PLANES %s" % ( parameters.numClippingPlanes - parameters.numClipIntersection ),

                # opt( "#define USE_SHADOWMAP", parameters.shadowMapEnabled ),
                # opt( "#define %s" % shadowMapTypeDefine, parameters.shadowMapEnabled ),

                opt( "#define PREMULTIPLIED_ALPHA", parameters.premultipliedAlpha ),

                # opt( "#define PHYSICALLY_CORRECT_LIGHTS", parameters.physicallyCorrectLights ),

                opt( "#define USE_LOGDEPTHBUF", parameters.logarithmicDepthBuffer ),
                # opt( "#define USE_LOGDEPTHBUF_EXT", parameters.logarithmicDepthBuffer and extensions.get( "EXT_frag_depth" ) ),

                # opt( "#define TEXTURE_LOD_EXT", parameters.envMap and extensions.get( "EXT_shader_texture_lod" ) ),

                "uniform mat4 viewMatrix;",
                "uniform vec3 cameraPosition;",

                "#define TONE_MAPPING" if parameters.toneMapping != NoToneMapping else "",
                ShaderChunk[ "tonemapping_pars_fragment" ] if parameters.toneMapping != NoToneMapping else "",
                getToneMappingFunction( "toneMapping", parameters.toneMapping ) if parameters.toneMapping != NoToneMapping else "",

                opt( "#define DITHERING", parameters.dithering ),

                ShaderChunk[ "encodings_pars_fragment" ] if parameters.outputEncoding or parameters.mapEncoding or parameters.envMapEncoding or parameters.emissiveMapEncoding else "",
                getTexelDecodingFunction( "mapTexelToLinear", parameters.mapEncoding ) if parameters.mapEncoding else "",
                getTexelDecodingFunction( "envMapTexelToLinear", parameters.envMapEncoding ) if parameters.envMapEncoding else "",
                getTexelDecodingFunction( "emissiveMapTexelToLinear", parameters.emissiveMapEncoding ) if parameters.emissiveMapEncoding else "",
                getTexelEncodingFunction( "linearToOutputTexel", parameters.outputEncoding ) if parameters.outputEncoding else "",

                opt( "#define DEPTH_PACKING %s" % material.depthPacking, parameters.depthPacking ),

                "\n"
            ] )

        vertexShader = parseIncludes( vertexShader )
        vertexShader = replaceLightNums( vertexShader, parameters )

        fragmentShader = parseIncludes( fragmentShader )
        fragmentShader = replaceLightNums( fragmentShader, parameters )

        if hasattr( material, "isShaderMaterial" ):

            vertexShader = unrollLoops( vertexShader )
            fragmentShader = unrollLoops( fragmentShader )
        
        vertexGlsl = prefixVertex + vertexShader
        fragmentGlsl = prefixFragment + fragmentShader

        # logging.warning( "*VERTEX*\n%s", vertexGlsl )
        # logging.warning( "*FRAGMENT*\n%s", fragmentGlsl )

        self.vertexShader = openGLShader.OpenGLShader( GL_VERTEX_SHADER, vertexGlsl )
        self.fragmentShader = openGLShader.OpenGLShader( GL_FRAGMENT_SHADER, fragmentGlsl )

        glAttachShader( self.program, self.vertexShader )
        glAttachShader( self.program, self.fragmentShader )

        # Force a particular attribute to index 0

        # if material.index0AttributeName:

        #     glBindAttribLocation( self.program, 0, "position" )
        
        # TODO morph Target

        glLinkProgram( self.program )

        programLog = glGetProgramInfoLog( self.program )
        vertexLog = glGetShaderInfoLog( self.vertexShader )
        fragmentLog = glGetShaderInfoLog( self.fragmentShader )

        runnable = True
        haveDiagnostics = True

        # TODO debug code

        # clean up

        glDeleteShader( self.vertexShader )
        glDeleteShader( self.fragmentShader )

        self.cachedUniforms = None
        self.cachedAttributes = None
    
    def getUniforms( self ):

        if not self.cachedUniforms:

            self.cachedUniforms = OpenGLUniforms( self.program )
        
        return self.cachedUniforms

    def getAttributes( self ):

        if not self.cachedAttributes:

            self.cachedAttributes = fetchAttributeLocations( self.program )

        return self.cachedAttributes

    def destroy( self ):

        glDeleteProgram( self.program )