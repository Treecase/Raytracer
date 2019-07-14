#!/usr/bin/python3
#
# See LICENSE file for copyright and license details.
# parser.py
#
#   Raytracer file parser
#

from quad import Quad



def parse(f):
    """ Parse a raytracer world file. """

    # Strip comment and blank lines
    data_lines = []
    for line in f.read().splitlines():
        line = line.strip()
        if len(line) != 0:
            if not line.startswith('#'):
                data_lines.append(line)

    quad_defs = []
    current_def = []

    # Split the data into separate quad definitions
    for line in data_lines:
        if line != ';':
            current_def.append(line)
        else:
            quad_defs.append(current_def)
            current_def = []

    # Build the quad list
    quads = []
    for quad_def in quad_defs:

        points = []
        colour = ( 255, 255, 255 )

        # First 3 lines of the def are the 3D points defining the quad
        for point in quad_def[0:3]:
            p = point.split()
            points.append([ float(v) for v in p ])

        # Optional 4th line is the quad's colour
        try:
            colour = ( int(v, 16) for v in quad_def[3].split() )
        except IndexError:
            colour = ( 255, 255, 255 )

        quads.append(Quad(points, colour))

    return tuple(quads)



def main(_argv=None):

    input_filename = 'world.txt'
    if (_argv is not None
            and len(_argv) > 1):
        input_filename = _argv[1]

    with open(input_filename, 'r') as f:
        quads = parse(f)

        for quad in quads:
            print(quad.points)
            print(quad.colour)



if __name__ == '__main__':
    from sys import argv
    main(argv)

