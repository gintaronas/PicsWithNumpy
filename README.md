# PicsWithNumpy - Dog or cat or whatever breeder
This is a program resembling slicing of the photo vertically into many slices, then separating every other slice into separate picture.
As a second step, horizontal slicing is done and again every second horizontal slice is separated into new picture.
As a result, out of one cat or dog or whatever we get four.

[INSTALLATION]

To run the program you need Numpy and easygui. Check the requirements.txt

[CONFIGURATION]

There is only one parameter in config.ini file. It sets the width of slice in pixels. That is, yo can set here how wide slicing should be done.
Setting this parameter to 1 px gives the highest quality pictures.

[RUNNING]

Put the picture(s) into "input" directory for processing. Program will open file selection dialog with this directory as default location.
Select picture and enjoy. 
Output files are stored in "output" directory. Depending on the picture and the slicing, the will be 2 or 3 files created:
1. The first saved file contains picture split vertically into 2 by reshuffling and regrouping vertical slices;
2. The second file contains picture further processed with horizontal slicing nad reshuffling;
3. The third file is created if widths of the original and two mentioned above match. In this case, all three are merged vertically into one.


