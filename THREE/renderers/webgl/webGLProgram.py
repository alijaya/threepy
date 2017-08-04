from __future__ import division

import logging

from OpenGL import GL

import re

import webGLUniforms
import webGLShader
from ..shaders import shaderChunk
from ...constants import NoToneMapping, AddOperation, MixOperation, MultiplyOperation, EquirectangularRefractionMapping, CubeRefractionMapping, SphericalReflectionMapping, EquirectangularReflectionMapping, CubeUVRefractionMapping, CubeUVReflectionMapping, CubeReflectionMapping, PCFSoftShadowMap, PCFShadowMap, CineonToneMapping, Uncharted2ToneMapping, ReinhardToneMapping, LinearToneMapping, GammaEncoding, RGBDEncoding, RGBM16Encoding, RGBM7Encoding, RGBEEncoding, sRGBEncoding, LinearEncoding
"""
 * @author mrdoob / "http":#mrdoob.com/
 """

programIdCount = 0

def getEncodingComponents( self, encoding ):

    if encoding == LinearEncoding:
        return [ "Linear","( value )" ]
    elif encoding == sRGBEncoding:
        return [ "sRGB","( value )" ]
    elif encoding == RGBEEncoding:
        return [ "RGBE","( value )" ]
    elif encoding == RGBM7Encoding:
        return [ "RGBM","( value, 7.0 )" ]
    elif encoding == RGBM16Encoding:
        return [ "RGBM","( value, 16.0 )" ]
    elif encoding == RGBDEncoding:
        return [ "RGBD","( value, 256.0 )" ]
    elif encoding == GammaEncoding:
        return [ "Gamma","( value, float( GAMMA_FACTOR ) )" ]
    else:
        raise ValueError( "unsupported encoding: %s" % encoding )

def getTexelDecodingFunction( self, functionName, encoding ):

    components = getEncodingComponents( encoding )
    return "vec4 %s( vec4 value ): return %sToLinear%s }" % ( functionName, components[ 0 ], components[ 1 ] )

def getTexelEncodingFunction( self, functionName, encoding ):

    components = getEncodingComponents( encoding )
    return "vec4 %s( vec4 value ): return LinearTo%s%s }" % ( functionName, components[ 0 ], components[ 1 ] )

def getToneMappingFunction( self, functionName, toneMapping ):

    toneMappingName = None

    if toneMapping == LinearToneMapping:
        toneMappingName = "Linear"

    elif toneMapping == ReinhardToneMapping:
        toneMappingName = "Reinhard"

    elif toneMapping == Uncharted2ToneMapping:
        toneMappingName = "Uncharted2"

    elif toneMapping == CineonToneMapping:
        toneMappingName = "OptimizedCineon"

    else:
        raise ValueError( "unsupported toneMapping: %s" % toneMapping )

    return "vec3 %s( vec3 color ): return %sToneMapping( color ) }" % ( functionName, toneMappingName )

def generateExtensions( extensions, parameters, rendererExtensions ):

    extensions = extensions or {}
    chunks = [
        "#extension GL_OES_standard_derivatives: enable" if ( extensions.derivatives or parameters.envMapCubeUV or parameters.bumpMap or parameters.normalMap or parameters.flatShading ) else "",
        "#extension GL_EXT_frag_depth: enable" if ( extensions.fragDepth or parameters.logarithmicDepthBuffer ) and rendererExtensions.get( "EXT_frag_depth" ) else "",
        "#extension GL_EXT_draw_buffers: require" if ( extensions.drawBuffers ) and rendererExtensions.get( "WEBGL_draw_buffers" ) else "",
        "#extension GL_EXT_shader_texture_lod: enable" if ( extensions.shaderTextureLOD or parameters.envMap ) and rendererExtensions.get( "EXT_shader_texture_lod" ) else ""
    ]

    return "\n".join( chunks.filter( filterEmptyLine ) )

def generateDefines( defines ):

    chunks = []

    for name in defines :

        value = defines[ name ]

        if value == False : continue

        chunks.append( "#define " + name + " " + value )

    return "\n".join( chunks )

