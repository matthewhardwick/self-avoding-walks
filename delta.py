"""This module contains the transition function and some state lists."""


SINGLE_ENDED = [
    '1000', '1200', '1220',  # T
    '0100', '2100', '0120',  # M
    '0010', '0210', '2210'   # B
    ]

DOUBLE_ENDED = [
    '1010', '1210',  # T, B
    '1100', '1120',  # T, M
    '0110', '2110'   # M, B
    ]

TRIPLE_ENDED = [
    '1111',  # M is connected to B
    '1112'   # T is connected to M
    ]

OTHER_STATES = ['start', 'dead', 'done']

STATE_LIST = SINGLE_ENDED + DOUBLE_ENDED + TRIPLE_ENDED + OTHER_STATES


def delta(current_state, symbol):
    """Given a state and input symbol, find the next state.

    Arguments:
    * current_state is a 4-char string over ['0', '1', '2']; a valid state.
    * symbol is a 5-char string over ['0', '1'].
    """
    if current_state == 'start':
        if symbol == '00000':
            return '0010'  # Single: B
        if symbol == '00010':
            return '0120'  # Single: M
        if symbol == '01000':
            return '1112'  # Triple: T-M
        if symbol == '01010':
            return '1220'  # Single: T
        return 'dead'

    if current_state == 'done':
        if symbol == '00000':
            return 'done'
        else:
            return 'dead'

    if current_state == 'dead':
        return 'dead'

    if symbol == '00000':  # Handle trivial input (from non-'done' state).
        if current_state in SINGLE_ENDED:
            return 'done'
        else:
            return 'dead'

    t = sum(int(symbol[i]) for i in [0, 1])
    m = sum(int(symbol[i]) for i in [1, 2, 3])
    b = sum(int(symbol[i]) for i in [3, 4])
    next_state = ''.join(str(i) for i in [t, m, b])

    if next_state == '111':
        if current_state in TRIPLE_ENDED:  # Triple -> triple.
            next_state += current_state[3]
        elif current_state in SINGLE_ENDED:  # Single -> triple.
            if current_state in ['1000', '1200']:  # Top.
                next_state += '1'
            elif current_state in ['0010', '0210']:  # Bottom.
                next_state += '2'
            else:  # Invalid.
                next_state += '0'
        else:  # Invalid.
            next_state += '0'
    else:  # Not a triple-ended state.
        next_state += '0'

    if ('3' in next_state[0:3] or
        int(current_state[0]) + int(symbol[0]) > 2 or
        int(current_state[1]) + int(symbol[2]) > 2 or
        int(current_state[2]) + int(symbol[4]) > 2):  # Branch.
        #print('branch')
        return 'dead'

    if (symbol[0] == '0' and symbol[2] == '0' and symbol[4] == '0' and
        (symbol[1] == '1' or symbol[3] == '1')):  # Jump: horizontal.
        #print('horizontal jump')
        return 'dead'

    if (current_state in SINGLE_ENDED and
        (current_state[0] == '1' and symbol[0] == '0' or
        current_state[1] == '1' and symbol[2] == '0' or
        current_state[2] == '1' and symbol[4] == '0')):  # Jump: walk end.
        #print('Jump: walk end')
        return 'dead'

    if (current_state in DOUBLE_ENDED and
        (int(current_state[0]) + int(symbol[0]) == 1 or
        int(current_state[1]) + int(symbol[2]) == 1 or
        int(current_state[2]) + int(symbol[4]) == 1)):  # Double -> jump.
        #print('double -> jump')
        return 'dead'

    if (current_state[3] == '1' and symbol[2:5] == '111' or 
        current_state[3] == '2' and symbol[0:3] == '111'):  # Closed loop.
        #print('closed loop')
        return 'dead'

    if current_state in DOUBLE_ENDED and next_state not in STATE_LIST:
        return 'done'

    return next_state
