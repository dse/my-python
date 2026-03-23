import statistics, math
from enum import Enum

class FontSpacing(Enum):
    NONE = 0
    MONOSPACE = 1
    DUALSPACE = 2
    PROPORTIONAL = 3
    @classmethod
    def nameof(cls, value):
        if value == FontSpacing.NONE:
            return "none"
        if value == FontSpacing.MONOSPACE:
            return "monospace"
        if value == FontSpacing.DUALSPACE:
            return "dualspace"
        if value == FontSpacing.PROPORTIONAL:
            return "proportional"

# stolen partially from fontconfig/src/fcfreetype.c
def approx_equal(x, y, fudge=1.01):
    if fudge == 1:
        return x == y
    fudge = abs(fudge if fudge > 1 else 1 / fudge)
    return abs(x - y) <= max(abs(x), abs(y)) * (fudge - 1)

# stolen partially from fontconfig/src/fcfreetype.c
def get_font_spacing_type(font, confidence=1, fudge=1, get_widths=False):
    glyphs = [g for g in font.glyphs() if g.unicode >= 0 and g.width >= (fudge - 1) * font.em]
    widths = [g.width for g in glyphs]
    spacings = get_spacings(widths, confidence=confidence, fudge=fudge)
    if len(spacings) > 2:
        spacing_type = FontSpacing.PROPORTIONAL
    elif len(spacings) == 2:
        spacing_type = FontSpacing.DUALSPACE
    elif len(spacings) == 1:
        spacing_type = FontSpacing.MONOSPACE
    else:
        spacing_type = FontSpacing.NONE
    if get_widths:
        return tuple([spacing_type] + spacings)
    return spacing_type

# stolen partially from fontconfig/src/fcfreetype.c
def get_spacings(widths, confidence=1, fudge=1):
    arrays = []
    for width in widths:
        for array in arrays:
            if approx_equal(width, statistics.median(array), fudge=fudge):
                array.append(width)
                break
        else:
            arrays.append([width])
    arrays = [a for a in arrays if len(a) > 0 and len(a) >= (1 - confidence) * len(widths) / len(arrays)]
    spacings = [statistics.median(a) for a in arrays]
    if len(spacings) == 2:
        square = spacings[0] * spacings[1] / 2
        single = int(math.sqrt(square))
        double = single * 2
        return [single, double]
    return spacings
