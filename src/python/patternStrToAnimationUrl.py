import re
from string import ascii_lowercase
from math import gcd, ceil
from ast import literal_eval
import sys


# helper for passist link
def shift_left(mypattern, myshift):
    newpattern = list(mypattern)
    i = 0
    while i < len(mypattern):
        newpattern[i] = mypattern[(i + myshift) % len(mypattern)]
        i += 1
    return "".join(newpattern)

# helper for passist link
def replace_zeros(strings: list, pattern_length: int):
    result = ""
    for i in range(pattern_length):
        replace_zero = "0"
        for string in strings:
            if string[i] != "0":
                replace_zero = string[i]
                break
        result += replace_zero
    return result

# helper for passist link
def number_to_alphabet(n):
    if not n.isdigit():
        return n
    if int(n) < 10:
        return n
    if int(n) - 10 > 25:
        print('none', end='')
        sys.exit()
    return ascii_lowercase[int(n) - 10]


def passist_link(triples, n):

    pattern_length = len(triples)

    one_juggler_siteswap = "" # to be filled below

    for triple in triples:

        # take the first number (the throw value) of each triple
        first_number = triple.split(",")[0].split("(")[-1]

        # try to cope with the prechacthis rounding convention
        if abs(float(first_number)*n - int(float(first_number)*n)) < 10**(-5):
            myfun = round
        else:
            myfun = ceil
        first_number = float(myfun(float(first_number)*n)/n)

        # numbers > 10 become letters
        first_number = number_to_alphabet(str(round(n * float(first_number))))

        one_juggler_siteswap += first_number + (n - 1) * "0"

    shifted_one_juggler_siteswaps = [] # to be filled below

    for _ in range(n):

        shifted_one_juggler_siteswap = shift_left(one_juggler_siteswap, pattern_length)
        shifted_one_juggler_siteswaps.append(shifted_one_juggler_siteswap)
        one_juggler_siteswap = shifted_one_juggler_siteswap

    # merge shifted one-juggler siteswaps and output the result
    siteswap = ''.join(replace_zeros(shifted_one_juggler_siteswaps, pattern_length))

    url = f'https://passist.org/siteswap/{siteswap}?jugglers={n}'
    return url


# helper for jugglinglab_link
def build_jlab_pattern(throws, pass_flags, n):

    # one-person siteswap, 'p' included
    throws_with_ps = []
    for i in range(len(throws)):
        throw_number = throws[i]
        pass_flag = pass_flags[i]
        throw_with_p = f'{throw_number}p' if pass_flag else f'{throw_number}'
        throws_with_ps.append(throw_with_p)

    # pattern_length / n is integer
    # shift by that n times

    # shifted one-person siteswaps
    pattern = throws_with_ps
    shifted_patterns = [pattern]
    for i in range(1,n):
        i *= len(pattern)//n
        shifted_pattern = []
        for j in range(len(pattern)):
            shifted_pattern.append(
                pattern[(j - i) % len(pattern)]
            )
        shifted_patterns.append(shifted_pattern)

    # https://stackoverflow.com/questions/6473679/transpose-list-of-lists
    transposed_patterns = list(map(list, zip(*shifted_patterns)))

    pattern = ''.join(
        '<' + '|'.join(p) + '>' for p in transposed_patterns
    )

    return pattern

def jugglinglab_link(triples, n):

    # strip each triple of the initial 'p' and convert to a tuple of int tuples
    triples = tuple(
        literal_eval(''.join(list(t)[1:])) for t in triples
    )

    # test if we have alphabet throws (disabled)
    if max(max(t) for t in triples) > 9:
        print('none', end='')
        sys.exit()

    throws = tuple(t[0] for t in triples)
    pass_flags = tuple(t[1] for t in triples)

    pattern = build_jlab_pattern(throws, pass_flags, n)

    url = f'https://jugglinglab.org/anim?pattern={pattern}'
    return url


def patternStrToAnimationUrl(patternStr, n):
    '''
    patternStr: a list of p(a,b,c) triples as a string

    '''
    n = int(n)
    triples = list(re.findall(r"p\(\d[\.\d]*,\d+,\d+\)", patternStr))
    pattern_length = len(triples)

    # do we know how to create the animation link
    # todo: remaining cases
    animation_type = 'passist'
    if gcd(pattern_length, n) != 1:
        if (pattern_length % n) == 0:
            animation_type='jugglinglab'
        else:
            print('none', end='')
            return

    if animation_type == 'passist':
        url = passist_link(triples, n)
    else:
        # todo: fix hand specs
        url = jugglinglab_link(triples, n)

    print(url, end='')


### main ###

patternStr, numberOfJugglers = sys.argv[1:]

patternStrToAnimationUrl(patternStr, numberOfJugglers)
