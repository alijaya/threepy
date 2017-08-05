#version 120
#define SHADER_NAME PointsMaterial
#define ALPHATEST 0.5
#define GAMMA_FACTOR 2.0
#define USE_MAP
#define NUM_CLIPPING_PLANES 0
uniform mat4 viewMatrix;
uniform vec3 cameraPosition;
#define TONE_MAPPING
#define saturate(a) clamp( a, 0.0, 1.0 )

uniform float toneMappingExposure;
uniform float toneMappingWhitePoint;

// exposure only
vec3 LinearToneMapping( vec3 color ) {

        return toneMappingExposure * color;

}

// source: https://www.cs.utah.edu/~reinhard/cdrom/
vec3 ReinhardToneMapping( vec3 color ) {

        color *= toneMappingExposure;
        return saturate( color / ( vec3( 1.0 ) + color ) );

}

// source: http://filmicgames.com/archives/75
#define Uncharted2Helper( x ) max( ( ( x * ( 0.15 * x + 0.10 * 0.50 ) + 0.20 * 0.02 ) / ( x * ( 0.15 * x + 0.50 ) + 0.20 * 0.30 ) )- 0.02 / 0.30, vec3( 0.0 ) )
vec3 Uncharted2ToneMapping( vec3 color ) {

        // John Hable's filmic operator from Uncharted 2 video game
        color *= toneMappingExposure;
        return saturate( Uncharted2Helper( color ) / Uncharted2Helper( vec3( toneMappingWhitePoint ) ) );

}

// source: http://filmicgames.com/archives/75
vec3 OptimizedCineonToneMapping( vec3 color ) {

        // optimized filmic operator by Jim Hejl and Richard Burgess-Dawson
        color *= toneMappingExposure;
        color = max( vec3( 0.0 ), color - 0.004 );
        return pow( ( color * ( 6.2 * color + 0.5 ) ) / ( color * ( 6.2 * color + 1.7 ) + 0.06 ), vec3( 2.2 ) );

}

vec3 toneMapping( vec3 color ) { return LinearToneMapping( color ); }
// For a discussion of what this is, please read this: http://lousodrome.net/blog/light/2013/05/26/gamma-correct-and-hdr-rendering-in-a-32-bits-buffer/

vec4 LinearToLinear( in vec4 value ) {
        return value;
}

vec4 GammaToLinear( in vec4 value, in float gammaFactor ) {
        return vec4( pow( value.xyz, vec3( gammaFactor ) ), value.w );
}
vec4 LinearToGamma( in vec4 value, in float gammaFactor ) {
        return vec4( pow( value.xyz, vec3( 1.0 / gammaFactor ) ), value.w );
}

vec4 sRGBToLinear( in vec4 value ) {
        return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.w );
}
vec4 LinearTosRGB( in vec4 value ) {
        return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.w );
}

vec4 RGBEToLinear( in vec4 value ) {
        return vec4( value.rgb * exp2( value.a * 255.0 - 128.0 ), 1.0 );
}
vec4 LinearToRGBE( in vec4 value ) {
        float maxComponent = max( max( value.r, value.g ), value.b );
        float fExp = clamp( ceil( log2( maxComponent ) ), -128.0, 127.0 );
        return vec4( value.rgb / exp2( fExp ), ( fExp + 128.0 ) / 255.0 );
//  return vec4( value.brg, ( 3.0 + 128.0 ) / 256.0 );
}

// reference: http://iwasbeingirony.blogspot.ca/2010/06/difference-between-rgbm-and-rgbd.html
vec4 RGBMToLinear( in vec4 value, in float maxRange ) {
        return vec4( value.xyz * value.w * maxRange, 1.0 );
}
vec4 LinearToRGBM( in vec4 value, in float maxRange ) {
        float maxRGB = max( value.x, max( value.g, value.b ) );
        float M      = clamp( maxRGB / maxRange, 0.0, 1.0 );
        M            = ceil( M * 255.0 ) / 255.0;
        return vec4( value.rgb / ( M * maxRange ), M );
}

