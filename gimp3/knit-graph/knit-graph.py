#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# GIMP 3 port of knit-graph.py
#
# Take an image and turn it into a knitting pattern: expand it by
# configurable X/Y scale factors and place black grid lines around each box.

import sys

import gi
gi.require_version("Gimp", "3.0")
gi.require_version("Gegl", "0.4")
gi.require_version('GimpUi', '3.0')

from gi.repository import Gimp
from gi.repository import GimpUi
from gi.repository import Gegl
from gi.repository import GObject
from gi.repository import GLib


PROC_NAME = "python-fu-knit-graph"

def N_(message): return message
def _(message): return GLib.dgettext(None, message)

def knit_graph_run(procedure, run_mode, image, drawables, config, data):
    if len(drawables) < 1:
        return procedure.new_return_values(
            Gimp.PDBStatusType.CALLING_ERROR,
            GLib.Error("Knit graph needs an active drawable/layer", PROC_NAME, 0),
        )

    src_drawable = drawables[0]

    x_scale = config.get_property("x-scale")
    y_scale = config.get_property("y-scale")

    if x_scale < 1 or y_scale < 1:
        return procedure.new_return_values(
            Gimp.PDBStatusType.CALLING_ERROR,
            GLib.Error("Scale values must be at least 1", PROC_NAME, 0),
        )

    src_w = src_drawable.get_width()
    src_h = src_drawable.get_height()

    dst_w = src_w * x_scale + 3
    dst_h = src_h * y_scale + 3

    # This is an RGB plug-in result, matching the original GIMP 2 script.
    bytes_per_pixel = 3
    pixel_format = "RGB u8"

    src_rect = Gegl.Rectangle.new(0, 0, src_w, src_h)
    src_buffer = src_drawable.get_buffer()
    src_pixels = bytes(src_buffer.get(src_rect, 1.0, pixel_format, Gegl.AbyssPolicy.NONE))

    dst_pixels = bytearray(dst_w * dst_h * bytes_per_pixel)  # black background/grid

    for y in range(src_h):
        for x in range(src_w):
            src_pos = (x + src_w * y) * bytes_per_pixel
            newval = src_pixels[src_pos:src_pos + bytes_per_pixel]

            x1 = x_scale * x
            x2 = x1 + x_scale
            y1 = y_scale * y
            y2 = y1 + y_scale

            # Preserve the original "heavy line every 10 cells" behavior.
            if x % 10 == 9:
                x2 -= 1
            if y % 10 == 9:
                y2 -= 1

            if x % 10 == 0:
                x1 = x_scale * x + 2
            else:
                x1 = x_scale * x + 1

            if y % 10 == 0:
                y1 = y_scale * y + 2
            else:
                y1 = y_scale * y + 1

            for yy in range(y1, y2):
                row_pos = yy * dst_w * bytes_per_pixel
                for xx in range(x1, x2):
                    dst_pos = row_pos + xx * bytes_per_pixel
                    dst_pixels[dst_pos:dst_pos + bytes_per_pixel] = newval

    new_image = Gimp.Image.new(dst_w, dst_h, Gimp.ImageBaseType.RGB)
#   new_image.disable_undo()

    layer = Gimp.Layer.new(
        new_image,
        "Graph",
        dst_w,
        dst_h,
        Gimp.ImageType.RGB_IMAGE,
        100.0,
        Gimp.LayerMode.NORMAL,
    )
    new_image.insert_layer(layer, None, 0)

    dst_rect = Gegl.Rectangle.new(0, 0, dst_w, dst_h)
    dst_buffer = layer.get_buffer()
    dst_buffer.set(dst_rect, pixel_format, bytes(dst_pixels))
    dst_buffer.flush()
    layer.update(0, 0, dst_w, dst_h)

#   new_image.enable_undo()
    Gimp.Display.new(new_image)
    Gimp.displays_flush()

    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)


class KnitGraph(Gimp.PlugIn):
    def do_query_procedures(self):
        return [PROC_NAME]

    def do_create_procedure(self, name):
        if name != PROC_NAME:
            return None

        procedure = Gimp.ImageProcedure.new(
            self,
            name,
            Gimp.PDBProcType.PLUGIN,
            knit_graph_run,
            None,
        )

        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.DRAWABLE)
        procedure.set_menu_label("Knit_graph...")
        procedure.add_menu_path("<Image>/Image")

        procedure.set_documentation(
            "Stretch the specified image for use as a knitting pattern",
            "Stretch the specified image for use as a knitting pattern",
            None,
        )
        procedure.set_attribution("Kate Hedstrom; GIMP 3 port by ChatGPT", "Kate Hedstrom", "2013/2026")

        procedure.add_int_argument(
            "x-scale",
            "X scale",
            "Horizontal cell scale",
            1,
            1000,
            14,
            GObject.ParamFlags.READWRITE,
        )
        procedure.add_int_argument(
            "y-scale",
            "Y scale",
            "Vertical cell scale",
            1,
            1000,
            10,
            GObject.ParamFlags.READWRITE,
        )

        return procedure


Gimp.main(KnitGraph.__gtype__, sys.argv)
