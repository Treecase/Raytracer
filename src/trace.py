#!/usr/bin/python3
#
# See LICENSE file for copyright and license details.
# trace.py
#
#   Raytracer
#
#   Positive X is right, negative X is left
#   Positive Y is down, negative Y is up
#   Positive Z is backwards, negative Z is forwards
#       (ie. out of/into the screen respectively)
#
#       ___ +X
#     /|
#    / |
#  +Z +Y
#

import numpy
from PIL import Image
import os

from parser import parse
from quad import Quad



def main(_argv=None):

    input_filename = 'world.txt'
    output_filename = 'render.png'

    if argv is not None and len(argv) > 1:
        if _argv[1] == '--help' :
            print('Usage: ' + _argv[0] + '[INPUT_FILE] [OUTPUT_FILE]')
            print("INPUT_FILE defaults to '" + input_filename + "'")
            print("OUTPUT_FILE defaults to '" + output_filename + "'")
            return
        else:
            input_filename = _argv[1]

        if len(_argv) > 2:
            output_filename = _argv[2]


    # The output image
    _canvas = Image.new('RGB', ( 100, 100 ))
    canvas = _canvas.load()

    # Width and height of the output image
    WIDTH,HEIGHT = _canvas.size

    # Focal length, aka zoom
    FOCAL_LENGTH = 1


    # Camera position
    camera_x = 0
    camera_y = 0
    camera_z = -5

    # The origin, aka camera's position as a vector
    origin = numpy.array([ camera_x, camera_y, camera_z ])


    # Read the world definition file
    with open(input_filename) as world_file:
        # Iterable of all the quads in the world
        quads = parse(world_file)

    for screen_y in range(HEIGHT):
        for screen_x in range(WIDTH):

            # The pixel's colour -- set to the background colour
            colour = ( 0, 0, 0 )

            # The ray's x/y deltas.
            # These range from -1 to 1, where screen coordinate (0, 0)
            # corresponds to 3D space coordinate (-1,-1), and screen
            # coordinate (WIDTH, HEIGHT) corresponds to 3D space
            # coordinate (1, 1)
            x_view = (screen_x / WIDTH ) - 0.5
            y_view = (screen_y / HEIGHT) - 0.5

            # The ray vector
            ray = numpy.array([ x_view, y_view, FOCAL_LENGTH ])


            # The 't' value of the closest intersection
            intersection_t = None

            # Check each quad for an intersection
            for quad in quads:
                p0 = quad[0] - origin
                p1 = quad[1] - origin
                p2 = quad[2] - origin

                # NOTE: these formulas have been simplified, because
                #       we subtract the quad's points back so we can
                #       treat 'origin' as (0, 0, 0).
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
                # TODO: add logic for the 'within' case
                if determinant == 0:
                    #print('determinant is 0, no unique solutions')
                    pass
                # The ray might intersect with the quad
                else:
                    t = (
                          numpy.dot(numpy.cross(p01, p02), -p0)
                        / numpy.dot(-ray, numpy.cross(p01, p02)))
                    u = (
                          numpy.dot(numpy.cross(p02, -ray), -p0)
                        / numpy.dot(-ray, numpy.cross(p01, p02)))
                    v = (
                          numpy.dot(numpy.cross(-ray, p01), -p0)
                        / numpy.dot(-ray, numpy.cross(p01, p02)))

                    # The ray intersects, but behind the origin
                    if t < 0:
                        #print('behind!')
                        pass
                    # The ray intersects, but outside of the quad
                    elif not (0 <= u and u <= 1
                            and 0 <= v and v <= 1):
                        #print('not in quad')
                        pass
                    # The ray intersects
                    else:
                        #print('soln:', t * ray)
                        # This quad is the closest intersection
                        if (intersection_t is None
                                or t < intersection_t):
                            intersection_t = t
                            colour = quad.colour

                canvas[( screen_x, screen_y )] = colour

    # Save the rendered image
    _canvas.save(output_filename)



if __name__ == '__main__':
    from sys import argv
    main(argv)

