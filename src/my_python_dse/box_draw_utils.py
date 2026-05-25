import math
from font_draw_utils import rect

light_stroke_width = 96
heavy_stroke_width = 336
double_stroke_width = 384
arc_drawing_radius = 5/6
heavy_circle_radius = 2/3

C = 0.5519150244935105707435627

ARC_TYPE_A = 0
ARC_TYPE_B = 1

def set_metrics(light=None,
                heavy=None,
                double=None,
                arc=None,
                heavycircle=None):
    global light_stroke_width
    global heavy_stroke_width
    global double_stroke_width
    global arc_drawing_radius
    global heavy_circle_radius
    if light is not None:
        light_stroke_width = light
    if heavy is not None:
        heavy_stroke_width = heavy
    if double is not None:
        double_stroke_width = double
    if arc is not None:
        arc_drawing_radius = arc
    if heavycircle is not None:
        heavy_circle_radius = heavycircle

def draw_light_vertical(glyph, clockwise=True):
    global light_stroke_width
    font = glyph.font
    x1 = glyph.width / 2 - light_stroke_width / 2
    x2 = glyph.width / 2 + light_stroke_width / 2
    rect(glyph, x1, x2, font.ascent, -font.descent, clockwise=clockwise)

def draw_light_horizontal(glyph, clockwise=True):
    global light_stroke_width
    font = glyph.font
    y1 = glyph.font.capHeight / 2 - light_stroke_width / 2
    y2 = glyph.font.capHeight / 2 + light_stroke_width / 2
    rect(glyph, 0, glyph.width, y1, y2, clockwise=clockwise)

def draw_light_horizontal_left(glyph, clockwise=True):
    global light_stroke_width
    font = glyph.font
    y1 = glyph.font.capHeight / 2 - light_stroke_width / 2
    y2 = glyph.font.capHeight / 2 + light_stroke_width / 2
    x1 = 0
    x2 = glyph.width / 2 + light_stroke_width / 2
    rect(glyph, x1, x2, y1, y2, clockwise=clockwise)

def draw_light_horizontal_right(glyph, clockwise=True):
    global light_stroke_width
    font = glyph.font
    y1 = glyph.font.capHeight / 2 - light_stroke_width / 2
    y2 = glyph.font.capHeight / 2 + light_stroke_width / 2
    x1 = glyph.width / 2 - light_stroke_width / 2
    x2 = glyph.width
    rect(glyph, x1, x2, y1, y2, clockwise=clockwise)

def draw_light_vertical_top(glyph, clockwise=True):
    global light_stroke_width
    font = glyph.font
    y1 = glyph.font.capHeight / 2 - light_stroke_width / 2
    y2 = glyph.font.ascent
    x1 = glyph.width / 2 - light_stroke_width / 2
    x2 = glyph.width / 2 + light_stroke_width / 2
    rect(glyph, x1, x2, y1, y2, clockwise=clockwise)

def draw_light_vertical_bottom(glyph, clockwise=True):
    global light_stroke_width
    font = glyph.font
    y1 = -glyph.font.descent
    y2 = glyph.font.capHeight / 2 + light_stroke_width / 2
    x1 = glyph.width / 2 - light_stroke_width / 2
    x2 = glyph.width / 2 + light_stroke_width / 2
    rect(glyph, x1, x2, y1, y2, clockwise=clockwise)

