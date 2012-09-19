#!/usr/bin/python

# Copyright 2006-2007 Nanorex, Inc.  See LICENSE file for details. 
"""Try to do all the OpenGL stuff in Python, on the theory that
C extensions are hard to debug.
"""

import CruftDialog
from qt import *
from qtcanvas import *
from qtgl import *
from OpenGL.GL import *
import numpy.oldnumeric
import sys
import random
import time
import foo

_FONT_DATA = [
    "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    "\x00\x00\x18\x18\x00\x00\x18\x18\x18\x18\x18\x18\x18",
    "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x36\x36\x36\x36",
    "\x00\x00\x00\x66\x66\xff\x66\x66\xff\x66\x66\x00\x00",
    "\x00\x00\x18\x7e\xff\x1b\x1f\x7e\xf8\xd8\xff\x7e\x18",
    "\x00\x00\x0e\x1b\xdb\x6e\x30\x18\x0c\x76\xdb\xd8\x70",
    "\x00\x00\x7f\xc6\xcf\xd8\x70\x70\xd8\xcc\xcc\x6c\x38",
    "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x1c\x0c\x0e",
    "\x00\x00\x0c\x18\x30\x30\x30\x30\x30\x30\x30\x18\x0c",
    "\x00\x00\x30\x18\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x18\x30",
    "\x00\x00\x00\x00\x99\x5a\x3c\xff\x3c\x5a\x99\x00\x00",
    "\x00\x00\x00\x18\x18\x18\xff\xff\x18\x18\x18\x00\x00",
    "\x00\x00\x30\x18\x1c\x1c\x00\x00\x00\x00\x00\x00\x00",
    "\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00",
    "\x00\x00\x00\x38\x38\x00\x00\x00\x00\x00\x00\x00\x00",
    "\x00\x60\x60\x30\x30\x18\x18\x0c\x0c\x06\x06\x03\x03",
    "\x00\x00\x3c\x66\xc3\xe3\xf3\xdb\xcf\xc7\xc3\x66\x3c",
    "\x00\x00\x7e\x18\x18\x18\x18\x18\x18\x18\x78\x38\x18",
    "\x00\x00\xff\xc0\xc0\x60\x30\x18\x0c\x06\x03\xe7\x7e",
    "\x00\x00\x7e\xe7\x03\x03\x07\x7e\x07\x03\x03\xe7\x7e",
    "\x00\x00\x0c\x0c\x0c\x0c\x0c\xff\xcc\x6c\x3c\x1c\x0c",
    "\x00\x00\x7e\xe7\x03\x03\x07\xfe\xc0\xc0\xc0\xc0\xff",
    "\x00\x00\x7e\xe7\xc3\xc3\xc7\xfe\xc0\xc0\xc0\xe7\x7e",
    "\x00\x00\x30\x30\x30\x30\x18\x0c\x06\x03\x03\x03\xff",
    "\x00\x00\x7e\xe7\xc3\xc3\xe7\x7e\xe7\xc3\xc3\xe7\x7e",
    "\x00\x00\x7e\xe7\x03\x03\x03\x7f\xe7\xc3\xc3\xe7\x7e",
    "\x00\x00\x00\x38\x38\x00\x00\x38\x38\x00\x00\x00\x00",
    "\x00\x00\x30\x18\x1c\x1c\x00\x00\x1c\x1c\x00\x00\x00",
    "\x00\x00\x06\x0c\x18\x30\x60\xc0\x60\x30\x18\x0c\x06",
    "\x00\x00\x00\x00\xff\xff\x00\xff\xff\x00\x00\x00\x00",
    "\x00\x00\x60\x30\x18\x0c\x06\x03\x06\x0c\x18\x30\x60",
    "\x00\x00\x18\x00\x00\x18\x18\x0c\x06\x03\xc3\xc3\x7e",
    "\x00\x00\x3f\x60\xcf\xdb\xd3\xdd\xc3\x7e\x00\x00\x00",
    "\x00\x00\xc3\xc3\xc3\xc3\xff\xc3\xc3\xc3\x66\x3c\x18",
    "\x00\x00\xfe\xc7\xc3\xc3\xc7\xfe\xc7\xc3\xc3\xc7\xfe",
    "\x00\x00\x7e\xe7\xc0\xc0\xc0\xc0\xc0\xc0\xc0\xe7\x7e",
    "\x00\x00\xfc\xce\xc7\xc3\xc3\xc3\xc3\xc3\xc7\xce\xfc",
    "\x00\x00\xff\xc0\xc0\xc0\xc0\xfc\xc0\xc0\xc0\xc0\xff",
    "\x00\x00\xc0\xc0\xc0\xc0\xc0\xc0\xfc\xc0\xc0\xc0\xff",
    "\x00\x00\x7e\xe7\xc3\xc3\xcf\xc0\xc0\xc0\xc0\xe7\x7e",
    "\x00\x00\xc3\xc3\xc3\xc3\xc3\xff\xc3\xc3\xc3\xc3\xc3",
    "\x00\x00\x7e\x18\x18\x18\x18\x18\x18\x18\x18\x18\x7e",
    "\x00\x00\x7c\xee\xc6\x06\x06\x06\x06\x06\x06\x06\x06",
    "\x00\x00\xc3\xc6\xcc\xd8\xf0\xe0\xf0\xd8\xcc\xc6\xc3",
    "\x00\x00\xff\xc0\xc0\xc0\xc0\xc0\xc0\xc0\xc0\xc0\xc0",
    "\x00\x00\xc3\xc3\xc3\xc3\xc3\xc3\xdb\xff\xff\xe7\xc3",
    "\x00\x00\xc7\xc7\xcf\xcf\xdf\xdb\xfb\xf3\xf3\xe3\xe3",
    "\x00\x00\x7e\xe7\xc3\xc3\xc3\xc3\xc3\xc3\xc3\xe7\x7e",
    "\x00\x00\xc0\xc0\xc0\xc0\xc0\xfe\xc7\xc3\xc3\xc7\xfe",
    "\x00\x00\x3f\x6e\xdf\xdb\xc3\xc3\xc3\xc3\xc3\x66\x3c",
    "\x00\x00\xc3\xc6\xcc\xd8\xf0\xfe\xc7\xc3\xc3\xc7\xfe",
    "\x00\x00\x7e\xe7\x03\x03\x07\x7e\xe0\xc0\xc0\xe7\x7e",
    "\x00\x00\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\xff",
    "\x00\x00\x7e\xe7\xc3\xc3\xc3\xc3\xc3\xc3\xc3\xc3\xc3",
    "\x00\x00\x18\x3c\x3c\x66\x66\xc3\xc3\xc3\xc3\xc3\xc3",
    "\x00\x00\xc3\xe7\xff\xff\xdb\xdb\xc3\xc3\xc3\xc3\xc3",
    "\x00\x00\xc3\x66\x66\x3c\x3c\x18\x3c\x3c\x66\x66\xc3",
    "\x00\x00\x18\x18\x18\x18\x18\x18\x3c\x3c\x66\x66\xc3",
    "\x00\x00\xff\xc0\xc0\x60\x30\x7e\x0c\x06\x03\x03\xff",
    "\x00\x00\x3c\x30\x30\x30\x30\x30\x30\x30\x30\x30\x3c",
    "\x00\x03\x03\x06\x06\x0c\x0c\x18\x18\x30\x30\x60\x60",
    "\x00\x00\x3c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x3c",
    "\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc3\x66\x3c\x18",
    "\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x38\x30\x70",
    "\x00\x00\x7f\xc3\xc3\x7f\x03\xc3\x7e\x00\x00\x00\x00",
    "\x00\x00\xfe\xc3\xc3\xc3\xc3\xfe\xc0\xc0\xc0\xc0\xc0",
    "\x00\x00\x7e\xc3\xc0\xc0\xc0\xc3\x7e\x00\x00\x00\x00",
    "\x00\x00\x7f\xc3\xc3\xc3\xc3\x7f\x03\x03\x03\x03\x03",
    "\x00\x00\x7f\xc0\xc0\xfe\xc3\xc3\x7e\x00\x00\x00\x00",
    "\x00\x00\x30\x30\x30\x30\x30\xfc\x30\x30\x30\x33\x1e",
    "\x7e\xc3\x03\x03\x7f\xc3\xc3\xc3\x7e\x00\x00\x00\x00",
    "\x00\x00\xc3\xc3\xc3\xc3\xc3\xc3\xfe\xc0\xc0\xc0\xc0",
    "\x00\x00\x18\x18\x18\x18\x18\x18\x18\x00\x00\x18\x00",
    "\x38\x6c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x00\x00\x0c\x00",
    "\x00\x00\xc6\xcc\xf8\xf0\xd8\xcc\xc6\xc0\xc0\xc0\xc0",
    "\x00\x00\x7e\x18\x18\x18\x18\x18\x18\x18\x18\x18\x78",
    "\x00\x00\xdb\xdb\xdb\xdb\xdb\xdb\xfe\x00\x00\x00\x00",
    "\x00\x00\xc6\xc6\xc6\xc6\xc6\xc6\xfc\x00\x00\x00\x00",
    "\x00\x00\x7c\xc6\xc6\xc6\xc6\xc6\x7c\x00\x00\x00\x00",
    "\xc0\xc0\xc0\xfe\xc3\xc3\xc3\xc3\xfe\x00\x00\x00\x00",
    "\x03\x03\x03\x7f\xc3\xc3\xc3\xc3\x7f\x00\x00\x00\x00",
    "\x00\x00\xc0\xc0\xc0\xc0\xc0\xe0\xfe\x00\x00\x00\x00",
    "\x00\x00\xfe\x03\x03\x7e\xc0\xc0\x7f\x00\x00\x00\x00",
    "\x00\x00\x1c\x36\x30\x30\x30\x30\xfc\x30\x30\x30\x00",
    "\x00\x00\x7e\xc6\xc6\xc6\xc6\xc6\xc6\x00\x00\x00\x00",
    "\x00\x00\x18\x3c\x3c\x66\x66\xc3\xc3\x00\x00\x00\x00",
    "\x00\x00\xc3\xe7\xff\xdb\xc3\xc3\xc3\x00\x00\x00\x00",
    "\x00\x00\xc3\x66\x3c\x18\x3c\x66\xc3\x00\x00\x00\x00",
    "\xc0\x60\x60\x30\x18\x3c\x66\x66\xc3\x00\x00\x00\x00",
    "\x00\x00\xff\x60\x30\x18\x0c\x06\xff\x00\x00\x00\x00",
    "\x00\x00\x0f\x18\x18\x18\x38\xf0\x38\x18\x18\x18\x0f",
    "\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18",
    "\x00\x00\xf0\x18\x18\x18\x1c\x0f\x1c\x18\x18\x18\xf0",
    "\x00\x00\x00\x00\x00\x00\x06\x8f\xf1\x60\x00\x00\x00"
    ]


