#!/usr/bin/env python
from chiplotle.hpgl.commands import PU, PD
from chiplotle.geometry.core.path import Path
from chiplotle.geometry.core.group import Group
from chiplotle.tools.hpgltools.get_all_coordinates import get_all_coordinates
from chiplotle.tools.measuretools.pu_to_in import pu_to_in
from math import sqrt

def pupd_to_paths(hpgl):
    # slurp in PUs and PDs, and convert to a group of simple paths
    # probably fragile, but works on the output of pstoedit -f hpgl
    results = Group()
    builder = []
    
    for command in hpgl:
        if isinstance(command, PU):
            if builder:
                # must be starting a new path, so stash the last
                coords = get_all_coordinates(builder)
                results.append(Path(coords))
                builder = []
            builder.append(command)
        elif isinstance(command, PD):
            builder.append(command)
            
    return results
        
def distance_between_coordinates(p1, p2):
    # take two coordinate objects, return the distance
    # between them in plotter units
    a = abs(p1.x - p2.x)
    b = abs(p1.y - p2.y)

    return sqrt(a**2 + b**2)

def length_of_path(path):
    # take a path object, return its length in plotter units
    length = 0
    coords = path.points.xy[:]
    
    p1 = coords.pop()
    while coords:
       p2 = coords.pop()
       length += distance_between_coordinates(p1, p2)
       p1 = p2
    
    return length

def length_of_paths(group):
    # take a group of paths, return the total path length
    length = 0
    
    for path in group:
        length += length_of_path(path)
    
    return length

def length_of_seeks(group):
    # take an ordered group of paths, return the total
    # length of seeks between paths
    length = 0
    
    count = 1
    while count < len(group):
        length += distance_between_coordinates(group[count - 1].points.xy[-1],group[count].points.xy[0])
        count += 1
    
    return length

def efficiency_report(group):
    print length_of_paths(group)
    print length_of_seeks(group)

def dumb_sort(group):
    zoot = 'zoink'
    #test.points.xy.reverse()

if __name__ == '__main__':
    from chiplotle import *
    import glob
    
    hpgl_files = glob.glob('./hpgl/*.hpgl')
    
    for hpgl_file in hpgl_files:
        efficiency_report(pupd_to_paths(io.import_hpgl_file(hpgl_file)))

