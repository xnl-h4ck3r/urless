## Changelog

- v0.7

  - New

    - Add `-rcid` / `--regex-custom-id` argument to provide a regex expression for a Custom ID that your target uses.
    - Add `-nb` / `--no-banner` argument to hide the tool banner. This is only needed if you are not piping input to `urless`.
    - Add `-khw` / `--keep-human-written` argument to prevent URLs with a path part that contains 3 or more dashes (-) from being removed (e.g. blog post). These are normally removed by default.
    - Add `-kym` / `--keep-yyyymm` argument to prevent URLs with a path part that contains a year and month in the format `/YYYY/DD` (e.g. blog or news). These are normally removed by default.
    - Add `-iq` / `--ignore-querystring` argument to remove the query string (including URL fragments `#`) so output is unique paths only.

  - Changed

    - Fix bug where `/blah/1337` was not being treated differently to `/1337` for example.
    - When a Custom ID, GUID or Integer ID is found in a URL, and only one URL from many in the same format are returned in the output, use the first ID found in the input for that ID type.

- v0.6

  - New

    - By default, a trailing `/` will be removed from the end of a URL.
    - Added new argument `-ks`/`--keep-slash` that will ensure any links that do have a trailing slash in the input will not have the slash removed in the output, and therefore there may be identical URLs output, one with and one without a trailing slash.

- v0.5

  - Changed

    - Fixed Github Issue #3 to remove port 80 and 443 correctly

- v0.4

  - Changed

    - Various bug fixes

- v0.3

  - New

    - Add an `__init_.py` file to store the version, and move the image to a separate folder to make it cleaner.

  - Changed

    - If a line in the input throws an error due to not being a valid URL when parsed, then skip it, but output an error showing the URL if the `-v` arg is passed.

- v0.2

  - Fixed the bug `ERROR matchesPatterns 1: missing ), unterminated subpattern at position 237` by escaping the regex string before searching

- v0.1

  - Inital release. Please see README.md
