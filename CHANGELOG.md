## Changelog

- v2.2

  - New

    - Add argument `-c`/`--config` to specify a path to a custom `config.yml` file. This resolves [Issue 9](https://github.com/xnl-h4ck3r/urless/issues/9).
    - Add argument `-dp`/`--disregard-params`. There is certain filtering that is not done if the URLs have parameters, because by default we want to see all possible parameters. If this argument is passed, then the filtering will be done, regardless of the existence of any parameters. This resolves [Issue 11](https://github.com/xnl-h4ck3r/urless/issues/11) and [Issue 12](https://github.com/xnl-h4ck3r/urless/issues/12).

  - Changed

    - The description for argument `-khw`/`--keep-human-written` says `By default, any URL with a path part that contains 3 or more dashes (-) are removed` but this will be corrected to `contains more than 3 dashes`.
    - Correct the description for argument `-kym`/`--keep-yyyymm` on the `-h` output and `README.md`. It says `By default, any URL with a path containing 3 /YYYY/MM` but the `3` should be removed.

- v2.1

  - New

    - Add `long_description_content_type` to `setup.py` to upload to PyPi
    - Add `urless` to `PyPi` so can be installed with `pip install urless`

- v2.0

  - New

    - Add `REMOVE_PARAMS` to `config.yml`. This will be a comma separated list of case sensitive parameter names that you want removed completely from URLs. This can be useful to remove cache buster parameters, so will default to `cachebuster,cacheBuster` to show examples.
    - Add arg `-rp`/`--remove-params` which can be used to pass a comma separated list of parameter names to remove from URLs. This will override the `REMOVE_PARAMS` list in `config.yml`.
    - Show the current version of the tool in the banner, and whether it is the latest, or outdated.
    - Add arg `--version` to show the current version of the tool.
    - When installing `urless`, if the `config.yml` already exists then it will keep that one and create `config.yml.NEW` in case you need to replace the old config.

  - Changed

    - Fix a bug that meant defaults were not set correctly if `config.yml` keys are missing.

- v1.3

  - New

    - Add argument `-fnp`/`--fragment-not-param`. If passed the URL fragments `#` will NOT be treated in the same way as parameters, e.g. if a link has a filter keyword and a fragment (or param) the link is usually kept, but if this argument is passed and a link has a filter word and fragment, the link will be removed. Also, if this arg is passed and `-iq` / `--ignore-querystring` is used, the fragment will NOT be removed from links if no query string is in the link.

- v1.2

  - Changed

    - Changes to prevent `SyntaxWarning: invalid escape sequence` errors when Python 3.12 is used.

- v1.1

- Changed

  - Add support to automatically identify file encoding.

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
