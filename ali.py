from OpenGLContext import testingcontext

BaseContext = testingcontext.getInteractive()

from OpenGL.GL import *

from OpenGL.arrays import vbo

from OpenGLContext.arrays import *

from OpenGL.GL import shaders

class TestContext( BaseContext ):
    """Creates a simple vertex shader..."""

    def OnInit( self ):

        VERTEX_SHADER = shaders.compileShader("""#version 120
        void main() {
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }""", GL_VERTEX_SHADER)

        FRAGMENT_SHADER = shaders.compileShader("""#version 120
        void main() {
            gl_FragColor = vec4( 0, 1, 0, 1 );
        }""", GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)

        self.vbo = vbo.VBO(
            array( [
                [  0,  1, 0 ],
                [ -1, -1, 0 ],
                [  1, -1, 0 ],
                [  2, -1, 0 ],
                [  4, -1, 0 ],
                [  4,  1, 0 ],
                [  2, -1, 0 ],
                [  4,  1, 0 ],
                [  2,  1, 0 ],
            ], "f")
        )

        def Render( self, mode ):
            """Render the geometry for the scene."""

            shaders.glUseProgram(self.shader)

            try:
                self.vbo.bind()
                try:
                    glEnableClientState(GL_VERTEX_ARRAY)
                    glVertexPointerf(self.vbo)
                    glDrawArrays(GL_TRIANGLES, 0, 9)
                finally:
                    self.vbo.unbind()
                    glDisableClientState(GL_VERTEX_ARRAY)
            finally:
                shaders.glUseProgram(0)

if __name__ == "__main__":
    TestContext.ContextMainLoop()