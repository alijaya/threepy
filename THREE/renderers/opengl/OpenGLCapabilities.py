from OpenGL.GL import *

import OpenGLExtensions as extensions

import logging

def getMaxAnisotropy():

    global maxAnisotropy

    if maxAnisotropy is not None: return maxAnisotropy

    extension = extensions.get( "EXT_texture_filter_anisotropic" )

    if extension:

        maxAnisotropy = glGetFloatv( extension.GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT )

    else:

        maxAnisotropy = 0

    return maxAnisotropy

def getMaxPrecision( precision ):

    # because the code doesn't work, just hack it
    return "highp"

    # if precision == "highp":

    #     if  glGetShaderPrecisionFormat( GL_VERTEX_SHADER, GL_HIGH_FLOAT ).precision > 0 and \
    #         glGetShaderPrecisionFormat( GL_FRAGMENT_SHADER, GL_HIGH_FLOAT ).precision > 0:

    #         return "highp"

    #     precision = "mediump"
    
    # if precision == "mediump":

    #     if  glGetShaderPrecisionFormat( GL_VERTEX_SHADER, GL_MEDIUM_FLOAT ).precision > 0 and \
    #         glGetShaderPrecisionFormat( GL_FRAGMENT_SHADER, GL_MEDIUM_FLOAT ).precision > 0:

    #         return "mediump"

    # return "lowp"

maxAnisotropy = None
precision = "highp"
maxPrecision = getMaxPrecision( precision )

if maxPrecision != precision:

    logging.warning( "THREE.WebGLRenderer: %s not supported, using %s instead.", precision, maxPrecision)
    precision = maxPrecision

def init():

    global maxTextures

    maxTextures = glGetInteger( GL_MAX_TEXTURE_IMAGE_UNITS )