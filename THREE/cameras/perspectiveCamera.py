from __future__ import division
import math

import camera
from ..core import object3D
from ..math import _Math

from ..utils import Expando

"""
 * @author mrdoob / http:#mrdoob.com/
 * @author greggman / http:#games.greggman.com/
 * @author zz85 / http:#www.lab4games.net/zz85/blog
 * @author tschw
 """

class PerspectiveCamera( camera.Camera ):

    def __init__( self, fov = 50, aspect = 1, near = 0.1, far = 2000 ):

        super( PerspectiveCamera, self ).__init__()

        self.type = "PerspectiveCamera"

        self.fov = fov
        self.zoom = 1

        self.near = near
        self.far = far
        self.focus = 10

        self.aspect = aspect
        self.view = None

        self.filmGauge = 35    # width of the film (default in millimeters)
        self.filmOffset = 0    # horizontal film offset (same unit as gauge)

        self.updateProjectionMatrix()

        self.isPerspectiveCamera = True

    def clone( self ):

        return PerspectiveCamera().copy( self )

    def copy( self, source, recursive = True ):

        super( PerspectiveCamera, self).copy( source, recursive )

        self.fov = source.fov
        self.zoom = source.zoom

        self.near = source.near
        self.far = source.far
        self.focus = source.focus

        self.aspect = source.aspect
        self.view = None if source.view is None else source.view.copy()

        self.filmGauge = source.filmGauge
        self.filmOffset = source.filmOffset

        return self

    """
     * Sets the FOV by focal length in respect to the current .filmGauge.
     *
     * The default film gauge is 35, so that the focal length can be specified for
     * a 35mm (full frame) camera.
     *
     * Values for focal length and film gauge must have the same unit.
     """
    def setFocalLength( self, focalLength ):

        # see http:#www.bobatkins.com/photography/technical/field_of_view.html
        vExtentSlope = 0.5 * self.getFilmHeight() / focalLength

        self.fov = _math.RAD2DEG * 2 * math.atan( vExtentSlope )
        self.updateProjectionMatrix()

    """
     * Calculates the focal length from the current .fov and .filmGauge.
     """
    def getFocalLength( self ):

        vExtentSlope = math.tan( _math.DEG2RAD * 0.5 * self.fov )

        return 0.5 * self.getFilmHeight() / vExtentSlope

    def getEffectiveFOV( self ):

        return _Math.RAD2DEG * 2 * math.atan(
                math.tan( _Math.DEG2RAD * 0.5 * self.fov ) / self.zoom )

    def getFilmWidth( self ):

        # film not completely covered in portrait format (aspect < 1)
        return self.filmGauge * min( self.aspect, 1 )

    def getFilmHeight( self ):

        # film not completely covered in landscape format (aspect > 1)
        return self.filmGauge / max( self.aspect, 1 )

    """
     * Sets an offset in a larger frustum. This is useful for multi-window or
     * multi-monitor/multi-machine setups.
     *
     * For example, if you have 3x2 monitors and each monitor is 1920x1080 and
     * the monitors are in grid like self
     *
     *   +---+---+---+
     *   | A | B | C |
     *   +---+---+---+
     *   | D | E | F |
     *   +---+---+---+
     *
     * then for each monitor you would call it like self
     *
     *   w = 1920
     *   h = 1080
     *   fullWidth = w * 3
     *   fullHeight = h * 2
     *
     *   --A--
     *   camera.setOffset( fullWidth, fullHeight, w * 0, h * 0, w, h )
     *   --B--
     *   camera.setOffset( fullWidth, fullHeight, w * 1, h * 0, w, h )
     *   --C--
     *   camera.setOffset( fullWidth, fullHeight, w * 2, h * 0, w, h )
     *   --D--
     *   camera.setOffset( fullWidth, fullHeight, w * 0, h * 1, w, h )
     *   --E--
     *   camera.setOffset( fullWidth, fullHeight, w * 1, h * 1, w, h )
     *   --F--
     *   camera.setOffset( fullWidth, fullHeight, w * 2, h * 1, w, h )
     *
     *   Note there is no reason monitors have to be the same size or in a grid.
     """
    def setViewOffset( self, fullWidth, fullHeight, x, y, width, height ):

        self.aspect = fullWidth / fullHeight

        self.view = Expando(
            fullWidth = fullWidth,
            fullHeight = fullHeight,
            offsetX = x,
            offsetY = y,
            width = width,
            height = height
        )

        self.updateProjectionMatrix()

    def clearViewOffset( self ):

        self.view = None
        self.updateProjectionMatrix()

    def updateProjectionMatrix( self ):

        near = self.near
        top = near * math.tan( _Math.DEG2RAD * 0.5 * self.fov ) / self.zoom
        height = 2 * top
        width = self.aspect * height
        left = - 0.5 * width
        view = self.view

        if view != None:

            fullWidth = view.fullWidth
            fullHeight = view.fullHeight

            left += view.offsetX * width / fullWidth
            top -= view.offsetY * height / fullHeight
            width *= view.width / fullWidth
            height *= view.height / fullHeight

        skew = self.filmOffset
        if skew != 0: left += near * skew / self.getFilmWidth()

        self.projectionMatrix.makePerspective( left, left + width, top, top - height, near, self.far )

    def toJSON( self, meta ):

        data = super( PerspectiveCamera, self ).toJSON( meta )

        data.object.fov = self.fov
        data.object.zoom = self.zoom

        data.object.near = self.near
        data.object.far = self.far
        data.object.focus = self.focus

        data.object.aspect = self.aspect

        if self.view != None: data.object.view = self.view.copy()

        data.object.filmGauge = self.filmGauge
        data.object.filmOffset = self.filmOffset

        return data
