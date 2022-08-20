<center><img src="https://github.com/xnl-h4ck3r/urless/raw/main/title.png"></center>

## About - v0.1

This is a tool used to de-clutter a list of URLs.
As a starting point, I took the amazing tool [uro](https://github.com/s0md3v/uro/) by Somdev Sangwan. But I wanted to change a few things, make some improvements (like deal with GUIDs) and make it more customisable.

## Installation

urless supports **Python 3**.

```
$ git clone https://github.com/xnl-h4ck3r/urless.git
$ cd urless
$ python setup.py install
```

If you would prefer to use `urless` instead of `python3 urless.py`, you could add an alias to your `.bashrc` file for example:

```
$ echo "alias urless='python3 $PWD/urless.py'" >> ~/.bashrc
$ source ~/.bashrc
```

## Usage

| Arg | Long Arg            | Description                                                                                                                                                   |
| --- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -i  | --input             | A file of URLs to de-clutter.                                                                                                                                 |
| -o  | --output            | The output file that will contain the de-cluttered list of URLs (default: output.txt). If piped to another program, output will be written to STDOUT instead. |
| -fk | --filter-keywords   | A comma separated list of keywords to exclude links (if there no parameters). This will override the `FILTER_KEYWORDS` list specified in config.yml           |
| -fe | --filter-extensions | A comma separated list of file extensions to exclude. This will override the `FILTER_EXTENSIONS` list specified in `config.yml`                               |
| -v  | --verbose           | Verbose output                                                                                                                                                |

## What does it do exactly?

You basically pass a list of URLs in (from a file, or pipe from STDIN), and get a de-cluttered file or URLs out. But in what way are they de-cluttered?
I'll explain this below, but first here are some terms that will be used:

- **FILTER-EXTENSIONS**: This refers to the list of extensions that can either be passed with `-fe`, specified with `FILTER_EXTENSIONS` in the `config.yml`, or if neither of those exist, a default list of `.css,.ico,.jpg,.jpeg,.png,.bmp,.svg,.img,.gif,.mp4,.flv,.ogv,.webm,.webp,.mov,.mp3,.m4a,.m4p,.scss,.tif,.tiff,.ttf,.otf,.woff,.woff2,.bmp,.ico,.eot,.htc,.rtf,.swf,.image`.
- **FILTER-KEYWORDS**: This refers to the list of keywords that can either be passed with `-fk`, specified with `FILTER_KEYWORDS` in the `config.yml`, or if neither of those exist, a default list of `blog,article,news,bootstrap,jquery,captcha,node_modules`
- **UNWANTED-CONTENT**:
  - A section of the URL path contains more than 3 dashes (`-`), BUT isn't a GUID. This implies human written content, e.g. `how-to-hack-the-planet`)
  - The URL contains `/YYYY/MM/` , e.g. a year, month . This is usually static content such as a blog

Here's what happens:

- If a URL has port 80 or 443 explicitly given, then remove it from the URL (e.g. http://example.com:80/test -> http://example.com/test)
- If the URL has any **FILTER-EXTENSIONS**, it will be removed from the output.
- If the URL has NO parameters:
  - If the URL contains a **FILTER-KEYWORDS** or **UNWANTED-CONTENT**, it will be removed.
  - If the URL path contains a GUID, only one of the GUIDs will be included if there are multiple URLs where the GUID is the only difference.
  - If the URL path contains an Integer ID, only one of the Integer IDs will be included if there are multiple URLs where the Integer ID is the only difference.
- Else the URL has Parameters (or a fragment `#`):
  - If there are multiple URLs with the same parameters, then only URLs with unique parameter values are included.
  - If there are URL's with a Parameter, but no value (or a fragment), then this will be included.

## Examples

### Basic use

```
cat target_urls.txt | python3 urless.py
```

or

```
python3 urless.py -i target_urls.txt
```

### Capture output

```
cat target_urls.txt | python3 urless.py > output.txt
```

or

```
python3 urless.py -i target_urls.txt -o output.txt
```

## config.yml

The `config.yml` file has the keys which can be updated to suit your needs:

- `FILTER_KEYWORDS` - A comma separated list of keywords (e.g. `blog,article,news` etc.) that URLs are checked against in certain circumstances.
- `FILTER_EXTENSIONS` - A comma separated list of file extensions (e.g. `.css,.jpg,.jpeg` etc.) that all URLs are checked against. If a URL includes any of the strings then it will be excluded from the output.

## Issues

If you come across any problems at all, or have ideas for improvements, please feel free to raise an issue on Github. If there is a problem, it will be useful if you can provide the exact command you ran and a detailed description of the problem. If possible, run with `-v` to reproduce the problem and let me know about any error messages that are given.

## TODO

- Add a `-rcid`/`--regex-custom-id` argument that allows a user to add a custom ID regex that may be specific to a target.

## And finally...

Good luck and good hunting!
If you really love the tool (or any others), or they helped you find an awesome bounty, consider [BUYING ME A COFFEE!](https://ko-fi.com/xnlh4ck3r) ☕ (I could use the caffeine!)

🤘 /XNL-h4ck3r
