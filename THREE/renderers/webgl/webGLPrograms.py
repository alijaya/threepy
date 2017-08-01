from __future__ import division

import logging

from OpenGL import GL

from ...constants import BackSide, DoubleSide, CubeUVRefractionMapping, CubeUVReflectionMapping, GammaEncoding, LinearEncoding
import webGLProgram
"""
 * @author mrdoob / "http":#mrdoob.com/
 """

class WebGLPrograms( object ):

    def __init__( self, renderer, extensions, capabilities ):

        self.renderer = renderer
        self.extension = extensions
        self.capabilities = capabilities

        self.programs = []

        self.shaderIDs = {
            "MeshDepthMaterial": "depth",
            "MeshDistanceMaterial": "distanceRGBA",
            "MeshNormalMaterial": "normal",
            "MeshBasicMaterial": "basic",
            "MeshLambertMaterial": "lambert",
            "MeshPhongMaterial": "phong",
            "MeshToonMaterial": "phong",
            "MeshStandardMaterial": "physical",
            "MeshPhysicalMaterial": "physical",
            "LineBasicMaterial": "basic",
            "LineDashedMaterial": "dashed",
            "PointsMaterial": "points",
            "ShadowMaterial": "shadow"
        }

        self.parameterNames = [
            "precision", "supportsVertexTextures", "map", "mapEncoding", "envMap", "envMapMode", "envMapEncoding",
            "lightMap", "aoMap", "emissiveMap", "emissiveMapEncoding", "bumpMap", "normalMap", "displacementMap", "specularMap",
            "roughnessMap", "metalnessMap", "gradientMap",
            "alphaMap", "combine", "vertexColors", "fog", "useFog", "fogExp",
            "flatShading", "sizeAttenuation", "logarithmicDepthBuffer", "skinning",
            "maxBones", "useVertexTexture", "morphTargets", "morphNormals",
            "maxMorphTargets", "maxMorphNormals", "premultipliedAlpha",
            "numDirLights", "numPointLights", "numSpotLights", "numHemiLights", "numRectAreaLights",
            "shadowMapEnabled", "shadowMapType", "toneMapping", "physicallyCorrectLights",
            "alphaTest", "doubleSided", "flipSided", "numClippingPlanes", "numClipIntersection", "depthPacking", "dithering"
        ]

    def allocateBones( self, object ):

        skeleton = object.skeleton
        bones = skeleton.bones

        if self.capabilities.floatVertexTextures :

            return 1024

        else:

            # default for when object is not specified
            # ( for example when prebuilding shader to be used with multiple objects )
            #
            #  - leave some extra space for other uniforms
            #  - limit here is ANGLE"s 254 max uniform vectors
            #    (up to 54 should be safe)

            nVertexUniforms = self.capabilities.maxVertexUniforms
            nVertexMatrices = math.floor( ( nVertexUniforms - 20 ) / 4 )

            maxBones = min( nVertexMatrices, len( bones ) )

            if maxBones < len( bones ) :

                logging.warning( "THREE.WebGLRenderer: Skeleton has %s bones. This GPU supports %s." % ( len( bones ), maxBones ) )
                return 0

            return maxBones

    def getTextureEncodingFromMap( self, map, gammaOverrideLinear ):

        encoding = None

        if not map :

            encoding = LinearEncoding

        elif hasattr( map, "isTexture" ) :

            encoding = map.encoding

        elif hasattr( map, "isWebGLRenderTarget" ) :

            logging.warning( "THREE.WebGLPrograms.getTextureEncodingFromMap: don't use render targets as textures. Use their .texture property instead." )
            encoding = map.texture.encoding

        # add backwards compatibility for WebGLRenderer.gammaInput/gammaOutput parameter, should probably be removed at some point.
        if encoding == LinearEncoding and gammaOverrideLinear :

            encoding = GammaEncoding

        return encoding

    def getParameters( self, material, lights, shadows, fog, nClipPlanes, nClipIntersection, object ):

        shaderID = self.shaderIDs[ material.type ]

        # heuristics to create shader parameters according to lights in the scene
        # (not to blow over maxLights budget)

        maxBones = allocateBones( object ) if hasattr( object, "isSkinnedMesh" ) else 0
        precision = self.capabilities.precision

        if material.precision is not None :

            precision = self.capabilities.getMaxPrecision( material.precision )

            if precision != material.precision :

                logging.warning( "THREE.WebGLProgram.getParameters: %s not supported, using %s instead." % ( material.precision, precision ) )

        currentRenderTarget = self.renderer.getRenderTarget()

        parameters = {

            "shaderID": shaderID,

            "precision": precision,
            "supportsVertexTextures": self.capabilities.vertexTextures,
            "outputEncoding": getTextureEncodingFromMap( None if ( not currentRenderTarget ) else currentRenderTarget.texture, self.renderer.gammaOutput ),
            "map": material.map,
            "mapEncoding": getTextureEncodingFromMap( material.map, self.renderer.gammaInput ),
            "envMap": material.envMap,
            "envMapMode": material.envMap and material.envMap.mapping,
            "envMapEncoding": getTextureEncodingFromMap( material.envMap, self.renderer.gammaInput ),
            "envMapCubeUV": ( material.envMap ) and ( ( material.envMap.mapping == CubeUVReflectionMapping ) or ( material.envMap.mapping == CubeUVRefractionMapping ) ),
            "lightMap": material.lightMap,
            "aoMap": material.aoMap,
            "emissiveMap": material.emissiveMap,
            "emissiveMapEncoding": getTextureEncodingFromMap( material.emissiveMap, self.renderer.gammaInput ),
            "bumpMap": material.bumpMap,
            "normalMap": material.normalMap,
            "displacementMap": material.displacementMap,
            "roughnessMap": material.roughnessMap,
            "metalnessMap": material.metalnessMap,
            "specularMap": material.specularMap,
            "alphaMap": material.alphaMap,

            "gradientMap": material.gradientMap,

            "combine": material.combine,

            "vertexColors": material.vertexColors,

            "fog": fog,
            "useFog": material.fog,
            "fogExp": ( fog and hasattr( fog, "isFogExp2" ) ),

            "flatShading": material.flatShading,

            "sizeAttenuation": material.sizeAttenuation,
            "logarithmicDepthBuffer": self.capabilities.logarithmicDepthBuffer,

            "skinning": material.skinning and maxBones > 0,
            "maxBones": maxBones,
            "useVertexTexture": self.capabilities.floatVertexTextures,

            "morphTargets": material.morphTargets,
            "morphNormals": material.morphNormals,
            "maxMorphTargets": self.renderer.maxMorphTargets,
            "maxMorphNormals": self.renderer.maxMorphNormals,

            "numDirLights": len( lights.directional ),
            "numPointLights": len( lights.point ),
            "numSpotLights": len( lights.spot ),
            "numRectAreaLights": len( lights.rectArea ),
            "numHemiLights": len( lights.hemi ),

            "numClippingPlanes": nClipPlanes,
            "numClipIntersection": nClipIntersection,

            "dithering": material.dithering,

            "shadowMapEnabled": self.renderer.shadowMap.enabled and object.receiveShadow and len( shadows ) > 0,
            "shadowMapType": self.renderer.shadowMap.type,

            "toneMapping": self.renderer.toneMapping,
            "physicallyCorrectLights": self.renderer.physicallyCorrectLights,

            "premultipliedAlpha": material.premultipliedAlpha,

            "alphaTest": material.alphaTest,
            "doubleSided": material.side == DoubleSide,
            "flipSided": material.side == BackSide,

            "depthPacking": material.depthPacking if ( material.depthPacking is not None ) else False

        }

        return parameters

    def getProgramCode( self, material, parameters ):

        array = []

        if parameters.shaderID :

            array.append( parameters.shaderID )

        else:

            array.append( material.fragmentShader )
            array.append( material.vertexShader )

        if material.defines is not None :

            for name in material.defines :

                array.append( name )
                array.append( material.defines[ name ] )

        for i in range( len( self.parameterNames ) ) :

            array.append( parameters[ self.parameterNames[ i ] ] )

        array.append( material.onBeforeCompile.toString() )

        array.append( self.renderer.gammaOutput )

        return array.join()

    def acquireProgram( self, material, shader, parameters, code ):

        program = None

        # Check if code has been already compiled
        for programInfo in self.programs :

            programInfo = self.programs[ p ]

            if programInfo.code == code :

                program = programInfo
                program.usedTimes += 1

                break

        if program is None :

            program = webGLProgram.WebGLProgram( self.renderer, self.extensions, code, material, shader, parameters )
            self.programs.append( program )

        return program

    def releaseProgram( self, program ):

        program.usedTimes -= 1
        if program.usedTimes == 0 :

            # Remove from unordered set
            i = self.programs.indexOf( program )
            self.programs[ i ] = self.programs[ len( self.programs ) - 1 ]
            self.programs.pop()

            # Free WebGL resources
            program.destroy()
