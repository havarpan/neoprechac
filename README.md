
The [prechacthis](https://github.com/prechac/prechacthis) repository patched:

- unnecessary dirs and files removed
- `src/index.php` updated
- `src/info.php` updated
- `src/pl/siteswap_preprocessing.pl` updated
- `src/python` added (calculate animation link)
- `src/pl/siteswap_info.pl` modified (display animation link).

Runs at [https://neoprechac.org](https://neoprechac.org) with swi-prolog 9.2.9 on ubuntu.

Animation link:
- [passist](https://github.com/helbling/passist) when `gcd(pattern length, number of jugglers) = 1`
- [jugglinglab](https://github.com/jkboyce/jugglinglab) otherwise:
  - async when `pattern length % number of jugglers = 0`
  - sync in the remaining cases:
    - under construction
    - all the cases with four jugglers should be more or less okay
    - the case with six jugglers and period three is there but may bug
    - no link displayed in other cases.

Thanks to Miika Toukola for help!

