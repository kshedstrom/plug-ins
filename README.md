I have designed a few knitting patterns in gimp. One pixel per
stitch works pretty well - until it's time to print the thing. This
script expands your pattern (scale factor is user selectable) and
draws it with black lines, thicker black lines every ten stitches.

Nov 2021: I have now made a similar script for kogin sashiko
embroidery patterns. I'm adding modoko from koginbank.com to the
Kogin_brushes directory, with all the small ones so far. Copy the
ones you want to your brushes directory.

Place the *.py scripts in your $HOME/.gimp-2.10/plug-ins directory (or
similar) then change them to executable:

chmod 755 *.py

They should show up under the Image menu.

On a Mac, the directories are now:

   $HOME/Library/Application\ Support/GIMP/2.10/plug-ins
   $HOME/Library/Application\ Support/GIMP/2.10/brushes

I don't have a PC to test, so I don't know where to put things there.

Note: If you have an alpha channel, the results of the knitting
script looks weird. Better to remove the alpha channel, though that
is a bug I might fix someday, someday.
