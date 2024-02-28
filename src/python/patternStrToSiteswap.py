import re
from string import ascii_lowercase
from math import gcd
from fractions import Fraction
import sys


def shift_left(mystring, myshift):
    newstring = list(mystring)
    i = 0
    while i < len(mystring):
        newstring[i] = mystring[(i + myshift) % len(mystring)]
        i += 1
    return "".join(newstring)


def replace_zeros(strings: list):
    result = ""
    common_length = len(strings[0])
    for i in range(common_length):
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
    n = int(n)
    result = ""
    triples = list(re.findall(r"p\(\d[\.\d]*,\d+,\d+\)", patternStr))
    pattern_length = len(triples)
    if gcd(pattern_length, n) != 1:
        print('none', end='')
        return
    for triple in triples:
        first_number = triple.split(",")[0].split("(")[-1]
        first_number = Fraction(float(first_number)).limit_denominator(1000)
        first_number = number_to_alphabet(str(round(n * float(first_number))))
        result += first_number + (n - 1) * "0"
    shifted_results = []
    for _ in range(n):
        shifted_result = shift_left(result, int(len(result) / n))
        shifted_results.append(shifted_result)
        result = shifted_result
    siteswap = ''.join(replace_zeros(shifted_results)[:pattern_length])
    print(siteswap, end='')



patternStr = sys.argv[1]
n = sys.argv[2]

patternStrToSiteswap(patternStr, n)
