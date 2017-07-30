from __future__ import division

import THREE

width = 800
height = 600

scene = THREE.Scene()
camera = THREE.PerspectiveCamera( 75, width / height, 0.1, 1000 )

geometry = THREE.BoxGeometry( 1, 1, 1 );
# material = THREE.MeshBasicMaterial( { "color": 0x00ff00 } );
# cube = THREE.Mesh( geometry, material );
# scene.add( cube );

# camera.position.z = 5;