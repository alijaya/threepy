import material
from ..math import vector2

"""
 * @author mrdoob / "http":#mrdoob.com/
 * @author WestLangley / "http":#github.com/WestLangley
 *
 * parameters = {
 *  "opacity": <float>,
 *
 *  "bumpMap": THREE.Texture( <Image> ),
 *  "bumpScale": <float>,
 *
 *  "normalMap": THREE.Texture( <Image> ),
 *  "normalScale": <Vector2>,
 *
 *  "displacementMap": THREE.Texture( <Image> ),
 *  "displacementScale": <float>,
 *  "displacementBias": <float>,
 *
 *  "wireframe": <boolean>,
 *  "wireframeLinewidth": <float>
 *
 *  "skinning": <bool>,
 *  "morphTargets": <bool>,
 *  "morphNormals": <bool>
 * """

class MeshNormalMaterial( material.Material ):

    def __init__( self, **parameters ):

        super( MeshNormalMaterial, self ).__init__()

        self.isMeshNormalMaterial = True

        self.type = "MeshNormalMaterial"

        self.bumpMap = None
        self.bumpScale = 1

        self.normalMap = None
        self.normalScale = vector2.Vector2( 1, 1 )

        self.displacementMap = None
        self.displacementScale = 1
        self.displacementBias = 0

        self.wireframe = False
        self.wireframeLinewidth = 1

        self.fog = False
        self.lights = False

        self.skinning = False
        self.morphTargets = False
        self.morphNormals = False

        self.setValues( **parameters )

    def copy( self, source ):

        super( MeshNormalMaterial, self ).copy( source )

        self.bumpMap = source.bumpMap
        self.bumpScale = source.bumpScale

        self.normalMap = source.normalMap
        self.normalScale.copy( source.normalScale )

        self.displacementMap = source.displacementMap
        self.displacementScale = source.displacementScale
        self.displacementBias = source.displacementBias

        self.wireframe = source.wireframe
        self.wireframeLinewidth = source.wireframeLinewidth

        self.skinning = source.skinning
        self.morphTargets = source.morphTargets
        self.morphNormals = source.morphNormals

        return self
