'''
Under construction.

This script should create the animation link when

gcd(number of jugglers, pattern length) != 1 and pattern length % number of jugglers != 0.

'''
import sys
from bs4 import BeautifulSoup
import json

def parse_table(html_table):

    table_data = []
    soup = BeautifulSoup(html_table, 'lxml')
    table = soup.find('table')

    for row in table.find_all('tr'):
        cells = row.find_all('td')
        row_data = [cell.text for cell in cells]
        table_data.append(row_data)

    return json.dumps(table_data, indent=4)


def patternStrToSyncAnimationUrl(html_table):

    '''
    mydata = parse_table(html_table)
    url = f'<p><pre>{mydata}</pre></p>'
    print(url, end='')
    sys.stdout.flush()
    sys.exit()
    '''

    if True:
        print('none', end='')
        sys.stdout.flush()
        sys.exit()

    '''
    url = f'https://jugglinglab.org/anim?pattern={pattern}'
    url = f'<p><a href="{url}" target="_blank">JugglingLab animation</p>'
    print(url, end='')
    sys.stdout.flush()
    '''


### main ###

html_table = sys.stdin.read()
patternStrToSyncAnimationUrl(html_table)
