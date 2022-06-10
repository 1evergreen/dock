"""
parse the antibodys from results of rosetta antibody designer
"""
import os
import re

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
    return [file for file in files if os.path.isfile(file) and re.match(pattern, file)]

def _get_pattern(pattern):
    pattern = f'{pattern}_\d+.pdb'
    pattern = re.compile(pattern)
    return pattern
# parse('.')

