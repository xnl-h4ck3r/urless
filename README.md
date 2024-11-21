<center><img src="https://github.com/xnl-h4ck3r/urless/blob/main/urless/images/title.png"></center>

## About - v2.2

This is a tool used to de-clutter a list of URLs.
As a starting point, I took the amazing tool [uro](https://github.com/s0md3v/uro/) by Somdev Sangwan. But I wanted to change a few things, make some improvements (like deal with GUIDs) and make it more customizable.

## Installation

`urless` supports **Python 3**.

Install `urless` in default (global) python environment.

```bash
pip install urless
```

OR

```bash
pip install git+https://github.com/xnl-h4ck3r/urless.git -v
```

You can upgrade with

```bash
pip install --upgrade urless
```

### pipx

Quick setup in isolated python environment using [pipx](https://pypa.github.io/pipx/)

```bash
pipx install git+https://github.com/xnl-h4ck3r/urless.git
```

## Usage

| Argument | Long Argument        | Description                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -i       | --input              | A file of URLs to de-clutter.                                                                                                                                                                                                                                                                                                                                                                                   |
| -o       | --output             | The output file that will contain the de-cluttered list of URLs (default: output.txt). If piped to another program, output will be written to STDOUT instead.                                                                                                                                                                                                                                                   |
| -fk      | --filter-keywords    | A comma separated list of keywords to exclude links (if there no parameters). This will override the `FILTER_KEYWORDS` list specified in config.yml                                                                                                                                                                                                                                                             |
| -fe      | --filter-extensions  | A comma separated list of file extensions to exclude. This will override the `FILTER_EXTENSIONS` list specified in `config.yml`                                                                                                                                                                                                                                                                                 |
| -rp      | --remove-params      | A comma separated list of **case senistive** parameters to remove from ALL URLs. This will override the `REMOVE_PARAMS` list specified in `config.yml`. This can be useful to remove cache buster parameters for example.\*\*                                                                                                                                                                                   |
| -ks      | --keep-slash         | A trailing slash at the end of a URL in input will not be removed. Therefore there may be identical URLs output, one with and one without a trailing slash.                                                                                                                                                                                                                                                     |
| -khw     | --keep-human-written | By default, any URL with a path part that contains more than 3 dashes (-) are removed because it is assumed to be human written content (e.g. blog post), and not interesting. Passing this argument will keep them in the output.                                                                                                                                                                              |
| -kym     | --keep-yyyymm        | By default, any URL with a path containing /YYYY/MM (where YYYY is a year and MM month) are removed because it is assumed to be blog/news content, and not interesting. Passing this argument will keep them in the output.                                                                                                                                                                                     |
| -rcid    | --regex-custom-id    | **USE WITH CAUTION!** Regex for a Custom ID that your target uses. Ensure the value is passed in quotes. See the section below for more details on this.                                                                                                                                                                                                                                                        |
| -iq      | --ignore-querystring | Remove the query string (including URL fragments `#`) so output is unique paths only.                                                                                                                                                                                                                                                                                                                           |
| -fnp     | --fragment-not-param | Don't treat URL fragments `#` in the same way as parameters, e.g. if a link has a filter keyword and a fragment (or param) the link is usually kept, but if this argument is passed and a link has a filter word and fragment, the link will be removed. Also, if this arg is passed and `-iq` / `--ignore-querystring` is used, the fragment will NOT be removed from links if no query string is in the link. |
| -lang    | --language           | If passed and there are multiple URLs with different language codes as a part of the path, only one version of the URL will be output. The codes are specified in the `LANGUAGE` section of `config.yml`.                                                                                                                                                                                                       |
| -c       | --config             | Path to the YML config file. If not passed, it looks for file `config.yml` in the default config directory, e.g. `~/.config/urless/`.                                                                                                                                                                                                                                                                           |
| -dp      | --disregard-params   | There is certain filtering that is not done if the URLs have parameters, because by default we want to see all possible parameters. If this argument is passed, then the filtering will be done, regardless of the existence of any parameters.                                                                                                                                                                 |
| -nb      | --no-banner          | Hides the tool banner (it is hidden by default if you pipe input to urless) output.                                                                                                                                                                                                                                                                                                                             |
|          | --version            | Show current version number.                                                                                                                                                                                                                                                                                                                                                                                    |
| -v       | --verbose            | Verbose output                                                                                                                                                                                                                                                                                                                                                                                                  |

## What does it do exactly?

You basically pass a list of URLs in (from a file, or pipe from STDIN), and get a de-cluttered file or URLs out. But in what way are they de-cluttered?
I'll explain this below, but first here are some terms that will be used:

- **FILTER-EXTENSIONS**: This refers to the list of extensions that can either be passed with `-fe`, specified with `FILTER_EXTENSIONS` in the `config.yml`, or if neither of those exist, a default list of `.css,.ico,.jpg,.jpeg,.png,.bmp,.svg,.img,.gif,.mp4,.flv,.ogv,.webm,.webp,.mov,.mp3,.m4a,.m4p,.scss,.tif,.tiff,.ttf,.otf,.woff,.woff2,.bmp,.ico,.eot,.htc,.rtf,.swf,.image`.
- **FILTER-KEYWORDS**: This refers to the list of keywords that can either be passed with `-fk`, specified with `FILTER_KEYWORDS` in the `config.yml`, or if neither of those exist, a default list of `blog,article,news,bootstrap,jquery,captcha,node_modules`
- **LANGUAGE**: This refers to the list of language codes that can be specified with `LANGUAGE` in the `config.yml`, or if it doesn't exist, a default list of the most common codes `en,en-us,en-gb,fr,de,pl,nl,fi,sv,it,es,pt,ru,pt-br,es-mx,zh-tw,js.ko`
- **UNWANTED-CONTENT**:
  - A section of the URL path contains more than 3 dashes (`-`), BUT isn't a GUID. This implies human written content, e.g. `how-to-hack-the-planet`. If arg `-khw` is passed, then this won't be removed.
  - The URL contains `/YYYY/MM/` , e.g. a year, month . This is usually static content such as a blog. If arg `-kym` is passed, then this won't be removed.

Here's what happens:

- If a URL has port 80 or 443 explicitly given, then remove it from the URL (e.g. http://example.com:80/test -> http://example.com/test)
- If the URL has any **FILTER-EXTENSIONS**, it will be removed from the output.
- If the URL has NO parameters **OR** the `-dp`/`--disregard-params` argument was passed:
  - If the URL contains a **FILTER-KEYWORDS** or **UNWANTED-CONTENT**, it will be removed.
  - if the URL query string contains unwanted parameters specified in config `REMOVE_PARAMS` (or overridden wit argument `-rp`/`--remove-params`), they will be removed from all URLs before processing.
  - If `-rcid`/`--regex-custom-id` is passed and the URL path contains a Custom ID, only one match to the Custom ID regex will be included if there are multiple URLs where that is the only difference.
  - If the URL path contains a GUID, only one of the GUIDs will be included if there are multiple URLs where the GUID is the only difference.
  - If the URL path contains an Integer ID, only one of the Integer IDs will be included if there are multiple URLs where the Integer ID is the only difference.
  - If the `-lang` argument is passed and the URL contains a language code (e.g. `en-gb`), only one of the language codes will be included if there are multiple URLs where the language code is different.
- Else the URL has Parameters (or a fragment `#`) **AND** the `-dp`/`--disregard-params` argument was NOT passed:
  - If there are multiple URLs with the same parameters, then only URLs with unique parameter values are included.
  - If there are URL's with a Parameter, but no value (or a fragment), then this will be included.

## Examples

### Basic use

```
cat target_urls.txt | urless
```

or

```
urless -i target_urls.txt
```

### Capture output

```
cat target_urls.txt | urless > output.txt
```

or

```
urless -i target_urls.txt -o output.txt
```

## config.yml

The `config.yml` file has the keys which can be updated to suit your needs:

- `FILTER_KEYWORDS` - A comma separated list of keywords (e.g. `blog,article,news` etc.) that URLs are checked against in certain circumstances.
- `FILTER_EXTENSIONS` - A comma separated list of file extensions (e.g. `.css,.jpg,.jpeg` etc.) that all URLs are checked against. If a URL includes any of the strings then it will be excluded from the output.
- `LANGUAGE` - A comma separated list of language codes (e.g. `en-gb,fr,nl` etc.) that all URLs are checked against when the `-lang` argument is passed. If there are multiple URLs with different language codes, only one version of the URL will be output.
- `REMOVE_PARAMS` - A comma separated list of **case sensitive** parameter names (e.g. `cachebuster,cacheBuster`) that will be removed from all URLs before processing.

## Custom Regex

There are currently automatic regex checks for a path part being a Globally Unique ID (GUID) and an Integer ID, but the `-rcid` / `--regex-custom-id` argument lets you provide a regular expression to identify a custom ID. For example, if a target has a specific ID format (that isn't a GUID or Integer) then you can specify a regex expression for it, and then only one of those will be returned in the output if the rest of the URL is the same. For example:

- Assume the target has a user ID in a format like `U-65241X`
- And there are multiple URLs like the following:
  ```
  https://target.com/blah/U-61723A/settings
  https://target.com/blah/U-63352B/settings
  https://target.com/blah/U-61351A/profile
  https://target.com/blah/U-61723A/settings
  https://target.com/blah/U-64135C/profile
  ```
- You can call `urless` and pass `-rcid 'U-[0-9]{5}[A-Z]'`, then the output would be:
  ```
  https://target.com/blah/U-61723A/settings
  https://target.com/blah/U-64135C/profile
  ```

**IMPORTANT REGEX NOTES:**

- Writing correct regex expressions can be difficult, and if it isn't correct, you could end up with unpredictable and incorrect output.
- Always enclose your regex expression in single quotes when passing to the `-rcid` argument.
- You don't need to add a custom regex for a GUID or Integer ID - these are dealt with already.
- The regex expression should highlight the whole part of the path. So, if your regex only identifies the start of the path, then add `[^(\?|\/|#|$)]*` to the end of your regex which will mean ALL other characters up until the end of the path part.
- You can add `^` at the start, and `$` at the end, of your regex to ensure it represents the whole part of a path between slashes. However, these will be added for you if they are left out.
- Make sure the regex only identifies the sections you are interested in, otherwise you may have unexpected results. To test your regex, you can take your input file and do `cat input.txt | grep -E 'U-[0-9]{5}[A-Z]'` for example, and see whether your expression looks correct (it should only highlight what you are interested in, and highlight the whole part of the path that is the custom ID).
- You can also test using [Regex101](https://regex101.com), entering sample URLs in the **TEST STRING** section to check if it is correct. Make sure the **REGEX FLAGS** **g**lobal and **m**ultiline are selected.
- There maybe cases where you just can't supply a regex that is going to identify the Custom ID correctly without treating other values as the same. For example, if there are URLs like `https://target.com/blah/xnl/settings` where `xnl` is a User Name, you won't be able to create a regex for user name because it is not a unique enough format to distinguish it from other possible path values.

## Issues

If you come across any problems at all, or have ideas for improvements, please feel free to raise an issue on Github. If there is a problem, it will be useful if you can provide the exact command you ran and a detailed description of the problem. If possible, run with `-v` to reproduce the problem and let me know about any error messages that are given.

## TODO

None - feel free to raise a Github issue to suggest any enhancements.

## And finally...

Good luck and good hunting!
If you really love the tool (or any others), or they helped you find an awesome bounty, consider [BUYING ME A COFFEE!](https://ko-fi.com/xnlh4ck3r) ☕ (I could use the caffeine!)

🤘 /XNL-h4ck3r

<p>
<a href='https://ko-fi.com/B0B3CZKR5' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
