# -*- coding: utf-8 -*-
# Copyright (c) 2015, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

"""
Checkerboard volume visualisation.
"""

import sys
import numpy as np

from vispy import app, gloo
from vispy.visuals import VolumeVisual, XYZAxisVisual, transforms


def checkerboard(nx,ny,nz):
    """ Generates a 3D checkerboard, with alternating white (1.0) and
    black (0.0) voxels.

    Parameters
    ----------
    nx : int
        Number of voxels in x direction.
    ny : int
        Number of voxels in y direction.
    nz : int
        Number of voxels in z direction.

    Returns
    -------
    vol : numpy.ndarray
        The checkerboard volume.
    """
    vol = np.zeros((nx,ny,nz))
    firstz = 1.0
    for k in range(nz):
        firsty = firstz
        for j in range(ny):
            nextval = firsty
            for i in range(nx):
                vol[(i,j,k)] = nextval
                nextval = 1.0 if ( nextval == 0.0 ) else 0.0
            firsty = 1.0 if ( firsty == 0.0 ) else 0.0
        firstz = 1.0 if ( firstz == 0.0 ) else 0.0
    return vol


class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, 'Checkerboard', keys='interactive',
                            size=(600, 600))

        # volume visual with default parameters
        self.volume = VolumeVisual(checkerboard(10,3,5),method='mip')
        self.axis = XYZAxisVisual()
        self.extents = (
            (self.volume.bounds('',0)[1] - self.volume.bounds('',0)[0]),
            (self.volume.bounds('',1)[1] - self.volume.bounds('',1)[0]),
            (self.volume.bounds('',2)[1] - self.volume.bounds('',2)[0]))
        self.theta = -0.5 + 60.0
        self.phi = -0.5 + 30.0

        # Create a TransformSystem that will tell the visual how to draw
        self.vol_transform = transforms.AffineTransform()
        self.tr_sys = transforms.TransformSystem(self)
        self.tr_sys.visual_to_document = self.vol_transform

#        self._timer = app.Timer('auto', connect=self.on_timer, start=True)

        self.show()
        self.on_timer(None)

    def on_draw(self, event):
        gloo.set_viewport(0, 0, *self.physical_size)
        gloo.clear('black')
        self.tr_sys.auto_configure()
        self.volume.draw(self.tr_sys)
        self.axis.draw(self.tr_sys)

    def on_timer(self, event):
        self.theta += .5
        self.phi += .5
        self.vol_transform.reset()
        self.vol_transform.rotate(self.theta, (0, 0, 1))
        self.vol_transform.rotate(self.phi, (0, 1, 0))
        self.vol_transform.scale((180 / self.extents[0],
                                  180 / self.extents[0],
                                0.001 / self.extents[0]))
        self.vol_transform.translate((300, 300))
        self.update()

if __name__ == '__main__':
    win = Canvas()
    win.show()
    if sys.flags.interactive != 1:
        win.app.run()
