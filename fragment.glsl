#define highp
#define mediump
#define lowp
#define SHADER_NAME MeshBasicMaterial
#define GAMMA_FACTOR 2.0
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
#define Uncharted2Helper( x ) max( ( ( x * ( 0.15 * x + 0.10 * 0.50 ) + 0.20 * 0.02 ) / ( x * ( 0.15 * x + 0.50 ) + 0.20 * 0.30 ) ) - 0.02 / 0.30, vec3( 0.0 ) )
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
highp float rand( const in vec2 uv ) {
        const highp float a = 12.9898, b = 78.233, c = 43758.5453;
        highp float dt = dot( uv.xy, vec2( a,b ) ), sn = mod( dt, PI );
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

mat3 transpose( const in mat3 v ) {

        mat3 tmp;
        tmp[0] = vec3(v[0].x, v[1].x, v[2].x);
        tmp[1] = vec3(v[0].y, v[1].y, v[2].y);
        tmp[2] = vec3(v[0].z, v[1].z, v[2].z);

        return tmp;

}

void main() {

        vec4 diffuseColor = vec4( diffuse, opacity );

float specularStrength;

        specularStrength = 1.0;

        ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );

                reflectedLight.indirectDiffuse += vec3( 1.0 );




        reflectedLight.indirectDiffuse *= diffuseColor.rgb;

        vec3 outgoingLight = reflectedLight.indirectDiffuse;

        gl_FragColor = vec4( outgoingLight, diffuseColor.a );

#if defined( TONE_MAPPING )

  gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );

#endif

  gl_FragColor = linearToOutputTexel( gl_FragColor );

}