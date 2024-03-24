'''
Under construction.

This script should create the animation link in the remaining cases:

    gcd(number of jugglers, pattern length) != 1 and (pattern length % number of jugglers) != 0.

Currently may do most cases with four jugglers.


'''
import sys
from bs4 import BeautifulSoup
from math import gcd, ceil
from string import ascii_lowercase, ascii_uppercase
# from ast import literal_eval
from copy import deepcopy
import os
from collections import Counter


# global
patch_factor = None

# rudimentary logging facility
cwd = os.path.abspath(os.path.dirname(__file__))
def mylog(mystr):
    with open(f'{cwd}/log.txt', 'a') as handle:
        handle.write(f'{mystr}\n\n')


def number_to_alphabet(n):
    if not str(n).isdigit():
        return n
    if int(n) < 10:
        return n
    if int(n) - 10 > 25:
        # print('none', end='')
        print(f'<p>No JugglingLab animation link (experimental): number too large</p>', end='')
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

    global patch_factor

    patched_rows = []

    pattern_length = len([i for i in table_data[0] if i])

    patch_factor = len(table_data[0])//pattern_length

    for j, row in enumerate(table_data):

        patched_row = []

        for i, cell in enumerate(row):

            cell = '-' if not cell else cell

            if 'p' in cell:

                # target_juggler should never be empty
                # (those cases are in the other script)
                throw_number, target_juggler = cell.split('p')

                # try to cope with the prechacthis rounding convention
                if abs(float(throw_number)*patch_factor - int(float(throw_number)*patch_factor)) < 10**(-5):
                    myfun = round
                else:
                    myfun = ceil

                throw_number = int(myfun(patch_factor*float(throw_number)))
                target_juggler = ascii_uppercase.index(target_juggler) + 1

                cell = f'{throw_number}p{target_juggler}'

            elif '-' not in cell:

                cell = f'{int(patch_factor*float(cell))}'

            else: # empty cell

                pass


            ### patch (r,l) ####

            # j = row, i = col
            right_left_condition = ( (i-j) % len(row) ) % (patch_factor * 2) == 0

            if cell == '-':
                patched_cell = ('0','0')
            elif right_left_condition:
                patched_cell = (cell,'0')
            else:
                patched_cell = ('0',cell)

            patched_row.append(patched_cell)

        patched_rows.append(patched_row)
    return patched_rows


