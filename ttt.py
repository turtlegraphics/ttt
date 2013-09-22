"""
Tic-tac-toe class for Python
"""
from copy import deepcopy

class Position:
    """Store one position."""
    def __init__(self,moves=[]):
        """Create a new position, optionally making the given list
        of tuples, which are moves."""
        # The only state stored in a position is the actual board.
        # Everything else (who's move it is, position quality, etc.)
        # is calculated every time, on the fly.
        self.board = [' ']*9
        for m in moves:
            self.move(m)

    def __getitem__(self,loc):
        (x,y) = loc
        return self.board[x+3*y]

    def __setitem__(self,loc,val):
        (x,y) = loc
        self.board[x+3*y] = val

    def tomove(self):
        """Return the player whose turn it is."""
        return 'x' if self.board.count(' ') % 2 else 'o'

    def nottomove(self):
        """Return the player whose turn it is not."""
        return 'o' if self.board.count(' ') % 2 else 'x'

    def move(self,loc):
        """The current player moves in (r,c) = loc."""
        (r,c) = loc
        self[r,c] = self.tomove()

    # Position class gameplay routines
    #
    def win(self,who):
        """Return true if player who has won this position."""
        for a in range(3):
            if self[a,0] == who and self[a,1] == who and self[a,2] == who:
                return True
            if self[0,a] == who and self[1,a] == who and self[2,a] == who:
                return True
        if self[0,0] == who and self[1,1] == who and self[2,2] == who:
            return True
        if self[0,2] == who and self[1,1] == who and self[2,0] == who:
            return True

    def drawn(self):
        """Returns true if the board is full and a draw."""
        if ' ' in self.board:
            return False
        else:
            return not(self.win('x') or self.win('o'))

    def wouldwin(self,move,who):
        """Return true if the given move (r,c) by who would win the game."""
        (r,c) = move
        self[r,c] = who
        result = self.win(who)
        self[r,c] = ' '
        return result

    def evaluatemove(self,move):
        """
        Return an evaluation of the move m in this position.
        Returns 'x' or 'o' if 'x' or 'o' can force a win, None if drawn.
        """
        (r,c) = move
        self[r,c] = self.tomove()
        result = self.evaluate()
        self[r,c] = ' '
        return result

    def evaluate(self):
        """
        Return an evaluation of this position with best play by both sides.
        Returns 'x' or 'o' if 'x' or 'o' can force a win, None if drawn.
        """
        possibleMoves = self.moves(strategy='legal')
        if not possibleMoves:
            if self.win('x'):
                return 'x'
            if self.win('o'):
                return 'o'
            return None  # draw

        best = self.nottomove()
        who = self.tomove()
        for m in possibleMoves:
            score = self.evaluatemove(m)
            if score == who:
                return score
            if score == None:
                best = None
        return best

    """A list of strategies implemented in moves() function."""
    strategies = {
           'all' :
               """All empty squares, even if the game is over.""",
           'legal' :
               """Any empty square, unless one player has already won.""",
           'winblock' :
               """Any move which wins, if possible,
                      else any move which blocks, if possible,
                      else legal.""",
           'heuristic' :
               """Any move which wins, if possible,
                      else any move which blocks, if possible,
                      else play in the center, else any corner,
                      else any legal move.""",
           'rational' :
               """All optimal moves, assuming opponent is also rational."""
           }

    def moves(self,strategy='legal'):
        """Return a list of possible moves, given as tuples.
           Only take moves according to given strategy."""
        assert(strategy in Position.strategies)

        if strategy != 'all':
            # check if game is already over
            if self.win('x') or self.win('o'):
                return []

        # find all empty squares
        moves = []
        for row in range(3):
            for col in range(3):
                if self[row,col] == ' ':
                    moves.append((row,col))

        if strategy == 'rational':
            outcomes = [self.evaluatemove(m) for m in moves]
            if self.tomove() in outcomes:            
                # player can win
                best = self.tomove()
            elif None in outcomes:
                # it's a draw
                best = None
            else:
                # player will lose
                best = self.nottomove()
            bestmoves = []
            for i in range(len(moves)):
                if outcomes[i] == best:
                    bestmoves.append(moves[i])
            return bestmoves

        if strategy == 'winblock' or strategy == 'heuristic':
            who = self.tomove()
            wins = [m for m in moves if self.wouldwin(m,who)]
            if wins:
                return wins
            notwho = 'x' if who=='o' else 'o'
            blocks = [m for m in moves if self.wouldwin(m,notwho)]
            if blocks:
                return blocks

        if strategy == 'heuristic':
            if self[1,1]==' ':
                return [(1,1)]
            corners = [m for m in moves if (m[0]+m[1])%2 == 0]
            if corners:
                return corners

        return moves

    # Position class symmetry routines
    #
    def rowflip(self):
        """Swap row 0 and row 2."""
        for c in range(3):
            (self[0,c],self[2,c]) = (self[2,c],self[0,c])

    def diagflip(self):
        """Flip board across the NW-SE diagonal."""
        (self[1,0],self[0,1]) = (self[0,1],self[1,0])
        (self[2,0],self[0,2]) = (self[0,2],self[2,0])
        (self[2,1],self[1,2]) = (self[1,2],self[2,1])

    def standardize(self):
        """Apply symmetry to put self in standardized form."""
        bestboard = self.board[:]
        for i in range(8):
            # Loop through all symmetries by alternating row and diag flips
            if i % 2:
                self.rowflip()
            else:
                self.diagflip()
            if self.board > bestboard:
                bestboard = self.board[:]
        self.board = bestboard

    # Position class output routines
    #
    def __str__(self):
        out = ''
        for row in range(3):
            out += self[row,0] + '|' + self[row,1] + '|' + self[row,2] + '\n'
            if row < 2:
                out += '-+-+-\n'
        return out

    def dotrepr(self):
        """Return a string representing the position as a graphviz record,
        for example: {{x|o| }|{ |x|o}|{ | |x}}"""
        out = '{'
        for row in range(3):
            out += '{' + self[row,0] + '|' + self[row,1] + '|' + self[row,2] + '}'
            if row < 2:
                out += '|'
        out += '}'
        return out

