from __future__ import division
import math

from ...math import color
from ...math import matrix4
from ...math import vector2
from ...math import vector3
from ...utils import Expando

class UniformsCache( object ):

    def __init__( self ):

        self.lights = {}

    def get( self, light ):

        if light.id in self.lights: return self.lights[ light.id ] # cached

        uniforms = None

        if light.type == "DirectionalLight":

            uniforms = Expando(
                direction = vector3.Vector3(),
                color = color.Color(),

                shadow = False,
                shadowBias = 0,
                shadowRadius = 1,
                shadowMapSize = vector2.Vector2()
            )
        
        elif light.type == "SpotLight":

            uniforms = Expando(
                position = vector3.Vector3(),
                direction = vector3.Vector3(),
                color = color.Color(),
                distance = 0,
                coneCos = 0,
                penumbraCos = 0,
                decay = 0,

                shadow = False,
                shadowBias = 0,
                shadowRadius = 1,
                shadowMapSize = vector2.Vector2()
            )

        elif light.type == "PointLight":

            uniforms = Expando(
                position = vector3.Vector3(),
                color = color.Color(),
                distance = 0,
                decay = 0,

                shadow = False,
                shadowBias = 0,
                shadowRadius = 1,
                shadowMapSize = vector2.Vector2(),
                shadowCameraNear = 1,
                shadowCameraFar = 1000
            )

        elif light.type == "HemisphereLight":

            uniforms = Expando(
                direction = vector3.Vector3(),
                skyColor = color.Color(),
                groundColor = color.Color(),
            )

        elif light.type == "RectAreaLight":

            uniforms = Expando(
                color = color.Color(),
                position = vector3.Vector3(),
                halfWidth = vector3.Vector3(),
                halfHeight = vector3.Vector3()
                # TODO (abelnation): set RectAreaLight shadow uniforms
            )

        self.lights[ light.id ] = uniforms

        return uniforms

cache = UniformsCache()

state = Expando(
    
    hash = "",

    ambient = [ 0, 0, 0 ],
    directional = [],
    directionalShadowMap = [],
    directionalShadowMatrix = [],
    spot = [],
    spotShadowMap = [],
    spotShadowMatrix = [],
    rectArea = [],
    point = [],
    pointShadowMap = [],
    pointShadowMatrix = [],
    hemi = []

)

