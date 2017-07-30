from __future__ import division

import logging

from OpenGL import GL

from ...math import matrix3
from ...math import plane
"""
 * @author tschw
 """

class WebGLClipping( object ):

    def __init__( self ):

        globalState = None
        numGlobalPlanes = 0
        localClippingEnabled = False
        renderingShadows = False

        plane = plane.Plane()
        viewNormalMatrix = matrix3.Matrix3()

        uniform = { "value": None, "needsUpdate": False }

        self.uniform = uniform
        self.numPlanes = 0
        self.numIntersection = 0

    def init( self, planes, enableLocalClipping, camera ):

        enabled = \
            len( planes ) != 0 or \
            enableLocalClipping or \
            numGlobalPlanes != 0 or \
            localClippingEnabled
            # enable state of previous frame - the clipping code has to
            # run another frame in order to reset the "state":

        localClippingEnabled = enableLocalClipping

        globalState = projectPlanes( planes, camera, 0 )
        numGlobalPlanes = len( planes )

        return enabled

    def beginShadows( self ):

        renderingShadows = True
        projectPlanes( None )

    def endShadows( self ):

        renderingShadows = False
        resetGlobalState()

    def setState( self, planes, clipIntersection, clipShadows, camera, cache, fromCache ):

        if not localClippingEnabled or \
                planes is None or len( planes ) == 0 or \
                renderingShadows and not clipShadows :
            # there"s no local clipping

            if renderingShadows :
                # there"s no global clipping

                projectPlanes( None )

            else:

                resetGlobalState()

        else:

            nGlobal = 0 if renderingShadows else numGlobalPlanes
            lGlobal = nGlobal * 4

            dstArray = cache.clippingState or None

            uniform.value = dstArray # ensure unique state

            dstArray = projectPlanes( planes, camera, lGlobal, fromCache )

            for i in range( lGlobal ):

                dstArray[ i ] = globalState[ i ]

            cache.clippingState = dstArray
            self.numIntersection = self.numPlanes if clipIntersection else 0
            self.numPlanes += nGlobal

    def resetGlobalState( self ):

        if uniform.value != globalState :

            uniform.value = globalState
            uniform.needsUpdate = numGlobalPlanes > 0

        self.numPlanes = numGlobalPlanes
        self.numIntersection = 0

    def projectPlanes( self, planes, camera, dstOffset, skipTransform ):

        nPlanes = len( planes ) if planes is not None else 0
        dstArray = None

        if nPlanes != 0 :

            dstArray = uniform.value

            if skipTransform != True or dstArray is None :

                flatSize = dstOffset + nPlanes * 4
                viewMatrix = camera.matrixWorldInverse

                viewNormalMatrix.getNormalMatrix( viewMatrix )

                if dstArray is None or len( dstArray ) < flatSize :

                    dstArray = Float32Array( flatSize )

                i = 0
                i4 = dstOffset
                while i < nPlanes :

                    plane.copy( planes[ i ] ).applyMatrix4( viewMatrix, viewNormalMatrix )

                    plane.normal.toArray( dstArray, i4 )
                    dstArray[ i4 + 3 ] = plane.constant

                    i += 1
                    i4 += 4

            uniform.value = dstArray
            uniform.needsUpdate = True

        self.numPlanes = nPlanes

        return dstArray
