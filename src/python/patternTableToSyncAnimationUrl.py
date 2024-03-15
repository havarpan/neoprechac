'''
Under construction.

This script should create the animation link in the remaining cases:

    gcd(number of jugglers, pattern length) != 1 and (pattern length % number of jugglers) != 0.

Currently does the case n = 4, p = 2 in a hand-to-mouth fashion:

    Premature optimization is the root of all evil!

'''
import sys
from bs4 import BeautifulSoup
from math import gcd
from string import ascii_lowercase, ascii_uppercase
from ast import literal_eval


def number_to_alphabet(n):
    if not str(n).isdigit():
        return n
    if int(n) < 10:
        return n
    if int(n) - 10 > 25:
        print('none', end='')
        sys.stdout.flush()
        sys.exit()
    return ascii_lowercase[int(n) - 10]


def alphabet_to_number(a):
    if str(a).isdigit():
        return int(a)
    return ascii_lowercase.index(a) + 10


def parse_table(html_table):

    table_data = []
    soup = BeautifulSoup(html_table, 'lxml')
    table = soup.find('table')

    for row in table.find_all('tr'):
        cells = row.find_all('td')
        row_data = [' '.join(cell.text.split()) for cell in cells]
        table_data.append(row_data[1:]) # drop "juggler A:" etc

    return table_data



def sync_zero_patch(table_data):

    patched_rows = []

    for j, row in enumerate(table_data):
        patched_row = []

        for i, cell in enumerate(row):
            cell = '0' if not cell else cell

            if 'p' in cell:

                # target_juggler should never be empty
                # (those cases in the other script)
                throw_number, target_juggler = cell.split('p')

                throw_number = number_to_alphabet(int(len(row)*float(throw_number)))
                target_juggler = ascii_uppercase.index(target_juggler) + 1

                cell = f'{throw_number}p{target_juggler}'
            else:
                cell = f'{number_to_alphabet(int(len(row)*float(cell)))}'

            # TODO: generalize 4
            if ((i-j) % 4)  in (0,1):
                patched_cell = (cell,'0')
            else:
                patched_cell = ('0',cell)

            patched_row.append(patched_cell)

        patched_rows.append(patched_row)
    return patched_rows


