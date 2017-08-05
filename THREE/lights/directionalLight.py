import light
# import directionalLightShadow
from ..core import object3D

"""
 * @author mrdoob / "http":#mrdoob.com/
 * @author alteredq / "http":#alteredqualia.com/
 """

class DirectionalLight( light.Light ):

    def __init__( self, color = 0xffffff, intensity = 1 ):

        super( DirectionalLight, self ).__init__( color, intensity )

        self.isDirectionalLight = True

        self.type = "DirectionalLight"

        self.position.copy( object3D.Object3D.DefaultUp )
        self.updateMatrix()

        self.target = object3D.Object3D()

        # self.shadow = directionalLightShadow.DirectionalLightShadow()
        self.shadow = None

    def copy( self, source ):

        super( DirectionalLight, self ).copy( source )

        self.target = source.target.clone()

        self.shadow = source.shadow.clone()

        return self
