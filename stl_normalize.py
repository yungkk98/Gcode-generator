import sys
from ui import Ui_MainWindow
import numpy as np
from stl_data import StlData
from PyQt5 import QtWidgets
import math
import struct
import numbers
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import multiprocessing

from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from tkinter import (Tk, Canvas, BOTH, ROUND, NW, ALL, mainloop)

import geometry2d as geom
try:
    from itertools import zip_longest as ziplong
except ImportError:
    from itertools import izip_longest as ziplong

from vector import Vector
from point3d import Point3D
from line_segment3d import LineSegment3D


class GcodeGenerater:

    def __init__(self):
        self.infile = ''
        self.verbose = True
        self.check_manifold = True
        self.outfile = ''
        self.write_binary = False
        self.slice_to_file = True
        self.show_slicing = False
        self.threads = 1
        self.paths = None
        self.unit_E = 1
        self.z_range = []
        self.x_lim = []
        self.y_lim = []

    def analyze(self):
        stl = StlData()
        stl.read_file(self.infile)
        if self.verbose:
            print("Read {0} ({1:.1f} x {2:.1f} x {3:.1f})".format(
                self.infile,
                stl.points.maxx - stl.points.minx,
                stl.points.maxy - stl.points.miny,
                stl.points.maxz - stl.points.minz,
            ))

        manifold = True
        if self.check_manifold:
            manifold = stl.check_manifold(verbose=self.verbose)
            if manifold and self.verbose:
                print("{} is manifold.".format(self.infile))
        if not manifold:
            sys.exit(-1)

        if self.outfile:
            stl.write_file(self.outfile, binary=self.write_binary)
            if self.verbose:
                print("Wrote {0} ({1})".format(
                    self.outfile,
                    ("binary" if self.write_binary else "ASCII"),
                ))

        if self.slice_to_file:
            try:
                from slicer_mod import Slicer
                slicer = Slicer(stl)
                self.paths = slicer.slice_to_file(self.slice_to_file, showgui=self.show_slicing, threads=self.threads)

                x, y = [], []
                for z_plane in self.paths:
                    self.z_range.append(z_plane[0])
                    for path in z_plane[1]:
                        for point in path:
                            x.append(point[0])
                            y.append(point[1])
                self.z_range.sort()

                r = max(max(x) - min(x), max(y) - min(y))
                self.x_lim = [(max(x) + min(x)) / 2 - r * 0.6, (max(x) + min(x)) / 2 + r * 0.6]
                self.y_lim = [(max(y) + min(y)) / 2 - r * 0.6, (max(y) + min(y)) / 2 + r * 0.6]
            except Exception as e:
                print(e)

    def draw_plane(self, ax, z):
        ax.clear()
        try:
            ax.set_xlim(self.x_lim)
            ax.set_ylim(self.y_lim)
            ax.set_aspect(1.0)
            for path in self.paths[z][1]:
                x, y = [], []
                for point in path:
                    x.append(point[0])
                    y.append(point[1])
                ax.plot(x, y)
        except Exception as e:
            print(e)

    def write_file(self):
        try:
            with open(self.outfile, 'w') as f:
                e = 0
                x_prev, y_prev, z_prev = 0, 0, 0
                for z_plane in self.paths:
                    z, coords_list = z_plane
                    for coords in coords_list:
                        move = True
                        for coor in coords:
                            x, y = coor
                            if not move:
                                e += np.sqrt(sum(list(map(lambda a: (a[0] - a[1]) ** 2, [(x, x_prev), (y, y_prev), (z, z_prev)])))) * self.unit_E
                            else:
                                move = False
                            x_prev, y_prev, z_prev = x, y, z
                            f.write('G1 X' + str(x) + ' Y' + str(y) + ' Z' + str(z) + ' E' + str(e) + '\n')
        except Exception as e:
            print(e)


if __name__ == "__main__":
    import sys
    gcode_gen = GcodeGenerater()
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow(gcode_gen)
    ui.show()
    sys.exit(app.exec_())
