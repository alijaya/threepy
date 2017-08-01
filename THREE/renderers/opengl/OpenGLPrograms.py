import openGLProgram

from ...utils import Expando

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

def getParameters( material, lights, shadows, fog, nClipPlanes, nClipIntersection, object ):

    shaderId = shaderIDs.get( material.type )

    # TODO maxBones
    # TODO precision

    # currentRenderTarget = renderer.getRenderTarget()

    parameters = Expando(
        shaderID = shaderId,

        # precision = precision,
        # supportsVertexTextures =
        # outputEncoding =
        map = bool( material.map ),
        # mapEncoding =
        # envMap = bool( material.envMap),
        # envMapMode = material.envMap and material.envMap.mapping,
        # envMapEncoding =

        fog = bool( fog ),
        useFog = material.fog,
        fogExp = fog and fog.isFogExp2,

        flatShading = material.flatShading,

        # etc
    )

    return parameters

# get hash code from parameters
def getProgramCode( material, parameters ):

    array = []

    if parameters.shaderID:

        array.append( parameters.shaderID )
    
    else:

        array.append( material.fragmentShader )
        array.append( material.vertexShader )
    
    # if material.defines:

    #     for key, value in material.defines:

    #         array.append( key )
    #         array.append( value )
    
    for param in parameterNames:

        array.append( parameters[ param ] )
    
    # array.push()

    # array.push( renderer.gammaOutput )

    return "".join( map( str, array ) )

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