// reference: http://iwasbeingirony.blogspot.ca/2010/06/difference-between-rgbm-and-rgbd.html
vec4 RGBDToLinear( in vec4 value, in float maxRange ) {
        return vec4( value.rgb * ( ( maxRange / 255.0 ) / value.a ), 1.0 );
}
vec4 LinearToRGBD( in vec4 value, in float maxRange ) {
        float maxRGB = max( value.x, max( value.g, value.b ) );
        float D      = max( maxRange / maxRGB, 1.0 );
        D            = min( floor( D ) / 255.0, 1.0 );
        return vec4( value.rgb * ( D * ( 255.0 / maxRange ) ), D );
}

// LogLuv reference: http://graphicrants.blogspot.ca/2009/04/rgbm-color-encoding.html

// M matrix, for encoding
const mat3 cLogLuvM = mat3( 0.2209, 0.3390, 0.4184, 0.1138, 0.6780, 0.7319, 0.0102, 0.1130, 0.2969 );
vec4 LinearToLogLuv( in vec4 value )  {
        vec3 Xp_Y_XYZp = value.rgb * cLogLuvM;
        Xp_Y_XYZp = max(Xp_Y_XYZp, vec3(1e-6, 1e-6, 1e-6));
        vec4 vResult;
        vResult.xy = Xp_Y_XYZp.xy / Xp_Y_XYZp.z;
        float Le = 2.0 * log2(Xp_Y_XYZp.y) + 127.0;
        vResult.w = fract(Le);
        vResult.z = (Le - (floor(vResult.w*255.0))/255.0)/255.0;
        return vResult;
}

// Inverse M matrix, for decoding
const mat3 cLogLuvInverseM = mat3( 6.0014, -2.7008, -1.7996, -1.3320, 3.1029, -5.7721, 0.3008, -1.0882, 5.6268 );
vec4 LogLuvToLinear( in vec4 value ) {
        float Le = value.z * 255.0 + value.w;
        vec3 Xp_Y_XYZp;
        Xp_Y_XYZp.y = exp2((Le - 127.0) / 2.0);
        Xp_Y_XYZp.z = Xp_Y_XYZp.y / value.y;
        Xp_Y_XYZp.x = value.x * Xp_Y_XYZp.z;
        vec3 vRGB = Xp_Y_XYZp.rgb * cLogLuvInverseM;
        return vec4( max(vRGB, 0.0), 1.0 );
}

vec4 mapTexelToLinear( vec4 value ) { return LinearToLinear( value ); }
vec4 envMapTexelToLinear( vec4 value ) { return LinearToLinear( value ); }
vec4 emissiveMapTexelToLinear( vec4 value ) { return LinearToLinear( value ); }
vec4 linearToOutputTexel( vec4 value ) { return LinearToLinear( value ); }

uniform vec3 diffuse;
uniform float opacity;

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

vec3 packNormalToRGB( const in vec3 normal ) {
        return normalize( normal ) * 0.5 + 0.5;
}

vec3 unpackRGBToNormal( const in vec3 rgb ) {
        return 1.0 - 2.0 * rgb.xyz;
}

const float PackUpscale = 256. / 255.; // fraction -> 0..1 (including 1)
const float UnpackDownscale = 255. / 256.; // 0..1 -> fraction (excluding 1)

const vec3 PackFactors = vec3( 256. * 256. * 256., 256. * 256.,  256. );
const vec4 UnpackFactors = UnpackDownscale / vec4( PackFactors, 1. );

const float ShiftRight8 = 1. / 256.;

vec4 packDepthToRGBA( const in float v ) {
        vec4 r = vec4( fract( v * PackFactors ), v );
        r.yzw -= r.xyz * ShiftRight8; // tidy overflow
        return r * PackUpscale;
}

float unpackRGBAToDepth( const in vec4 v ) {
        return dot( v, UnpackFactors );
}

// NOTE: viewZ/eyeZ is < 0 when in front of the camera per OpenGL conventions

float viewZToOrthographicDepth( const in float viewZ, const in float near, const in float far ) {
        return ( viewZ + near ) / ( near - far );
}
float orthographicDepthToViewZ( const in float linearClipZ, const in float near, const in float far ) {
        return linearClipZ * ( near - far ) - near;
}