def fetchAttributeLocations( self, program, identifiers ):

    attributes = {}
    n = GL.glGetProgramParameter( program, GL.GL_ACTIVE_ATTRIBUTES )

    for i in xrange( n ):

        info = GL.glGetActiveAttrib( program, i )
        name = info.name

        # "logging.info("THREE.WebGLProgram": ACTIVE VERTEX "ATTRIBUTE":", name, i )

        attributes[ name ] = GL.glGetAttribLocation( program, name )

    return attributes

def filterEmptyLine( self, string ):

    return string != ""

def replaceLightNums( self, string, parameters ):

    string = re.sub( "NUM_DIR_LIGHTS", parameters.numDirLights, string )
    string = re.sub( "NUM_SPOT_LIGHTS", parameters.numSpotLights, string )
    string = re.sub( "NUM_RECT_AREA_LIGHTS", parameters.numRectAreaLights, string )
    string = re.sub( "NUM_POINT_LIGHTS", parameters.numPointLights, string )
    string = re.sub( "NUM_HEMI_LIGHTS", parameters.numHemiLights, string )

    return string

def parseIncludes( string ):

    pattern = "^[ \t]*#include +<([\w\d.]+)>"

    def replace( match ):

        include = match.group( 1 )

        replace = shaderChunk.ShaderChunk[ include ]

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

