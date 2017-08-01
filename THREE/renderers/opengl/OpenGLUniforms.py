from OpenGL.GL import *

class OpenGLUniforms( UniformContainer ):

    def __init__( self, program ):

        super( OpenGLUniforms, self ).__init__()

        n = glGetProgramiv( program, glActiveUniforms )

        for i in range( n ):

            info = glGetActiveUniform( program, i )
            path = info.name
            addr = glGetUniformLocation( program, path )

        parseUniform( info, add, self )

    def setValue( self, name, value ):

        if name in self.map: self.map[ name ].setValue( value )

    def setOptional( self, object, name ):

        if name in self.object: self.setValue( name, self.object[ name ] )