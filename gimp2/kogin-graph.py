#!/usr/bin/env python
#
#  Take an image and turn it into a kogin pattern: expand it by
#  some (you pick) number and place black lines around each box.
#  Chunks stolen from Akkana Peck's arclayer script.

import math
from gimpfu import *
from array import array

def python_kogin_graph(timg, tdrawable, x_scale=12, y_scale=12):
    w = tdrawable.width
    h = tdrawable.height
    bpp = tdrawable.bpp
    width = w*x_scale
    height = h*y_scale + 2
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
#  Just let it fill with white
    dest_pixels = array("B", "\xff" * (width * height * p_size))

    blackval = array("B", "\x00" * (1 * 1 * p_size))
    whiteval = array("B", "\xff" * (1 * 1 * p_size))

    for y in range(0, h):
        for x in range(0, w):
	    src_pos = (x + w * y) * p_size
	    # Fetch the color of the original square
	    newval = src_pixels[src_pos: src_pos + p_size]

	    # Draw black lines first

            # Horizontal lines
            x1 = x_scale*x
            x2 = x1 + x_scale
            y1 = y_scale*y
	    if (y%10 == 0):
                y2 = y1 + 2
            else:
                y2 = y1 + 1
	    for yy in range(y1, y2):
	        for xx in range(x1, x2):
                    dest_pos = (xx + width * yy) * p_size
                    dest_pixels[dest_pos: dest_pos + p_size] = blackval

            y1 = y_scale*(y+1)
	    if (y%10 == 9):
                y2 = y1 - 2
            else:
                y2 = y1 - 1
	    for yy in range(y1, y2):
	        for xx in range(x1, x2):
                    dest_pos = (xx + width * yy) * p_size
                    dest_pixels[dest_pos: dest_pos + p_size] = blackval

            # Vertical line
            y1 = y_scale*y
            y2 = y1 + y_scale
	    if (x%10 == 0):
                x1 = x_scale*x + int(x_scale * 0.5) - 1
		x2 = x1 + 3
            else:
                x1 = x_scale*x + int(x_scale * 0.5)
		x2 = x1 + 1
	    for yy in range(y1, y2):
	        for xx in range(x1, x2):
                    dest_pos = (xx + width * yy) * p_size
                    dest_pixels[dest_pos: dest_pos + p_size] = blackval

	    # Draw non-white lines second
	    if (newval != whiteval):
                x1 = x_scale*x
                x2 = x1 + x_scale
                y1 = y_scale*y + int(y_scale * 0.25)
                y2 = y1 + int(y_scale * 0.5)

	        for yy in range(y1, y2):
	            for xx in range(x1, x2):
                        dest_pos = (xx + width * yy) * p_size
                        dest_pixels[dest_pos: dest_pos + p_size] = newval
    y = h*y_scale
    x = w*x_scale
    for yy in range(y, y+2):
        for xx in range(0, x):
            dest_pos = (xx + width * yy) * p_size
            dest_pixels[dest_pos: dest_pos + p_size] = blackval

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
        "python_kogin_graph",
        "Stretch the specified image for use as a kogin embroidery pattern",
        "Stretch the specified image for use as a kogin embroidery pattern",
        "Kate Hedstrom",
        "Kate Hedstrom",
        "2021",
        "<Image>/Image/Kogin_graph...",
        "*",
        [
            (PF_INT, "x_scale", "X scale", 12),
            (PF_INT, "y_scale", "Y scale", 12)
        ],
        [],
        python_kogin_graph)

main()
