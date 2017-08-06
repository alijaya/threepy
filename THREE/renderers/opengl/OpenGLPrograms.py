import openGLProgram

from ...constants import BackSide, DoubleSide, CubeUVRefractionMapping, CubeUVReflectionMapping, GammaEncoding, LinearEncoding
from ...utils import Expando
import OpenGLCapabilities as capabilities

programs = []

shaderIDs = {
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
    "ShadowMaterial": "shadow",
}

parameterNames = [
    "precision", "supportsVertexTextures", "map", "mapEncoding", "envMap", "envMapMode", "envMapEncoding",
    "lightMap", "aoMap", "emissiveMap", "emissiveMapEncoding", "bumpMap", "normalMap", "displacementMap", "specularMap",
    "roughnessMap", "metalnessMap", "gradientMap",
    "alphaMap", "combine", "vertexColors", "fog", "useFog", "fogExp",
    "flatShading", "sizeAttenuation", "logarithmicDepthBuffer", "skinning",
    "maxBones", "useVertexTexture", "morphTargets", "morphNormals",
    "maxMorphTargets", "maxMorphNormals", "premultipliedAlpha",
    "numDirLights", "numPointLights", "numSpotLights", "numHemiLights", "numRectAreaLights",
    "shadowMapEnabled", "shadowMapType", "toneMapping", 'physicallyCorrectLights',
    "alphaTest", "doubleSided", "flipSided", "numClippingPlanes", "numClipIntersection", "depthPacking", "dithering"
]

def getTextureEncodingFromMap( map, gammaOverrideLinear ):

    encoding = None

    if not map:

        encoding = LinearEncoding

    elif hasattr( map, "isTexture" ):

        encoding = map.encoding

    elif hasattr( map, isOpenGLRenderTarget ):

        logging.warning( "THREE.WebGLPrograms.getTextureEncodingFromMap: don't use render targets as textures. Use their .texture property instead.")
        encoding = map.texture.encoding
    
    if encoding == LinearEncoding and gammaOverrideLinear:

        encoding = GammaEncoding

    return encoding

def getParameters( material, lights, shadows, fog, nClipPlanes, nClipIntersection, object ):

    from .. import OpenGLRenderer as renderer

    shaderId = shaderIDs.get( material.type )

    # TODO maxBones

    precision = capabilities.precision

    if material.precision != None:

        precision = capabilities.getMaxPrecision( material.precision )

        if precision != material.precision:

            logging.warning( "THREE.WebGLProgram.getParameters: %s not supported, using %s instead.", material.precision, precision )

    currentRenderTarget = renderer.getRenderTarget()
    
    parameters = Expando(
        shaderID = shaderId,

        precision = precision,
        # supportsVertexTextures = capabilities.vertexTextures,
        outputEncoding = getTextureEncodingFromMap( None if not currentRenderTarget else currentRenderTarget.texture, renderer.gammaOutput ),
        map = bool( material.map ),
        mapEncoding = getTextureEncodingFromMap( material.map, renderer.gammaInput ),
        envMap = bool( material.envMap ),
        envMapMode = material.envMap and material.envMap.mapping,
        envMapEncoding = getTextureEncodingFromMap( material.envMap, renderer.gammaInput ),
        envMapCubeUV = bool( material.envMap ) and ( material.envMap.mapping == CubeUVReflectionMapping or material.envMap.mapping == CubeUVRefractionMapping ),
        lightMap = bool( material.lightMap ),
        aoMap = bool( material.aoMap ),
        emissiveMap = bool( material.emissiveMap ),
        emissiveMapEncoding = getTextureEncodingFromMap( material.emissiveMap, renderer.gammaInput ),
        bumpMap = bool( material.bumpMap ),
        normalMap = bool( material.normalMap ),
        displacementMap = bool( material.displacementMap ),
        roughnessMap = bool( material.roughnessMap ),
        metalnessMap = bool( material.metalnessMap ),
        specularMap = bool( material.specularMap ),
        alphaMap = bool( material.alphaMap ),

        gradientMap = bool( material.gradientMap ),

        combine = material.combine,

        vertexColors = material.vertexColors,

        fog = bool( fog ),
        useFog = material.fog,
        fogExp = fog and hasattr( fog, "isFogExp2" ),

        flatShading = material.flatShading,

        sizeAttenuation = material.sizeAttenuation,
        # logarithmicDepthBuffer = capabilities.logarithmicDepthBuffer,

        # skinning = material.skinning and maxBones > 0,
        # maxBones = maxBones,
        # useVertexTexture = capabilities.floatVertexTextures,

        # morphTargets = material.morphTargets,
        # morphNormals = material.morphNormals,
        # maxMorphTargets = renderer.maxMorphTargets,
        # maxMorphNormals = renderer.maxMorphNormals,

        numDirLights = len( lights.directional ),
        numPointLights = len( lights.point ),
        numSpotLights = len( lights.spot ),
        numRectAreaLights = len( lights.rectArea ),
        numHemiLights = len( lights.hemi ),

        numClippingPlanes = nClipPlanes, # TODO
        numClipIntersection = nClipIntersection,

        # dithering = material.dithering,

        # shadowMapEnabled = renderer.shadowMap.enabled and object.receiveShadow and len( shadows ) > 0,
        # shadowMapType = renderer.shadowMap.type,

        toneMapping = renderer.toneMapping,
        # physicallyCorrectLights = renderer.physicallyCorrectLights,

        # premultipliedAlpha = material.premultipliedAlpha,

        alphaTest = material.alphaTest,
        doubleSided = material.side == DoubleSide,
        flipSided = material.side == BackSide,

        # depthPacking = bool( material.depthPacking )
        # etc
    )

    return parameters

# get hash code from parameters
def getProgramCode( material, parameters ):

    from .. import OpenGLRenderer as renderer

    array = []

    if parameters.shaderID:

        array.append( parameters.shaderID )
    
    else:

        array.append( material.fragmentShader )
        array.append( material.vertexShader )
    
    if material.defines:

        for key, value in material.defines:

            array.append( key )
            array.append( value )
    
    for param in parameterNames:

        array.append( parameters[ param ] if parameters[ param ] is not None else "" )
    
    array.append( str( material.onBeforeCompile ) )

    array.append( renderer.gammaOutput )

    return ",".join( map( str, array ) )

def acquireProgram( material, shader, parameters, code ):

    program = None

    # check in cache

    for programInfo in programs:

        if programInfo.code == code:

            program = programInfo
            program.usedTimes += 1

            break

    if not program: # if not found, create new

        program = openGLProgram.OpenGLProgram( code, material, shader, parameters )
        programs.append( program )
    
    return program

def releaseProgram( program ):

    program.usedTimes -= 1

    if program.usedTimes == 0:

        programs.remove( program )
        
        program.destroy()