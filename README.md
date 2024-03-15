
The [prechacthis](https://github.com/prechac/prechacthis) repository patched:

- `src/pl/siteswap_preprocessing.pl` updated
- `src/index.php` updated
- unnecessary dirs and files removed
- `src/python` added (calculate animation link)
- `src/pl/siteswap_info.pl` modified (display animation link).

Runs at [https://neoprechac.org](https://neoprechac.org) with swi-prolog 9.2.1 on ubuntu.

Animation link:
- [passist](https://github.com/helbling/passist) when `gcd(pattern length, number of jugglers) = 1`
- [jugglinglab](https://github.com/jkboyce/jugglinglab) otherwise:
  - async when `pattern length % number of jugglers = 0`
  - sync in the remaining cases:
    - under construction
    - the case with four jugglers & period two implemented
    - otherwise no link displayed (yet).

Thanks to Miika Toukola for help!

