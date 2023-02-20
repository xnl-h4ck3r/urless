## Changelog

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
