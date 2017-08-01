import OpenGLGeometries as geometries

# update to opengl
def update( object ):

    geometry = object.geometry
    buffergeometry = geometries.get( object, geometry )

    # TODO update once per frame

    if True:

        if hasattr( geometry, "isGeometry" ):

            buffergeometry.updateFromObject( object )
        
        geometries.update( buffergeometry )
    
    return buffergeometry