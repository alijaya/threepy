from ...math import vector4
from ...math import color
from ...math import vector2
from ...utils import Expando

"""
 * Uniforms library for shared webgl shaders
 """

UniformsLib = {

	"common": Expando(

		diffuse = Expando( value = color.Color( 0xeeeeee ) ),
		opacity = Expando( value = 1.0 ),

		map = Expando( value = None ),
		offsetRepeat = Expando( value = vector4.Vector4( 0, 0, 1, 1 ) ),

		alphaMap = Expando( value = None ),

	),

	"specularmap": Expando(

		specularMap = Expando( value = None ),

	),

	"envmap": Expando(

		envMap = Expando( value = None ),
		flipEnvMap = Expando( value = - 1 ),
		reflectivity = Expando( value = 1.0 ),
		refractionRatio = Expando( value = 0.98 )

	),

	"aomap": Expando(

		aoMap = Expando( value = None ),
		aoMapIntensity = Expando( value = 1 )

	),

	"lightmap": Expando(

		lightMap = Expando( value = None ),
		lightMapIntensity = Expando( value = 1 )

	),

	"emissivemap": Expando(

		emissiveMap = Expando( value = None )

	),

	"bumpmap": Expando(

		bumpMap = Expando( value = None ),
		bumpScale = Expando( value = 1 )

	),

	"normalmap": Expando(

		normalMap = Expando( value = None ),
		normalScale = Expando( value = vector2.Vector2( 1, 1 ) )

	),

	"displacementmap": Expando(

		displacementMap = Expando( value = None ),
		displacementScale = Expando( value = 1 ),
		displacementBias = Expando( value = 0 )

	),

	"roughnessmap": Expando(

		roughnessMap = Expando( value = None )

	),

	"metalnessmap": Expando(

		metalnessMap = Expando( value = None )

	),

	"gradientmap": Expando(

		gradientMap = Expando( value = None )

	),

	"fog": Expando(

		fogDensity = Expando( value = 0.00025 ),
		fogNear = Expando( value = 1 ),
		fogFar = Expando( value = 2000 ),
		fogColor = Expando( value = color.Color( 0xffffff ) )

	),

	"lights": Expando(

		ambientLightColor = Expando( value = [] ),

		directionalLights = Expando( value = [], properties = Expando(
			direction = Expando(),
			color = Expando(),

			shadow = Expando(),
			shadowBias = Expando(),
			shadowRadius = Expando(),
			shadowMapSize = Expando()
		) ),

		directionalShadowMap = Expando( value = [] ),
		directionalShadowMatrix = Expando( value = [] ),

		spotLights = Expando( value = [], properties = Expando(
			color = Expando(),
			position = Expando(),
			direction = Expando(),
			distance = Expando(),
			coneCos = Expando(),
			penumbraCos = Expando(),
			decay = Expando(),

			shadow = Expando(),
			shadowBias = Expando(),
			shadowRadius = Expando(),
			shadowMapSize = Expando()
		) ),

		spotShadowMap = Expando( value = [] ),
		spotShadowMatrix = Expando( value = [] ),

		pointLights = Expando( value = [], properties = Expando(
			color = Expando(),
			position = Expando(),
			decay = Expando(),
			distance = Expando(),

			shadow = Expando(),
			shadowBias = Expando(),
			shadowRadius = Expando(),
			shadowMapSize = Expando(),
			shadowCameraNear = Expando(),
			shadowCameraFar = Expando()
		) ),

		pointShadowMap = Expando( value = [] ),
		pointShadowMatrix = Expando( value = [] ),

		hemisphereLights = Expando( value = [], properties = Expando(
			direction = Expando(),
			skycolor= Expando(),
			groundcolor = Expando()
		) ),

		# TODO (abelnation) = RectAreaLight BRDF data needs to be moved from example to main src
		rectAreaLights = Expando( value = [], properties = Expando(
			color = Expando(),
			position = Expando(),
			width = Expando(),
			height = Expando()
		) )

	),

	"points": Expando(

		diffuse = Expando( value = color.Color( 0xeeeeee ) ),
		opacity = Expando( value = 1.0 ),
		size = Expando( value = 1.0 ),
		scale = Expando( value = 1.0 ),
		map = Expando( value = None ),
		offsetRepeat = Expando( value = vector4.Vector4( 0, 0, 1, 1 ) )

	)

}