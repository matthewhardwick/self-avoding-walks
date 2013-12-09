"""File: dfa.py

Usage: python dfa.py

Represent the automaton using the mechanisms available in David Eppstein's
python library for automata processing: PADS.Automata
"""


from PADS import Automata
from delta import *


def makeDFA():
    """Return the DFA."""
    dfa = Automata.DFA()
    dfa.alphabet = {bin(i)[2:].zfill(5) for i in range(32)}
    dfa.initial = 'start'
    dfa.transition = lambda st, a: delta(st, a)
    dfa.isfinal = lambda st: st in SINGLE_ENDED + ['done', 'start']
    return dfa


if __name__ == '__main__':
    makeDFA().pprint()
