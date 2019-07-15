#!/usr/bin/python3
#
# See LICENSE file for copyright and license details.
# parser.py
#
#   Raytracer file parser
#

import re

from quad import Quad
from pointlight import PointLight



def parse(f):
    """ Parse a raytracer world file. """

    UNNAMED_ATTRS = {
        'Quad': 3,
        'PointLight': 1
        }

    data = f.read()

    # parse the object definitions
    definitions = re.finditer(
        '^([A-Za-z]+)\n{\n((?:.*\n)*?)}', data, re.MULTILINE)


    object_defs = []

    for match in definitions:
        _type = match.group(1).strip()
        body = match.group(2)


        # parse the unnamed attributes
        unnamed_count = UNNAMED_ATTRS[_type]
        raw_unnamed = body.splitlines()[:unnamed_count]

        unnamed = [
            [ float(v) for v in attr.strip().split() ]
            for attr in raw_unnamed ]


        # parse named attributes
        attributes = dict()

        tmp2 = re.finditer('(.*?):(.*?)\n', body)
        for m in tmp2:
            name = m.group(1).strip()
            value = m.group(2).strip()

            attributes[name] = value


        object_defs.append([ _type,
            unnamed,
            attributes ])


    # build objects from the parsed data
    output = []

    for objdef in object_defs:
        constructor = eval(objdef[0])
        output.append(
            constructor(*objdef[1], **objdef[2]))

    return output



def main(_argv=None):

    input_filename = 'world.txt'
    if (_argv is not None
            and len(_argv) > 1):
        input_filename = _argv[1]

    with open(input_filename, 'r') as f:
        objects = parse(f)

        for _object in objects:
            print(str(_object))



if __name__ == '__main__':
    from sys import argv
    main(argv)

