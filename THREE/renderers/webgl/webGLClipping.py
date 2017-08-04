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

        self.globalState = None
        self.numGlobalPlanes = 0
        self.localClippingEnabled = False
        self.renderingShadows = False

        self.viewNormalMatrix = matrix3.Matrix3()

        self.uniform = { "value": None, "needsUpdate": False }

        self.numPlanes = 0
        self.numIntersection = 0

    def init( self, planes, enableLocalClipping, camera ):

        enabled = \
            len( planes ) != 0 or \
            enableLocalClipping or \
            self.numGlobalPlanes != 0 or \
            self.localClippingEnabled
            # enable state of previous frame - the clipping code has to
            # run another frame in order to reset the "state":

        self.localClippingEnabled = enableLocalClipping

        self.globalState = self.projectPlanes( planes, camera, 0 )
        self.numGlobalPlanes = len( planes )

        return enabled

    def beginShadows( self ):

        self.renderingShadows = True
        projectPlanes( None )

    def endShadows( self ):

        self.renderingShadows = False
        resetGlobalState()

    def setState( self, planes, clipIntersection, clipShadows, camera, cache, fromCache ):

        if not self.localClippingEnabled or \
                planes is None or len( planes ) == 0 or \
                self.renderingShadows and not clipShadows :
            # there"s no local clipping

            if self.renderingShadows :
                # there"s no global clipping

                projectPlanes( None )

            else:

                resetGlobalState()

        else:

            nGlobal = 0 if self.renderingShadows else self.numGlobalPlanes
            lGlobal = nGlobal * 4

            dstArray = cache.clippingState or None

            self.uniform.value = dstArray # ensure unique state

            dstArray = projectPlanes( planes, camera, lGlobal, fromCache )

            for i in xrange( lGlobal ):

                dstArray[ i ] = self.globalState[ i ]

            cache.clippingState = dstArray
            self.numIntersection = self.numPlanes if clipIntersection else 0
            self.numPlanes += nGlobal

    def resetGlobalState( self ):

        if self.uniform.value != self.globalState :

            self.uniform.value = self.globalState
            self.uniform.needsUpdate = self.numGlobalPlanes > 0

        self.numPlanes = self.numGlobalPlanes
        self.numIntersection = 0

    def projectPlanes( self, planes, camera, dstOffset, skipTransform = False ):

        nPlanes = len( planes ) if planes is not None else 0
        dstArray = None

        if nPlanes != 0 :

            dstArray = self.uniform.value

            if skipTransform != True or dstArray is None :

                flatSize = dstOffset + nPlanes * 4
                viewMatrix = camera.matrixWorldInverse

                self.viewNormalMatrix.getNormalMatrix( viewMatrix )

                if dstArray is None or len( dstArray ) < flatSize :

                    dstArray = Float32Array( flatSize )

                i = 0
                i4 = dstOffset
                while i < nPlanes :

                    plane = planes[ i ].clone().applyMatrix4( viewMatrix, self.viewNormalMatrix )

                    plane.normal.toArray( dstArray, i4 )
                    dstArray[ i4 + 3 ] = plane.constant

                    i += 1
                    i4 += 4

            self.uniform.value = dstArray
            self.uniform.needsUpdate = True

        self.numPlanes = nPlanes

        return dstArray