def positionListString(plist):
    """Take a list of positions and produce a multiline string with
    all boards horizontally across the page."""
    # bow to me
    return '\n'.join(map('  '.join,
                         zip(*map(lambda v: v.split('\n'),
                                  map(str,plist)))))

class GameTree:
    """Generate a game tree accounting for symmetry."""
    def __init__(self,levels=0, positions=None, strategy='legal'):
        """Create a tree that starts with the given positions (or the empty
        board, by default), and which has the given number of levels.
        If strategy is a string, it specifies the strategy for both players.
        If it is a dictionary, is specifies an 'x' and 'o' strategy.
        See Position.moves() for strategy options."""
        # The tree is a list of levels, each level with positions
        # links is a list of possible moves from each position at that level,
        # the values of links are lists of integers that index into the
        # next level.  Generally, the vertices list is one longer than
        # the links list, since the last layer of vertices has nothing to link to.
        if positions:
            self.vertices = [list(positions)]
        else:
            self.vertices = [[Position()]]
        self.links = []

        if isinstance(strategy,str):
            self.strategy = {}
            self.strategy['x'] = strategy
            self.strategy['o'] = strategy
        else:
            self.strategy = strategy

        while levels > 0:
            self.addlevel()
            levels -= 1

    def addlevel(self):
        """Add one level of moves to the game tree."""
        found = []
        foundstrs = []
        moves = []
        for pos in self.vertices[-1]:
            children = set()
            for m in pos.moves(strategy=self.strategy[pos.tomove()]):
                newpos = deepcopy(pos)
                newpos.move(m)
                newpos.standardize()
                hash = str(newpos)
                try:
                    child = foundstrs.index(hash)
                except ValueError:
                    child = len(foundstrs)
                    found.append(newpos)
                    foundstrs.append(hash)
                children.add(child)
            moves.append(children)

        self.links.append(moves)
        self.vertices.append(found)

    def sizes(self):
        """Return a list of the nubmer of nodes at each level."""
        return map(len,self.vertices)

    def display(self):
        """Print an ascii text representation of the tree."""
        for level in range(len(self.vertices)):
            print positionListString(self.vertices[level]).rstrip()
            for i in range(len(self.vertices[level])):
                print '%3d   ' % i,
            print
            try:
                for children in self.links[level]:
                    s = ''
                    for i in children:
                        s += str(i) + ' '
                    if len(s) > 7:
                        print s[:4] + '..',
                    else:
                        print s,
                print
            except IndexError:
                pass
            print

    def dotrepr(self):
        """Return a representation of the game tree as a graphviz dot file."""
        out = ''
        out += 'digraph G {\n'
        out += 'graph [ranksep=3, rankdir="LR"];\n'
        out += 'node [shape=record, fontname="monaco",margin=0];\n'
        
        def nodestyle(color):
            return ',color="%s",fontcolor="%s"' % (color,color)

        fontsize = [48,48,24,14,14,14,14,14,24,48]
        for level in range(len(self.vertices)):
            out += '/* Level %d */\n' % level
            for i in range(len(self.vertices[level])):
                v = self.vertices[level][i]
                vdesc = 'V'+ str(i) + 'L' + str(level)
                vdesc += ' [label="%s"' % v.dotrepr()
                vdesc += ',fontsize=%d' % fontsize[level]
                if v.win('x'):
                    vdesc += nodestyle('blue')
                elif v.win('o'):
                    vdesc += nodestyle('red')
                elif v.drawn():
                    vdesc += nodestyle('green')
                vdesc += '];\n'
                out += vdesc

        for level in range(len(self.links)):
            out += '/* Level %d */\n' % level
            for i in range(len(self.vertices[level])):
                for c in self.links[level][i]:
                    ldesc = 'V' + str(i) + 'L' + str(level)
                    ldesc += ' -> '
                    ldesc += 'V' + str(c) + 'L' + str(level + 1)
                    ldesc += ';\n'
                    out += ldesc
        out += '}'
        return out

