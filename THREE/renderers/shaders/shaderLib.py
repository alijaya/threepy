import ShaderChunk
import UniformsUtils
from ...math import vector3
from uniformsLib import UniformsLib
from ...math import color

"""
 * @author alteredq / "http":#alteredqualia.com/
 * @author mrdoob / "http":#mrdoob.com/
 * @author mikael emtinger / "http":#gomo.se/
 """

ShaderLib = {

    "basic": {

        "uniforms": UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "specularmap" ],
            UniformsLib[ "envmap" ],
            UniformsLib[ "aomap" ],
            UniformsLib[ "lightmap" ],
            UniformsLib[ "fog" ]
        ] ),

        "vertexShader": ShaderChunk.meshbasic_vert,
        "fragmentShader": ShaderChunk.meshbasic_frag
    },

    "lambert": {

        "uniforms": UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "specularmap" ],
            UniformsLib[ "envmap" ],
            UniformsLib[ "aomap" ],
            UniformsLib[ "lightmap" ],
            UniformsLib[ "emissivemap" ],
            UniformsLib[ "fog" ],
            UniformsLib[ "lights" ],
            {
                "emissive": { "value": color.Color( 0x000000 ) }
            }
        ] ),

        "vertexShader": ShaderChunk.meshlambert_vert,
        "fragmentShader": ShaderChunk.meshlambert_frag
        
    },

    "phong": {

        "uniforms": UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "specularmap" ],
            UniformsLib[ "envmap" ],
            UniformsLib[ "aomap" ],
            UniformsLib[ "lightmap" ],
            UniformsLib[ "emissivemap" ],
            UniformsLib[ "bumpmap" ],
            UniformsLib[ "normalmap" ],
            UniformsLib[ "displacementmap" ],
            UniformsLib[ "gradientmap" ],
            UniformsLib[ "fog" ],
            UniformsLib[ "lights" ],
            {
                "emissive": { "value": color.Color( 0x000000 ) },
                "specular": { "value": color.Color( 0x111111 ) },
                "shininess": { "value": 30 }
            }
        ] ),

        "vertexShader": ShaderChunk.meshphong_vert,
        "fragmentShader": ShaderChunk.meshphong_frag
    },

    "standard": {

        "uniforms": UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "envmap" ],
            UniformsLib[ "aomap" ],
            UniformsLib[ "lightmap" ],
            UniformsLib[ "emissivemap" ],
            UniformsLib[ "bumpmap" ],
            UniformsLib[ "normalmap" ],
            UniformsLib[ "displacementmap" ],
            UniformsLib[ "roughnessmap" ],
            UniformsLib[ "metalnessmap" ],
            UniformsLib[ "fog" ],
            UniformsLib[ "lights" ],
            {
                "emissive": { "value": color.Color( 0x000000 ) },
                "roughness": { "value": 0.5 },
                "metalness": { "value": 0.5 },
                "envMapIntensity": { "value": 1 } # temporary
            }
        ] ),

        "vertexShader": ShaderChunk.meshphysical_vert,
        "fragmentShader": ShaderChunk.meshphysical_frag

    },

    "points": {

        "uniforms": UniformsUtils.merge( [
            UniformsLib[ "points" ],
            UniformsLib[ "fog" ]
        ] ),

        "vertexShader": ShaderChunk.points_vert,
        "fragmentShader": ShaderChunk.points_frag
    
    },

    "dashed": {

        "uniforms": UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "fog" ],
            {
                "scale": { "value": 1 },
                "dashSize": { "value": 1 },
                "totalSize": { "value": 2 }
            }
        ] ),

        "vertexShader": ShaderChunk.linedashed_vert,
        "fragmentShader": ShaderChunk.linedashed_frag
    
    },

    "depth": {

        "uniforms": UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "displacementmap" ]
        ] ),

        "vertexShader": ShaderChunk.depth_vert,
        "fragmentShader": ShaderChunk.depth_frag
    
    },

    "normal": {

        "uniforms": UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "bumpmap" ],
            UniformsLib[ "normalmap" ],
            UniformsLib[ "displacementmap" ],
            {
                "opacity": { "value": 1.0 }
            }
        ] ),

        "vertexShader": ShaderChunk.normal_vert,
        "fragmentShader": ShaderChunk.normal_frag
    
    },

    """ -= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-
    #    Cube map shader
     -= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1- """

    "cube": {

        "uniforms": {
            "tCube": { "value": None },
            "tFlip": { "value": - 1 },
            "opacity": { "value": 1.0}
        },
        "vertexShader": ShaderChunk.cube_vert,
        "fragmentShader": ShaderChunk.cube_frag
    
    },

    "equirect": {

        "uniforms": {
            "tEquirect": { "value": None },
        },
        "vertexShader": ShaderChunk.equirect_vert,
        "fragmentShader": ShaderChunk.equirect_frag

    },

    "distanceRGBA": {

        "uniforms": UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "displacementmap" ],
            {
                "referencePosition": { "value": vector3.Vector3() },
                "nearDistance": { "value": 1 },
                "farDistance": { "value": 1000 }
            }
        ] ),

        "vertexShader": ShaderChunk.distanceRGBA_vert,
        "fragmentShader": ShaderChunk.distanceRGBA_frag
    
    },

    "shadow": {

        "uniforms": UniformsUtils.merge( [
            UniformsLib[ "lights" ],
            {
                "color": { "value": color.Color( 0x00000 ) },
                "opacity": { "value": 1.0 },
            }
        ] ),

        "vertexShader": ShaderChunk.shadow_vert,
        "fragmentShader": ShaderChunk.shadow_frag
    
    },

}

ShaderLib[ "physical" ] = {

    "uniforms": UniformsUtils.merge( [
        ShaderLib[ "standard" ][ "uniforms" ],
        {
            "clearCoat": { "value": 0 },
            "clearCoatRoughness": { "value": 0 },
        }
    ] ),

    "vertexShader": ShaderChunk.meshphysical_vert,
    "fragmentShader": ShaderChunk.meshphysical_frag

}
