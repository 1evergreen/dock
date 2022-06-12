"""
parse the antibodys from results of rosetta antibody designer
"""
import os
import re
from absl import logging

def parse(path : str, pattern: str):
    """Read all pdb files that match a certain pattern

    Parameters
    ----------
    path : str
    pattern  : str
    Returns
    -------
    List
        list of files
    """    
    files = os.listdir(path)
    pattern = _get_pattern(pattern)
    print(f'Parsing files that matches {pattern}')
    return [file for file in files if os.path.isfile(os.path.join(path, file)) \
         and re.match(pattern, file)]

def _get_pattern(pattern):
    pattern = rf'{pattern}_\d+.pdb$'
    pattern = re.compile(pattern)
    return pattern
# print(parse('/data/wangww/protein/ab/ccs_ab/round2/results', 'round2start'))

