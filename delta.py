"""This module contains the transition function and some state lists."""

"""
Valid State Definitions:
    Single Ended - Where one possible valid connection point exists in a given state.
    Double Ended - Where two possible valid connection points exist in a given state.
    Triple Ended - Where three possible valid connection points exist in a given state.

    [T]op connection possible
    [M]iddle connection possible
    [B]ottom connection possible
    
    Valid char set ['0', '1', '2'], where that number signifies the current degree of 
     
"""
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
        The initial 3 symbols indicate the degree for possible connecting vertices.
        The fourth symbol indicates the position for a triple ended connection vertical bar
        where 1 indicates a M-B connection, and 2 indicates a T-M connection. 
    * symbol is a 5-char string over ['0', '1'].
        Each position of the string represents if an edge connects two vertices. 0 represents
        a no connection, and 1 represents a connection.

    Expected Output:
        If a valid transition to a state exists, then the 4-char string representing that 
            state will be returned, 'done' represents if that state transitions to an accepting
            state. If the transition is no valid, then the state of 'dead' is returned, and the
            entire input is not valid, and the input is rejected.
    """

    # Handle valid transitions from the start state, or reject into the dead state
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


    # When already in the 'done' state, stay in that state if the symbol is trivial, or empty, 
    # otherwise, reject and transition to the 'dead' state.
    if current_state == 'done':
        if symbol == '00000':
            return 'done'
        else:
            return 'dead'

    # When the current state is dead, or rejected, there is no possible way to recover, but
    # it is possible to self loop on a dead state transition. 
    if current_state == 'dead':
        return 'dead'

    # Handle the initial trivial input, meaning if our symbol has no connections
    # and our current state is that we are in a single ended connection then we
    # have a valid ending, and we can return 'done'. If we are in any other state
    # then it is an invalid transition, and we must transition to the dead state. 
    if symbol == '00000': 
        if current_state in SINGLE_ENDED:
            return 'done'
        else:
            return 'dead'

    # Generate the next state by calculating the degree of connection for each
    # vertex with a connection point based on the current input symbol. 
    t = sum(int(symbol[i]) for i in [0, 1])
    m = sum(int(symbol[i]) for i in [1, 2, 3])
    b = sum(int(symbol[i]) for i in [3, 4])
    next_state = ''.join(str(i) for i in [t, m, b]) # Helper next state string for 
                                                    # comparison.

    # Handle triple ended connection, and set the closure position if necessary.
    # Triples in general can only either connect to another triple, 
    # or a single ended state, and will be rejected otherwise. 
    if next_state == '111':
        if current_state in TRIPLE_ENDED:  # Triple -> triple.
            next_state += current_state[3]
        elif current_state in SINGLE_ENDED:  # Single -> triple.
            if current_state in ['1000', '1200', '1220']:  # Top sided closure.
                next_state += '1'
            elif current_state in ['0010', '0210', '2210']:  # Bottom sided closure.
                next_state += '2'
            else:  # Invalid.
                next_state += '0'
        else:  # Invalid.
            next_state += '0'
    else:  # Not a triple-ended state.
        next_state += '0'

    # Handle Branch condition. If a vertex has a degree of 3 or higher, then that means
    # it is being connected to by more than two edges, and is therefore rejected. 
    if ('3' in next_state[0:3] or
        int(current_state[0]) + int(symbol[0]) > 2 or
        int(current_state[1]) + int(symbol[2]) > 2 or
        int(current_state[2]) + int(symbol[4]) > 2):
        return 'dead'

    # Handles the Horizontal Jump Condition, where a gap of a horizontal
    # nature is created, and is therefore rejected.
    if (symbol[0] == '0' and symbol[2] == '0' and symbol[4] == '0' and
        (symbol[1] == '1' or symbol[3] == '1')):
        return 'dead'

    # Handles the vertical jump condition in a single ended state, where
    # a gap is created in a way such that a vertical gap is created between
    # two vertices where only one connection is possible, and is therefore rejected.
    if (current_state in SINGLE_ENDED and
        (current_state[0] == '1' and symbol[0] == '0' or
        current_state[1] == '1' and symbol[2] == '0' or
        current_state[2] == '1' and symbol[4] == '0')):  # Jump: walk end.
        return 'dead'

    # Handles the vertical jump condition in a double ended state, where
    # a gap is created in such a way that a vertical gap is created between
    # two vertices where two possible vertices have a connection point, and
    # is therefore rejected.
    if (current_state in DOUBLE_ENDED and
        (int(current_state[0]) + int(symbol[0]) == 1 or
        int(current_state[1]) + int(symbol[2]) == 1 or
        int(current_state[2]) + int(symbol[4]) == 1)):
        return 'dead'

    if (current_state in TRIPLE_ENDED and  # If the 'main' walk ends.
        (current_state[3] == '1' and 
        int(current_state[0]) + int(symbol[0]) == 1 or
        current_state[3] == '2' and
        int(current_state[2]) + int(symbol[4]) == 1)):
        return 'dead'

    if (current_state[3] == '1' and symbol[2:5] == '111' or 
        current_state[3] == '2' and symbol[0:3] == '111'):  # Closed loop.
        return 'dead'

    if next_state not in STATE_LIST:
        return 'done'

    return next_state
