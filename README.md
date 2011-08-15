# Ronald Tools

These are some tools I'm noodling with to make my plotting with
[Chiplotle](http://music.columbia.edu/cmc/chiplotle/) tastier and more efficient.
Currently, I'm focused on optimizing the drawing path to minimize seek times.

I'm learning python as I go, so do be gentle, but feel free to tell me all
about how stupid I am.

## pupd\_to\_paths(hpgl) 

Slurp in PUs and PDs, and converts them to a chiplotle group of simple paths. This
is probably very fragile, but its works on the simple output of pstoedit -f hpgl.
        
## distance\_between\_coordinates(p1, p2)

Doi. Pass it two coordinate objects, recieve the distance between them in plotter units.

## length\_of\_path(path)

Takes a path object, returns its ful length in plotter units.

## length\_of\_paths(group)

Takes a chiplotle group of paths, returns the total length the pen was down.
 
## length\_of\_seeks(group)

Takes a chiplotle group of paths, return the total length of seeks between paths.

## efficiency_report(group):

_In progress_. Reports on drawing vs. seeking, possibly with comparisons between sorting routines.

