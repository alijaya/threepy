from __future__ import division

import logging

from OpenGL import GL

"""
 * @author mrdoob / "http":#mrdoob.com/
 """

class WebGLBufferRenderer( object ):

    def __init__( self, extensions, infoRender ):

        self.mode = None
        self.extensions = extensions
        self.infoRender = infoRender

    def setMode( self, value ):

        self.mode = value

    def render( self, start, count ):

        GL.glDrawArrays( self.mode, start, count )

        self.infoRender.calls += 1
        self.infoRender.vertices += count

        if self.mode == GL.GL_TRIANGLES : self.infoRender.faces += count / 3
        elif self.mode == GL.GL_POINTS : self.infoRender.points += count

    def renderInstances( self, geometry, start, count ):

        extension = self.extensions.get( "ANGLE_instanced_arrays" )

        if extension is None :

            logging.error( "THREE.WebGLBufferRenderer: using THREE.InstancedBufferGeometry but hardware does not support extension ANGLE_instanced_arrays." )
            return

        position = geometry.attributes.position

        if hasattr( position, "isInterleavedBufferAttribute" ) :

            count = position.data.count

            extension.drawArraysInstancedANGLE( self.mode, 0, count, geometry.maxInstancedCount )

        else:

            extension.drawArraysInstancedANGLE( self.mode, start, count, geometry.maxInstancedCount )

        self.infoRender.calls += 1
        self.infoRender.vertices += count * geometry.maxInstancedCount

        if self.mode == GL.GL_TRIANGLES : self.infoRender.faces += geometry.maxInstancedCount * count / 3
        elif self.mode == GL.GL_POINTS : self.infoRender.points += geometry.maxInstancedCount * count