float viewZToPerspectiveDepth( const in float viewZ, const in float near, const in float far ) {
        return (( near + viewZ ) * far ) / (( far - near ) * viewZ );
}
float perspectiveDepthToViewZ( const in float invClipZ, const in float near, const in float far ) {
        return ( near * far ) / ( ( far - near ) * invClipZ - far );
}

#ifdef USE_COLOR

        varying vec3 vColor;

#endif

#ifdef USE_MAP

        uniform vec4 offsetRepeat;
        uniform sampler2D map;

#endif

#ifdef USE_FOG

        uniform vec3 fogColor;
        varying float fogDepth;

        #ifdef FOG_EXP2

                uniform float fogDensity;

        #else

                uniform float fogNear;
                uniform float fogFar;

        #endif

#endif

#ifdef USE_SHADOWMAP

        #if 0 > 0

                uniform sampler2D directionalShadowMap[ 0 ];
                varying vec4 vDirectionalShadowCoord[ 0 ];

        #endif

        #if 0 > 0

                uniform sampler2D spotShadowMap[ 0 ];
                varying vec4 vSpotShadowCoord[ 0 ];

        #endif

        #if 0 > 0

                uniform sampler2D pointShadowMap[ 0 ];
                varying vec4 vPointShadowCoord[ 0 ];

        #endif

        /*
        #if 0 > 0

                // TODO (abelnation): create uniforms for area light shadows

        #endif
        */

        float texture2DCompare( sampler2D depths, vec2 uv, float compare ) {

                return step( compare, unpackRGBAToDepth( texture2D( depths, uv ) ) );

        }

        float texture2DShadowLerp( sampler2D depths, vec2 size, vec2 uv, float compare ) {

                const vec2 offset = vec2( 0.0, 1.0 );

                vec2 texelSize = vec2( 1.0 ) / size;
                vec2 centroidUV = floor( uv * size + 0.5 ) / size;

                float lb = texture2DCompare( depths, centroidUV + texelSize * offset.xx, compare );
                float lt = texture2DCompare( depths, centroidUV + texelSize * offset.xy, compare );
                float rb = texture2DCompare( depths, centroidUV + texelSize * offset.yx, compare );
                float rt = texture2DCompare( depths, centroidUV + texelSize * offset.yy, compare );

                vec2 f = fract( uv * size + 0.5 );

                float a = mix( lb, lt, f.y );
                float b = mix( rb, rt, f.y );
                float c = mix( a, b, f.x );

                return c;

        }

        float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowBias, float shadowRadius, vec4 shadowCoord ) {

                float shadow = 1.0;

                shadowCoord.xyz /= shadowCoord.w;
                shadowCoord.z += shadowBias;

                // if ( something && something ) breaks ATI OpenGL shader compiler
                // if ( all( something, something ) ) using this instead

                bvec4 inFrustumVec = bvec4 ( shadowCoord.x >= 0.0, shadowCoord.x <= 1.0, shadowCoord.y >= 0.0, shadowCoord.y <= 1.0);
                bool inFrustum = all( inFrustumVec );

                bvec2 frustumTestVec = bvec2( inFrustum, shadowCoord.z <= 1.0 );

                bool frustumTest = all( frustumTestVec );

                if ( frustumTest ) {

                #if defined( SHADOWMAP_TYPE_PCF )

                        vec2 texelSize = vec2( 1.0 ) / shadowMapSize;

                        float dx0 = - texelSize.x * shadowRadius;
                        float dy0 = - texelSize.y * shadowRadius;
                        float dx1 = + texelSize.x * shadowRadius;
                        float dy1 = + texelSize.y * shadowRadius;

                        shadow = (
                                texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, dy0 ), shadowCoord.z ) +
                                texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy0 ), shadowCoord.z ) +
                                texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, dy0 ), shadowCoord.z ) +
                                texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, 0.0 ), shadowCoord.z ) +
                                texture2DCompare( shadowMap, shadowCoord.xy, shadowCoord.z ) +
                                texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, 0.0 ), shadowCoord.z ) +
                                texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, dy1 ), shadowCoord.z ) +
                                texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy1 ), shadowCoord.z ) +
                                texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, dy1 ), shadowCoord.z )
                        ) * ( 1.0 / 9.0 );

                #elif defined( SHADOWMAP_TYPE_PCF_SOFT )

                        vec2 texelSize = vec2( 1.0 ) / shadowMapSize;

                        float dx0 = - texelSize.x * shadowRadius;
                        float dy0 = - texelSize.y * shadowRadius;
                        float dx1 = + texelSize.x * shadowRadius;
                        float dy1 = + texelSize.y * shadowRadius;

                        shadow = (
                                texture2DShadowLerp( shadowMap, shadowMapSize, shadowCoord.xy + vec2( dx0, dy0 ), shadowCoord.z ) +
                                texture2DShadowLerp( shadowMap, shadowMapSize, shadowCoord.xy + vec2( 0.0, dy0 ), shadowCoord.z ) +
                                texture2DShadowLerp( shadowMap, shadowMapSize, shadowCoord.xy + vec2( dx1, dy0 ), shadowCoord.z ) +
                                texture2DShadowLerp( shadowMap, shadowMapSize, shadowCoord.xy + vec2( dx0, 0.0 ), shadowCoord.z ) +
                                texture2DShadowLerp( shadowMap, shadowMapSize, shadowCoord.xy, shadowCoord.z ) +
                                texture2DShadowLerp( shadowMap, shadowMapSize, shadowCoord.xy + vec2( dx1, 0.0 ), shadowCoord.z ) +
                                texture2DShadowLerp( shadowMap, shadowMapSize, shadowCoord.xy + vec2( dx0, dy1 ), shadowCoord.z ) +
                                texture2DShadowLerp( shadowMap, shadowMapSize, shadowCoord.xy + vec2( 0.0, dy1 ), shadowCoord.z ) +
                                texture2DShadowLerp( shadowMap, shadowMapSize, shadowCoord.xy + vec2( dx1, dy1 ), shadowCoord.z )
                        ) * ( 1.0 / 9.0 );

                #else // no percentage-closer filtering:

                        shadow = texture2DCompare( shadowMap, shadowCoord.xy, shadowCoord.z );

                #endif

                }

                return shadow;

        }

        // cubeToUV() maps a 3D direction vector suitable for cube texture mapping to a 2D
        // vector suitable for 2D texture mapping. This code uses the following layout for the
        // 2D texture:
        //
        // xzXZ
        //  y Y
        //
        // Y - Positive y direction
        // y - Negative y direction
        // X - Positive x direction
        // x - Negative x direction
        // Z - Positive z direction
        // z - Negative z direction
        //
        // Source and test bed:
        // https://gist.github.com/tschw/da10c43c467ce8afd0c4

        vec2 cubeToUV( vec3 v, float texelSizeY ) {

                // Number of texels to avoid at the edge of each square

                vec3 absV = abs( v );

                // Intersect unit cube

                float scaleToCube = 1.0 / max( absV.x, max( absV.y, absV.z ) );
                absV *= scaleToCube;

                // Apply scale to avoid seams

                // two texels less per square (one texel will do for NEAREST)
                v *= scaleToCube * ( 1.0 - 2.0 * texelSizeY );

                // Unwrap

                // space: -1 ... 1 range for each square
                //
                // #X##         dim    := ( 4 , 2 )
                //  # #         center := ( 1 , 1 )

                vec2 planar = v.xy;

                float almostATexel = 1.5 * texelSizeY;
                float almostOne = 1.0 - almostATexel;

                if ( absV.z >= almostOne ) {

                        if ( v.z > 0.0 )
                                planar.x = 4.0 - v.x;

                } else if ( absV.x >= almostOne ) {

                        float signX = sign( v.x );
                        planar.x = v.z * signX + 2.0 * signX;

                } else if ( absV.y >= almostOne ) {

                        float signY = sign( v.y );
                        planar.x = v.x + 2.0 * signY + 2.0;
                        planar.y = v.z * signY - 2.0;

                }

                // Transform to UV space

                // scale := 0.5 / dim
                // translate := ( center + 0.5 ) / dim
                return vec2( 0.125, 0.25 ) * planar + vec2( 0.375, 0.75 );

        }

        float getPointShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {

                vec2 texelSize = vec2( 1.0 ) / ( shadowMapSize * vec2( 4.0, 2.0 ) );

                // for point lights, the uniform @vShadowCoord is re-purposed to hold
                // the vector from the light to the world-space position of the fragment.
                vec3 lightToPosition = shadowCoord.xyz;

                // dp = normalized distance from light to fragment position
                float dp = ( length( lightToPosition ) - shadowCameraNear ) / ( shadowCameraFar - shadowCameraNear ); // need to clamp?
                dp += shadowBias;

                // bd3D = base direction 3D
                vec3 bd3D = normalize( lightToPosition );

                #if defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_PCF_SOFT )

                        vec2 offset = vec2( - 1, 1 ) * shadowRadius * texelSize.y;

                        return (
                                texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xyy, texelSize.y ), dp ) +
                                texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yyy, texelSize.y ), dp ) +
                                texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xyx, texelSize.y ), dp ) +
                                texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yyx, texelSize.y ), dp ) +
                                texture2DCompare( shadowMap, cubeToUV( bd3D, texelSize.y ), dp ) +
                                texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xxy, texelSize.y ), dp ) +
                                texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yxy, texelSize.y ), dp ) +
                                texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xxx, texelSize.y ), dp ) +
                                texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yxx, texelSize.y ), dp )
                        ) * ( 1.0 / 9.0 );

                #else // no percentage-closer filtering

                        return texture2DCompare( shadowMap, cubeToUV( bd3D, texelSize.y ), dp );

                #endif

        }

