#!/usr/bin/python3
#
# See LICENSE file for copyright and license details.
# quad.py
#
#   Quad class definition
#

import numpy

from common import *



class Quad:
    """
    3D quadrilateral.

    p0,p1,p2
        Iterables each containing 3 numbers.

    Keyword args are:

        colour/color
            An iterable containing 3 integers in the range
            0-255; alternatively, a string of 3 hexadecimal
            numbers from 00-FF, in the form 'RR GG BB'.
    """

    def __init__(self, p0, p1, p2, **kwargs):

            self.points = tuple(
                [ numpy.array(p0), numpy.array(p1), numpy.array(p2) ])

            # Compute the normalized normal vector
            edge_1 = self.points[0] - self.points[1]
            edge_2 = self.points[0] - self.points[2]

            self.normal = numpy.cross(edge_1, edge_2)
            self.normal /= numpy.sqrt((self.normal**2).sum())


            # keyword arguments
            col = None
            if 'colour' in kwargs:
                col = kwargs['colour']
            elif 'color' in kwargs:
                col = kwargs['color']

            if isinstance(col, str):
                self.colour = tuple(
                    [ int(v, 16) for v in col.split() ])
            else:
                if col is not None:
                    self.colour = tuple(col)
                else:
                    self.colour = ( 255, 255, 255 )

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        raise TypeError(
              "'" + type(self).__name__
              + "' object does not support item assignment")

    def __repr__(self):
        return (
              type(self).__name__ + '('
            + ', '.join(str(point) for point in self.points)
            + ', colour=' + str(self.colour) + ')')

    def hit(self, origin, ray):
        """
        Test if ray ever intersects with self, where ray begins
        travelling from origin.

        origin
            3D vector, origin
        ray
            3D vector, delta
        """

        # Points on the quad, relative to the origin
        p0 = self[0] - origin
        p1 = self[1] - origin
        p2 = self[2] - origin

        #
        # Vector-Quad Intersection Algorithm
        # ==================================
        #
        # Paraphrased from
        # [https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection]
        #
        # NOTE: these formulas have been simplified, since we
        #       subtract 'origin' from the quad's points, we
        #       can treat the 'origin' as (0, 0, 0).
        #
        # The POI is
        #
        #   t*ray = p0 + u*(p1 - p0) + v*(p2 - p0)
        #
        # which can be rewritten as
        #
        #   -p0 = -t*ray + u*(p1 - p0) + v*(p2 - p0)
        #
        # which, in matrix form, is
        #                                          [ t ]
        #   [ -p0 ] = [ -ray  p1 - p0  p2 - p0 ] * | u |
        #                                          [ v ]
        #
        # This can be solved for 't', 'u', and 'v'. If
        # t E [0, 1],  then the POI is between 'origin' and
        # 'ray'. If  u,v E [0,1],  then the POI is within the
        # parallelogram formed by 'p0', 'p01', and 'p02'. If
        # (u + v) <= 1,  then the POI is within the triangle
        # formed by 'p0', 'p1', and 'p2'.
        #
        # If  -ray @ ((p1 - p0) x (p2 - p0)) = 0,  then the
        # line is either in or parallel to the quad.
        # Otherwise, 't', 'u', and 'v' can be found:
        #
        #       (p01 x p02) @ -p0
        #   t = ------------------
        #       -ray @ (p01 x p02)
        #
        #       (p02 x -ray) @ -p0
        #   u = ------------------
        #       -ray @ (p01 x p02)
        #
        #       (-ray x p01) @ -p0
        #   v = ------------------
        #       -ray @ (p01 x p02)
        #

        p01 = (p1 - p0)
        p02 = (p2 - p0)

        # Calculate the determinant
        determinant = numpy.dot(-ray, numpy.cross(p02, -p0))

        # No unique solutions, ray is either within or
        # parallel to the quad
        if determinant == 0:
            # TODO: add logic for the 'within' case
            pass

        # The ray might intersect with the quad
        else:
            denom = numpy.dot(-ray, numpy.cross(p01, p02))

            t = numpy.dot(numpy.cross(p01, p02), -p0) / denom
            u = numpy.dot(numpy.cross(p02, -ray), -p0) / denom
            v = numpy.dot(numpy.cross(-ray, p01), -p0) / denom

            # The ray intersects behind the origin
            behind = t < 0

            # The ray intersects outside of the quad
            outside = (
                not ((0 <= u and u <= 1)
                 and (0 <= v and v <= 1)))

            # If the ray is in front of the origin and within
            # the quad, it's a valid intersection
            if not (behind or outside):
                return Intersection(self, origin + t * ray)

        # No intersection
        return None



def main():
    q = Quad([0,0,0], [1,1,1], [2,2,2])
    print('q:', q)

    q = Quad([0,0,0], [1,1,1], [2,2,2],
        colour=( 0, 255, 0 ))
    print('q:', q)

    q = Quad([0,0,0], [1,1,1], [2,2,2],
        colour='ff ff ff')
    print('q:', q)



if __name__ == '__main__':
    main()

