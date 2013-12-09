"""File: dfa_tb.py
This file contains test code for dfa.
"""


from delta import *
from dfa import makeDFA


def main():
    dfa = makeDFA()
    for i in range(1, 6):
        inputs = [s.rstrip() for s in open('sample_text_inputs/pass{}.in'.format(i)).readlines()]
        #manually_check(inputs)
        print dfa(inputs)
        inputs = [s.rstrip() for s in open('sample_text_inputs/fail{}.in'.format(i)).readlines()]
        print dfa(inputs)


def manually_check(inputs):
    state = 'start'
    print state,
    for input_ in inputs:
        print input_
        state = delta(state, input_)
        print state, 
        

if __name__ == '__main__':
    main()
