#!/usr/bin/env python
from chiplotle.hpgl.commands import PU, PD
from chiplotle.geometry.core.path import Path
from chiplotle.geometry.core.group import Group
from chiplotle.tools.hpgltools.get_all_coordinates import get_all_coordinates
from chiplotle.tools.measuretools.pu_to_in import pu_to_in
from math import sqrt

def pupd_to_paths(hpgl):
    # slurp in PUs and PDs, and convert to a group of simple paths
    # probably fragile, but works fine on the output of pstoedit -f hpgl
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
        
def distance_between(p1, p2):
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
       length += distance_between(p1, p2)
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

    for index in range(len(group) - 1):
        length += distance_between(group[index].points.xy[-1],group[index + 1].points.xy[0])
    
    return length


#    print str(hpgl_file).ljust(30), repr(drawing).rjust(20), repr(seeking).rjust(20), repr(sorting1).rjust(20)

def sort1(group):
    # dumb sort. find closest endpoint to current endpoint, append, rinse, repeat
    sortedgroup = Group()
    original = group[:]
    
    sortedgroup.append(original[0])
    del original[0]
    
    while original:
        p1 = sortedgroup[-1].points.xy[-1]
        bestvalue = 99999999999999999999 # i know this is stupid. ugh.
        bestindex = 0
        reverseflag = False
        
        for index in range(len(original)):
            distance = distance_between(p1, original[index].points.xy[0])
            if distance < bestvalue:
                bestvalue = distance
                bestindex = index
                reverseflag = False
                
            distance = distance_between(p1, original[index].points.xy[-1])
            if distance < bestvalue:
                bestvalue = distance
                bestindex = index
                reverseflag = True
        
        if reverseflag:
            original[bestindex].points.xy.reverse()

        sortedgroup.append(original[bestindex])
        del original[bestindex]

    return sortedgroup

if __name__ == '__main__':
    from chiplotle import *
    import glob
    
    hpgl_files = glob.glob('./hpgl/*.hpgl')
    
    for hpgl_file in hpgl_files:
        group = pupd_to_paths(io.import_hpgl_file(hpgl_file))

        drawing = pu_to_in(length_of_paths(group))
        seeking = pu_to_in(length_of_seeks(group))
        sorting1 = pu_to_in(length_of_seeks(sort1(group)))
        
        tabulate = '{:<30} {:>10.1f} {:>10.1f} {:>10.1f} ({:>5.1%})'
        print tabulate.format(hpgl_file, drawing, seeking, sorting1, sorting1 / seeking)

