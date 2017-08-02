from shaderChunk import ShaderChunk
import UniformsUtils
from ...math import vector3
from uniformsLib import UniformsLib
from ...math import color
from ...utils import Expando

"""
 * @author alteredq / http =#alteredqualia.com/
 * @author mrdoob / http =#mrdoob.com/
 * @author mikael emtinger / http =#gomo.se/
 """

ShaderLib = {

    "basic": Expando(

        uniforms = UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "specularmap" ],
            UniformsLib[ "envmap" ],
            UniformsLib[ "aomap" ],
            UniformsLib[ "lightmap" ],
            UniformsLib[ "fog" ]
        ] ),

        vertexShader = ShaderChunk[ "meshbasic_vert" ],
        fragmentShader = ShaderChunk[ "meshbasic_frag" ]
    ),

    "lambert": Expando(

        uniforms = UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "specularmap" ],
            UniformsLib[ "envmap" ],
            UniformsLib[ "aomap" ],
            UniformsLib[ "lightmap" ],
            UniformsLib[ "emissivemap" ],
            UniformsLib[ "fog" ],
            UniformsLib[ "lights" ],
            Expando(
                emissive = Expando( value = color.Color( 0x000000 ) )
            )
        ] ),

        vertexShader = ShaderChunk[ "meshlambert_vert" ],
        fragmentShader = ShaderChunk[ "meshlambert_frag" ]
        
    ),

    "phong": Expando(

        uniforms = UniformsUtils.merge( [
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
            Expando(
                emissive = Expando( value = color.Color( 0x000000 ) ),
                specular = Expando( value = color.Color( 0x111111 ) ),
                shininess = Expando( value = 30 )
            )
        ] ),

        vertexShader = ShaderChunk[ "meshphong_vert" ],
        fragmentShader = ShaderChunk[ "meshphong_frag" ]
    ),

    "standard": Expando(

        uniforms = UniformsUtils.merge( [
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
            Expando(
                emissive = Expando( value = color.Color( 0x000000 ) ),
                roughness = Expando( value = 0.5 ),
                metalness = Expando( value = 0.5 ),
                envMapIntensity = Expando( value = 1 ) # temporary
            )
        ] ),

        vertexShader = ShaderChunk[ "meshphysical_vert" ],
        fragmentShader = ShaderChunk[ "meshphysical_frag" ]

    ),

    "points": Expando(

        uniforms = UniformsUtils.merge( [
            UniformsLib[ "points" ],
            UniformsLib[ "fog" ]
        ] ),

        vertexShader = ShaderChunk[ "points_vert" ],
        fragmentShader = ShaderChunk[ "points_frag" ]
    
    ),

    "dashed": Expando(

        uniforms = UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "fog" ],
            Expando(
                scale = Expando( value = 1 ),
                dashSize = Expando( value = 1 ),
                totalSize = Expando( value = 2 )
            )
        ] ),

        vertexShader = ShaderChunk[ "linedashed_vert" ],
        fragmentShader = ShaderChunk[ "linedashed_frag" ]
    
    ),

    "depth": Expando(

        uniforms = UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "displacementmap" ]
        ] ),

        vertexShader = ShaderChunk[ "depth_vert" ],
        fragmentShader = ShaderChunk[ "depth_frag" ]
    
    ),

    "normal": Expando(

        uniforms = UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "bumpmap" ],
            UniformsLib[ "normalmap" ],
            UniformsLib[ "displacementmap" ],
            Expando(
                opacity = Expando( value = 1.0 )
            )
        ] ),

        vertexShader = ShaderChunk[ "normal_vert" ],
        fragmentShader = ShaderChunk[ "normal_frag" ]
    
    ),

    """ -= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-
    #    Cube map shader
     -= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1-= 1- """

    "cube": Expando(

        uniforms = Expando(
            tCube = Expando( value = None ),
            tFlip = Expando( value = - 1 ),
            opacity = Expando( value = 1.0)
        ),
        vertexShader = ShaderChunk[ "cube_vert" ],
        fragmentShader = ShaderChunk[ "cube_frag" ]
    
    ),

    "equirect": Expando(

        uniforms = Expando(
            tEquirect = Expando( value = None ),
        ),
        vertexShader = ShaderChunk[ "equirect_vert" ],
        fragmentShader = ShaderChunk[ "equirect_frag" ]

    ),

    "distanceRGBA": Expando(

        uniforms = UniformsUtils.merge( [
            UniformsLib[ "common" ],
            UniformsLib[ "displacementmap" ],
            Expando(
                referencePosition = Expando( value = vector3.Vector3() ),
                nearDistance = Expando( value = 1 ),
                farDistance = Expando( value = 1000 )
            )
        ] ),

        vertexShader = ShaderChunk[ "distanceRGBA_vert" ],
        fragmentShader = ShaderChunk[ "distanceRGBA_frag" ]
    
    ),

    "shadow": Expando(

        uniforms = UniformsUtils.merge( [
            UniformsLib[ "lights" ],
            Expando(
                color = Expando( value = color.Color( 0x00000 ) ),
                opacity = Expando( value = 1.0 ),
            )
        ] ),

        vertexShader = ShaderChunk[ "shadow_vert" ],
        fragmentShader = ShaderChunk[ "shadow_frag" ]
    
    ),

}

ShaderLib[ "physical" ] = Expando(

    uniforms = UniformsUtils.merge( [
        ShaderLib[ "standard" ].uniforms,
        Expando(
            clearCoat = Expando( value = 0 ),
            clearCoatRoughness = Expando( value = 0 ),
        )
    ] ),

    vertexShader = ShaderChunk[ "meshphysical_vert" ],
    fragmentShader = ShaderChunk[ "meshphysical_frag" ]

)