#endif

#ifdef USE_LOGDEPTHBUF

        uniform float logDepthBufFC;

        #ifdef USE_LOGDEPTHBUF_EXT

                varying float vFragDepth;

        #endif

#endif

#if NUM_CLIPPING_PLANES > 0

        #if ! defined( PHYSICAL ) && ! defined( PHONG )
                varying vec3 vViewPosition;
        #endif

        uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];

#endif


void main() {

#if NUM_CLIPPING_PLANES > 0

        for ( int i = 0; i < UNION_CLIPPING_PLANES; ++ i ) {

                vec4 plane = clippingPlanes[ i ];
                if ( dot( vViewPosition, plane.xyz ) > plane.w ) discard;

        }

        #if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES

                bool clipped = true;
                for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; ++ i ) {
                        vec4 plane = clippingPlanes[ i ];
                        clipped = ( dot( vViewPosition, plane.xyz ) > plane.w ) && clipped;
                }

                if ( clipped ) discard;

        #endif

#endif


        vec3 outgoingLight = vec3( 0.0 );
        vec4 diffuseColor = vec4( diffuse, opacity );

#if defined(USE_LOGDEPTHBUF) && defined(USE_LOGDEPTHBUF_EXT)

        gl_FragDepthEXT = log2(vFragDepth) * logDepthBufFC * 0.5;

