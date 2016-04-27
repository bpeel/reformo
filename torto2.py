#!/usr/bin/env python3

import cairo
import math

parties = [
    [ "Slytherine", (0x00, 0x41, 0x01), 54, 1 ],
    [ "Gryffindor", (0xf3, 0x9f, 0x00), 40, 1 ],
    [ "Ravenclaw", (0x00, 0x00, 0xa0), 50, 1 ],
]

SIZE = 800
KEY_CIRCLE_RADIUS = 10
KEY_LINE_SIZE = 30

def set_party_color(cr, party):
    cr.set_source_rgb(*map(lambda x: x / 255.0, party[1]))

def draw_chart(cr, value_index):
    total = sum(map(lambda x: x[value_index], parties))

    pos = -math.pi / 2.0

    cr.save()
    cr.translate(SIZE / 2, SIZE / 2)
    
    for party in parties:
        value = party[value_index]
        size = value * 2 * math.pi / total
        end = pos + size

        cr.move_to(0, 0)
        cr.arc(0, 0, SIZE / 2, pos, end)
        cr.close_path()

        set_party_color(cr, party)
        cr.fill()

        pos = end

    cr.restore()

surf = cairo.SVGSurface("torto.svg", SIZE * 3, SIZE)
cr = cairo.Context(surf)

draw_chart(cr, 3)
cr.save()
cr.translate(SIZE, 0)
draw_chart(cr, 2)
cr.restore()

cr.save()
cr.set_font_size(KEY_LINE_SIZE * 0.9)

party_num = 0
for party in parties:
    cr.save()
    cr.translate(SIZE * 2 + KEY_CIRCLE_RADIUS * 4,
                 SIZE / 2 - KEY_LINE_SIZE * len(parties) / 2 +
                 party_num * KEY_LINE_SIZE)

    cr.arc(KEY_CIRCLE_RADIUS / 2,
           KEY_LINE_SIZE / 2,
           KEY_CIRCLE_RADIUS,
           0, 2 * math.pi)
    set_party_color(cr, party)
    cr.fill()
    (ascent, descent, height, max_x_advance, max_y_advance) = cr.font_extents()
    cr.set_source_rgb(0, 0, 0)
    cr.move_to(KEY_CIRCLE_RADIUS * 3,
               KEY_LINE_SIZE / 2 + height / 2 - descent)
    cr.show_text(party[0])

    cr.restore()

    party_num += 1

cr.restore()
