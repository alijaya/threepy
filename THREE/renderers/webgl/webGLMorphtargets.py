from __future__ import division

import numpy as np

import logging

from OpenGL import GL

"""
 * @author mrdoob / "http":#mrdoob.com/
 """

class WebGLMorphtargets( object ):

    def __init__( self ):

        self.influencesList = {}
        self.morphInfluences = np.zeros( 8, np.float32 )

    def update( self, object, geometry, material, program ):

        objectInfluences = object.morphTargetInfluences

        length = len( objectInfluences )

        influences = self.influencesList.get( geometry.id )

        if influences is None :

            # initialise list

            influences = []

            for i in range( length ) :

                influences[ i ] = [ i, 0 ]

            self.influencesList[ geometry.id ] = influences

        morphTargets = material.morphTargets and geometry.morphAttributes.position
        morphNormals = material.morphNormals and geometry.morphAttributes.normal

        # Remove current morphAttributes

        for i in range( length ) :

            influence = influences[ i ]

            if influence[ 1 ] != 0 :

                if morphTargets : geometry.removeAttribute( "morphTarget" + i )
                if morphNormals : geometry.removeAttribute( "morphNormal" + i )

        # Collect influences

        for i in range( length ) :

            influence = influences[ i ]

            influence[ 0 ] = i
            influence[ 1 ] = objectInfluences[ i ]

        sorted( influences, key = lambda v: abs( v ) )

        # Add morphAttributes

        for i in range( 8 ) :

            influence = influences[ i ]

            if influence :

                index = influence[ 0 ]
                value = influence[ 1 ]

                if value :

                    if morphTargets : geometry.addAttribute( "morphTarget" + i, morphTargets[ index ] )
                    if morphNormals : geometry.addAttribute( "morphNormal" + i, morphNormals[ index ] )

                    self.morphInfluences[ i ] = value
                    continue

            self.morphInfluences[ i ] = 0

        program.getUniforms().setValue( gl, "morphTargetInfluences", self.morphInfluences )