def draw_light_arc(glyph, upper=True, left=True, arc_type=ARC_TYPE_A, clockwise=True):
    global light_stroke_width
    font = glyph.font

    x_sign = 1 if left else -1
    y_sign = 1 if upper else -1

    if arc_type == ARC_TYPE_A:
        rx = compute_arc_radius_A(glyph)
        ry = compute_arc_radius_A(glyph)
    elif arc_type == ARC_TYPE_B:
        (rx, ry) = compute_arc_radius_B(glyph)

    rx1 = rx - light_stroke_width / 2
    rx2 = rx + light_stroke_width / 2
    ry1 = ry - light_stroke_width / 2
    ry2 = ry + light_stroke_width / 2

    x = glyph.width / 2
    y = glyph.font.capHeight / 2
    x1 = x - x_sign * light_stroke_width / 2
    x2 = x + x_sign * light_stroke_width / 2
    y1 = y + y_sign * light_stroke_width / 2
    y2 = y - y_sign * light_stroke_width / 2

    x3 = x - x_sign * rx
    y3 = y + y_sign * ry

    x4 = x3 + x_sign * rx1 * C
    x5 = x3 + x_sign * rx2 * C
    y4 = y3 - y_sign * ry1 * C
    y5 = y3 - y_sign * ry2 * C

    x0 = 0 if left else glyph.width
    y0 = font.ascent if upper else -font.descent

    this_way = True
    if not clockwise:
        this_way = not this_way
    if upper != left:
        this_way = not this_way

    p00 = (x0, y1)
    p01 = (x3, y1)
    p02x = (x4, y1)
    p03x = (x1, y4)
    p04 = (x1, y3)
    p05 = (x1, y0)
    p06 = (x2, y0)
    p07 = (x2, y3)
    p08x = (x2, y5)
    p09x = (x5, y2)
    p10 = (x3, y2)
    p11 = (x0, y2)

    pen = glyph.glyphPen(replace=False)
    if this_way:
        # this path is clockwise if upper left or lower right arc
        pen.moveTo(p00)
        pen.lineTo(p01)
        pen.curveTo(p02x, p03x, p04)
        pen.lineTo(p05)
        pen.lineTo(p06)
        pen.lineTo(p07)
        pen.curveTo(p08x, p09x, p10)
        pen.lineTo(p11)
        pen.lineTo(p00)
    else:
        # this path is clockwise if upper right or lower left arc
        pen.moveTo(p00)
        pen.lineTo(p11)
        pen.lineTo(p10)
        pen.curveTo(p09x, p08x, p07)
        pen.lineTo(p06)
        pen.lineTo(p05)
        pen.lineTo(p04)
        pen.curveTo(p03x, p02x, p01)
        pen.lineTo(p00)
    pen.closePath()
    pen = None

def draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_A, clockwise=True):
    draw_light_arc(glyph, upper=True, left=True, arc_type=arc_type, clockwise=clockwise)

def draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_A, clockwise=True):
    draw_light_arc(glyph, upper=True, left=False, arc_type=arc_type, clockwise=clockwise)

def draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_A, clockwise=True):
    draw_light_arc(glyph, upper=False, left=True, arc_type=arc_type, clockwise=clockwise)

def draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_A, clockwise=True):
    draw_light_arc(glyph, upper=False, left=False, arc_type=arc_type, clockwise=clockwise)

def draw_dot(glyph, clockwise=True):
    global light_stroke_width
    draw_heavy_circle(glyph, r = light_stroke_width * 1.25)

def draw_heavy_circle(glyph, r=None, clockwise=True):
    if r is None:
        r = heavy_circle_radius * glyph.width / 2
    x0 = glyph.width / 2
    y0 = glyph.font.capHeight / 2
    x1 = x0 - r
    x2 = x0 + r
    y1 = y0 + r
    y2 = y0 - r
    cp = r * C
    x3 = x0 - r * C
    x4 = x0 + r * C
    y3 = y0 + r * C
    y4 = y0 - r * C
    pen = glyph.glyphPen(replace=False)
    pen.moveTo((x1, y0))
    if clockwise:
        pen.curveTo((x1, y3), (x3, y1), (x0, y1))
        pen.curveTo((x4, y1), (x2, y3), (x2, y0))
        pen.curveTo((x2, y4), (x4, y2), (x0, y2))
        pen.curveTo((x3, y2), (x1, y4), (x1, y0))
    else:
        pen.curveTo((x1, y4), (x3, y2), (x0, y2))
        pen.curveTo((x4, y2), (x2, y4), (x2, y0))
        pen.curveTo((x2, y3), (x4, y1), (x0, y1))
        pen.curveTo((x3, y1), (x1, y3), (x1, y0))
    pen.closePath()
    pen = None

