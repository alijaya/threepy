#version 120
#define SHADER_NAME PointsMaterial
#define GAMMA_FACTOR 2.0
#define USE_MAP
#define NUM_CLIPPING_PLANES 0
uniform mat4 modelMatrix;
uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat3 normalMatrix;
uniform vec3 cameraPosition;
attribute vec3 position;
attribute vec3 normal;
attribute vec2 uv;
#ifdef USE_COLOR
    attribute vec3 color;
#endif
#ifdef USE_MORPHTARGETS
    attribute vec3 morphTarget0;
    attribute vec3 morphTarget1;
    attribute vec3 morphTarget2;
    attribute vec3 morphTarget3;
    #ifdef USE_MORPHNORMALS
        attribute vec3 morphNormal0;
        attribute vec3 morphNormal1;
        attribute vec3 morphNormal2;
        attribute vec3 morphNormal3;
    #else
        attribute vec3 morphTarget4;
        attribute vec3 morphTarget5;
        attribute vec3 morphTarget6;
        attribute vec3 morphTarget7;
    #endif
#endif
#ifdef USE_SKINNING
    attribute vec4 skinIndex;
    attribute vec4 skinWeight;
#endif

uniform float size;
uniform float scale;

#define PI 3.14159265359
#define PI2 6.28318530718
#define PI_HALF 1.5707963267949
#define RECIPROCAL_PI 0.31830988618
#define RECIPROCAL_PI2 0.15915494
#define LOG2 1.442695
#define EPSILON 1e-6

#define saturate(a) clamp( a, 0.0, 1.0 )
#define whiteCompliment(a) ( 1.0 - saturate( a ) )

float pow2( const in float x ) { return x*x; }
float pow3( const in float x ) { return x*x*x; }
float pow4( const in float x ) { float x2 = x*x; return x2*x2; }
float average( const in vec3 color ) { return dot( color, vec3( 0.3333 ) ); }
// expects values in the range of [0,1]x[0,1], returns values in the [0,1] range.
// do not collapse into a single function per: http://byteblacksmith.com/improvements-to-the-canonical-one-liner-glsl-rand-for-opengl-es-2-0/
float rand( const in vec2 uv ) {
        const float a = 12.9898, b = 78.233, c = 43758.5453;
        float dt = dot( uv.xy, vec2( a,b ) ), sn = mod( dt, PI );
        return fract(sin(sn) * c);
}

struct IncidentLight {
        vec3 color;
        vec3 direction;
        bool visible;
};

struct ReflectedLight {
        vec3 directDiffuse;
        vec3 directSpecular;
        vec3 indirectDiffuse;
        vec3 indirectSpecular;
};

struct GeometricContext {
        vec3 position;
        vec3 normal;
        vec3 viewDir;
};

vec3 transformDirection( in vec3 dir, in mat4 matrix ) {

        return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );

}

// http://en.wikibooks.org/wiki/GLSL_Programming/Applying_Matrix_Transformations
vec3 inverseTransformDirection( in vec3 dir, in mat4 matrix ) {

        return normalize( ( vec4( dir, 0.0 ) * matrix ).xyz );

}

vec3 projectOnPlane(in vec3 point, in vec3 pointOnPlane, in vec3 planeNormal ) {

        float distance = dot( planeNormal, point - pointOnPlane );

        return - distance * planeNormal + point;

}

float sideOfPlane( in vec3 point, in vec3 pointOnPlane, in vec3 planeNormal ) {

        return sign( dot( point - pointOnPlane, planeNormal ) );

}

vec3 linePlaneIntersect( in vec3 pointOnLine, in vec3 lineDirection, in vec3 pointOnPlane, in vec3 planeNormal ) {

        return lineDirection * ( dot( planeNormal, pointOnPlane - pointOnLine ) / dot( planeNormal, lineDirection ) ) + pointOnLine;

}

#ifdef USE_COLOR

        varying vec3 vColor;

#endif
#ifdef USE_FOG

  varying float fogDepth;

#endif

#ifdef USE_SHADOWMAP

        #if 0 > 0

                uniform mat4 directionalShadowMatrix[ 0 ];
                varying vec4 vDirectionalShadowCoord[ 0 ];

        #endif

        #if 0 > 0

                uniform mat4 spotShadowMatrix[ 0 ];
                varying vec4 vSpotShadowCoord[ 0 ];

        #endif

        #if 0 > 0

                uniform mat4 pointShadowMatrix[ 0 ];
                varying vec4 vPointShadowCoord[ 0 ];

        #endif

        /*
        #if 0 > 0

                // TODO (abelnation): uniforms for area light shadows

        #endif
        */

#endif

#ifdef USE_LOGDEPTHBUF

        #ifdef USE_LOGDEPTHBUF_EXT

                varying float vFragDepth;

        #endif

        uniform float logDepthBufFC;

#endif
#if NUM_CLIPPING_PLANES > 0 && ! defined( PHYSICAL ) && ! defined( PHONG )
        varying vec3 vViewPosition;
#endif


void main() {

#ifdef USE_COLOR

        vColor.xyz = color.xyz;

#endif

vec3 transformed = vec3( position );

vec4 mvPosition = modelViewMatrix * vec4( transformed, 1.0 );

gl_Position = projectionMatrix * mvPosition;


        #ifdef USE_SIZEATTENUATION
                gl_PointSize = size * ( scale / - mvPosition.z );
        #else
                gl_PointSize = size;
        #endif

#ifdef USE_LOGDEPTHBUF

        gl_Position.z = log2(max( EPSILON, gl_Position.w + 1.0 )) * logDepthBufFC;

        #ifdef USE_LOGDEPTHBUF_EXT

                vFragDepth = 1.0 + gl_Position.w;

        #else

                gl_Position.z = (gl_Position.z - 1.0) * gl_Position.w;

        #endif

#endif

#if NUM_CLIPPING_PLANES > 0 && ! defined( PHYSICAL ) && ! defined( PHONG )
        vViewPosition = - mvPosition.xyz;
#endif


#if defined( USE_ENVMAP ) || defined( PHONG ) || defined( PHYSICAL ) || defined( LAMBERT ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP )

        vec4 worldPosition = modelMatrix * vec4( transformed, 1.0 );

#endif

#ifdef USE_SHADOWMAP

        #if 0 > 0

        for ( int i = 0; i < 0; i ++ ) {

                vDirectionalShadowCoord[ i ] = directionalShadowMatrix[ i ] * worldPosition;

        }

        #endif

        #if 0 > 0

        for ( int i = 0; i < 0; i ++ ) {

                vSpotShadowCoord[ i ] = spotShadowMatrix[ i ] * worldPosition;

        }

        #endif

        #if 0 > 0

        for ( int i = 0; i < 0; i ++ ) {

                vPointShadowCoord[ i ] = pointShadowMatrix[ i ] * worldPosition;

        }

        #endif

        /*
        #if 0 > 0

                // TODO (abelnation): update vAreaShadowCoord with area light info

        #endif
        */

#endif


#ifdef USE_FOG
fogDepth = -mvPosition.z;
#endif

}
