from OpenGL.GL import *

from ...constants import MaxEquation, MinEquation, RGB_ETC1_Format, RGBA_PVRTC_2BPPV1_Format, RGBA_PVRTC_4BPPV1_Format, RGB_PVRTC_2BPPV1_Format, RGB_PVRTC_4BPPV1_Format, RGBA_S3TC_DXT5_Format, RGBA_S3TC_DXT3_Format, RGBA_S3TC_DXT1_Format, RGB_S3TC_DXT1_Format, SrcAlphaSaturateFactor, OneMinusDstColorFactor, DstColorFactor, OneMinusDstAlphaFactor, DstAlphaFactor, OneMinusSrcAlphaFactor, SrcAlphaFactor, OneMinusSrcColorFactor, SrcColorFactor, OneFactor, ZeroFactor, ReverseSubtractEquation, SubtractEquation, AddEquation, DepthFormat, DepthStencilFormat, LuminanceAlphaFormat, LuminanceFormat, RGBAFormat, RGBFormat, AlphaFormat, HalfFloatType, FloatType, UnsignedIntType, IntType, UnsignedShortType, ShortType, ByteType, UnsignedInt248Type, UnsignedShort565Type, UnsignedShort5551Type, UnsignedShort4444Type, UnsignedByteType, LinearMipMapLinearFilter, LinearMipMapNearestFilter, LinearFilter, NearestMipMapLinearFilter, NearestMipMapNearestFilter, NearestFilter, MirroredRepeatWrapping, ClampToEdgeWrapping, RepeatWrapping
"""
 * @author thespite / "http":#www.twitter.com/thespite
 """

def convert ( p ):

    if p == RepeatWrapping : return GL_REPEAT
    if p == ClampToEdgeWrapping : return GL_CLAMP_TO_EDGE
    if p == MirroredRepeatWrapping : return GL_MIRRORED_REPEAT

    if p == NearestFilter : return GL_NEAREST
    if p == NearestMipMapNearestFilter : return GL_NEAREST_MIPMAP_NEAREST
    if p == NearestMipMapLinearFilter : return GL_NEAREST_MIPMAP_LINEAR

    if p == LinearFilter : return GL_LINEAR
    if p == LinearMipMapNearestFilter : return GL_LINEAR_MIPMAP_NEAREST
    if p == LinearMipMapLinearFilter : return GL_LINEAR_MIPMAP_LINEAR

    if p == UnsignedByteType : return GL_UNSIGNED_BYTE
    if p == UnsignedShort4444Type : return GL_UNSIGNED_SHORT_4_4_4_4
    if p == UnsignedShort5551Type : return GL_UNSIGNED_SHORT_5_5_5_1
    if p == UnsignedShort565Type : return GL_UNSIGNED_SHORT_5_6_5

    if p == ByteType : return GL_BYTE
    if p == ShortType : return GL_SHORT
    if p == UnsignedShortType : return GL_UNSIGNED_SHORT
    if p == IntType : return GL_INT
    if p == UnsignedIntType : return GL_UNSIGNED_INT
    if p == FloatType : return GL_FLOAT

    # if p == HalfFloatType :

    #     extension = extensions.get( "OES_texture_half_float" )

    #     if extension is not None : return extension.HALF_FLOAT_OES

    if p == AlphaFormat : return GL_ALPHA
    if p == RGBFormat : return GL_RGB
    if p == RGBAFormat : return GL_RGBA
    if p == LuminanceFormat : return GL_LUMINANCE
    if p == LuminanceAlphaFormat : return GL_LUMINANCE_ALPHA
    if p == DepthFormat : return GL_DEPTH_COMPONENT
    if p == DepthStencilFormat : return GL_DEPTH_STENCIL

    if p == AddEquation : return GL_FUNC_ADD
    if p == SubtractEquation : return GL_FUNC_SUBTRACT
    if p == ReverseSubtractEquation : return GL_FUNC_REVERSE_SUBTRACT

    if p == ZeroFactor : return GL_ZERO
    if p == OneFactor : return GL_ONE
    if p == SrcColorFactor : return GL_SRC_COLOR
    if p == OneMinusSrcColorFactor : return GL_ONE_MINUS_SRC_COLOR
    if p == SrcAlphaFactor : return GL_SRC_ALPHA
    if p == OneMinusSrcAlphaFactor : return GL_ONE_MINUS_SRC_ALPHA
    if p == DstAlphaFactor : return GL_DST_ALPHA
    if p == OneMinusDstAlphaFactor : return GL_ONE_MINUS_DST_ALPHA

    if p == DstColorFactor : return GL_DST_COLOR
    if p == OneMinusDstColorFactor : return GL_ONE_MINUS_DST_COLOR
    if p == SrcAlphaSaturateFactor : return GL_SRC_ALPHA_SATURATE

    # if ( p == RGB_S3TC_DXT1_Format or p == RGBA_S3TC_DXT1_Format or
    #     p == RGBA_S3TC_DXT3_Format or p == RGBA_S3TC_DXT5_Format ) {

    #     extension = extensions.get( "WEBGL_compressed_texture_s3tc" )

    #     if extension is not None :

    #         if p == RGB_S3TC_DXT1_Format : return extension.COMPRESSED_RGB_S3TC_DXT1_EXT
    #         if p == RGBA_S3TC_DXT1_Format : return extension.COMPRESSED_RGBA_S3TC_DXT1_EXT
    #         if p == RGBA_S3TC_DXT3_Format : return extension.COMPRESSED_RGBA_S3TC_DXT3_EXT
    #         if p == RGBA_S3TC_DXT5_Format : return extension.COMPRESSED_RGBA_S3TC_DXT5_EXT

    # if ( p == RGB_PVRTC_4BPPV1_Format or p == RGB_PVRTC_2BPPV1_Format or
    #     p == RGBA_PVRTC_4BPPV1_Format or p == RGBA_PVRTC_2BPPV1_Format ) {

    #     extension = extensions.get( "WEBGL_compressed_texture_pvrtc" )

    #     if extension is not None :

    #         if p == RGB_PVRTC_4BPPV1_Format : return extension.COMPRESSED_RGB_PVRTC_4BPPV1_IMG
    #         if p == RGB_PVRTC_2BPPV1_Format : return extension.COMPRESSED_RGB_PVRTC_2BPPV1_IMG
    #         if p == RGBA_PVRTC_4BPPV1_Format : return extension.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG
    #         if p == RGBA_PVRTC_2BPPV1_Format : return extension.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG

    # if p == RGB_ETC1_Format :

    #     extension = extensions.get( "WEBGL_compressed_texture_etc1" )

    #     if extension is not None : return extension.COMPRESSED_RGB_ETC1_WEBGL

    # if p == MinEquation or p == MaxEquation :

    #     extension = extensions.get( "EXT_blend_minmax" )

    #     if extension is not None :

    #         if p == MinEquation : return extension.MIN_EXT
    #         if p == MaxEquation : return extension.MAX_EXT

    # if p == UnsignedInt248Type :

    #     extension = extensions.get( "WEBGL_depth_texture" )

    #     if extension is not None : return extension.UNSIGNED_INT_24_8_WEBGL

    return 0
