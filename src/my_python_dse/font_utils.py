# font_utils.py

import re, unicodedata, os
from types import SimpleNamespace

import silence
silence.on()
import fontforge
silence.off()

def parse_char(param, throw=False, default=None, _orig=None):
    """Return the codepoint of the supplied single character, Unicode
glyph name, Adobe glyph name, hex code as a string, or codepoint as an
int or float.

**Any** string containing one character results in that character's
codepoint; this includes '0' to '9', which results in codepoints 48 to
57.

Hex code string formats are: 'U+1F4A9', 'U1F4A9', '0x1f4a9', and
'x1f4a9'.

Unicode glyph names can be in lower- or upper-case.  Adobe glyph names
are case-sensitive.

If the supplied parameter is invalid, raises an exception if the
`throw` parameter is truthy, returns the `default` paramter if
specified, or failing all of that, returns None.

The `_orig` parameter is not intended for your use.

This function is intended to be used for command line arguments, but
can be used for other purposes too.

    """
    _orig = param if _orig is None else param
    kwargs = { "throw": throw, "_orig": _orig }
    try:
        if type(param) == int:
            if param not in range(0, 0x110000):
                raise ValueError("invalid codepoint: %s" % repr(_orig))
            return param
        if type(param) == float:
            if round(param) != param:
                raise ValueError("float param must be an int: %s" % repr(_orig))
            return parse_char(int(param), **kwargs)
        if type(param) == str:
            if len(param) == 1:
                return ord(param)
            if match := re.fullmatch(r'(?:u\+?|0?x)([0-9a-f]+)', param, re.IGNORECASE):
                return parse_char(int(match[1], 16), **kwargs)
            try:
                return ord(unicodedata.lookup(param.upper()))
            except KeyError:
                pass
            codepoint = fontforge.unicodeFromName(param)
            if codepoint in range(0, 0x110000):
                return codepoint
            raise ValueError("invalid character spec: %s" % repr(_orig))
        return TypeError("invalid param type: must be int, float, or str; "
                         + "got %s" % repr(type(_orig)))
    except Exception:
        if throw:
            raise
        return default

def u(param, pad=False):
    """Returns a string like 'U+1F4A9' if the supplied codepoint (or
parameter passed to parse_char) is non-negative; otherwise returns a
string like '-1'.

    """
    codepoint = parse_char(param, default=-1)
    if codepoint < 0:
        if pad:
            if type(pad) == int:
                return "%*d" % (pad, codepoint)
            return "%8d" % codepoint
        return "%d" % codepoint
    result = "U+%04X" % codepoint
    if pad:
        if type(pad) == int:
            return "%-*s" % (pad, result)
        return "%-8s" % result
    return result

def get_font_count(filenames):
    return list(fonts_in(filenames, filenamesonly=True))

def fonts_in(filenames, filenamesonly=False, close=True, verbose=False, ttc=True, open_font=True, names=False):
    """Utility function used by a lot of my crappy fontforge scripts.

    """
    if not open_font and not names:
        raise Exception("fonts_in without open_font or names does not make sense")
    for filename in filenames:
        fonts_in_file = fontforge.fontsInFile(filename)
        if (not ttc) and len(fonts_in_file) >= 2:
            raise Exception("fonts_in: .ttc files not supported when ttc=%s is specified" % repr(ttc))
        font_structs = []
        if len(fonts_in_file) < 2:
            if filenamesonly:
                yield filename
                continue
            font_structs = [SimpleNamespace(
                filename=filename,
                filename_open=filename,
                filename_noext=os.path.splitext(filename)[0],
                fontname=None,
                ttc=False,
            )]
        else:
            if filenamesonly:
                for font_in_file in fonts_in_file:
                    yield font_in_file
                    continue
            font_structs = [SimpleNamespace(
                filename=filename,
                filename_open="%s(%s)" % (filename, font_in_file),
                filename_noext="%s(%s)" % (os.path.splitext(filename)[0], font_in_file),
                fontname=font_in_file,
                ttc=True,
            ) for font_in_file in fonts_in_file]
        for font_struct in font_structs:
            if not open_font:
                yield font_struct
                continue
            try:
                silence.on()
                font = fontforge.open(font_struct.filename_open)
                silence.off()
            except Exception as err:
                silence.off()
                raise err
            if names:
                if font_struct.fontname is None:
                    font_struct.fontname = font.fontname
                font_struct.font = font
                yield font_struct
            else:
                yield font
            if close:
                font.close()

def get_base_codepoint(glyph, default=-1):
    base_glyphname = glyph.glyphname.split(".")[0]
    result = fontforge.unicodeFromName(base_glyphname)
    if result < 0:
        return default
    return result