class WebGLProgram( object ):

    def __init__( self, renderer, extensions, code, material, shader, parameters ):

        self.renderer = renderer
        self.extensions = extensions
        self.code = code
        self.material = material
        self.shader = shader
        self.parameters = parameters

        defines = self.material.defines

        self.vertexShader = self.shader.vertexShader
        self.fragmentShader = self.shader.fragmentShader

        shadowMapTypeDefine = "SHADOWMAP_TYPE_BASIC"

        if self.parameters.shadowMapType == PCFShadowMap :

            shadowMapTypeDefine = "SHADOWMAP_TYPE_PCF"

        elif self.parameters.shadowMapType == PCFSoftShadowMap :

            shadowMapTypeDefine = "SHADOWMAP_TYPE_PCF_SOFT"

        envMapTypeDefine = "ENVMAP_TYPE_CUBE"
        envMapModeDefine = "ENVMAP_MODE_REFLECTION"
        envMapBlendingDefine = "ENVMAP_BLENDING_MULTIPLY"

        if self.parameters.envMap :

            mapping = self.material.envMap.mapping

            if mapping == CubeReflectionMapping or \
               mapping == CubeRefractionMapping:
                envMapTypeDefine = "ENVMAP_TYPE_CUBE"

            elif mapping == CubeUVReflectionMapping or \
                 mapping == CubeUVRefractionMapping:
                envMapTypeDefine = "ENVMAP_TYPE_CUBE_UV"

            elif mapping == EquirectangularReflectionMapping or \
                 mapping == EquirectangularRefractionMapping:
                envMapTypeDefine = "ENVMAP_TYPE_EQUIREC"

            elif mapping == SphericalReflectionMapping:
                envMapTypeDefine = "ENVMAP_TYPE_SPHERE"

            if mapping == CubeRefractionMapping or \
               mapping == EquirectangularRefractionMapping:
                envMapModeDefine = "ENVMAP_MODE_REFRACTION"

            combine = self.material.combine

            if combine == MultiplyOperation:
                envMapBlendingDefine = "ENVMAP_BLENDING_MULTIPLY"

            elif combine == MixOperation:
                envMapBlendingDefine = "ENVMAP_BLENDING_MIX"

            elif combine == AddOperation:
                envMapBlendingDefine = "ENVMAP_BLENDING_ADD"

        gammaFactorDefine = self.renderer.gammaFactor if self.renderer.gammaFactor > 0 else 1.0

        # logging.info( "building program " )

        #

        customExtensions = generateExtensions( self.material.extensions, self.parameters, self.extensions )

        customDefines = generateDefines( defines )

        #

        program = GL.glCreateProgram()

        prefixVertex = None
        prefixFragment = None

        if hasattr( self.material, "isRawShaderMaterial" ) :

            prefixVertex = "\n".join( filter( filterEmptyLine, [

                customDefines,

                "\n"

            ] ) )

            prefixFragment = "\n".join( filter( filterEmptyLine, [

                customExtensions,
                customDefines,

                "\n"

            ] ) )

        else:

            prefixVertex = "\n".join( filter( filterEmptyLine, [

                "precision %s float" % self.parameters.precision,
                "precision %s int" % self.parameters.precision,

                "#define SHADER_NAME %s" % self.shader.name,

                customDefines,

                "#define VERTEX_TEXTURES" if self.parameters.supportsVertexTextures else "",

                "#define GAMMA_FACTOR " + gammaFactorDefine,

                "#define MAX_BONES " + self.parameters.maxBones,
                "#define USE_FOG" if ( self.parameters.useFog and self.parameters.fog ) else "",
                "#define FOG_EXP2" if ( self.parameters.useFog and self.parameters.fogExp ) else "",

                "#define USE_MAP" if self.parameters.map else "",
                "#define USE_ENVMAP" if self.parameters.envMap else "",
                "#define %s" % envMapModeDefine if self.parameters.envMap else "",
                "#define USE_LIGHTMAP" if self.parameters.lightMap else "",
                "#define USE_AOMAP" if self.parameters.aoMap else "",
                "#define USE_EMISSIVEMAP" if self.parameters.emissiveMap else "",
                "#define USE_BUMPMAP" if self.parameters.bumpMap else "",
                "#define USE_NORMALMAP" if self.parameters.normalMap else "",
                "#define USE_DISPLACEMENTMAP" if self.parameters.displacementMap and self.parameters.supportsVertexTextures else "",
                "#define USE_SPECULARMAP" if self.parameters.specularMap else "",
                "#define USE_ROUGHNESSMAP" if self.parameters.roughnessMap else "",
                "#define USE_METALNESSMAP" if self.parameters.metalnessMap else "",
                "#define USE_ALPHAMAP" if self.parameters.alphaMap else "",
                "#define USE_COLOR" if self.parameters.vertexColors else "",

                "#define FLAT_SHADED" if self.parameters.flatShading else "",

                "#define USE_SKINNING" if self.parameters.skinning else "",
                "#define BONE_TEXTURE" if self.parameters.useVertexTexture else "",

                "#define USE_MORPHTARGETS" if self.parameters.morphTargets else "",
                "#define USE_MORPHNORMALS" if self.parameters.morphNormals and self.parameters.flatShading == False else "",
                "#define DOUBLE_SIDED" if self.parameters.doubleSided else "",
                "#define FLIP_SIDED" if self.parameters.flipSided else "",

                "#define NUM_CLIPPING_PLANES " + self.parameters.numClippingPlanes,

                "#define USE_SHADOWMAP" if self.parameters.shadowMapEnabled else "",
                "#define %s" % shadowMapTypeDefine if self.parameters.shadowMapEnabled else "",

                "#define USE_SIZEATTENUATION" if self.parameters.sizeAttenuation else "",

                "#define USE_LOGDEPTHBUF" if self.parameters.logarithmicDepthBuffer else "",
                "#define USE_LOGDEPTHBUF_EXT" if self.parameters.logarithmicDepthBuffer and self.extensions.get( "EXT_frag_depth" ) else "",

                "uniform mat4 modelMatrix",
                "uniform mat4 modelViewMatrix",
                "uniform mat4 projectionMatrix",
                "uniform mat4 viewMatrix",
                "uniform mat3 normalMatrix",
                "uniform vec3 cameraPosition",

                "attribute vec3 position",
                "attribute vec3 normal",
                "attribute vec2 uv",

                "#ifdef USE_COLOR",

                "    attribute vec3 color",

                "#endif",

                "#ifdef USE_MORPHTARGETS",

                "    attribute vec3 morphTarget0",
                "    attribute vec3 morphTarget1",
                "    attribute vec3 morphTarget2",
                "    attribute vec3 morphTarget3",

                "    #ifdef USE_MORPHNORMALS",

                "        attribute vec3 morphNormal0",
                "        attribute vec3 morphNormal1",
                "        attribute vec3 morphNormal2",
                "        attribute vec3 morphNormal3",

                "    #else",

                "        attribute vec3 morphTarget4",
                "        attribute vec3 morphTarget5",
                "        attribute vec3 morphTarget6",
                "        attribute vec3 morphTarget7",

                "    #endif",

                "#endif",

                "#ifdef USE_SKINNING",

                "    attribute vec4 skinIndex",
                "    attribute vec4 skinWeight",

                "#endif",

                "\n"

            ] ) )

            prefixFragment = "\n".join( filter( filterEmptyLine, [

                customExtensions,

                "precision %s float" % self.parameters.precision,
                "precision %s int" % self.parameters.precision,

                "#define SHADER_NAME %s" % self.shader.name,

                customDefines,

                "#define ALPHATEST %s" % parameters.alphaTest if self.parameters.alphaTest else "",

                "#define GAMMA_FACTOR %s" % gammaFactorDefine,

                "#define USE_FOG" if ( self.parameters.useFog and self.parameters.fog ) else "",
                "#define FOG_EXP2" if ( self.parameters.useFog and self.parameters.fogExp ) else "",

                "#define USE_MAP" if self.parameters.map else "",
                "#define USE_ENVMAP" if self.parameters.envMap else "",
                "#define %s" % envMapTypeDefine if self.parameters.envMap else "",
                "#define %s" % envMapModeDefine if self.parameters.envMap else "",
                "#define %s" % envMapBlendingDefine if self.parameters.envMap else "",
                "#define USE_LIGHTMAP" if self.parameters.lightMap else "",
                "#define USE_AOMAP" if self.parameters.aoMap else "",
                "#define USE_EMISSIVEMAP" if self.parameters.emissiveMap else "",
                "#define USE_BUMPMAP" if self.parameters.bumpMap else "",
                "#define USE_NORMALMAP" if self.parameters.normalMap else "",
                "#define USE_SPECULARMAP" if self.parameters.specularMap else "",
                "#define USE_ROUGHNESSMAP" if self.parameters.roughnessMap else "",
                "#define USE_METALNESSMAP" if self.parameters.metalnessMap else "",
                "#define USE_ALPHAMAP" if self.parameters.alphaMap else "",
                "#define USE_COLOR" if self.parameters.vertexColors else "",

                "#define USE_GRADIENTMAP" if self.parameters.gradientMap else "",

                "#define FLAT_SHADED" if self.parameters.flatShading else "",

                "#define DOUBLE_SIDED" if self.parameters.doubleSided else "",
                "#define FLIP_SIDED" if self.parameters.flipSided else "",

                "#define NUM_CLIPPING_PLANES %s" % self.parameters.numClippingPlanes,
                "#define UNION_CLIPPING_PLANES %s" % (parameters.numClippingPlanes - self.parameters.numClipIntersection),

                "#define USE_SHADOWMAP" if self.parameters.shadowMapEnabled else "",
                "#define %S" % shadowMapTypeDefine if self.parameters.shadowMapEnabled else "",

                "#define PREMULTIPLIED_ALPHA" if self.parameters.premultipliedAlpha else "",

                "#define PHYSICALLY_CORRECT_LIGHTS" if self.parameters.physicallyCorrectLights else "",

                "#define USE_LOGDEPTHBUF" if self.parameters.logarithmicDepthBuffer else "",
                "#define USE_LOGDEPTHBUF_EXT" if self.parameters.logarithmicDepthBuffer and self.extensions.get( "EXT_frag_depth" ) else "",

                "#define TEXTURE_LOD_EXT" if self.parameters.envMap and self.extensions.get( "EXT_shader_texture_lod" ) else "",

                "uniform mat4 viewMatrix",
                "uniform vec3 cameraPosition",

                "#define TONE_MAPPING" if ( self.parameters.toneMapping != NoToneMapping ) else "",
                shaderChunk.ShaderChunk[ "tonemapping_pars_fragment" ] if ( self.parameters.toneMapping != NoToneMapping ) else "",  # self code is required here because it is used by the toneMapping() function defined below
                getToneMappingFunction( "toneMapping", self.parameters.toneMapping ) if ( self.parameters.toneMapping != NoToneMapping ) else "",

                "#define DITHERING" if self.parameters.dithering else "",

                shaderChunk.ShaderChunk[ "encodings_pars_fragment" ] if ( self.parameters.outputEncoding or self.parameters.mapEncoding or self.parameters.envMapEncoding or self.parameters.emissiveMapEncoding ) else "", # self code is required here because it is used by the various encoding/decoding function defined below
                getTexelDecodingFunction( "mapTexelToLinear", self.parameters.mapEncoding ) if self.parameters.mapEncoding else "",
                getTexelDecodingFunction( "envMapTexelToLinear", self.parameters.envMapEncoding ) if self.parameters.envMapEncoding else "",
                getTexelDecodingFunction( "emissiveMapTexelToLinear", self.parameters.emissiveMapEncoding ) if self.parameters.emissiveMapEncoding else "",
                getTexelEncodingFunction( "linearToOutputTexel", self.parameters.outputEncoding ) if self.parameters.outputEncoding else "",

                "#define DEPTH_PACKING %s" % material.depthPacking if self.parameters.depthPacking else "",

                "\n"

            ] ) )

        self.vertexShader = parseIncludes( self.vertexShader )
        self.vertexShader = replaceLightNums( self.vertexShader, self.parameters )

        self.fragmentShader = parseIncludes( self.fragmentShader )
        self.fragmentShader = replaceLightNums( self.fragmentShader, self.parameters )

        if not hasattr( self.material, "isShaderMaterial" ) :

            self.vertexShader = unrollLoops( self.vertexShader )
            self.fragmentShader = unrollLoops( self.fragmentShader )

        vertexGlsl = prefixVertex + self.vertexShader
        fragmentGlsl = prefixFragment + self.fragmentShader

        # logging.info( "*VERTEX*", vertexGlsl )
        # logging.info( "*FRAGMENT*", fragmentGlsl )

        glVertexShader = webGLShader.WebGLShader( GL.GL_VERTEX_SHADER, vertexGlsl )
        glFragmentShader = webGLShader.WebGLShader( GL.GL_FRAGMENT_SHADER, fragmentGlsl )

        GL.glAttachShader( program, glVertexShader )
        GL.glAttachShader( program, glFragmentShader )

        # Force a particular attribute to index 0.

        if self.material.index0AttributeName is not None :

            GL.glBindAttribLocation( program, 0, self.material.index0AttributeName )

        elif self.parameters.morphTargets == True :

            # programs with morphTargets displace position out of attribute 0
            GL.glBindAttribLocation( program, 0, "position" )

        GL.glLinkProgram( program )

        programLog = GL.glGetProgramInfoLog( program )
        vertexLog = GL.glGetShaderInfoLog( glVertexShader )
        fragmentLog = GL.glGetShaderInfoLog( glFragmentShader )

        runnable = True
        haveDiagnostics = True

        # logging.info( "**VERTEX**", GL.glGetExtension( "WEBGL_debug_shaders" ).getTranslatedShaderSource( glVertexShader ) )
        # logging.info( "**FRAGMENT**", GL.glGetExtension( "WEBGL_debug_shaders" ).getTranslatedShaderSource( glFragmentShader ) )

        if GL.glGetProgramParameter( program, GL.GL_LINK_STATUS ) == False :

            runnable = False

            logging.error( "THREE.WebGLProgram: shader error: %s GL.GL_VALIDATE_STATUS %s GL.glGetProgramInfoLog %s %s %s", GL.glGetError(), GL.glGetProgramParameter( program, GL.GL_VALIDATE_STATUS ), programLog, vertexLog, fragmentLog )

        elif programLog != "" :

            logging.warning( "THREE.WebGLProgram: GL.glGetProgramInfoLog() %s", programLog )

        elif vertexLog == "" or fragmentLog == "" :

            haveDiagnostics = False

        if haveDiagnostics :

            self.diagnostics = {

                "runnable": runnable,
                "material": self.material,

                "programLog": programLog,

                "vertexShader": {

                    "log": vertexLog,
                    "prefix": prefixVertex

                },

                "fragmentShader": {

                    "log": fragmentLog,
                    "prefix": prefixFragment

                },
            
            }

        # clean up

        GL.glDeleteShader( glVertexShader )
        GL.glDeleteShader( glFragmentShader )

        self.id = programIdCount
        programIdCount += 1
        self.code = code
        self.usedTimes = 1
        self.program = program
        self.vertexShader = glVertexShader
        self.fragmentShader = glFragmentShader

        self.cachedUniforms = None

        self.cachedAttributes = None

    # set up caching for uniform locations

    def getUniforms( self ):

        if cachedUniforms is None :

            cachedUniforms = webGLUniforms.WebGLUniforms( self.program, self.renderer )

        return cachedUniforms

    # set up caching for attribute locations

    def getAttributes( self ):

        if cachedAttributes is None :

            cachedAttributes = fetchAttributeLocations( self.program )

        return cachedAttributes

        # free resource

    def destroy( self ):

        GL.glDeleteProgram( program )
        self.program = None

