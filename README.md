
The original [prechacthis](https://github.com/prechac/prechacthis) repository patched:

- `src/pl/siteswap_preprocessing.pl` modified (modern prolog)
- `src/index.php` modified (modern prolog)
- some unnecessary dirs and files removed
- `src/python` added (calculate animation link)
- `src/pl/siteswap_info.pl` modified (display animation link)

Runs [here](http://209.38.178.145/neoprechac/src/index.php) with swi-prolog 9.2.1 on ubuntu.

Animation link:
- passist when `gcd(pattern length, number of jugglers) = 1`
- jugglinglab when `pattern length % number of jugglers = 0`
- no link otherwise

