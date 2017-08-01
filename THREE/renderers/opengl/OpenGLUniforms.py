from OpenGL.GL import *

import re

class UniformContainer( object ):

    def __init__( self ):

        self.seq = []
        self.map = {}

RePathPart = re.compile( "([\w\d_]+)(\])?(\[|\.)?" )

# def parseUniform( activeInfo, addr, container ):

#     path = activeInfo.name
#     pathLength = path.length

#     while True:

#         match = RePathPart.search( path )
#         matchEnd = 

class OpenGLUniforms( UniformContainer ):

    def __init__( self, program ):

        super( OpenGLUniforms, self ).__init__()

        n = glGetProgramiv( program, GL_ACTIVE_UNIFORMS )

        for i in range( n ):

            info = glGetActiveUniform( program, i )
            path = info.name
            addr = glGetUniformLocation( program, path )

            logging.warning( info )
            # parseUniform( info, add, self )

    def setValue( self, name, value ):

        if name in self.map: self.map[ name ].setValue( value )

    def setOptional( self, object, name ):

        if name in self.object: self.setValue( name, self.object[ name ] )

    @staticmethod

    def seqWithValue( seq, values ):

        r = []

        for u in seq:

            if u.id in values: r.append( u )

        return r