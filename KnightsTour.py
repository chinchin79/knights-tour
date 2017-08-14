import sys
import collections
from Memoization import Memoized


class KnightTour:

    def __init__(self, key_len, key_pad, vowels_allowed=0):
        self.key_len = key_len
        self.key_pad = key_pad
        self.vowels_allowed = vowels_allowed
        self._sequences = {k: [k] for k in key_pad.iterkeys()}
        self._moves = self.all_moves
        self._paths = self.all_paths

    def run(self):
        num_done = 0
        if self.key_len == 1:
            if self.vowels_allowed >= 1:
                num_done = len(self._paths)
            elif self.vowels_allowed == 0:
                num_done = len([k for k, v in self._paths.iteritems() if k not in 'aeiou'])
        else:
            for k, v in self.key_pad.items():
                for n in range(0, self.key_len):
                    num = self.sequence_engine(k)
                    num_done += num

        print "Possible knight moves are %s with %s vowel(s) allowed per move" % (str(num_done), self.vowels_allowed)

    #@profile
    def sequence_engine(self, k):
        replace = []
        num_done = 0

        for i in range(0, len(self._sequences[k])):

            next_k = self.link_sequences(self._sequences[k][i][-1:])
            seqs = [self._sequences[k][i] + l for l in next_k]

            for seq in seqs:
                # Need to make sure we don't have a sequence with 2 or more vowels
                if len([letter for letter in seq if letter in 'aeiou']) > self.vowels_allowed:
                    seqs.remove(seq)

            if len(seqs[0]) == self.key_len:
                # LISANDRO TO DO:  sanity check, this should be done using pytest
                if len([letter for letter in seq if letter in 'aeiou']) <= self.vowels_allowed:
                    mul = self.sequence_adder(seqs)
                    num_done += mul

            if len(seqs[0]) < self.key_len:
                replace.extend(seqs)

        self._sequences[k] = replace
        return num_done

    def link_sequences(self, link):
        """
        Find all possible links to letter provided.
        Using @memoized decorator to save evaluation efforts on repeat calls

        :param link: str
        :param omit: str
        :return: list generator

        """
        return [l for l in self._moves.get(link)]

    def key(self, value):
        return [k for k, v in self.key_pad.iteritems() if v == value]

    @property
    def all_paths(self):
        """

        This property returns all possible path combinations for each keypad position key.
        For example, knight sitting on keypad position 'a' can move to
        keypad position 'l' through path 'afkl' or path 'abgl'

        :return: <type collections.OrderedDict>

        """

        steps = [[right, right, down], [right, right, up], [right, up, up], [right, down, down],
                 [left, left, down], [left, left, up], [left, up, up], [left, down, down], [up, up, left],
                 [up, up, right], [up, left, left], [up, right, right], [down, down, left], [down, down, right],
                 [down, left, left], [down, right, right]]

        paths = collections.OrderedDict()

        for k, v in self.key_pad.items():
            kp = []
            for moves in steps:
                s = [k]
                dx, dy = v[0], v[1]
                for m in moves:
                    dx, dy = m(dx, dy)
                    try:
                        s.append(self.key((dx, dy)).pop())
                        if len(s) == 4:
                            kp.append(''.join(s for s in s))
                            continue
                    except IndexError:  # This means we are out of bounds on the key_pad
                        pass
            paths[k] = kp

        return paths

    @property
    def all_moves(self):
        """

        This property returns all the allowed destinations 'moves' (coordinates)
        based on the key_pad variable.

        :return: <type collections.OrderedDict>

        """
        moves = collections.OrderedDict()

        for k, v in self.key_pad.iteritems():
            j, i = v[0], v[1]

            positions = validate_position(j, i)

            moves[k] = [self.key(t).pop() for t in positions]

        return moves

    #@profile
    def sequence_adder(self, seqs):
        """

        This method receives a list of sequences that differ only in the last character.

        I add the possible paths for the FIRST sequence. For example, key 'a' knight move to key 'h'
        can be done in two ways (eg: ('abch') + ('afgh') = 2 moves))

        For all remaining sequences on the list, I only add the final path char combination.

        The input is a list of sequences based on the key_len, for example here are the
        possible sequences for key_len=10 starting at key_pad='a':

            seqs = ['ahen1h3j3j', 'ahen1h3j3l', 'ahen1h3j3h']

        The returned object is the count of moves for the sequence


        :param seqs: <type 'list'>
        :return:
        :rtype: <type 'int'>
        """

        def adder_generator(o, r=0): #not implemented yet
            return (1 for x in self._paths[seqs[r][o]] if x[3] == seqs[r][o + 1])

        adder = 0

        for o in range(0, self.key_len - 1):
            for x in self._paths[seqs[0][o]]:
                if x[3] == seqs[0][o + 1]:
                    adder += 1

        for r in range(1, len(seqs)):
            for x in self._paths[seqs[r][o]]:
                if x[3] == seqs[r][o + 1]:
                    adder += 1

        return adder


def validate_position(j, i, omit=[]):
    """
        This allows me to validate the knight's landing coordinates.
        but since it did not cover all possible paths,
        I created the all_paths functions as complement.

        :param j: <type int>
        :param i: <type int>
        :param omit: <type list>
        :return: <type list> (returns a list of tuple objects)
    """
    move_combinations = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]

    return filter(lambda x: True if 1 <= x[0] < 6 and 1 <= x[1] < 6 and x != (4, 1) and x != (4, 5) and
                  x[0] != 5 and x not in omit else False,
                  map(lambda x: tuple(map(sum, zip((j, i), x))), move_combinations))


@Memoized
def left(j, i): return j - 1, i


@Memoized
def right(j, i): return j + 1, i


@Memoized
def up(j, i): return j, i - 1


@Memoized
def down(j, i): return j, i + 1


def main():
    key_pad = collections.OrderedDict([('a', (1, 1)), ('b', (1, 2)), ('c', (1, 3)), ('d', (1, 4)), ('e', (1, 5)),
                                      ('f', (2, 1)), ('g', (2, 2)), ('h', (2, 3)), ('i', (2, 4)), ('j', (2, 5)),
                                      ('k', (3, 1)), ('l', (3, 2)), ('m', (3, 3)), ('n', (3, 4)), ('o', (3, 5)),
                                      ('1', (4, 2)), ('2', (4, 3)), ('3', (4, 4))])

    key_len = int(sys.argv[1])
    assert key_len >= 1, 'Sequence key length needs to be greater than or equal to 1'

    vowels_allowed = int(sys.argv[2])

    KnightTour(key_len, key_pad, vowels_allowed).run()
    print('Done.')


if __name__ == "__main__":
    main()

