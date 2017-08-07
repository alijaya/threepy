import OpenGLGeometries as geometries

updateList = {}

# update to opengl
def update( object ):

    from ..OpenGLRenderer import _infoRender as infoRender

    frame = infoRender.frame

    geometry = object.geometry
    buffergeometry = geometries.get( object, geometry )

    # update once per frame

    if updateList.get( buffergeometry.id ) != frame:

        if hasattr( geometry, "isGeometry" ):

            buffergeometry.updateFromObject( object )
        
        geometries.update( buffergeometry )

        updateList[ buffergeometry.id ] = frame
    
    return buffergeometry