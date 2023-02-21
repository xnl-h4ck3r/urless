#!/usr/bin/env python
# Python 3
# urless - by @Xnl-h4ck3r: De-clutter a list of URLs
# Full help here: https://github.com/xnl-h4ck3r/urless/blob/main/README.md
# Good luck and good hunting! If you really love the tool (or any others), or they helped you find an awesome bounty, consider BUYING ME A COFFEE! (https://ko-fi.com/xnlh4ck3r) ☕ (I could use the caffeine!)

from ast import arg
import re
import os
import sys
from typing import Pattern
import yaml
import argparse
from signal import SIGINT, signal
from urllib.parse import urlparse
from termcolor import colored
from pathlib import Path

# Default values if config.yml not found
DEFAULT_FILTER_EXTENSIONS = '.css,.ico,.jpg,.jpeg,.png,.bmp,.svg,.img,.gif,.mp4,.flv,.ogv,.webm,.webp,.mov,.mp3,.m4a,.m4p,.scss,.tif,.tiff,.ttf,.otf,.woff,.woff2,.bmp,.ico,.eot,.htc,.rtf,.swf,.image'
DEFAULT_FILTER_KEYWORDS = 'blog,article,news,bootstrap,jquery,captcha,node_modules'

# Variables to hold config.yml values
FILTER_EXTENSIONS = ''
FILTER_KEYWORDS = ''

# Regex for a path folder of integer
REGEX_INTEGER = '\d+'
reIntPart = re.compile(REGEX_INTEGER)
reInt = re.compile(r'\/'+REGEX_INTEGER+'([?\/]|$)')

# Regex for a path folder of GUID
REGEX_GUID = '[({]?[a-fA-F0-9]{8}[-]?([a-fA-F0-9]{4}[-]?){3}[a-fA-F0-9]{12}[})]?'
reGuidPart = re.compile(REGEX_GUID)
reGuid = re.compile(r'\/'+REGEX_GUID+'([?\/]|$)')

# Regex for path of YYYY/MM
REGEX_YYYYMM = '\/[1|2][0|1|9]\\d{2}/[0|1]\\d{1}\/'
reYYYYMM = re.compile(REGEX_YYYYMM)

REGEX_END = '(\/?)$'

# Global variables
args = None
urlmap = {}
patternsSeen = []
outFile = None
reCustomID = Pattern
reCustomIDPart = Pattern
linesOrigCount = 0
linesFinalCount = 0

def verbose():
    '''
    Functions used when printing messages dependant on verbose option
    '''
    return args.verbose

def write(text='',pipe=False):
    # Only send text to stdout if the tool isn't piped to pass output to something else, 
    # or if the tool has been piped and the pipe parameter is True
    if sys.stdout.isatty() or (not sys.stdout.isatty() and pipe):
        sys.stdout.write(text+'\n')

def writerr(text=''):
    # Only send text to stdout if the tool isn't piped to pass output to something else, 
    # or If the tool has been piped to output the send to stderr
    if sys.stdout.isatty():
        sys.stdout.write(text+'\n')
    else:
        sys.stderr.write(text+'\n')
            
def showBanner():
    write('')
    write(colored('  __  _ ____  _   ___  ___ ____ ', 'red'))
    write(colored(' | | | |  _ \| | / _ \/ __/ __/ ', 'yellow'))
    write(colored(' | | | | |_) | ||  __/\__ \__ \ ', 'green'))
    write(colored(' | |_| |  _ <| |_\___/\___/___/ ', 'cyan'))
    write(colored('  \___/|_| \_\___/', 'magenta')+colored('by Xnl-h4ck3r','white'))
    write('')

