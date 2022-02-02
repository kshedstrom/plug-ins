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

# To Install

Place the *.py scripts in your plug-ins directory and the brushes
in the brushes directory. The plug-ins should show up under the Image menu.

## Linux

For GIMP 2.10, the files should go under:

   $HOME/.gimp-2.10/plug-ins directory
   $HOME/.gimp-2.10/brushes directory

Make sure the scripts are executable:

chmod 755 *.py

## Mac

On a Mac, the directories are now:

   $HOME/Library/Application\ Support/GIMP/2.10/plug-ins
   $HOME/Library/Application\ Support/GIMP/2.10/brushes

## PC

I don't have a PC to test, so I don't know where to put things there.

# Things to fix

Note: If you have an alpha channel, the results of the knitting
script looks weird. Better to remove the alpha channel (image -> flatten),
though that is a bug I might fix someday, someday.

I wish I knew how to make the brushes work with the foreground color.
Is that on my end or GIMP's?
