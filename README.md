# Knitting and Embroidery Charts in GIMP

I have designed a few knitting patterns in gimp. One pixel per
stitch works pretty well - until it's time to print the thing. This
script expands your pattern (scale factor is user selectable) and
draws it with black lines, thicker black lines every ten stitches.
See [Knitting wiki](https://github.com/kshedstrom/plug-ins/wiki/Knitting-charts)
for an example.

Nov 2021: I have now made a similar script for kogin sashiko
embroidery patterns. I'm adding modoko from koginbank.com to the
Kogin_brushes directory, with all the small ones so far. Copy the
ones you want to your brushes directory. See [Kogin
wiki](https://github.com/kshedstrom/plug-ins/wiki/Kogin-sashiko)
for an example.

# Warning

This all worked fine under Python 2 and Gimp 2 back in the day. For newer
operating systems that don't come with Python 2, it seems we have to migrate
to Gimp 3 which works with Python 3. This is a work in progress, meanwhile
there are both gimp2 and gimp3 directories containing the old and new codes.

# To Install

Place the *.py scripts in your plug-ins directory and the brushes
in the brushes directory. The plug-ins should show up under the Image menu.

To find where they have to go, Gimp has a Preferences menu. This menu is under
Settings in Gimp 3.2, with a Folders submenu that needs to be expanded. The
plug-ins path will show you both the system-wide path and your individual path.
You may have to create these directories first. For the plug-ins, Gimp 3
requires that they be in a subdirectory under this with the appropriate name,
for instance knit-graph/knit-graph.py.

## Linux

For GIMP 2.10, the files should go under:

   $HOME/.config/GIMP/2.10/plug-ins directory
   $HOME/.config/GIMP/2.10/brushes directory

Make sure the scripts are executable:

chmod 755 *.py

## Mac

On a Mac, the directories are now:

   $HOME/Library/Application\ Support/GIMP/2.10/plug-ins
   $HOME/Library/Application\ Support/GIMP/2.10/brushes

## PC

I don't have a PC to test.

# Things to fix

Note: If you have an alpha channel, the results of the knitting
script looks weird. Better to remove the alpha channel (image -> flatten),
though that is a bug I might fix someday, someday.

More work to do on Gimp 3 side.