def getConfig():
    '''
    Try to get the values from the config file, otherwise use the defaults
    '''
    global FILTER_EXTENSIONS, FILTER_KEYWORDS
    try:

        # Try to get the config file values
        try:        
            urlessPath = Path(
                os.path.dirname(os.path.realpath(__file__))
            )
            urlessPath.absolute
            if urlessPath == '':
                configPath = 'config.yml'
            else:
                configPath = Path(urlessPath / 'config.yml')
            config = yaml.safe_load(open(configPath))
            
            # If the user provided the --filter-extensions argument then it overrides the config value
            if args.filter_keywords:
                FILTER_KEYWORDS = args.filter_keywords
            else:
                try:
                    FILTER_KEYWORDS = config.get('FILTER_KEYWORDS')
                    if str(FILTER_KEYWORDS) == 'None':
                        writerr(colored('No value for FILTER_KEYWORDS in config.yml - default set', 'yellow'))
                        FILTER_KEYWORDS = ''
                except Exception as e:
                    writerr(colored('Unable to read FILTER_EXTENSIONS from config.yml - default set', 'red'))
                    FILTER_KEYWORDS = DEFAULT_FILTER_KEYWORDS
            
            # If the user provided the --filter-extensions argument then it overrides the config value
            if args.filter_extensions:
                FILTER_EXTENSIONS = args.filter_extensions
            else:    
                try:
                    FILTER_EXTENSIONS = config.get('FILTER_EXTENSIONS')
                    if str(FILTER_EXTENSIONS) == 'None':
                        writerr(colored('No value for FILTER_EXTENSIONS in config.yml - default set', 'yellow'))
                        FILTER_EXTENSIONS = ''
                except Exception as e:
                    writerr(colored('Unable to read FILTER_EXTENSIONS from config.yml - default set', 'red'))
                    FILTER_EXTENSIONS = DEFAULT_FILTER_EXTENSIONS
                    
        except:
            writerr(colored('WARNING: Cannot find config.yml, so using default values', 'yellow'))
            FILTER_EXTENSIONS = DEFAULT_FILTER_EXTENSIONS
            FILTER_KEYWORDS = DEFAULT_FILTER_KEYWORDS
            
    except Exception as e:
        writerr(colored('ERROR getConfig 1: ' + str(e), 'red'))

def handler(signal_received, frame):
    '''
    This function is called if Ctrl-C is called by the user
    An attempt will be made to try and clean up properly
    '''
    writerr(colored('>>> "Oh my God, they killed Kenny... and urless!" - Kyle', 'red'))
    sys.exit()
                        
def paramsToDict(params: str) -> list:
    '''
    converts query string to dict
    '''
    try:
        the_dict = {}
        if params:
            for pair in params.split('&'):
                # If there is a parameter but no = then add a value of {EMPTY}
                if pair.find('=') < 0:
                    key = pair+'{EMPTY}'
                    the_dict[key] = '{EMPTY}'
                else:
                    parts = pair.split('=')
                    try:
                        the_dict[parts[0]] = parts[1]
                    except IndexError:
                        pass
        return the_dict
    except Exception as e:
        writerr(colored('ERROR paramsToDict 1: ' + str(e), 'red'))

def dictToParams(params: dict) -> str:
    '''
    converts dict of params to query string
    '''
    try:
        # If a parameter has a value of {EMPTY} then just the name will be written and no =
        stringed = [name if value == '{EMPTY}' else name + '=' + value for name, value in params.items()]

        # Only add a ? at the start of parameters, unless the first starts with #
        if list(params.keys())[0][:1] == '#':
            paramString = ''.join(stringed)
        else:
            paramString = '?' + '&'.join(stringed)

        # If a there are any parameters with {EMPTY} in the name then remove the string
        return paramString.replace('{EMPTY}','')
    except Exception as e:
        writerr(colored('ERROR dictToParams 1: ' + str(e), 'red'))

def compareParams(currentParams: list, newParams: dict) -> bool:
    '''
    checks if newParams contain a param
    that doesn't exist in currentParams
    '''
    try:
        ogSet = set([])
        for each in currentParams:
            for key in each.keys():
                ogSet.add(key)
        return set(newParams.keys()) - ogSet
    except Exception as e:
        writerr(colored('ERROR compareParams 1: ' + str(e), 'red'))
        
