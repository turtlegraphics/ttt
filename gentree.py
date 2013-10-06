"""
This program generates interesting graphviz game trees for Tic-Tac-Toe.
Probably you want to use it in a pipeline:
python gentree.py heuristic | dot -Tpdf -o heuristic.pdf
"""

import sys
import ttt

class Trees:
    def rational():
        """Tree of all rational moves, up to symmetry.  This is all possible
           well-played games of Tic-Tac-Toe will go."""
        return ttt.GameTree(levels=9,strategy='rational')
    def legal():
        """Tree of all legal moves, up to symmetry.  This is all possible
           games Tic-Tac-Toe will go."""
        return ttt.GameTree(levels=9,strategy='legal')
    def heuristic():
        """Both players using the heuristic strategy (win, block, center,
        corner).  Most games go like this."""
        return ttt.GameTree(levels=9,strategy='heuristic')
    def beatChildren():
        """X plays rational, O plays the heuristic strategy."""
        return ttt.GameTree(levels=9,strategy={'x':'rational','o':'heuristic'})
    def canHeuristicLose():
        """X plays heuristic.  Is it possible to lose?"""
        return ttt.GameTree(levels=9,strategy={'x':'heuristic','o':'legal'})
    def centerThenWinblock():
        """X plays in the center, then just plays winblock strategy."""
        return ttt.GameTree(levels=8,strategy={'x':'winblock','o':'rational'},
                            positions = [ttt.Position( [(1,1)] )])
        
mytrees = [t for t in dir(Trees) if callable(Trees.__dict__[t])]

def usage():
    outstr = __doc__ + '\n'
    outstr += 'Select one of the following trees as a command line option'
    for t in mytrees:
        outstr += '\n* ' + t + '\n ' + Trees.__dict__[t].__doc__
    print >> sys.stderr, outstr
    sys.exit(1)

if len(sys.argv) != 2:
    usage()
t = sys.argv[1]
if t not in mytrees:
    usage()

thetree = Trees.__dict__[t]()
print thetree.dotrepr()
print >> sys.stderr, t,':',Trees.__dict__[t].__doc__
print >> sys.stderr, thetree.stats()
