## Changelog

- v1.0

- Changed

  - Add support for quick install using pip or pipx.

- v0.9

- Changed

  - Add i18N language codes `gb-en,ca-en,au-en,fr-fr,ca-fr,es-es,mx-es,de-de,it-it,br-pt,pt-pt,jp-ja,cn-zh,tw-zh,kr-ko,sa-ar,in-hi,ru-ru`

- v0.8

  - New

    - Add `DEFAULT_LANGUAGE` constant and `LANGUAGE` key in `config.yml` with the most common language codes: `en,en-us,en-gb,fr,de,pl,nl,fi,sv,it,es,pt,ru,pt-br,es-mx,zh-tw,js.ko`
    - Add `-lang`/`--language` argument. If passed and there are multiple URLs with different language codes as a part of the path, only one version of the URL will be output. The codes are specific in the `LANGUAGE` key of `config.yml`

  - Changed

    - A URL can have a GUID, Integer, CustomID and Language Code in the same URL and be de-cluttered properly.
    - If the Custom Regex ID doesn't start with `^` and end in `$`, those will be added.
    - Fix bug where it added the last occurrence of a regex pattern instead of the first.
    - Simplify the code in `processUrl` and `createPattern` functions... I had some strange logic that was unnecessary!
    - Make sure case is ignored when any `FILTER_EXTENSIONS` in `config.yml` or passed with `-fe` are compared with input.

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
