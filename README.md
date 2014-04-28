The Last Piece Puzzle solver
============================

This repository contains some code I made to solve an interesting little jigsaw called "The Last Piece Puzzle" by Dugald Keith.  The puzzle doesn't seem to have any obvious strategies beyond perseverance.  Any incorrect solution is simply wrong, and you are given no clues on how to improve and get closer to the answer.  The problem itself is simple enough.  You are given a board, and 14 pieces.  The initial configuration has a gap, into which the last piece will not fit because of a shape irregularity.  Closer inspection of the bottom right of the board reveals a corresponding irregularity.  The challenge is to remove the pieces and reassemble the puzzle with the last piece included.

Images of the empty board and pieces are included in this repository, as well as the initial piece placements and the 5 solutions my algorithm can find.

Solving the puzzle
==================

A pure brute force approach to this problem is possible - but incredibly slow and not particularly interesting from an implementation perspective. Instead, I decided to solve the puzzle using a simple, methodic approach: start at the bottom right and attempt to fill the puzzle one piece at a time without leaving any gaps.

This is done by first defining a strict order for the cells on the board. The gives a very nice metric for completeness in that the board is considered to have no-gaps up to a certan point if that cell (and every cell with a higher priority) is filled.  I was tempted to try and define a heuristic for board completeness that took actual gaps into account - but the cost of calculating that seemed like it would be too high to be worthwhile.

This still proved quite costly, given that every piece had to be considered as a candidate for filling each square.  This search is optimised by pre-calculating all the possible positions for every piece and storing them in a lookup.  Each cell on the board is assigned a candidate placement list, which contains a reference to a piece (and its corresponding orientation and position) only if that placement would result in that cell being filled.

At every stage of the algorithm, the next empty cell is located an each candidate placement for that cell is tested.  A recursive call is made for each valid placement, until the list of available pieces is exhaustsed and the puzzle is solved.
