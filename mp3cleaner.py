#/usr/bin/env python
import os
for file in os.listdir("."):
  if file.endswith(".mp3"):
    print "Cleaning mp3 file is %s" % file
    print os.popen("eyeD3 --remove-all '%s'" % file).read()