def isUnwantedContent(path: str) -> bool:
    '''
    checks if a path is likely to contain
    human written content e.g. a blog
    '''
    try:
        unwanted = False
        
        # If the path has more than 3 dashes '-' AND isn't a GUID AND (if specified) isn't a Custom ID, then assume it's human written content, e.g. blog
        for part in path.split('/'):
            if part.count('-') > 3:
                if args.regex_custom_id == '':
                    if not reGuidPart.search(part):
                        unwanted = True
                else:
                    if not reGuidPart.search(part) and reCustomIDPart.search(part):
                        unwanted = True
        
        # If it contains a year and month in the path then assume like blog/news content, r.g. .../2019/06/...
        if reYYYYMM.search(path):
            unwanted = True
            
        return unwanted
    except Exception as e:
        writerr(colored('ERROR isUnwantedContent 1: ' + str(e), 'red'))

def createPattern(path: str) -> str:
    '''
    creates patterns for urls with integers or GUIDs in them
    '''
    try:
        newParts = []
        subParts = []

        for part in path.split('/'):
            if reGuidPart.search(part):
                part = re.sub(reGuidPart.pattern, 'REGEX', part)
                for subPart in part.split('-'):
                    subParts.append(subPart)
                guidPart = '-'.join(subParts)
                newParts.append(guidPart.replace('REGEX',reGuidPart.pattern))
            elif args.regex_custom_id != '' and reCustomIDPart.search(part):
                part = re.sub(reCustomIDPart.pattern, 'CUSTOMREGEX', part)
                for subPart in part.split('-'):
                    subParts.append(subPart)
                customIDPart = '-'.join(subParts)
                newParts.append(customIDPart.replace('CUSTOMREGEX',reCustomIDPart.pattern))
            elif reIntPart.match(part):
                newParts.append(reIntPart.pattern)
            else:
                newParts.append(part)
        return '/'.join(newParts)
    except Exception as e:
        writerr(colored('ERROR createPattern 1: ' + str(e), 'red'))

def patternExists(pattern: str) -> bool:
    '''
    checks if a int pattern exists
    '''
    try:
        for i, seen_pattern in enumerate(patternsSeen):
            if pattern == seen_pattern:
                patternsSeen[i] = pattern
                return True
            elif seen_pattern in pattern:
                return True
        return False
    except Exception as e:
        writerr(colored('ERROR patternExists 1: ' + str(e), 'red'))

def matchesPatterns(path: str) -> bool:
    '''
    checks if the url matches any of the regex patterns
    '''
    try:
        for pattern in patternsSeen:
            if re.search(pattern, path) is not None:
                return True
        return False
    except Exception as e:
        writerr(colored('ERROR matchesPatterns 1: ' + str(e), 'red'))

def hasFilterKeyword(path: str) -> bool:
    '''
    checks if the url matches the blacklist regex
    '''
    global FILTER_KEYWORDS
    try:
        return re.search(FILTER_KEYWORDS.replace(',','|'), path, re.IGNORECASE)
    except Exception as e:
        writerr(colored('ERROR hasFilterKeyword 1: ' + str(e), 'red'))

def hasBadExtension(path: str) -> bool:
    '''
    checks if a url has a blacklisted extension
    '''
    global FILTER_EXTENSIONS
    try:
        badExtension = False
        if '/' not in path.split('.')[-1]:
            extensions = FILTER_EXTENSIONS.split(',')
            for extension in extensions:
                if path.lower().endswith(extension):
                    badExtension = True
        return badExtension
    except Exception as e:
        writerr(colored('ERROR hasBadExtension 1: ' + str(e), 'red'))

