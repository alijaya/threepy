from OpenGL import extensions as ext
from OpenGL.GL.ARB import depth_texture
from OpenGL.GL.EXT import texture_filter_anisotropic

extensions = {}

def get( name ):

    if name in extensions: return extensions[ name ] # cached

    extension = None

    if   name == "ARB_depth_texture": extension = depth_texture
    elif name == "EXT_texture_filter_anisotropic": extension = texture_filter_anisotropic

    extensions[ name ] = extension

    return extension