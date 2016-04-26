#!/usr/bin/env python3

import cairo
import math

parties = [
    [ "Konservemuloj", (29, 113, 184), 36.9, 331 ],
    [ "Laboristoj", (190, 22, 34), 30.4, 232 ],
    [ "UKIP", (106, 37, 118), 12.6, 1 ],
    [ "Liberalaj Demokratoj", (251, 186, 48), 7.9, 8 ],
    [ "SNP", (0, 242, 229), 4.7, 56 ],
    [ "Verda Partio", (156, 196, 58), 3.8, 1 ],
    [ "DUP", (193, 63, 91), 0.6, 8 ],
    [ "Plaid Cymru", (0, 130, 67), 0.6, 3 ],
    [ "Sinn Fein", (13, 103, 46), 0.6, 4 ],
    [ "Ulster Unionist Party", (168, 168, 212), 0.4, 2 ],
    [ "SDLP", (47, 172, 102), 0.3, 3 ],
    [ "Aliaj", (90, 90, 90), 1.2, 0 ]
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
