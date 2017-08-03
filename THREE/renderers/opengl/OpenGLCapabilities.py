from OpenGL.GL import *

import logging

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

precision = "highp"
maxPrecision = getMaxPrecision( precision )

if maxPrecision != precision:

    logging.warning( "THREE.WebGLRenderer: %s not supported, using %s instead.", precision, maxPrecision)
    precision = maxPrecision

def init():

    global maxTextures

    maxTextures = glGetInteger( GL_MAX_TEXTURE_IMAGE_UNITS )