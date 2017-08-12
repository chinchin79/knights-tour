import sys
import collections
from Memoization import Memoized


def key(value):
    return [k for k, v in board.iteritems() if v == value]


def validate_position(j, i, omit=[]):
    """
    type: (object, object, object) -> object

    NOTE:
        this allows me to quickly validate the knight's landing coordinates.
        but since it did not cover all possible paths,
        I created the all_paths functions as complement
        :param j: int
        :param i: int
        :param omit: list
        :return: list of tuples
    """
    move_combinations = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]

    return filter(lambda x: True if 1 <= x[0] < 6 and 1 <= x[1] < 6 and x != (4, 1) and x != (4, 5) and
                                    x[0] != 5 and x not in omit else False,
                  map(lambda x: tuple(map(sum, zip((j, i), x))),
                      move_combinations))


@Memoized
def left(j, i):
    return j - 1, i


@Memoized
def right(j, i):
    return j + 1, i


@Memoized
def up(j, i):
    return j, i - 1


@Memoized
def down(j, i):
    return j, i + 1


def all_paths():
    """
    This function creates all possible path combinations for each board position key.
    For example, knight sitting on board position 'a' can move to board position 'l' through path 'afkl' or path 'abgl'
    """
    steps = [[right, right, down], [right, right, up], [right, up, up], [right, down, down],
             [left, left, down], [left, left, up], [left, up, up], [left, down, down], [up, up, left],
             [up, up, right], [up, left, left], [up, right, right], [down, down, left], [down, down, right],
             [down, left, left], [down, right, right]]

    paths = collections.OrderedDict()

    for k, v in board.items():
        kp = []
        for moves in steps:
            s = [k]
            dx, dy = v[0], v[1]
            for m in moves:
                dx, dy = m(dx, dy)
                try:
                    s.append(key((dx, dy)).pop())
                    if len(s) == 4:
                        kp.append(''.join(s for s in s))
                        continue
                except IndexError:  # LISANDRO TO DO:  I need to skip over any error for now, but will find a better way
                    pass
        paths[k] = kp

    return paths


def all_moves():
    """this are all the allowed destinations coordinates"""
    moves = collections.OrderedDict()

    for k, v in board.iteritems():
        j, i = v[0], v[1]

        positions = validate_position(j, i)

        moves[k] = [key(t).pop() for t in positions]

    return moves


@Memoized
def link_sequences(link, omit=''):
    """
    Find all possible links to letter provided.
    Using @memoized decorator to save evaluation efforts on repeat calls

    :param link: str
    :param omit: str
    :return: list generator

    """
    return [l for l in all_moves.get(link) if l not in omit]


def sequence_engine(k, keySeqLen):
    # LISANDRO -- I should do this with a dictionary instead, it will likely increase the processing speed
    replace = []
    num_done = 0

    for i in range(0, len(sequences[k])):

        next_k = link_sequences(sequences[k][i][-1:])
        seqs = [sequences[k][i] + l for l in next_k]

        for seq in seqs:
            # Need to make sure we don't have a sequence with 2 or more vowels
            if len([letter for letter in seq if letter in 'aeiou']) > 2:
                seqs.remove(seq)
            else:
                continue

        if len(seqs[0]) == keySeqLen:
            # LISANDRO TO DO:  sanity check, this should be done using pytest
            if len([letter for letter in seq if letter in 'aeiou']) <= 2:
                mul = sequence_adder(seqs)
                num_done += mul

        if len(seqs[0]) < keySeqLen:
            replace.extend(seqs)

    sequences[k] = replace
    return num_done


def sequence_adder(seqs):
    """
    This was a late addition, here I get a list of sequences that differ only in the last character.
    I add the possible paths for the FIRST sequence (for example, ('a'->'h'=2) + ('h'->'a')=2))
    For all remaining sequences on the list, I only add the final path char combination
    :rtype: object
    """
    adder = 0

    for o in range(0, keyLen - 1):
        for x in all_paths[seqs[0][o]]:
            if x[3] == seqs[0][o + 1]:
                adder += 1

    for r in range(1, len(seqs)):
        for x in all_paths[seqs[r][o]]:
            if x[3] == seqs[r][o + 1]:
                adder += 1

    return adder


def knight_tours():
    num_done = 0
    for k, v in board.items():
        for n in range(1, keyLen):
            num = sequence_engine(k, keyLen)
            num_done += num
    print "Possible moves are: %s" % str(num_done)


if __name__ == "__main__":
    board = collections.OrderedDict([('a', (1, 1)), ('b', (1, 2)), ('c', (1, 3)), ('d', (1, 4)), ('e', (1, 5)),
                         ('f', (2, 1)), ('g', (2, 2)), ('h', (2, 3)), ('i', (2, 4)), ('j', (2, 5)),
                         ('k', (3, 1)), ('l', (3, 2)), ('m', (3, 3)), ('n', (3, 4)), ('o', (3, 5)),
                         ('1', (4, 2)), ('2', (4, 3)), ('3', (4, 4))])

    keyLen = int(sys.argv[1])

    sequences = {k: [k] for k in board.iterkeys()}

    all_moves = all_moves()

    all_paths = all_paths()

    knight_tours()
    print('Done.')
