import argparse
import re
import readline
readline.parse_and_bind('set editing-mode emacs')

from typing import Sequence
from .iter import unique

def argparser(opts):
    '''
    Helper function for argument parsing.
    '''
    parser = argparse.ArgumentParser()
    defaults = {}
    for i in opts:
        optname = i[0]
        optdescription = i[1]
        optdefault = i[2]
        opttype = i[3]
        # create help string and add argument to parsing
        help_string = '{0} (default: {1})'.format(optdescription,
                                                  str(optdefault))
        parser.add_argument('--' + optname, help = help_string, type = str)
    # do parsing
    args = vars(parser.parse_args()) #vars to change to a dict
    # defaults settings and types management
    for i in opts:
        optname = i[0]
        optdescription = i[1]
        optdefault = i[2]
        opttype = i[3]
        # se il valore è a none in args impostalo al valore di default
        # specificato
        if (args[optname] is None):
            args[optname] = optdefault
        # se il tipo è logico sostituisci un valore possibile true con
        # l'equivalente python
        if (opttype == bool):
            # mv to character if not already (not if used optdefault)
            args[optname] = str(args[optname])
            true_values = ('true', 'True', 'TRUE', 't', 'T', '1', 'y', 'Y',
                           'yes', 'Yes', 'YES') 
            if (args[optname] in true_values):
                args[optname] = 'True'
            else:
                args[optname] = ''
        # converti il tipo a quello specificato
        args[optname] = opttype(args[optname])
    return(args)

 
def line_to_numbers(x: str) -> list[int]:
    '''
    transform a string of positive numbers "1 2-3, 4, 6-10" to a list [1,2,3,4,6,7,8,9,10] 
    '''
    # replace comma with white chars
    x = x.replace(",", " ")
    # keep only digits, - and white spaces
    x = re.sub(r'[^\d\- ]', '', x)
    # split by whitespaces
    spl = x.split(" ")
    # change ranges to proper
    expanded = []
    single_page_re = re.compile("^\d+$")
    pages_range_re = re.compile("^(\d+)-(\d+)$")
    for i in range(len(spl)):
        # Check if the single element match one of the regular expression
        single_page = single_page_re.match(spl[i])
        pages_range =  pages_range_re.match(spl[i])
        if single_page:
            # A) One single page: append it to results
            expanded.append(spl[i])
        elif pages_range:
            # B) Pages range: append a list of (expanded) pages to results
            first = int(pages_range.group(1))
            second = int(pages_range.group(2))
            # step is 1 if first is less than or equal to second or -1
            # otherwise 
            step = 1 * int(first <= second)  - 1 * int(first > second)
            if step == 1:
                second += 1
            elif step == -1:
                second -= 1
            else:
                # do nothing (ignore if they don't match)
                pass
            expanded_range = [str(val) for \
                              val in range(first, second, step)]
            expanded += expanded_range
        else:
            ValueError(str(spl[i]) + "does not match a single page re nor a pages range re.")
    # coerce to integer expanded
    res: list[int] = [int(x) for x in expanded]
    return(res)

def menu(choices: Sequence[str],
         title: str|None = None,
         multiple: bool = False,
         repeated: bool = False,
         strict: bool   = True) -> Sequence[str]:
    """ 
    CLI menu for user single/multiple choices

    Returns either:
    - a single choice
    - a list of selected choiches 
    - None if nothing was choosed

    TODO: add a default options
    """
    available_ind = [i + 1 for i in range(len(choices))]
    avail_with_0  = [0] + available_ind
    the_menu = "\n".join([str(i) + '. '+ str(c)
                          for i, c in zip(available_ind, choices)])
    if multiple:
        select_msg = "Selection (values as '1, 2-3, 6') or 0 to exit: "
    else:
        select_msg = "Selection (0 to exit): "
    if title:
        ascii_header(title)
    print(the_menu, '\n')
    ind = line_to_numbers(input(select_msg))
    # normalize to list (for single selections, for now)
    if not isinstance(ind, list):
        ind = list(ind)
    if strict:
        # continue asking for input until all index are between the selectable
        while not all([i in avail_with_0 for i in ind]):
            not_in = [i for i in ind if i not in avail_with_0]
            print("Not valid insertion: ", not_in, "\n")
            ind = line_to_numbers(input(select_msg))
            if not isinstance(ind, list):
                ind = list(ind)
    else:
        # keep only the input in avail_with_0
        allowed = [i for i in ind if i in avail_with_0]
        any_not_allowed = not all(allowed)
        if any_not_allowed:
            print("Removed some values (not 0 or specified possibilities): ",
                  list(set(ind) - set(allowed)), ".")
            ind = allowed
    # make unique if not allowed repetitions
    if not repeated:
        ind = list(unique(ind))
    # obtain the selection
    rval = [choices[i - 1] for i in ind if i != 0]
    # return always a list should simplify the code
    return rval


def ascii_header(x: str) -> None:
    '''
    Create an ascii header given a string as title.
    '''
    l = len(x)
    header = ("=" * l)
    print(header)
    print(x)
    print(header, '\n')
