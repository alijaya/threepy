from __future__ import division

from array import array

import logging

from OpenGL import GL

from ...math import box2
from ...math import vector2
from ...math import vector3
"""
 * @author mikael emtinger / "http":#gomo.se/
 * @author alteredq / "http":#alteredqualia.com/
 """

class WebGLFlareRenderer( object ):

    def __init__( self, renderer, state, textures, capabilities ):

        self.renderer = renderer
        self.state = state
        self.textures = textures
        self.capabilities = capabilities

        self.vertexBuffer = None
        self.elementBuffer = None

        self.shader = None
        self.program = None
        self.attributes = None
        self.uniforms = None

        self.tempTexture = None
        self.occlusionTexture = None

    def init( self ):

        vertices = array( "f", [
            - 1, - 1,  0, 0,
             1, - 1,  1, 0,
             1,  1,  1, 1,
            - 1,  1,  0, 1
        ] )

        faces = array( "H", [
            0, 1, 2,
            0, 2, 3
        ] )

        # buffers

        self.vertexBuffer     = GL.glCreateBuffer()
        self.elementBuffer    = GL.glCreateBuffer()

        GL.glBindBuffer( GL.GL_ARRAY_BUFFER, self.vertexBuffer )
        GL.glBufferData( GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW )

        GL.glBindBuffer( GL.GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer )
        GL.glBufferData( GL.GL_ELEMENT_ARRAY_BUFFER, faces, GL.GL_STATIC_DRAW )

        # textures

        self.tempTexture      = GL.glCreateTexture()
        self.occlusionTexture = GL.glCreateTexture()

        self.state.bindTexture( GL.GL_TEXTURE_2D, self.tempTexture )
        GL.glTexImage2D( GL.GL_TEXTURE_2D, 0, GL.GL_RGB, 16, 16, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, None )
        GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE )
        GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE )
        GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST )
        GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST )

        self.state.bindTexture( GL.GL_TEXTURE_2D, self.occlusionTexture )
        GL.glTexImage2D( GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, 16, 16, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, None )
        GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE )
        GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE )
        GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST )
        GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST )

        self.shader = {

            "vertexShader": 

"""
uniform lowp int renderType

uniform vec3 screenPosition
uniform vec2 scale
uniform float rotation

uniform sampler2D occlusionMap

attribute vec2 position
attribute vec2 uv

varying vec2 vUV
varying float vVisibility

void main() {

    vUV = uv

    vec2 pos = position

    if renderType == 2 :

        vec4 visibility = texture2D( occlusionMap, vec2( 0.1, 0.1 ) )
        visibility += texture2D( occlusionMap, vec2( 0.5, 0.1 ) )
        visibility += texture2D( occlusionMap, vec2( 0.9, 0.1 ) )
        visibility += texture2D( occlusionMap, vec2( 0.9, 0.5 ) )
        visibility += texture2D( occlusionMap, vec2( 0.9, 0.9 ) )
        visibility += texture2D( occlusionMap, vec2( 0.5, 0.9 ) )
        visibility += texture2D( occlusionMap, vec2( 0.1, 0.9 ) )
        visibility += texture2D( occlusionMap, vec2( 0.1, 0.5 ) )
        visibility += texture2D( occlusionMap, vec2( 0.5, 0.5 ) )

        vVisibility =        visibility.r / 9.0
        vVisibility *= 1.0 - visibility.g / 9.0
        vVisibility *=       visibility.b / 9.0
        vVisibility *= 1.0 - visibility.a / 9.0

        pos.x = cos( rotation ) * position.x - sin( rotation ) * position.y
        pos.y = sin( rotation ) * position.x + cos( rotation ) * position.y

    }

    gl_Position = vec4( ( pos * scale + screenPosition.xy ).xy, screenPosition.z, 1.0 )

}
"""

            ,"fragmentShader": 

"""
uniform lowp int renderType

uniform sampler2D map
uniform float opacity
uniform vec3 color

varying vec2 vUV
varying float vVisibility

void main() {

    // pink square

    if renderType == 0 :

        gl_FragColor = vec4( 1.0, 0.0, 1.0, 0.0 )

    // restore

    elif renderType == 1 :

        gl_FragColor = texture2D( map, vUV )

    // flare

    else:

        vec4 texture = texture2D( map, vUV )
        texture.a *= opacity * vVisibility
        gl_FragColor = texture
        gl_FragColor.rgb *= color

    }

}
"""
        }

        self.program = createProgram( self.shader )

        self.attributes = {
            "vertex": GL.glGetAttribLocation ( self.program, "position" ),
            "uv":     GL.glGetAttribLocation ( self.program, "uv" )
        }

        self.uniforms = {
            "renderType":     GL.glGetUniformLocation( self.program, "renderType" ),
            "map":            GL.glGetUniformLocation( self.program, "map" ),
            "occlusionMap":   GL.glGetUniformLocation( self.program, "occlusionMap" ),
            "opacity":        GL.glGetUniformLocation( self.program, "opacity" ),
            "color":          GL.glGetUniformLocation( self.program, "color" ),
            "scale":          GL.glGetUniformLocation( self.program, "scale" ),
            "rotation":       GL.glGetUniformLocation( self.program, "rotation" ),
            "screenPosition": GL.glGetUniformLocation( self.program, "screenPosition" )
        }

    """
     * Render lens flares
     * "Method": renders 16x16 0xff00ff-colored points scattered over the light source area,
     *         reads these back and calculates occlusion.
     """

    def render( self, flares, scene, camera, viewport ):

        if len( flares ) == 0 : return

        tempPosition = vector3.Vector3()

        invAspect = viewport.w / viewport.z
        halfViewportWidth = viewport.z * 0.5
        halfViewportHeight = viewport.w * 0.5

        size = 16 / viewport.w
        scale = vector2.Vector2( size * invAspect, size )

        screenPosition = vector3.Vector3( 1, 1, 0 )
        screenPositionPixels = vector2.Vector2( 1, 1 )

        validArea = box2.Box2()

        validArea.min.set( viewport.x, viewport.y )
        validArea.max.set( viewport.x + ( viewport.z - 16 ), viewport.y + ( viewport.w - 16 ) )

        if self.program is None :

            init()

        self.state.useProgram( self.program )

        self.state.initAttributes()
        self.state.enableAttribute( self.attributes.vertex )
        self.state.enableAttribute( self.attributes.uv )
        self.state.disableUnusedAttributes()

        # loop through all lens flares to update their occlusion and positions
        # setup gl and common used attribs/uniforms

        GL.glUniform1i( self.uniforms.occlusionMap, 0 )
        GL.glUniform1i( self.uniforms.map, 1 )

        GL.glBindBuffer( GL.GL_ARRAY_BUFFER, self.vertexBuffer )
        GL.glVertexAttribPointer( self.attributes.vertex, 2, GL.GL_FLOAT, False, 2 * 8, 0 )
        GL.glVertexAttribPointer( self.attributes.uv, 2, GL.GL_FLOAT, False, 2 * 8, 8 )

        GL.glBindBuffer( GL.GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer )

        self.state.disable( GL.GL_CULL_FACE )
        self.state.buffers.depth.setMask( False )

        for flare in flares:

            size = 16 / viewport.w
            scale.set( size * invAspect, size )

            # calc object screen position

            tempPosition.set( flare.matrixWorld.elements[ 12 ], flare.matrixWorld.elements[ 13 ], flare.matrixWorld.elements[ 14 ] )

            tempPosition.applyMatrix4( camera.matrixWorldInverse )
            tempPosition.applyMatrix4( camera.projectionMatrix )

            # setup arrays for gl self.programs

            screenPosition.copy( tempPosition )

            # horizontal and vertical coordinate of the lower left corner of the pixels to copy

            screenPositionPixels.x = viewport.x + ( screenPosition.x * halfViewportWidth ) + halfViewportWidth - 8
            screenPositionPixels.y = viewport.y + ( screenPosition.y * halfViewportHeight ) + halfViewportHeight - 8

            # screen cull

            if validArea.containsPoint( screenPositionPixels ) == True :

                # save current RGB to temp texture

                self.state.activeTexture( GL.GL_TEXTURE0 )
                self.state.bindTexture( GL.GL_TEXTURE_2D, None )
                self.state.activeTexture( GL.GL_TEXTURE1 )
                self.state.bindTexture( GL.GL_TEXTURE_2D, self.tempTexture )
                GL.glCopyTexImage2D( GL.GL_TEXTURE_2D, 0, GL.GL_RGB, screenPositionPixels.x, screenPositionPixels.y, 16, 16, 0 )

                # render pink quad

                GL.glUniform1i( self.uniforms.renderType, 0 )
                GL.glUniform2f( self.uniforms.scale, scale.x, scale.y )
                GL.glUniform3f( self.uniforms.screenPosition, screenPosition.x, screenPosition.y, screenPosition.z )

                self.state.disable( GL.GL_BLEND )
                self.state.enable( GL.GL_DEPTH_TEST )

                GL.glDrawElements( GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_SHORT, 0 )

                # copy result to occlusionMap

                self.state.activeTexture( GL.GL_TEXTURE0 )
                self.state.bindTexture( GL.GL_TEXTURE_2D, self.occlusionTexture )
                GL.glCopyTexImage2D( GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, screenPositionPixels.x, screenPositionPixels.y, 16, 16, 0 )

                # restore graphics

                GL.glUniform1i( self.uniforms.renderType, 1 )
                self.state.disable( GL.GL_DEPTH_TEST )

                self.state.activeTexture( GL.GL_TEXTURE1 )
                self.state.bindTexture( GL.GL_TEXTURE_2D, self.tempTexture )
                GL.glDrawElements( GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_SHORT, 0 )

                # update object positions

                flare.positionScreen.copy( screenPosition )

                if flare.customUpdateCallback :

                    flare.customUpdateCallback( flare )

                else:

                    flare.updateLensFlares()

                # render flares

                GL.glUniform1i( self.uniforms.renderType, 2 )
                self.state.enable( GL.GL_BLEND )

                for sprite in flare.lensFlares:

                    if sprite.opacity > 0.001 and sprite.scale > 0.001 :

                        screenPosition.x = sprite.x
                        screenPosition.y = sprite.y
                        screenPosition.z = sprite.z

                        size = sprite.size * sprite.scale / viewport.w

                        scale.x = size * invAspect
                        scale.y = size

                        GL.glUniform3f( self.uniforms.screenPosition, screenPosition.x, screenPosition.y, screenPosition.z )
                        GL.glUniform2f( self.uniforms.scale, scale.x, scale.y )
                        GL.glUniform1f( self.uniforms.rotation, sprite.rotation )

                        GL.glUniform1f( self.uniforms.opacity, sprite.opacity )
                        GL.glUniform3f( self.uniforms.color, sprite.color.r, sprite.color.g, sprite.color.b )

                        self.state.setBlending( sprite.blending, sprite.blendEquation, sprite.blendSrc, sprite.blendDst )

                        self.textures.setTexture2D( sprite.texture, 1 )

                        GL.glDrawElements( GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_SHORT, 0 )

        # restore gl

        self.state.enable( GL.GL_CULL_FACE )
        self.state.enable( GL.GL_DEPTH_TEST )
        self.state.buffers.depth.setMask( True )

        self.state.reset()

    def createProgram( self, shader ):

        program = GL.glCreateProgram()

        fragmentShader = GL.glCreateShader( GL.GL_FRAGMENT_SHADER )
        vertexShader = GL.glCreateShader( GL.GL_VERTEX_SHADER )

        prefix = "precision " + self.capabilities.precision + " float\n"

        GL.glShaderSource( fragmentShader, prefix + shader.fragmentShader )
        GL.glShaderSource( vertexShader, prefix + shader.vertexShader )

        GL.glCompileShader( fragmentShader )
        GL.glCompileShader( vertexShader )

        GL.glAttachShader( program, fragmentShader )
        GL.glAttachShader( program, vertexShader )

        GL.glLinkProgram( program )

        return program