def hollow_out_heavy_circle(glyph, clockwise=False):
    global light_stroke_width
    r = heavy_circle_radius * glyph.width / 2 - light_stroke_width
    draw_heavy_circle(glyph, r=r, clockwise=clockwise)

def compute_arc_radius_A(glyph):
    font = glyph.font
    rx = glyph.width / 2 * arc_drawing_radius
    ry1 = (font.ascent - glyph.font.capHeight / 2) * arc_drawing_radius
    ry2 = (glyph.font.capHeight / 2 + font.descent) * arc_drawing_radius
    return min(rx, ry1, ry2)

def compute_arc_radius_B(glyph):
    font = glyph.font
    rx = glyph.width / 2 * arc_drawing_radius
    ry1 = (font.ascent - glyph.font.capHeight / 2) * arc_drawing_radius
    ry2 = (glyph.font.capHeight / 2 + font.descent) * arc_drawing_radius
    return (rx, min(ry1, ry2))

def draw_x_for_hollowed_out_heavy_circle(glyph, clockwise=True):
    global light_stroke_width
    global heavy_circle_radius
    r = glyph.width / 2 * heavy_circle_radius - light_stroke_width / 2
    print("r = %.4f" % r)
    xc = glyph.width / 2
    yc = glyph.font.capHeight / 2
    print("xc = %.4f; yc = %.4f" % (xc, yc));

    x5 = xc - light_stroke_width / math.sqrt(2)
    x6 = xc + light_stroke_width / math.sqrt(2)
    y5 = yc + light_stroke_width / math.sqrt(2)
    y6 = yc - light_stroke_width / math.sqrt(2)

    x_left  = xc - r / math.sqrt(2)
    x_right = xc + r / math.sqrt(2)
    y_upper = yc + r / math.sqrt(2)
    y_lower = yc - r / math.sqrt(2)

    x1 = x_left - light_stroke_width / math.sqrt(2) / 2
    x2 = x_left + light_stroke_width / math.sqrt(2) / 2
    x3 = x_right - light_stroke_width / math.sqrt(2) / 2
    x4 = x_right + light_stroke_width / math.sqrt(2) / 2

    y1 = y_upper + light_stroke_width / math.sqrt(2) / 2
    y2 = y_upper - light_stroke_width / math.sqrt(2) / 2
    y3 = y_lower + light_stroke_width / math.sqrt(2) / 2
    y4 = y_lower - light_stroke_width / math.sqrt(2) / 2

    print("x = %.4f, %.4f, %.4f, %.4f, %.4f, %.4f" % (x1, x2, x5, x6, x3, x4))
    print("y = %.4f, %.4f, %.4f, %.4f, %.4f, %.4f" % (y1, y2, y5, y6, y3, y4))

    pen = glyph.glyphPen(replace=False)
    if clockwise:
        pen.moveTo((x1, y2))
        pen.lineTo((x2, y1))
        pen.lineTo((xc, y5))
        pen.lineTo((x3, y1))
        pen.lineTo((x4, y2))
        pen.lineTo((x6, yc))
        pen.lineTo((x4, y3))
        pen.lineTo((x3, y4))
        pen.lineTo((xc, y6))
        pen.lineTo((x2, y4))
        pen.lineTo((x1, y3))
        pen.lineTo((x5, yc))
    else:
        pen.moveTo((x1, y2))
        pen.lineTo((x5, yc))
        pen.lineTo((x1, y3))
        pen.lineTo((x2, y4))
        pen.lineTo((xc, y6))
        pen.lineTo((x3, y4))
        pen.lineTo((x4, y3))
        pen.lineTo((x6, yc))
        pen.lineTo((x4, y2))
        pen.lineTo((x3, y1))
        pen.lineTo((xc, y5))
        pen.lineTo((x2, y1))
    pen.closePath()
    pen = None
