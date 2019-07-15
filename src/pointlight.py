#!/usr/bin/python3
#
# See LICENSE file for copyright and license details.
# pointlight.py
#
#   A point light source
#

import numpy



class PointLight:
    """ Point light source. """

    def __init__(self, pos, **kwargs):
        self.pos = numpy.array(pos)

        col = None
        if 'colour' in kwargs:
            col = kwargs['colour']
        elif 'color' in kwargs:
            col = kwargs['color']

        if isinstance(col, str):
            self.colour = tuple(
                [ int(v, 16) for v in col.split() ]
                )
        else:
            if col is not None:
                self.colour = tuple(col)
            else:
                self.colour = ( 255, 255, 255 )

    def __repr__(self):
        return (
              type(self).__name__ + '(' + str(self.pos)
            + ', ' + 'colour=' + str(self.colour) + ')')



def main():
    p = PointLight([ 0,0,0 ])
    print(p)
    p = PointLight([ 0,0,0 ], colour=( 5,5,5 ))
    print(p)
    p = PointLight([ 0,0,0 ], colour='ff ff ff')
    print(p)



if __name__ == '__main__':
    main()

