
def clone( uniforms_src ):

    uniforms_dst = {}

    for u in uniforms_src:

        uniforms_dst[ u ] = {}

        for p in uniforms_src[ u ]:

            parameter_src = uniforms_src[ u ][ p ]

            if parameter_src and (  hasattr( parameter_src, "isColor" ) or \
                                    hasattr( parameter_src, "isMatrix3" ) or \
                                    hasattr( parameter_src, "isMatrix4" ) or \
                                    hasattr( parameter_src, "isVector2" ) or \
                                    hasattr( parameter_src, "isVector3" ) or \
                                    hasattr( parameter_src, "isVector4" ) or \
                                    hasattr( parameter_src, "isTexture" ) ):

                uniforms_dst[ u ][ p ] = parameter_src.clone()

            elif isinstance( parameter_src, list ):

                uniforms_dst[ u ][ p ] = parameter_src[:]

            else:

                uniforms_dst[ u ][ p ] = parameter_src

    return uniforms_dst

def merge( uniforms ):

    merged = {}

    for u in uniforms:

        tmp = clone( u )

        for p in tmp:

            merged[ p ] = tmp[ p ]
    
    return merged