def processUrl(line):
    
    try:
        parsed = urlparse(line.strip())
        
        # Set the host
        scheme = parsed.scheme
        if scheme == '':
            host = parsed.netloc
        else:
            host = scheme + '://' + parsed.netloc
            
        # If the link specifies port 80 or 443, e.g. http://example.com:80, then remove the port
        if str(parsed.port) == '80':
            host = host.replace(':80','',1)
        if str(parsed.port) == '443':
            host = host.replace(':443','',1)
            
        # Build the path and parameters
        path, params = parsed.path, paramsToDict(parsed.query)
        
        # If there is a fragment, add as the last parameter with a name but with value {EMPTY} that doesn't add an = afterwards
        if parsed.fragment:
            params['#'+parsed.fragment] = '{EMPTY}'
        
        # Add the host to the map if it hasn't already been seen
        if host not in urlmap:
            urlmap[host] = {}
        
        # If the path has an extension we want to exclude, then just return to continue with the next line   
        if hasBadExtension(path):
            return
        
        # If the are no parameters
        if not params:
            
            # If its unwanted content or has a keyword to be excluded, then just return to continue with the next line
            if isUnwantedContent(path) or hasFilterKeyword(path):
                return
            
            # If the current path already matches a previously saved pattern then just return to continue with the next line
            if matchesPatterns(path):
                return
            
            # Create a pattern for the current path
            pattern = createPattern(path)
            
            # If the path contains a GUID and the pattern doesn't already exist, then add it to the dictionary of patterns seen
            if reGuidPart.search(path) and not patternExists(pattern):
                patternsSeen.append(pattern + REGEX_END)
            # Else if the path contains an integer ID and the pattern doesn't already exist, then add it to the dictionary of patterns seen
            elif reInt.search(path) and not patternExists(pattern):
                patternsSeen.append(pattern + REGEX_END)
            # Else if the path contains a Custom ID and the pattern doesn't already exist, then add it to the dictionary of patterns seen
            elif args.regex_custom_id != '' and reCustomIDPart.search(path) and not patternExists(pattern):
                patternsSeen.append(pattern + REGEX_END)
            
        # Update the url map
        if path not in urlmap[host]:
            urlmap[host][path] = [params] if params else []
        elif params and compareParams(urlmap[host][path], params):
            urlmap[host][path].append(params)
    
    except ValueError as ve:
        if verbose():
            writerr(colored('This URL caused a Value Error and was not included: ' + line, 'red'))
    except Exception as e:
        writerr(colored('ERROR processUrl 1: ' + str(e), 'red'))
        
def processInput():
    
    global linesOrigCount
    try:
        if not sys.stdin.isatty():
            for line in sys.stdin:
                processUrl(line)
        else:
            try:
                inFile = open(os.path.expanduser(args.input), 'r')
                lines = inFile.readlines()
                linesOrigCount = len(lines)
                for line in lines:
                    processUrl(line.rstrip('\n'))
            except Exception as e:
                writerr(colored('ERROR processInput 2 ' + str(e), 'red'))    
            
            try:
                inFile.close()
            except:
                pass            
    except Exception as e:
        writerr(colored('ERROR processInput 1: ' + str(e), 'red'))   
        
def processOutput():
    global linesFinalCount, linesOrigCount 
    try:
        # If an output file was specified, open it
        if args.output is not None:
            try:
                outFile = open(os.path.expanduser(args.output), 'w')
            except Exception as e:
                writerr(colored('ERROR processOutput 2 ' + str(e), 'red'))   
        
        # Output all URLs    
        for host, value in urlmap.items():
            for path, params in value.items():
                if params:
                    for param in params:
                        linesFinalCount = linesFinalCount + 1
                        # If an output file was specified, write to the file
                        if args.output is not None:
                            outFile.write(host + path + dictToParams(param) + '\n')
                        else:    
                            # If output is piped or the --output argument was not specified, output to STDOUT
                            if not sys.stdin.isatty() or args.output is None:
                                write(host + path + dictToParams(param),True)
                else:
                    linesFinalCount = linesFinalCount + 1
                    # If an output file was specified, write to the file
                    if args.output is not None:
                        outFile.write(host + path + '\n')
                    else:    
                        # If output is piped or the --output argument was not specified, output to STDOUT
                        if not sys.stdin.isatty() or args.output is None:
                            write(host + path,True)
        
        if verbose() and sys.stdin.isatty():
            writerr(colored('\nInput reduced from '+str(linesOrigCount)+' to '+str(linesFinalCount)+' lines 🤘', 'cyan'))
            
        # Close the output file if it was opened
        try:
            if args.output is not None:
                write(colored('Output successfully written to file: ', 'cyan')+colored(args.output,'white'))
                write()
                outFile.close()
        except Exception as e:
            writerr(colored('ERROR processOutput 3: ' + str(e), 'red'))
                            
    except Exception as e:
        writerr(colored('ERROR processOutput 1: ' + str(e), 'red'))