useFont = True

class Craft(CruftDialog.CruftDialog):

    def __init__(self, parent=None, name=None, modal=0, fl=0):
        CruftDialog.CruftDialog.__init__(self,parent,name,modal,fl)
        glformat = QGLFormat()
        print dir(glformat)
        print glformat.plane()
        # glformat.setStencil(True)
        self.qglwidget = qlgw = QGLWidget(glformat, self.frame1, "glpane")
        if useFont:
            # init the font in Python
            glShadeModel(GL_FLAT)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            self.fontOffset = fontOffset = glGenLists(len(_FONT_DATA))
            for i in range(len(_FONT_DATA)):
                # (i + 32) is ASCII codes from 32 to 126
                glNewList(i + 32 + fontOffset, GL_COMPILE)
                glBitmap(8, 13, 0.0, 2.0, 10.0, 0.0, _FONT_DATA[i])
            glEndList()
            w = 200; h = 200
            glViewport(0, 0, w, h)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho (0.0, w, 0.0, h, -1.0, 1.0)
            glMatrixMode(GL_MODELVIEW)
            
    def pushButton1_clicked(self):
        self.app.quit()

    # http://www.koders.com/python/fid96CE542E468E82FE726DC8705087F282A27A119D.aspx

    def paintEvent(self, e):
        """Draw a colorful collection of lines and circles.
        """
        white = Numeric.array((1.0, 1.0, 1.0), Numeric.Float)
        # clearing works fine
        glClearColor(0.0, 0.5, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)
        if useFont:
            glColor3fv(white)
            glRasterPos2i(20, 100)
            str = "The quick brown fox jumps"
            glPushAttrib(GL_LIST_BIT)

            glListBase(self.fontOffset)
            # PyOpenGL's glCallLists requires a Numeric array
            glCallLists(Numeric.array(map(ord, str)))

            # glCallList(self.fontOffset + ord('A'))
            glPopAttrib()

def main():
    app = QApplication(sys.argv)
    cr = Craft()
    cr.app = app
    app.setMainWidget(cr)
    cr.show()
    cr.update()
    app.exec_loop()

if __name__ == "__main__":
    main()
