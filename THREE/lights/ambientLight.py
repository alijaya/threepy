import light

"""
 * @author mrdoob / "http":#mrdoob.com/
 """

class AmbientLight( light.Light ):

    def __init__( self, color = 0xffffff, intensity = 1 ):

        super( AmbientLight, self ).__init__( color, intensity )

        self.isAmbientLight = True

        self.type = "AmbientLight"

        self.castShadow = None