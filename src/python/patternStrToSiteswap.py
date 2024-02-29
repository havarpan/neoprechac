import re
from string import ascii_lowercase
from math import gcd, ceil
import sys


def shift_left(mystring, myshift):
    newstring = list(mystring)
    i = 0
    while i < len(mystring):
        newstring[i] = mystring[(i + myshift) % len(mystring)]
        i += 1
    return "".join(newstring)


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


def number_to_alphabet(n):
    if not n.isdigit():
        return n
    if int(n) < 10:
        return n
    if int(n) - 10 > 25:
        print('none', end='')
        sys.exit()
    return ascii_lowercase[int(n) - 10]


def patternStrToSiteswap(patternStr, n):
    '''
    patternStr: a list of p(a,b,c) triples as a string

    '''
    n = int(n)
    triples = list(re.findall(r"p\(\d[\.\d]*,\d+,\d+\)", patternStr))
    pattern_length = len(triples)
    if gcd(pattern_length, n) != 1:
        print('none', end='')
        return

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
    print(siteswap, end='')


### main ###

patternStr, numberOfJugglers = sys.argv[1:]

patternStrToSiteswap(patternStr, numberOfJugglers)
