from ...math import vector4
from ...math import color
from ...math import vector2

"""
 * Uniforms library for shared webgl shaders
 """

UniformsLib = {

	"common": {

		"diffuse": { "value": color.Color( 0xeeeeee ) },
		"opacity": { "value": 1.0 },

		"map": { "value": None },
		"offsetRepeat": { "value": vector4.Vector4( 0, 0, 1, 1 ) },

		"alphaMap": { "value": None },

	},

	"specularmap": {

		"specularMap": { "value": None },

	},

	"envmap": {

		"envMap": { "value": None },
		"flipEnvMap": { "value": - 1 },
		"reflectivity": { "value": 1.0 },
		"refractionRatio": { "value": 0.98 }

	},

	"aomap": {

		"aoMap": { "value": None },
		"aoMapIntensity": { "value": 1 }

	},

	"lightmap": {

		"lightMap": { "value": None },
		"lightMapIntensity": { "value": 1 }

	},

	"emissivemap": {

		"emissiveMap": { "value": None }

	},

	"bumpmap": {

		"bumpMap": { "value": None },
		"bumpScale": { "value": 1 }

	},

	"normalmap": {

		"normalMap": { "value": None },
		"normalScale": { "value": vector2.Vector2( 1, 1 ) }

	},

	"displacementmap": {

		"displacementMap": { "value": None },
		"displacementScale": { "value": 1 },
		"displacementBias": { "value": 0 }

	},

	"roughnessmap": {

		"roughnessMap": { "value": None }

	},

	"metalnessmap": {

		"metalnessMap": { "value": None }

	},

	"gradientmap": {

		"gradientMap": { "value": None }

	},

	"fog": {

		"fogDensity": { "value": 0.00025 },
		"fogNear": { "value": 1 },
		"fogFar": { "value": 2000 },
		"fogcolor.Color": { "value": color.Color( 0xffffff ) }

	},

	"lights": {

		"ambientLightcolor.Color": { "value": [] },

		"directionalLights": { "value": [], "properties": {
			"direction": {},
			"color": {},

			"shadow": {},
			"shadowBias": {},
			"shadowRadius": {},
			"shadowMapSize": {}
		} },

		"directionalShadowMap": { "value": [] },
		"directionalShadowMatrix": { "value": [] },

		"spotLights": { "value": [], "properties": {
			"color": {},
			"position": {},
			"direction": {},
			"distance": {},
			"coneCos": {},
			"penumbraCos": {},
			"decay": {},

			"shadow": {},
			"shadowBias": {},
			"shadowRadius": {},
			"shadowMapSize": {}
		} },

		"spotShadowMap": { "value": [] },
		"spotShadowMatrix": { "value": [] },

		"pointLights": { "value": [], "properties": {
			"color": {},
			"position": {},
			"decay": {},
			"distance": {},

			"shadow": {},
			"shadowBias": {},
			"shadowRadius": {},
			"shadowMapSize": {},
			"shadowCameraNear": {},
			"shadowCameraFar": {}
		} },

		"pointShadowMap": { "value": [] },
		"pointShadowMatrix": { "value": [] },

		"hemisphereLights": { "value": [], "properties": {
			"direction": {},
			"skycolor.Color": {},
			"groundcolor.Color": {}
		} },

		# TODO "(abelnation)": RectAreaLight BRDF data needs to be moved from example to main src
		"rectAreaLights": { "value": [], "properties": {
			"color": {},
			"position": {},
			"width": {},
			"height": {}
		} }

	},

	"points": {

		"diffuse": { "value": color.Color( 0xeeeeee ) },
		"opacity": { "value": 1.0 },
		"size": { "value": 1.0 },
		"scale": { "value": 1.0 },
		"map": { "value": None },
		"offsetRepeat": { "value": vector4.Vector4( 0, 0, 1, 1 ) }

	}

}