def setup( lights, shadows, camera ):

    r = 0
    g = 0
    b = 0

    viewMatrix = camera.matrixWorldInverse

    state.directional = []
    state.directionalShadowMap = []
    state.directionalShadowMatrix = []
    state.spot = []
    state.spotShadowMap = []
    state.spotShadowMatrix = []
    state.rectArea = []
    state.point = []
    state.pointShadowMap = []
    state.pointShadowMatrix = []
    state.hemi = []

    # helper var

    vec3 = vector3.Vector3()
    mat4 = matrix4.Matrix4()
    mat2 = matrix4.Matrix4()

    for light in lights:

        color = light.color
        intensity = light.intensity

        # shadowMap = light.shadow.map.texture if light.shadow and light.shadow.map else None

        if hasattr( light, "isAmbientLight" ):

            r += color.r * intensity
            g += color.g * intensity
            b += color.b * intensity

        elif hasattr( light, "isDirectionalLight" ):

            uniforms = cache.get( light )

            uniforms.color.copy( light.color ).multiplyScalar( light.intensity )
            uniforms.direction.setFromMatrixPosition( light.matrixWorld )
            vec3.setFromMatrixPosition( light.target.matrixWorld )
            uniforms.direction.sub( vec3 )
            uniforms.direction.transformDirection( viewMatrix )

            uniforms.shadow = light.castShadow

            if light.castShadow:

                shadow = light.shadow

                uniforms.shadowBias = shadow.bias
                uniforms.shadowRadius = shadow.radius
                uniforms.shadowMapSize = shadow.mapSize

            # state.directionalShadowMap.append( shadowMap )
            # state.directionalShadowMatrix.append( light.shadow.matrix )
            state.directional.append( uniforms )

        elif hasattr( light, "isSpotLight" ):

            uniforms = cache.get( light )

            uniforms.position.setFromMatrixPosition( light.matrixWorld )
            uniforms.position.applyMatrix4( viewMatrix )

            uniforms.color.copy( color ).multiplyScalar( intensity )
            uniforms.distance = distance

            uniforms.direction.setFromMatrixPosition( light.matrixWorld )
            vec3.setFromMatrixPosition( light.target.matrixWorld )
            uniforms.direction.sub( vec3 )
            uniforms.direction.transformDirection( viewMatrix )

            uniforms.coneCos = math.cos( light.angle )
            uniforms.penumbraCos = math.cos( light.angle * ( 1 - light.penumbra ) )
            uniforms.decay = 0.0 if light.distance == 0 else light.decay

            uniforms.shadow = light.castShadow

            if light.castShadow:

                shadow = light.shadow

                uniforms.shadowBias = shadow.bias
                uniforms.shadowRadius = shadow.radius
                uniforms.shadowMapSize = shadow.mapSize

            state.spotShadowMap.append( shadowMap )
            state.spotShadowMatrix.append( light.shadow.matrix )
            state.spot.append( uniforms )

            spotLength += 1

        elif hasattr( light, "isRectAreaLight" ):

            uniforms = cache.get( light )

            # (a) intensity controls irradiance of entire light
            uniforms.color.copy( color ).multiplyScalar( intensity / ( light.width * light.height ) )

            # (b) intensity controls the radiance per light area
            # uniforms.color.copy( color ).multiplyScalar( intensity )

            uniforms.position.setFromMatrixPosition( light.matrixWorld )
            uniforms.position.applyMatrix4( viewMatrix )

            # extract local rotation of light to derive width/height half vectors
            mat42.identity()
            mat4.copy( light.matrixWorld )
            mat4.premultiply( viewMatrix )
            mat42.extractRotation( mat4 )

            uniforms.halfWidth.set( light.width * 0.5, 0.0, 0.0 )
            uniforms.halfHeight.set( 0.0, light.height * 0.5, 0.0 )

            # TODO (abelnation): RectAreaLight distance?
            # uniforms.distance = distance

            state.rectArea.append( uniforms )

            rectAreaLength += 1

        elif hasattr( light, "isPointLight" ):

            uniforms = cache.get( light )

            uniforms.position.setFromMatrixPosition( light.matrixWorld )
            uniforms.position.applyMatrix4( viewMatrix )

            uniforms.color.copy( light.color ).multiplyScalar( light.intensity )
            uniforms.distance = light.distance
            uniforms.decay = 0.0 if light.distance == 0 else light.decay

            uniforms.shadow = light.castShadow

            if light.castShadow:

                shadow = light.shadow
                
                uniforms.shadowBias = shadow.bias
                uniforms.shadowRadius = shadow.radius
                uniforms.shadowMapSize = shadow.mapSize
                uniforms.shadowCameraNear = shadow.camera.near
                uniforms.shadowCameraFar = shadow.camera.far

            state.pointShadowMap.append( shadowMap )
            state.pointShadowMatrix.append( light.shadow.matrix )
            state.point.append( uniforms )

            pointLength += 1

        elif hasattr( light, "isHemisphereLight" ):

            uniforms = cache.get( light )

            uniforms.direction.setFromMatrixPosition( light.matrixWorld )
            uniforms.direction.transformDirection( viewMatrix )
            uniforms.direction.normalize()

            uniforms.skyColor.copy( light.color ).multiplyScalar( intensity )
            uniforms.groundColor.copy( light.groundColor ).multiplyScalar( intensity )

            state.hemi.append( uniforms )

            hemiLength += 1
    
    state.ambient[ 0 ] = r
    state.ambient[ 1 ] = g
    state.ambient[ 2 ] = b

    directionalLength = len( state.directional )
    pointLength = len( state.point )
    spotLength = len( state.spot )
    rectAreaLength = len( state.rectArea )
    hemiLength = len( state.hemi )
    shadowsLength = len( shadows )

    state.hash = ",".join( map( lambda v: str( v ), [ directionalLength, pointLength, spotLength, rectAreaLength, hemiLength, shadowsLength ] ) )