#endif
#ifdef USE_MAP

        vec4 mapTexel = texture2D( map, vec2( gl_PointCoord.x, 1.0 - gl_PointCoord.y ) * offsetRepeat.zw + offsetRepeat.xy );
        diffuseColor *= mapTexelToLinear( mapTexel );

#endif

#ifdef USE_COLOR

        diffuseColor.rgb *= vColor;

#endif
#ifdef ALPHATEST

        if ( diffuseColor.a < ALPHATEST ) discard;

#endif


        outgoingLight = diffuseColor.rgb;

        gl_FragColor = vec4( outgoingLight, diffuseColor.a );

#ifdef PREMULTIPLIED_ALPHA

        // Get get normal blending with premultipled, use with CustomBlending, OneFactor, OneMinusSrcAlphaFactor, AddEquation.
        gl_FragColor.rgb *= gl_FragColor.a;

#endif

#if defined( TONE_MAPPING )

  gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );

#endif

  gl_FragColor = linearToOutputTexel( gl_FragColor );

#ifdef USE_FOG

        #ifdef FOG_EXP2

                float fogFactor = whiteCompliment( exp2( - fogDensity * fogDensity * fogDepth * fogDepth * LOG2 ) );

        #else

                float fogFactor = smoothstep( fogNear, fogFar, fogDepth );

        #endif

        gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );

#endif


}