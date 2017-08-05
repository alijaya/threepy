import material
from ..constants import MultiplyOperation
from ..math import color

"""
 * @author mrdoob / "http":#mrdoob.com/
 * @author alteredq / "http":#alteredqualia.com/
 *
 * parameters = {
 *  "color": <hex>,
 *  "opacity": <float>,
 *
 *  "map": THREE.Texture( <Image> ),
 *
 *  "lightMap": THREE.Texture( <Image> ),
 *  "lightMapIntensity": <float>
 *
 *  "aoMap": THREE.Texture( <Image> ),
 *  "aoMapIntensity": <float>
 *
 *  "emissive": <hex>,
 *  "emissiveIntensity": <float>
 *  "emissiveMap": THREE.Texture( <Image> ),
 *
 *  "specularMap": THREE.Texture( <Image> ),
 *
 *  "alphaMap": THREE.Texture( <Image> ),
 *
 *  "envMap": THREE.TextureCube( [posx, negx, posy, negy, posz, negz] ),
 *  "combine": THREE.Multiply,
 *  "reflectivity": <float>,
 *  "refractionRatio": <float>,
 *
 *  "wireframe": <boolean>,
 *  "wireframeLinewidth": <float>,
 *
 *  "skinning": <bool>,
 *  "morphTargets": <bool>,
 *  "morphNormals": <bool>
 * """

class MeshLambertMaterial( material.Material ):

    def __init__( self, **parameters ):

        super( MeshLambertMaterial, self ).__init__()

        self.isMeshLambertMaterial = True

        self.type = "MeshLambertMaterial"

        self.color = color.Color( 0xffffff ) # diffuse

        self.map = None

        self.lightMap = None
        self.lightMapIntensity = 1.0

        self.aoMap = None
        self.aoMapIntensity = 1.0

        self.emissive = color.Color( 0x000000 )
        self.emissiveIntensity = 1.0
        self.emissiveMap = None

        self.specularMap = None

        self.alphaMap = None

        self.envMap = None
        self.combine = MultiplyOperation
        self.reflectivity = 1
        self.refractionRatio = 0.98

        self.wireframe = False
        self.wireframeLinewidth = 1
        self.wireframeLinecap = "round"
        self.wireframeLinejoin = "round"

        self.skinning = False
        self.morphTargets = False
        self.morphNormals = False

        self.setValues( **parameters )

    def copy( self, source ):

        super( MeshLambertMaterial, self ).copy( source )

        self.color.copy( source.color )

        self.map = source.map

        self.lightMap = source.lightMap
        self.lightMapIntensity = source.lightMapIntensity

        self.aoMap = source.aoMap
        self.aoMapIntensity = source.aoMapIntensity

        self.emissive.copy( source.emissive )
        self.emissiveMap = source.emissiveMap
        self.emissiveIntensity = source.emissiveIntensity

        self.specularMap = source.specularMap

        self.alphaMap = source.alphaMap

        self.envMap = source.envMap
        self.combine = source.combine
        self.reflectivity = source.reflectivity
        self.refractionRatio = source.refractionRatio

        self.wireframe = source.wireframe
        self.wireframeLinewidth = source.wireframeLinewidth
        self.wireframeLinecap = source.wireframeLinecap
        self.wireframeLinejoin = source.wireframeLinejoin

        self.skinning = source.skinning
        self.morphTargets = source.morphTargets
        self.morphNormals = source.morphNormals

        return self
