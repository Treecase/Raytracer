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
from pointlight import PointLight
from common import *



def trace_ray(origin, ray, surfaces):
    """
    Trace a ray, detecting intersections with any surface in surfaces.

    origin
        A 3D vector, representing the origin point.
    ray
        A 3D vector, representing the delta vector.
    surfaces
        Surfaces to consider for intersections.
    """

    # Intersection data
    nearest_intersection = None
    nearest_dist = None

    # Check each surface for an intersection
    for surface in surfaces:

        intersection = surface.hit(origin, ray)

        if intersection is not None:
            dist = numpy.linalg.norm(intersection.point - origin)

            # We're only interested in the intersection closest to
            # the origin
            if nearest_intersection is None or dist < nearest_dist:
                nearest_intersection = intersection
                nearest_dist = dist

    return nearest_intersection



def main(_argv=None):

    input_filename = 'world.txt'
    output_filename = 'render.png'


    # Handle command-line arguments
    if argv is not None and len(argv) > 1:
        # Help message
        if _argv[1] == '--help' :
            print('Usage: ' + _argv[0] + '[INPUT_FILE] [OUTPUT_FILE]')
            print("INPUT_FILE defaults to '" + input_filename + "'")
            print("OUTPUT_FILE defaults to '" + output_filename + "'")
            return
        # Set the input filename
        else:
            input_filename = _argv[1]

        # Set the output filename
        if len(_argv) > 2:
            output_filename = _argv[2]


    # The output image
    # TODO: The image size should be configurable
    _image = Image.new('RGB', ( 100, 100 ))
    image = _image.load()

    # Width and height of the output image
    WIDTH,HEIGHT = _image.size

    # Background colour
    # TODO: Make this configurable
    BACKGROUND_COLOUR = ( 0, 0, 0 )


    # Focal length, aka zoom
    # TODO: Make this configurable
    FOCAL_LENGTH = 1

    # Camera position
    # TODO: Make this configurable
    camera_x =  0
    camera_y =  0
    camera_z = -5

    # The origin, aka camera's position as a vector
    origin = numpy.array([ camera_x, camera_y, camera_z ])


    # Read the world definition file
    with open(input_filename) as world_file:
        world = parse(world_file)
        surfaces = [ o for o in world if isinstance(o, Quad) ]
        lights = [ l for l in world if isinstance(l, PointLight) ]



    # Raytracing
    for screen_y in range(HEIGHT):
        for screen_x in range(WIDTH):

            # Output pixel's colour
            colour = BACKGROUND_COLOUR

            # The ray's x/y deltas.
            # These range from -1 to 1, where screen coordinate (0, 0)
            # corresponds to 3D space coordinate (-1,-1), and screen
            # coordinate (WIDTH, HEIGHT) corresponds to 3D space
            # coordinate (1, 1)
            x_view = (screen_x / WIDTH ) - 0.5
            y_view = (screen_y / HEIGHT) - 0.5

            # The ray delta vector
            ray = numpy.array([ x_view, y_view, FOCAL_LENGTH ])

            intersection = trace_ray(origin, ray, surfaces)

            # Shading
            # TODO: (texturing)
            if intersection is not None:

                # The POI, in world coordinates
                point = intersection.point

                # Unit vector pointing from POI towards the origin
                v = origin - point
                v /= numpy.sqrt((v**2).sum())

                # Lights
                for light in lights:

                    # Unit vector pointing from POI towards the light
                    # source
                    l = light.pos - point
                    l /= numpy.sqrt((l**2).sum())

                    # Don't run the shader if the light is shadowed
                    if (trace_ray(point, l, (
                                s for s in surfaces
                                if s != intersection.surface ))
                            is None):
                        # Intensity of the light (ranges from 0-1)
                        intensity = tuple(
                            c / 255 for c in light.colour)

                        # Lambertian shading
                        colour = tuple(intersection.surface.colour[i]
                            * (intensity[i] * max(0, numpy.dot(
                                    intersection.surface.normal, l)))
                            for i in range(3))

                        # Blinn-Phong shading
                        # TODO: Make these configurable
                        specular_coefficient = ( 255, 255, 255 )
                        p = 1000

                        h = (v + l) / numpy.linalg.norm(v + l)
                        colour = tuple(colour[i]
                            + specular_coefficient[i] * intensity[i]
                            * (max(0, numpy.dot(
                                intersection.surface.normal, h))**p)
                            for i in range(3))

                # Ambient shading
                # TODO: Make these configurable
                ambient = ( 128, 208, 255 )
                ambient_brightness = 0.05

                colour = tuple(
                    colour[i] + (ambient[i] * ambient_brightness)
                    for i in range(3))



            image[(screen_x, screen_y)] = tuple(int(c) for c in colour)


    # Save the rendered image
    _image.save(output_filename)



if __name__ == '__main__':
    from sys import argv
    main(argv)

