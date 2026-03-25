import re, unicodedata

import silence
silence.on()
import fontforge
silence.off()

X = "X"
Y = "Y"

def rect(glyph, x1, x2, y1, y2):
    """Draw a rectangle onto the specified glyph.  Does not clear the glyph first.

    """
    print("rect(%s, %d, %d, %d, %d)" % (glyph, x1, x2, y1, y2))
    pen = glyph.glyphPen(replace=False)
    pen.moveTo((x1, y1))
    pen.lineTo((x2, y1))
    pen.lineTo((x2, y2))
    pen.lineTo((x1, y2))
    pen.closePath()
    pen = None

def poly(glyph, pairs):
    """Draw a polygon onto the specified glyph.  Does not clear the glyph first.

    Polygon will be closed.

    The `pairs` argument is a list of x,y coordinate pairs.  The first
    one is always two numbers.  Each subsequent coordinate pair can be:

    - (<x>, <y>) to draw a line to a new position

    - ("X", <x>) to move horizontally to a new position

    - ("Y", <x>) to move vertically to a new position.

    - ("X", <x>, <y>, <x>, <y>, ...) to move horizontally then
      alternate between vertical and horizontal.  This is equivalent
      to the following:

            ("X", x),
            ("Y", y),
            ("X", x),
            ("Y", y),
            ...

    - ("Y", <y>, <x>, <y>, <x>, ...) to move vertically then alternate
      between vertical and horizontal.

    - For convenience, I like to define:

          X = "X"
          Y = "Y"

      so that I can use barewords X and Y instead of strings.

    """
    pen = glyph.glyphPen(replace=False)
    x = pairs[0][0]
    y = pairs[0][1]
    pen.moveTo((x, y))
    for pair in pairs[1:]:
        if len(pair) > 2:
            if pair[0] == X:
                horizontal = True
            elif pair[0] == Y:
                horizontal = False
            else:
                raise Exception("tuple of more than 2 coordinates must start with X or Y")
            for i in range(1, len(pair)):
                if horizontal:
                    x = pair[i]
                else:
                    y = pair[i]
                pen.lineTo((x, y))
                horizontal = not horizontal
        elif pair[0] == X:
            x = pair[1]
            pen.lineTo((x, y))
        elif pair[0] == Y:
            y = pair[1]
            pen.lineTo((x, y))
        else:
            (x, y) = pair
            pen.lineTo((x, y))
    pen.closePath()
    pen = None

def clip(glyph, x1, y1, x2, y2):
    """Clips the foreground layer to the specified rectangle.

    """
    contour = fontforge.contour()
    contour.moveTo((x1, y1))
    contour.lineTo((x2, y1))
    contour.lineTo((x2, y2))
    contour.lineTo((x1, y2))
    contour.closed = True
    contour = None
    glyph.layers["Fore"] += clipContour
    glyph.intersect()

def GA(font, what):
    """Convenience function.

Returns an array containing a single item, that item being a FontForge
glyph object.

Used for `for glyph in GA(font, "CHARACTER NAME")` constructs, e.g.,

    for glyph in GA(font, "BOX DRAWINGS HEAVY TRIPLE DASH VERTICAL"):
        for i in range(0, 3):
            rect(glyph, x1_heavy, x2_heavy, dash_vert[3][i*2], dash_vert[3][i*2+1])
    for glyph in GA(font, "BOX DRAWINGS LIGHT QUADRUPLE DASH HORIZONTAL"):
        for i in range(0, 4):
            rect(glyph, dash_horiz[4][i*2], dash_horiz[4][i*2+1], y1_light, y2_light)

for visual separation.
"""
    g = None
    if type(what) == str:
        if len(what) == 1:
            g = font.createChar(ord(what))
        else:
            g = font.createChar(ord(unicodedata.lookup(what)))
    elif type(what) == int:
        g = font.createChar(what)
    else:
        raise Exception("GA: invalid argument type")
    g.clear()
    return [g]