def add_crosses(patched_rows):

    global patch_factor

    crossed_rows = []
    for j, row in enumerate(patched_rows):
        crossed_row = []
        for i, cell in enumerate(row):

            crossed_cell = []
            for h, throw in enumerate(cell):
                fixed_throw = throw
                if 'p' not in throw and throw != '0':
                    throw_number = throw
                    if ( int(throw_number)//patch_factor ) % 2 != 0:
                        fixed_throw = f'{throw_number}x'
                    else:
                        fixed_throw = f'{throw_number}'
                elif 'p' in throw:
                    throw_number, target_juggler = throw.split('p')
                    target_beat_phase = (i + int(throw_number)) % len(row)
                    target_cell = patched_rows[int(target_juggler)-1][target_beat_phase]

                    # h comes into play
                    if target_cell[h] != '0': # we should not cross
                        if (int(throw_number) % 2) != 0:
                            fixed_throw = f'{throw_number}xp{target_juggler}'
                        else:
                            pass
                    elif target_cell[1-h] != '0': # we should cross
                        if (int(throw_number) % 2) == 0:
                            fixed_throw = f'{throw_number}xp{target_juggler}'
                        else:
                            pass
                    else: # this should not happen
                        from textwrap import dedent
                        msg = f'''
                        patched rows: {patched_rows}

                        patch factor: {patch_factor}

                        row index: {j}

                        row: {row}

                        col index: {i}

                        cell: {cell}

                        throw: {throw}

                        target juggler: {target_juggler}

                        target beat phase: {target_beat_phase}

                        target cell: {target_cell}

                            '''
                        raise Exception(
                            f'{dedent(msg)}'
                        )
                        # print('none', end='')
                        # sys.stdout.flush()
                        # sys.exit()
                else: # throw == '0'
                    pass
                crossed_cell.append(fixed_throw)
            crossed_row.append(tuple(crossed_cell))
        crossed_rows.append(crossed_row)
    return crossed_rows


def alphabetize(crossed_rows):
    alphabetized_rows = []
    for row in crossed_rows:
        alphabetized_row = []
        for cell in row:

            if cell == ('0'):
                alphabetized_row.append('0')
                continue

            alphabetized_cell = []
            for throw in cell:
                if 'x' in throw:
                    throw_number, tail = throw.split('x')
                    throw_number = alphabet_to_number(throw_number)
                    new_throw = number_to_alphabet(throw_number)
                    alphabetized_cell.append(f'{new_throw}x{tail}')
                elif 'p' in throw:
                    throw_number, tail = throw.split('p')
                    throw_number = alphabet_to_number(throw_number)
                    new_throw = number_to_alphabet(throw_number)
                    alphabetized_cell.append(f'{new_throw}p{tail}')
                else:
                    throw = number_to_alphabet(int(alphabet_to_number(throw)))
                    alphabetized_cell.append(f'{throw}')
            alphabetized_row.append(tuple(alphabetized_cell))
        alphabetized_rows.append(alphabetized_row)
    return alphabetized_rows


def strip_zeros(myrows, table_data):
    stripped_rows = []
    for j, row in enumerate(myrows):
        stripped_row = []
        for i, throw in enumerate(row):
            if i == 0 and not table_data[j][i]:
                stripped_row.append('0')
            if table_data[j][i]:
                stripped_row.append(throw)
        stripped_rows.append(stripped_row)
    return stripped_rows

# helper for two_patch_rows
def two_patch_cell(cell):

    if cell == ('0','0') or any(set(cell) == {'0', mythrow} for mythrow in ('2x')):
        return cell

    # throwing hand index
    h = 1 if cell[0] == '0' else 0

    throw = cell[h]

    new_cell = [None, None]

    if 'x' in throw:
        throw_number, tail = throw.split('x')
        throw_number = alphabet_to_number(throw_number)
        new_throw_number = number_to_alphabet(throw_number - 2)
        if str(new_throw_number) == '0': # should not happen
            new_cell = cell
        else:
            new_cell[h] = f'{new_throw_number}x{tail}'
            new_cell[1-h] = '2'
    elif 'p' in throw:
        throw_number, tail = throw.split('p')
        throw_number = alphabet_to_number(throw_number)
        # new_throw_number = throw_number - 2
        new_throw_number = number_to_alphabet(throw_number - 2)
        if str(new_throw_number) == '0':
            new_cell = cell
        else:
            new_cell[h] = f'{new_throw_number}p{tail}'
            new_cell[1-h] = '2'
    else:
        throw_number = alphabet_to_number(throw)
        new_throw_number = throw_number - 2
        if str(new_throw_number) == '0':
            new_cell = cell
        else:
            new_throw_number = number_to_alphabet(new_throw_number)
            new_cell[h] = f'{new_throw_number}'
            new_cell[1-h] = '2'

    return new_cell


def two_patch_rows(stripped_rows):
    patched_rows = []
    for row in stripped_rows:
        patched_row = []
        for i, cell in enumerate(row):
            if cell == '0':
                patched_row.append(cell)
                continue
            patched_cell = two_patch_cell(cell)
            patched_row.append(tuple(patched_cell))
        patched_rows.append(patched_row)
    return patched_rows


# somewhat unorganized
def borrow_zeros(myrows):

    # probably futile but fixed an earlier bug
    two_patched_rows = deepcopy(myrows)

    def count_zeros(row):
        counter = 0
        for cell in row:
            if cell == ('0','0'):
                counter += 1
        return counter

    # this is okay: if only one (0,0) throw, then things work correctly
    if count_zeros(two_patched_rows[0]) == 1:

        for j, row in enumerate(two_patched_rows):
            for i, cell in enumerate(row):
                if cell != ('0','0'):
                    continue
                n = len(row)
                prev_cell_index = (i-1) % n
                prev_cell = two_patched_rows[j][prev_cell_index]
                if prev_cell == '0': # from strip_zeros (,)!0
                    prev_cell_index = (prev_cell_index-1) % n
                    prev_cell = two_patched_rows[j][prev_cell_index]

                for h, throw in enumerate(prev_cell):

                    if throw == '2':

                        new_current_cell = [None, None]
                        new_current_cell[h] = '0'
                        new_current_cell[1-h] = '2'
                        two_patched_rows[j][i] = tuple(new_current_cell)

                        new_prev_cell = [None, None]
                        new_prev_cell[h] = '0'
                        new_prev_cell[1-h] = prev_cell[1-h]
                        two_patched_rows[j][prev_cell_index] = tuple(new_prev_cell)


    else:
        '''
        currently we block all the other cases except the above and the case
        where all but one of the throws are zeros

        in that case the below should work although it's a bit messy

        '''

        for j, row in enumerate(two_patched_rows):

            cell_done = False
            for i, cell in enumerate(row):

                if cell == ('0','0') or any(set(cell) == {'0', mythrow} for mythrow in ('2x')):
                    continue

                n = len(row)
                prev_cell_index = (i-1) % n
                # next_cell_index = (i+1) % n

                prev_cell = two_patched_rows[j][prev_cell_index]
                # next_cell = two_patched_rows[j][next_cell_index]

                if prev_cell == '0': # from strip_zeros (,)!0
                    prev_cell_index = (prev_cell_index-1) % n
                    prev_cell = two_patched_rows[j][prev_cell_index]
                # if next_cell == '0': # from strip_zeros (,)!0
                    # next_cell_index = (next_cell_index-1) % n
                    # next_cell = two_patched_rows[j][next_cell_index]

                # need to have a destination for the "move two" operation
                # tested more thoroughly below
                if '0' not in prev_cell:
                    continue

                # adjacent_cell = prev_cell if prev_cell == ('0','0') else next_cell
                # adj_cell_index = prev_cell_index if prev_cell == ('0','0') else next_cell_index
                adjacent_cell = prev_cell
                adj_cell_index = prev_cell_index

                for h, throw in enumerate(cell):
                    if throw == '2':
                        new_adjacent_cell = [None, None]

                        if adjacent_cell[1-h] != '0':
                            continue

                        new_adjacent_cell[h] = adjacent_cell[h]
                        new_adjacent_cell[1-h] = '2'
                        two_patched_rows[j][adj_cell_index] = tuple(new_adjacent_cell)

                        new_current_cell = [None, None]
                        new_current_cell[h] = '0'
                        new_current_cell[1-h] = cell[1-h]
                        two_patched_rows[j][i] = tuple(new_current_cell)

                        cell_done = True
                        break

                if cell_done:
                    break

    return two_patched_rows


def sync_jlab(myrows):
    pattern = '<'
    for row in myrows:
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


def two_patch_condition(table_rows):

    # this ruined something like 5.5p 1 in the case n=4, p=2
    if any(set(cell) == {'0','2x'} for row in table_rows for cell in row):
        return False

    # don't know yet how to two-patch most of these cases
    count = Counter(table_rows[0])
    zero_count = count[('0','0')]
    if zero_count > 1 and zero_count <= len(table_rows[0]) - 2:
        return False

    # otherwise we should be mostly fine
    return True


def patternTableToSyncAnimationUrl(html_table):

    table_data = parse_table(html_table)

    n = len(table_data) # number of jugglers
    pattern_length = len([i for i in table_data[0] if i])

    # this case was done in the other script
    if gcd(n, pattern_length) == 1 or (pattern_length % n) == 0:
        print('none', end='')
        sys.stdout.flush()
        sys.exit()

    # let's try this first
    elif (
        (n == 4) # or
        # (n == 6 and pattern_length in [3])
    ):

        try:
            pattern = sync_zero_patch(table_data)
            # mylog(f'sync_zero_patch:\n{pattern}\n\n')
            pattern = add_crosses(pattern)
            # mylog(f'add_crosses:\n{pattern}\n\n')
            pattern = strip_zeros(pattern, table_data)
            # mylog(f'strip_zeros:\n{pattern}\n\n')
            if two_patch_condition(pattern):
            # if False:
                pattern = two_patch_rows(pattern)
                # mylog(f'two_patch_rows:\n{pattern}\n\n')
                pattern = borrow_zeros(pattern)
                # mylog(f'borrow_zeros:\n{pattern}\n\n')
            else:
                pattern = alphabetize(pattern)
                # mylog(f'alphabetize:\n{pattern}\n\n')
            pattern = sync_jlab(pattern)
            # mylog(f'sync_jlab:\n{pattern}\n\n')
        except Exception as e:
            # mylog(f'exception: {e}')
            print(f'<p>No JugglingLab animation link (experimental): exception occurred</p>', end='')
            sys.stdout.flush()
            sys.exit()

        url = f'https://jugglinglab.org/anim?pattern={pattern}'
        url = f'<p><a href="{url}" target="_blank">JugglingLab animation (experimental)</p>'
        print(url, end='')
        sys.stdout.flush()
        sys.exit()
        pass

    else:
        # print('none', end='')
        print(f'<p>No JugglingLab animation link (experimental): case not implemented</p>', end='')
        sys.stdout.flush()
        sys.exit()


### main ###

html_table = sys.stdin.read()
patternTableToSyncAnimationUrl(html_table)

# just in case
sys.stdout.flush()
sys.exit()
