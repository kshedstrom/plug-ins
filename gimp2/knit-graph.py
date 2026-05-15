#!/usr/bin/env python
#
#  Take an image and turn it into a knitting pattern: expand it by
#  some (you pick) number and place black lines around each box.
#  Chunks stolen from Akkana Peck's arclayer script.

import math
from gimpfu import *
from array import array

def python_knit_graph(timg, tdrawable, x_scale=14, y_scale=10):
    w = tdrawable.width
    h = tdrawable.height
    bpp = tdrawable.bpp
    width = w*x_scale + 3
    height = h*y_scale + 3
    img = gimp.Image(width, height, RGB)
    img.disable_undo()

    layer= gimp.Layer(img, "Graph", width, height, RGB_IMAGE,
                           100, NORMAL_MODE)
    img.add_layer(layer, 0)
    layers = img.layers
#    for l in layers:
#             print "Layer: Name=\"%s\" Width=%d Height=%d X=%d Y=%d\n"%(l.name, l.width, l.height, l.offsets[0], l.offsets[1])

     # initialize the regions and get their contents into arrays:
    srcRgn = tdrawable.get_pixel_rgn(0, 0, w, h, False, False)
    src_pixels = array("B", srcRgn[0:w, 0:h])

    dstRgn = layer.get_pixel_rgn(0, 0, width, height, True, True)
    p_size = len(dstRgn[0,0])               

#    fg_colour = gimp.get_foreground()
#  Just let it fill with black
    dest_pixels = array("B", "\x00" * (width * height * p_size))


    for y in range(0, h):
        for x in range(0, w):
	    src_pos = (x + w * y) * p_size
	    newval = src_pixels[src_pos: src_pos + p_size]
            x1 = x_scale*x
            x2 = x1 + x_scale
            y1 = y_scale*y
            y2 = y1 + y_scale
	    if (x%10 == 9):
                x2 = x2 - 1
	    if (y%10 == 9):
                y2 = y2 - 1
	    if (x%10 == 0):
                x1 = x_scale*x + 2
            else:
                x1 = x_scale*x + 1
	    if (y%10 == 0):
                y1 = y_scale*y + 2
            else:
                y1 = y_scale*y + 1

	    for yy in range(y1, y2):
	        for xx in range(x1, x2):
                    dest_pos = (xx + width * yy) * p_size
                    dest_pixels[dest_pos: dest_pos + p_size] = newval

    dstRgn[0:width, 0:height] = dest_pixels.tostring()

    layer.flush()
    layer.merge_shadow(True)
    layer.update(0, 0, width, height)

    img.enable_undo()
    gimp.Display(img)
    gimp.displays_flush()
#    drawable = pdb.gimp_image_get_active_layer(img)
#    pdb.gimp_file_save(img, drawable, file_name, file_name)

register(
        "python_knit_graph",
        "Stretch the specified image for use as a knitting pattern",
        "Stretch the specified image for use as a knitting pattern",
        "Kate Hedstrom",
        "Kate Hedstrom",
        "2013",
        "<Image>/Image/Knit_graph...",
        "*",
        [
            (PF_INT, "x_scale", "X scale", 14),
            (PF_INT, "y_scale", "Y scale", 10)
        ],
        [],
        python_knit_graph)

main()