if __name__=='__main__':
    class Tests:
        def postest():
            """Basic operation of the Position class"""
            b = Position([ (0,0), (1,1), (2,2), (0,2) ])
            print b
            print 'possible moves:'
            print b.moves()
            print 'move (2,0)'
            b[2,0] = 'x'
            print b
            print 'move (1,0)'
            b[1,0] = 'o'
            print b
            print 'move (2,1)'
            b[2,1] = 'x'
            print b
            assert(b.win('x'))
            print 'x has won!'

        def symmetrytest():
            """Position class symmetry operations."""
            b = Position( [(0,0),(1,0),(1,1),(2,2),(0,2)] )
            print 'board'
            print b
            b.rowflip()
            print 'board flipped horizontally'
            print b
            b.diagflip()
            print 'diagonally flip that one (rotation of original)'
            print b
            b.standardize()
            print 'standard symmetry rep of this board'
            print b

        def evaltest():
            """Position class evaluation operations."""
            for b in [
                Position( [(0,0),(1,0),(1,1),(2,2),(0,2)] ),
                Position( [(0,0),(1,0),(1,1),(2,2),(2,0)] ),
                Position( [(1,1),(0,0),(2,0),(0,2),(0,1),(2,1)] ),
                Position( [(1,1),(0,0),(2,0),(0,2),(0,1),(2,1),(2,2)] ),
                Position( [(1,1),(0,1)] ),
                Position( [(0,0),(0,1)] ),
                Position( [(1,1),(0,0)] ),
                Position( [(0,0),(1,1)] ),
                Position( [(1,0)] )
                ]:
                print
                print b,
                print 'is a win for', b.evaluate()

            b = Position( [(0,0)] )
            print
            print 'In this position:'
            print b
            for omove in [ (1,0), (1,1), (2,1), (2,2) ]:
                print 'o moves ',omove,
                print 'is a win for', b.evaluatemove(omove)

        def movestest():
            """Position class move generation."""
            for b in [
                Position( [(1,1)] ),
                Position( [(0,0)] ),
                Position( [(0,0),(1,1),(2,2)] ),
                Position( [(0,0),(1,1),(2,2),(0,2)] ),
                Position( [(0,0),(1,1),(2,2),(0,2),(1,0),(2,0)] ),
                ]:
                print
                print '='*30
                print 'In this position:'
                print b
                for s in Position.strategies:
                    print
                    print '-'*20
                    print "Strategy '%s':" % s
                    print Position.strategies[s]
                    print b.moves(strategy=s)

    from sys import exit
    tests = [t for t in Tests.__dict__ if callable(Tests.__dict__[t])]
    while True:
        i = 0
        for t in tests:
            print i,')',t,':',Tests.__dict__[t].__doc__
            i += 1
        try:
            number = int(raw_input('choose a test:'))
            choice = tests[number]
        except:
            exit()
        print '*'*15,choice,'*'*15
        Tests.__dict__[choice]()
        print '*'*(32+len(choice))
