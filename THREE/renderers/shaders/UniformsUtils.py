from ...utils import Expando

def clone( uniforms_src ):

    uniforms_dst = Expando()

    for u in uniforms_src:

        uniforms_dst[ u ] = Expando()

        for p in uniforms_src[ u ]:

            parameter_src = uniforms_src[ u ][ p ]

            if parameter_src and (  getattr( parameter_src, "isColor", None ) or \
                                    getattr( parameter_src, "isMatrix3", None ) or \
                                    getattr( parameter_src, "isMatrix4", None ) or \
                                    getattr( parameter_src, "isVector2", None ) or \
                                    getattr( parameter_src, "isVector3", None ) or \
                                    getattr( parameter_src, "isVector4", None ) or \
                                    getattr( parameter_src, "isTexture", None ) ):

                uniforms_dst[ u ][ p ] = parameter_src.clone()

            elif isinstance( parameter_src, list ):

                uniforms_dst[ u ][ p ] = parameter_src[:]

            else:

                uniforms_dst[ u ][ p ] = parameter_src

    return uniforms_dst

def merge( uniforms ):

    merged = Expando()

    for u in uniforms:

        tmp = clone( u )

        for p in tmp:

            merged[ p ] = tmp[ p ]
    
    return merged