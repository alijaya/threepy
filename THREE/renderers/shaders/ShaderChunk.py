import os

__here = os.path.dirname(__file__)
__join = os.path.join

alphamap_fragment = open( __join(__here, "ShaderChunk/alphamap_fragment.glsl"), "r" ).read()
alphamap_pars_fragment = open( __join(__here, "ShaderChunk/alphamap_pars_fragment.glsl"), "r" ).read()
alphatest_fragment = open( __join(__here, "ShaderChunk/alphatest_fragment.glsl"), "r" ).read()
aomap_fragment = open( __join(__here, "ShaderChunk/aomap_fragment.glsl"), "r" ).read()
aomap_pars_fragment = open( __join(__here, "ShaderChunk/aomap_pars_fragment.glsl"), "r" ).read()
begin_vertex = open( __join(__here, "ShaderChunk/begin_vertex.glsl"), "r" ).read()
beginnormal_vertex = open( __join(__here, "ShaderChunk/beginnormal_vertex.glsl"), "r" ).read()
bsdfs = open( __join(__here, "ShaderChunk/bsdfs.glsl"), "r" ).read()
bumpmap_pars_fragment = open( __join(__here, "ShaderChunk/bumpmap_pars_fragment.glsl"), "r" ).read()
clipping_planes_fragment = open( __join(__here, "ShaderChunk/clipping_planes_fragment.glsl"), "r" ).read()
clipping_planes_pars_fragment = open( __join(__here, "ShaderChunk/clipping_planes_pars_fragment.glsl"), "r" ).read()
clipping_planes_pars_vertex = open( __join(__here, "ShaderChunk/clipping_planes_pars_vertex.glsl"), "r" ).read()
clipping_planes_vertex = open( __join(__here, "ShaderChunk/clipping_planes_vertex.glsl"), "r" ).read()
color_fragment = open( __join(__here, "ShaderChunk/color_fragment.glsl"), "r" ).read()
color_pars_fragment = open( __join(__here, "ShaderChunk/color_pars_fragment.glsl"), "r" ).read()
color_pars_vertex = open( __join(__here, "ShaderChunk/color_pars_vertex.glsl"), "r" ).read()
color_vertex = open( __join(__here, "ShaderChunk/color_vertex.glsl"), "r" ).read()
common = open( __join(__here, "ShaderChunk/common.glsl"), "r" ).read()
cube_uv_reflection_fragment = open( __join(__here, "ShaderChunk/cube_uv_reflection_fragment.glsl"), "r" ).read()
defaultnormal_vertex = open( __join(__here, "ShaderChunk/defaultnormal_vertex.glsl"), "r" ).read()
displacementmap_pars_vertex = open( __join(__here, "ShaderChunk/displacementmap_pars_vertex.glsl"), "r" ).read()
displacementmap_vertex = open( __join(__here, "ShaderChunk/displacementmap_vertex.glsl"), "r" ).read()
emissivemap_fragment = open( __join(__here, "ShaderChunk/emissivemap_fragment.glsl"), "r" ).read()
emissivemap_pars_fragment = open( __join(__here, "ShaderChunk/emissivemap_pars_fragment.glsl"), "r" ).read()
encodings_fragment = open( __join(__here, "ShaderChunk/encodings_fragment.glsl"), "r" ).read()
encodings_pars_fragment = open( __join(__here, "ShaderChunk/encodings_pars_fragment.glsl"), "r" ).read()
envmap_fragment = open( __join(__here, "ShaderChunk/envmap_fragment.glsl"), "r" ).read()
envmap_pars_fragment = open( __join(__here, "ShaderChunk/envmap_pars_fragment.glsl"), "r" ).read()
envmap_pars_vertex = open( __join(__here, "ShaderChunk/envmap_pars_vertex.glsl"), "r" ).read()
envmap_vertex = open( __join(__here, "ShaderChunk/envmap_vertex.glsl"), "r" ).read()
fog_vertex = open( __join(__here, "ShaderChunk/fog_vertex.glsl"), "r" ).read()
fog_pars_vertex = open( __join(__here, "ShaderChunk/fog_pars_vertex.glsl"), "r" ).read()
fog_fragment = open( __join(__here, "ShaderChunk/fog_fragment.glsl"), "r" ).read()
fog_pars_fragment = open( __join(__here, "ShaderChunk/fog_pars_fragment.glsl"), "r" ).read()
gradientmap_pars_fragment = open( __join(__here, "ShaderChunk/gradientmap_pars_fragment.glsl"), "r" ).read()
lightmap_fragment = open( __join(__here, "ShaderChunk/lightmap_fragment.glsl"), "r" ).read()
lightmap_pars_fragment = open( __join(__here, "ShaderChunk/lightmap_pars_fragment.glsl"), "r" ).read()
lights_lambert_vertex = open( __join(__here, "ShaderChunk/lights_lambert_vertex.glsl"), "r" ).read()
lights_pars = open( __join(__here, "ShaderChunk/lights_pars.glsl"), "r" ).read()
lights_phong_fragment = open( __join(__here, "ShaderChunk/lights_phong_fragment.glsl"), "r" ).read()
lights_phong_pars_fragment = open( __join(__here, "ShaderChunk/lights_phong_pars_fragment.glsl"), "r" ).read()
lights_physical_fragment = open( __join(__here, "ShaderChunk/lights_physical_fragment.glsl"), "r" ).read()
lights_physical_pars_fragment = open( __join(__here, "ShaderChunk/lights_physical_pars_fragment.glsl"), "r" ).read()
lights_template = open( __join(__here, "ShaderChunk/lights_template.glsl"), "r" ).read()
logdepthbuf_fragment = open( __join(__here, "ShaderChunk/logdepthbuf_fragment.glsl"), "r" ).read()
logdepthbuf_pars_fragment = open( __join(__here, "ShaderChunk/logdepthbuf_pars_fragment.glsl"), "r" ).read()
logdepthbuf_pars_vertex = open( __join(__here, "ShaderChunk/logdepthbuf_pars_vertex.glsl"), "r" ).read()
logdepthbuf_vertex = open( __join(__here, "ShaderChunk/logdepthbuf_vertex.glsl"), "r" ).read()
map_fragment = open( __join(__here, "ShaderChunk/map_fragment.glsl"), "r" ).read()
map_pars_fragment = open( __join(__here, "ShaderChunk/map_pars_fragment.glsl"), "r" ).read()
map_particle_fragment = open( __join(__here, "ShaderChunk/map_particle_fragment.glsl"), "r" ).read()
map_particle_pars_fragment = open( __join(__here, "ShaderChunk/map_particle_pars_fragment.glsl"), "r" ).read()
metalnessmap_fragment = open( __join(__here, "ShaderChunk/metalnessmap_fragment.glsl"), "r" ).read()
metalnessmap_pars_fragment = open( __join(__here, "ShaderChunk/metalnessmap_pars_fragment.glsl"), "r" ).read()
morphnormal_vertex = open( __join(__here, "ShaderChunk/morphnormal_vertex.glsl"), "r" ).read()
morphtarget_pars_vertex = open( __join(__here, "ShaderChunk/morphtarget_pars_vertex.glsl"), "r" ).read()
morphtarget_vertex = open( __join(__here, "ShaderChunk/morphtarget_vertex.glsl"), "r" ).read()
normal_fragment = open( __join(__here, "ShaderChunk/normal_fragment.glsl"), "r" ).read()
normalmap_pars_fragment = open( __join(__here, "ShaderChunk/normalmap_pars_fragment.glsl"), "r" ).read()
packing = open( __join(__here, "ShaderChunk/packing.glsl"), "r" ).read()
premultiplied_alpha_fragment = open( __join(__here, "ShaderChunk/premultiplied_alpha_fragment.glsl"), "r" ).read()
project_vertex = open( __join(__here, "ShaderChunk/project_vertex.glsl"), "r" ).read()
dithering_fragment = open( __join(__here, "ShaderChunk/dithering_fragment.glsl"), "r" ).read()
dithering_pars_fragment = open( __join(__here, "ShaderChunk/dithering_pars_fragment.glsl"), "r" ).read()
roughnessmap_fragment = open( __join(__here, "ShaderChunk/roughnessmap_fragment.glsl"), "r" ).read()
roughnessmap_pars_fragment = open( __join(__here, "ShaderChunk/roughnessmap_pars_fragment.glsl"), "r" ).read()
shadowmap_pars_fragment = open( __join(__here, "ShaderChunk/shadowmap_pars_fragment.glsl"), "r" ).read()
shadowmap_pars_vertex = open( __join(__here, "ShaderChunk/shadowmap_pars_vertex.glsl"), "r" ).read()
shadowmap_vertex = open( __join(__here, "ShaderChunk/shadowmap_vertex.glsl"), "r" ).read()
shadowmask_pars_fragment = open( __join(__here, "ShaderChunk/shadowmask_pars_fragment.glsl"), "r" ).read()
skinbase_vertex = open( __join(__here, "ShaderChunk/skinbase_vertex.glsl"), "r" ).read()
skinning_pars_vertex = open( __join(__here, "ShaderChunk/skinning_pars_vertex.glsl"), "r" ).read()
skinning_vertex = open( __join(__here, "ShaderChunk/skinning_vertex.glsl"), "r" ).read()
skinnormal_vertex = open( __join(__here, "ShaderChunk/skinnormal_vertex.glsl"), "r" ).read()
specularmap_fragment = open( __join(__here, "ShaderChunk/specularmap_fragment.glsl"), "r" ).read()
specularmap_pars_fragment = open( __join(__here, "ShaderChunk/specularmap_pars_fragment.glsl"), "r" ).read()
tonemapping_fragment = open( __join(__here, "ShaderChunk/tonemapping_fragment.glsl"), "r" ).read()
tonemapping_pars_fragment = open( __join(__here, "ShaderChunk/tonemapping_pars_fragment.glsl"), "r" ).read()
uv_pars_fragment = open( __join(__here, "ShaderChunk/uv_pars_fragment.glsl"), "r" ).read()
uv_pars_vertex = open( __join(__here, "ShaderChunk/uv_pars_vertex.glsl"), "r" ).read()
uv_vertex = open( __join(__here, "ShaderChunk/uv_vertex.glsl"), "r" ).read()
uv2_pars_fragment = open( __join(__here, "ShaderChunk/uv2_pars_fragment.glsl"), "r" ).read()
uv2_pars_vertex = open( __join(__here, "ShaderChunk/uv2_pars_vertex.glsl"), "r" ).read()
uv2_vertex = open( __join(__here, "ShaderChunk/uv2_vertex.glsl"), "r" ).read()
worldpos_vertex = open( __join(__here, "ShaderChunk/worldpos_vertex.glsl"), "r" ).read()

