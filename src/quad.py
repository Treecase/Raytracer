#!/usr/bin/python3
#
# See LICENSE file for copyright and license details.
# quad.py
#
#   Quad class definition
#



class Quad:
    """ 3D quadrilateral. """

    def __init__(self, points, colour=(255, 255, 255)):
        self.points = tuple(points)
        self.colour = tuple(colour)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        raise TypeError(
              "'" + type(self).__name__
              + "' object does not support item assignment")



def main():
    pass



if __name__ == '__main__':
    main()

