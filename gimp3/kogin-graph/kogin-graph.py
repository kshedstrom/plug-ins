#!/usr/bin/env python3
#
# GIMP 3 version of kogin-graph.py
# Original by Kate Hedstrom
# Ported from GIMP 2 Python-Fu to GIMP 3 GI API
#
# Take an image and turn it into a kogin pattern: expand it by
# some (you pick) number and place black lines around each box.

import gi
import sys
from array import array

gi.require_version('Gimp', '3.0')
gi.require_version('Gegl', '0.4')
gi.require_version('Gio', '2.0')

from gi.repository import Gimp
from gi.repository import Gegl
from gi.repository import GLib
from gi.repository import Gio
from gi.repository import GObject


class KoginGraphPlugin(Gimp.PlugIn):

    def do_query_procedures(self):
        return ["python-fu-kogin-graph"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self,
            name,
            Gimp.PDBProcType.PLUGIN,
            self.run,
            None,
        )

        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(
            Gimp.ProcedureSensitivityMask.DRAWABLE
        )

        procedure.set_menu_label("Kogin Graph...")
        procedure.add_menu_path("<Image>/Image")

        procedure.set_documentation(
            "Stretch the specified image for use as a kogin embroidery pattern",
            "Stretch the specified image for use as a kogin embroidery pattern",
            name,
        )

        procedure.set_attribution(
            "Kate Hedstrom",
            "Kate Hedstrom",
            "2021",
        )

        procedure.add_int_argument(
            "x_scale",
            "X scale",
            "Horizontal scale factor",
            1,
            100,
            12,
            GObject.ParamFlags.READWRITE,
        )

        procedure.add_int_argument(
            "y_scale",
            "Y scale",
            "Vertical scale factor",
            1,
            100,
            12,
            GObject.ParamFlags.READWRITE,
        )

        return procedure

    def run(self, procedure, run_mode, image, drawables, config, data):
        drawable = drawables[0]

        x_scale = config.get_property("x_scale")
        y_scale = config.get_property("y_scale")

        width = drawable.get_width()
        height = drawable.get_height()

        new_width = width * x_scale
        new_height = height * y_scale + 2

        new_image = Gimp.Image.new(new_width, new_height, Gimp.ImageBaseType.RGB)

        layer = Gimp.Layer.new(
            new_image,
            "Graph",
            new_width,
            new_height,
            Gimp.ImageType.RGB_IMAGE,
            100.0,
            Gimp.LayerMode.NORMAL,
        )

        new_image.insert_layer(layer, None, 0)

        src_buffer = drawable.get_buffer()
        dst_buffer = layer.get_buffer()

        src_rect = Gegl.Rectangle.new(0, 0, width, height)
        src_bytes = src_buffer.get(
            src_rect,
            1.0,
            None,
            Gegl.AbyssPolicy.NONE,
        )

        src_pixels = array("B", src_bytes.get_data())

        p_size = drawable.get_bpp()

        # Start with white background
        dest_pixels = array("B", [255] * (new_width * new_height * p_size))

        blackval = array("B", [0] * p_size)
        whiteval = array("B", [255] * p_size)

        for y in range(height):
            for x in range(width):
                src_pos = (x + width * y) * p_size
                newval = src_pixels[src_pos: src_pos + p_size]

                # Horizontal lines
                x1 = x_scale * x
                x2 = x1 + x_scale
                y1 = y_scale * y

                if (y % 10 == 0):
                    y2 = y1 + 2
                else:
                    y2 = y1 + 1

                for yy in range(y1, y2):
                    for xx in range(x1, x2):
                        dest_pos = (xx + new_width * yy) * p_size
                        dest_pixels[dest_pos: dest_pos + p_size] = blackval

                y1 = y_scale * (y + 1)

                if (y % 10 == 9):
                    y2 = y1 - 2
                else:
                    y2 = y1 - 1

                for yy in range(y1, y2):
                    for xx in range(x1, x2):
                        dest_pos = (xx + new_width * yy) * p_size
                        dest_pixels[dest_pos: dest_pos + p_size] = blackval

                # Vertical line
                y1 = y_scale * y
                y2 = y1 + y_scale

                if (x % 10 == 0):
                    x1 = x_scale * x + int(x_scale * 0.5) - 1
                    x2 = x1 + 3
                else:
                    x1 = x_scale * x + int(x_scale * 0.5)
                    x2 = x1 + 1

                for yy in range(y1, y2):
                    for xx in range(x1, x2):
                        dest_pos = (xx + new_width * yy) * p_size
                        dest_pixels[dest_pos: dest_pos + p_size] = blackval

                # Draw non-white lines second
                if newval != whiteval:
                    x1 = x_scale * x
                    x2 = x1 + x_scale
                    y1 = y_scale * y + int(y_scale * 0.25)
                    y2 = y1 + int(y_scale * 0.5)

                    for yy in range(y1, y2):
                        for xx in range(x1, x2):
                            dest_pos = (xx + new_width * yy) * p_size
                            dest_pixels[dest_pos: dest_pos + p_size] = newval

        # Bottom border
        y = height * y_scale
        x = width * x_scale

        for yy in range(y, y + 2):
            for xx in range(0, x):
                dest_pos = (xx + new_width * yy) * p_size
                dest_pixels[dest_pos: dest_pos + p_size] = blackval

        dst_rect = Gegl.Rectangle.new(0, 0, new_width, new_height)

        dst_buffer.set(
            dst_rect,
            "R'G'B'A u8",
            bytes(dest_pixels),
        )

        layer.update(0, 0, new_width, new_height)

        display = Gimp.Display.new(new_image)
        Gimp.displays_flush()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


Gimp.main(KoginGraphPlugin.__gtype__, sys.argv)