def showOptionsAndConfig():
    global FILTER_EXTENSIONS, FILTER_KEYWORDS
    try:
        write(colored('Selected options and config:', 'cyan'))
        write(colored('-i: ' + args.input, 'magenta')+colored(' The input file of URLs to de-clutter.','white'))
        if args.output is not None:
            write(colored('-o: ' + args.output, 'magenta')+colored(' The output file that the de-cluttered URL list will be written to.','white'))
        else:
            write(colored('-o: <STDOUT>', 'magenta')+colored(' An output file wasn\'t given, so output will be written to STDOUT.','white'))
            
        if args.filter_keywords:
            write(colored('-fk (Keywords to Filter): ', 'magenta')+colored(args.filter_keywords,'white'))
        else:
            write(colored('Filter Keywords (from Config.yml): ', 'magenta')+colored(FILTER_KEYWORDS,'white'))
        
        if args.filter_extensions:
            write(colored('-fe (Extensions to Filter): ', 'magenta')+colored(args.filter_extensions,'white'))
        else:
            write(colored('Filter Extensions (from Config.yml): ', 'magenta')+colored(FILTER_EXTENSIONS,'white'))
        
        write()
        
    except Exception as e:
        writerr(colored('ERROR showOptionsAndConfig 1: ' + str(e), 'red'))    

def argCheckRegexCustomID(value):
    global reCustomIDPart, reCustomID
    try:
        # Try to compile the regex
        reCustomIDPart = re.compile(value)
        reCustomID = re.compile(r'/'+value+'([?/]|$)')
        return value
    except:
        raise argparse.ArgumentTypeError(
            'Valid regex must be passed.'
        )
                        
def main():
    
    global args, urlmap, patternsSeen
    
    # Tell Python to run the handler() function when SIGINT is received
    signal(SIGINT, handler)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='urless - by @Xnl-h4ck3r: De-clutter a list of URLs.'    
    )
    parser.add_argument(
        '-i',
        '--input',
        action='store',
        help='A file of URLs to de-clutter.'
    )
    parser.add_argument(
        '-o',
        '--output',
        action='store',
        help='The output file that will contain the de-cluttered list of URLs (default: output.txt). If piped to another program, output will be written to STDOUT instead.',
    )
    parser.add_argument(
        '-fk',
        '--filter_keywords',
        action='store',
        help='A comma separated list of keywords to exclude links (if there no parameters). This will override the FILTER_KEYWORDS list specified in config.yml',
        metavar='<comma separated list>'
    )
    parser.add_argument(
        '-fe',
        '--filter-extensions',
        action='store',
        help='A comma separated list of file extensions to exclude. This will override the FILTER_EXTENSIONS list specified in config.yml',
        metavar='<comma separated list>'
    )
    parser.add_argument(
        '-rcid',
        '--regex-custom-id',
        action='store',
        help='Regex for a Custom ID that your target uses. Ensure the value is passed in quotes.',
        default='',
        metavar='REGEX',
        type=argCheckRegexCustomID
    )
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output.')
    args = parser.parse_args()

    try:
        # If no input was given, raise an error
        if sys.stdin.isatty():
            if args.input is None:
                writerr(colored('You need to provide an input with -i argument or through <stdin>.', 'red'))
                sys.exit()

        # Get the config settings from the config.yml file
        getConfig()
                        
        # If input is not piped, show the banner, and if --verbose option was chosen show options and config values
        if sys.stdin.isatty():
            showBanner()
            if verbose():
                showOptionsAndConfig()

        # Process the input given on -i (--input), or <stdin>
        processInput()

        # Output the saved urls with parameters
        processOutput()
        
    except Exception as e:
        writerr(colored('ERROR main 1: ' + str(e), 'red'))      
          
    finally: # Clean up
        urlmap = None
        patternsSeen = None
           
if __name__ == '__main__':
    main()
    