cube_frag = open( __join(__here, "ShaderLib/cube_frag.glsl"), "r" ).read()
cube_vert = open( __join(__here, "ShaderLib/cube_vert.glsl"), "r" ).read()
depth_frag = open( __join(__here, "ShaderLib/depth_frag.glsl"), "r" ).read()
depth_vert = open( __join(__here, "ShaderLib/depth_vert.glsl"), "r" ).read()
distanceRGBA_frag = open( __join(__here, "ShaderLib/distanceRGBA_frag.glsl"), "r" ).read()
distanceRGBA_vert = open( __join(__here, "ShaderLib/distanceRGBA_vert.glsl"), "r" ).read()
equirect_frag = open( __join(__here, "ShaderLib/equirect_frag.glsl"), "r" ).read()
equirect_vert = open( __join(__here, "ShaderLib/equirect_vert.glsl"), "r" ).read()
linedashed_frag = open( __join(__here, "ShaderLib/linedashed_frag.glsl"), "r" ).read()
linedashed_vert = open( __join(__here, "ShaderLib/linedashed_vert.glsl"), "r" ).read()
meshbasic_frag = open( __join(__here, "ShaderLib/meshbasic_frag.glsl"), "r" ).read()
meshbasic_vert = open( __join(__here, "ShaderLib/meshbasic_vert.glsl"), "r" ).read()
meshlambert_frag = open( __join(__here, "ShaderLib/meshlambert_frag.glsl"), "r" ).read()
meshlambert_vert = open( __join(__here, "ShaderLib/meshlambert_vert.glsl"), "r" ).read()
meshphong_frag = open( __join(__here, "ShaderLib/meshphong_frag.glsl"), "r" ).read()
meshphong_vert = open( __join(__here, "ShaderLib/meshphong_vert.glsl"), "r" ).read()
meshphysical_frag = open( __join(__here, "ShaderLib/meshphysical_frag.glsl"), "r" ).read()
meshphysical_vert = open( __join(__here, "ShaderLib/meshphysical_vert.glsl"), "r" ).read()
normal_frag = open( __join(__here, "ShaderLib/normal_frag.glsl"), "r" ).read()
normal_vert = open( __join(__here, "ShaderLib/normal_vert.glsl"), "r" ).read()
points_frag = open( __join(__here, "ShaderLib/points_frag.glsl"), "r" ).read()
points_vert = open( __join(__here, "ShaderLib/points_vert.glsl"), "r" ).read()
shadow_frag = open( __join(__here, "ShaderLib/shadow_frag.glsl"), "r" ).read()
shadow_vert = open( __join(__here, "ShaderLib/shadow_vert.glsl"), "r" ).read()