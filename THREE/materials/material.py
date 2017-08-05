import logging

from ..core import eventDispatcher
from ..constants import NoColors, FrontSide, FlatShading, NormalBlending, LessEqualDepth, AddEquation, OneMinusSrcAlphaFactor, SrcAlphaFactor
from ..math import _Math
from ..utils import Expando

"""
 * @author mrdoob / http:#mrdoob.com/
 * @author alteredq / http:#alteredqualia.com/
 """

class Material( Expando, eventDispatcher.EventDispatcher ): # multiple inheritance? ugh

    MaterialId = 0

    @staticmethod
    def getMaterialId():

        ret = Material.MaterialId
        Material.MaterialId += 1
        return ret

    def __init__( self ):

        super( Material, self ).__init__()

        self.isMaterial = True

        self.id = Material.getMaterialId()
        self.uuid = _Math.generateUUID()

        self.name = ""
        self.type = "Material"

        self.fog = True
        self.lights = True

        self.blending = NormalBlending
        self.side = FrontSide
        self.flatShading = False
        self.vertexColors = NoColors # THREE.NoColors, THREE.VertexColors, THREE.FaceColors

        self.opacity = 1
        self.transparent = False

        self.blendSrc = SrcAlphaFactor
        self.blendDst = OneMinusSrcAlphaFactor
        self.blendEquation = AddEquation
        self.blendSrcAlpha = None
        self.blendDstAlpha = None
        self.blendEquationAlpha = None

        self.depthFunc = LessEqualDepth
        self.depthTest = True
        self.depthWrite = True

        self.clippingPlanes = None
        self.clipIntersection = False
        self.clipShadows = False

        self.colorWrite = True

        self.precision = None # override the renderer"s default precision for self material

        self.polygonOffset = False
        self.polygonOffsetFactor = 0
        self.polygonOffsetUnits = 0

        self.dithering = False

        self.alphaTest = 0
        self.premultipliedAlpha = False

        self.overdraw = 0 # Overdrawn pixels (typically between 0 and 1) for fixing antialiasing gaps in CanvasRenderer

        self.visible = True

        self.needsUpdate = True

        self.onBeforeCompile = lambda *args: None

    def setValues( self, **values ):

        if values is None : return

        for key in values :

            newValue = values[ key ]

            if newValue is None :

                logging.warning( "THREE.Material: \"%s\" parameter is None." % key )
                continue

            # for backward compatability if shading is set in the constructor
            if key == "shading" :

                logging.warning( "THREE.%s: .shading has been removed. Use the boolean .flatShading instead." % self.type )
                self.flatShading = True if ( newValue == FlatShading ) else False
                continue

            currentValue = self[ key ]

            if not key in self :

                logging.warning( "THREE.%s: \"%s\" is not a property of self material." % ( self.type, key ) )
                continue

            if currentValue and hasattr( currentValue, "isColor" ) :

                currentValue.set( newValue )

            elif ( currentValue is not None and hasattr( currentValue, "isVector3" ) ) and ( newValue is not None and hasattr( newValue, "isVector3" ) ) :

                currentValue.copy( newValue )

            elif key == "overdraw" :

                # ensure overdraw is backwards-compatible with legacy boolean type
                self[ key ] = int( newValue )

            else:

                self[ key ] = newValue

    def toJSON( self, meta = None ):

        isRoot = meta is None

        if isRoot :

            meta = Expando(
                textures = {},
                images = {}
            )

        data = Expando(
            metadata = Expando(
                version = 4.5,
                type = "Material",
                generator = "Material.toJSON"
            )
        )

        # standard Material serialization
        data.uuid = self.uuid
        data.type = self.type

        if self.name != "" : data.name = self.name

        if self.color and hasattr( self.color, "isColor" ) : data.color = self.color.getHex()

        if self.roughness is not None : data.roughness = self.roughness
        if self.metalness is not None : data.metalness = self.metalness

        if self.emissive and hasattr( self.emissive, "isColor" ) : data.emissive = self.emissive.getHex()
        if self.specular and hasattr( self.specular, "isColor" ) : data.specular = self.specular.getHex()
        if self.shininess is not None : data.shininess = self.shininess
        if self.clearCoat is not None : data.clearCoat = self.clearCoat
        if self.clearCoatRoughness is not None : data.clearCoatRoughness = self.clearCoatRoughness

        if self.map and hasattr( self.map, "isTexture" ) : data.map = self.map.toJSON( meta ).uuid
        if self.alphaMap and hasattr( self.alphaMap, "isTexture" ) : data.alphaMap = self.alphaMap.toJSON( meta ).uuid
        if self.lightMap and hasattr( self.lightMap, "isTexture" ) : data.lightMap = self.lightMap.toJSON( meta ).uuid
        if self.bumpMap and hasattr( self.bumpMap, "isTexture" ) :

            data.bumpMap = self.bumpMap.toJSON( meta ).uuid
            data.bumpScale = self.bumpScale

        if self.normalMap and hasattr( self.normalMap, "isTexture" ) :

            data.normalMap = self.normalMap.toJSON( meta ).uuid
            data.normalScale = self.normalScale.toArray()

        if self.displacementMap and hasattr( self.displacementMap, "isTexture" ) :

            data.displacementMap = self.displacementMap.toJSON( meta ).uuid
            data.displacementScale = self.displacementScale
            data.displacementBias = self.displacementBias

        if self.roughnessMap and hasattr( self.roughnessMap, "isTexture" ) : data.roughnessMap = self.roughnessMap.toJSON( meta ).uuid
        if self.metalnessMap and hasattr( self.metalnessMap, "isTexture" ) : data.metalnessMap = self.metalnessMap.toJSON( meta ).uuid

        if self.emissiveMap and hasattr( self.emissiveMap, "isTexture" ) : data.emissiveMap = self.emissiveMap.toJSON( meta ).uuid
        if self.specularMap and hasattr( self.specularMap, "isTexture" ) : data.specularMap = self.specularMap.toJSON( meta ).uuid

        if self.envMap and hasattr( self.envMap, "isTexture" ) :

            data.envMap = self.envMap.toJSON( meta ).uuid
            data.reflectivity = self.reflectivity # Scale behind envMap

        if self.gradientMap and hasattr( self.gradientMap, "isTexture" ) :

            data.gradientMap = self.gradientMap.toJSON( meta ).uuid

        if self.size is not None : data.size = self.size
        if self.sizeAttenuation is not None : data.sizeAttenuation = self.sizeAttenuation

        if self.blending != NormalBlending : data.blending = self.blending
        if self.flatShading == True : data.flatShading = self.flatShading
        if self.side != FrontSide : data.side = self.side
        if self.vertexColors != NoColors : data.vertexColors = self.vertexColors

        if self.opacity < 1 : data.opacity = self.opacity
        if self.transparent == True : data.transparent = self.transparent

        data.depthFunc = self.depthFunc
        data.depthTest = self.depthTest
        data.depthWrite = self.depthWrite

        if self.alphaTest > 0 : data.alphaTest = self.alphaTest
        if self.premultipliedAlpha == True : data.premultipliedAlpha = self.premultipliedAlpha
        if self.wireframe == True : data.wireframe = self.wireframe
        if self.wireframeLinewidth > 1 : data.wireframeLinewidth = self.wireframeLinewidth
        if self.wireframeLinecap != "round" : data.wireframeLinecap = self.wireframeLinecap
        if self.wireframeLinejoin != "round" : data.wireframeLinejoin = self.wireframeLinejoin

        data.skinning = self.skinning
        data.morphTargets = self.morphTargets

        data.dithering = self.dithering

        # TODO: Copied from Object3D.toJSON

        def extractFromCache( cache ):

            values = []

            for key in cache :

                data = cache[ key ]
                deldata.metadata
                values.append( data )

            return values

        if isRoot :

            textures = extractFromCache( meta.textures )
            images = extractFromCache( meta.images )

            if len( textures ) > 0 : data.textures = textures
            if len( images ) > 0 : data.images = images

        return data

    def clone( self ):

        return Material().copy( self )

    def copy( self, source ):

        self.name = source.name

        self.fog = source.fog
        self.lights = source.lights

        self.blending = source.blending
        self.side = source.side
        self.flatShading = source.flatShading
        self.vertexColors = source.vertexColors

        self.opacity = source.opacity
        self.transparent = source.transparent

        self.blendSrc = source.blendSrc
        self.blendDst = source.blendDst
        self.blendEquation = source.blendEquation
        self.blendSrcAlpha = source.blendSrcAlpha
        self.blendDstAlpha = source.blendDstAlpha
        self.blendEquationAlpha = source.blendEquationAlpha

        self.depthFunc = source.depthFunc
        self.depthTest = source.depthTest
        self.depthWrite = source.depthWrite

        self.colorWrite = source.colorWrite

        self.precision = source.precision

        self.polygonOffset = source.polygonOffset
        self.polygonOffsetFactor = source.polygonOffsetFactor
        self.polygonOffsetUnits = source.polygonOffsetUnits

        self.dithering = source.dithering

        self.alphaTest = source.alphaTest

        self.premultipliedAlpha = source.premultipliedAlpha

        self.overdraw = source.overdraw

        self.visible = source.visible
        self.clipShadows = source.clipShadows
        self.clipIntersection = source.clipIntersection

        srcPlanes = source.clippingPlanes
        dstPlanes = None

        if srcPlanes is not None :

            n = len( srcPlanes )
            dstPlanes = Array( n )

            for i in xrange( n ):
                dstPlanes[ i ] = srcPlanes[ i ].clone()

        self.clippingPlanes = dstPlanes

        return self

    def dispose( self ):

        self.dispatchEvent( Expando( type = "dispose" ) )