def add_crosses(patched_rows):

    crossed_rows = []
    for j, row in enumerate(patched_rows):
        crossed_row = []
        for i, cell in enumerate(row):

            crossed_cell = []
            for h, throw in enumerate(cell):
                fixed_throw = throw
                if 'p' not in throw and throw != '0':
                    throw_number = throw
                    if ((alphabet_to_number(throw_number)//len(row)) % 2) != 0:
                        fixed_throw = f'{number_to_alphabet(throw_number)}x'
                elif 'p' in throw:
                    throw_number, target_juggler = throw.split('p')
                    target_beat_phase = (i + int(alphabet_to_number(throw_number))//2) % len(row)
                    target_cell = patched_rows[int(target_juggler)-1][target_beat_phase]

                    # h comes into play
                    if target_cell[h] != '0': # we should not cross
                        if (int(alphabet_to_number(throw_number)) % 2) != 0:
                            fixed_throw = f'{throw_number}xp{target_juggler}'
                        else:
                            pass
                    elif target_cell[1-h] != '0': # we should cross
                        if (int(alphabet_to_number(throw_number)) % 2) == 0:
                            fixed_throw = f'{throw_number}xp{target_juggler}'
                        else:
                            pass
                    else: # this should not happen
                        print('none', end='')
                        sys.stdout.flush()
                        sys.exit()

                else: # throw == '0'
                    pass
                crossed_cell.append(fixed_throw)


            crossed_row.append(tuple(crossed_cell))
        crossed_rows.append(crossed_row)
    return crossed_rows


def halfen(crossed_rows):
    halfened_rows = []
    for row in crossed_rows:
        halfened_row = []
        for cell in row:
            halfened_cell = []
            for throw in cell:
                if 'x' in throw:
                    throw_number, tail = throw.split('x')
                    throw_number = alphabet_to_number(throw_number)
                    half_number = throw_number // 2
                    half_throw = number_to_alphabet(half_number)
                    if len(set([(half_number % 2), (throw_number % 2)])) > 1:
                        halfened_cell.append(f'{half_throw}{tail}')
                    else:
                        halfened_cell.append(f'{half_throw}x{tail}')
                elif 'p' in throw:
                    throw_number, tail = throw.split('p')
                    throw_number = alphabet_to_number(throw_number)
                    half_number = throw_number // 2
                    half_throw = number_to_alphabet(half_number)
                    if len(set([(half_number % 2), (throw_number % 2)])) > 1:
                        halfened_cell.append(f'{half_throw}xp{tail}')
                    else:
                        halfened_cell.append(f'{half_throw}p{tail}')
                else:
                    throw = number_to_alphabet(int(alphabet_to_number(throw))//2)
                    halfened_cell.append(f'{throw}')
            halfened_row.append(tuple(halfened_cell))
        halfened_rows.append(halfened_row)
    return halfened_rows


def strip_zeros(halfened_rows, table_data):
    stripped_rows = []
    for j, row in enumerate(halfened_rows):
        stripped_row = []
        for i, throw in enumerate(row):
            if i == 0 and not table_data[j][i]:
                stripped_row.append('0')
            if table_data[j][i]:
                stripped_row.append(throw)
        stripped_rows.append(stripped_row)
    return stripped_rows

def two_patch_cell(cell):

    # throwing hand index
    h = 1 if cell[0] == '0' else 0

    throw = cell[h]

    new_cell = [None, None]

    if 'x' in throw:
        throw_number, tail = throw.split('x')
        throw_number = alphabet_to_number(throw_number)
        new_throw_number = throw_number - 2
        new_cell[h] = f'{new_throw_number}x{tail}'
        new_cell[1-h] = '2'
    elif 'p' in throw:
        throw_number, tail = throw.split('p')
        throw_number = alphabet_to_number(throw_number)
        new_throw_number = throw_number - 2
        new_cell[h] = f'{new_throw_number}p{tail}'
        new_cell[1-h] = '2'
    else:
        throw_number = alphabet_to_number(throw)
        new_throw_number = throw_number - 2
        new_cell[h] = f'{new_throw_number}'
        new_cell[1-h] = '2'

    return new_cell


def two_patch_rows(stripped_rows):
    patched_rows = []
    for row in stripped_rows:
        patched_row = []
        for cell in row:
            if cell == '0':
                patched_row.append(cell)
                continue
            patched_cell = two_patch_cell(cell)
            patched_row.append(tuple(patched_cell))
        patched_rows.append(patched_row)
    return patched_rows

def sync_jlab(stripped_rows):
    pattern = '<'
    for row in stripped_rows:
        zero_found = False
        for cell in row:
            if cell == '0':
                zero_found = True
                # pattern += '(0,0)!'
                pattern += cell
            else:
                pattern += '(' + ','.join(cell) + ')'
        if zero_found:
            pattern += '!'
        pattern += '|'
    pattern = pattern[:-1] + '>'
    return pattern


def patternStrToSyncAnimationUrl(html_table):

    table_data = parse_table(html_table)

    n = len(table_data) # number of jugglers
    pattern_length = len([i for i in table_data[0] if i])

    # this case was done in the other script
    if gcd(n, pattern_length) == 1 or (pattern_length % n) == 0:
        print('none', end='')
        sys.stdout.flush()
        sys.exit()

    # let's try this first
    elif n == 4 and pattern_length == 2:

        patched_rows = sync_zero_patch(table_data)
        crossed_rows = add_crosses(patched_rows)
        halfened_rows = halfen(crossed_rows)
        stripped_rows = strip_zeros(halfened_rows, table_data)
        two_patched_rows = two_patch_rows(stripped_rows)
        pattern = sync_jlab(two_patched_rows)

        # test
        url = f'https://jugglinglab.org/anim?pattern={pattern}'
        url = f'<p><a href="{url}" target="_blank">JugglingLab animation (sync experiment)</p>'
        print(url, end='')
        sys.stdout.flush()

    else:
        print('none', end='')
        sys.stdout.flush()
        sys.exit()


### main ###

html_table = sys.stdin.read()
patternStrToSyncAnimationUrl(html_table)
